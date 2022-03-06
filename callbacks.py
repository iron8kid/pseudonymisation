from dash import Input, Output, callback,State, html
import base64
from app import facade
from layouts import uploading_layout, processing_layout,setting_layout
from pylighter import Annotation
import dash
from dash.exceptions import PreventUpdate
DEFAULT_LABEL_COLORS={'ORG': '#7aecec', 'PRODUCT': '#bfeeb7', 'GPE': '#feca74', 'LOC': '#ff9561', 'PER': '#aa9cfc', 'NORP': '#c887fb', 'FAC': '#9cc9cc', 'EVENT': '#ffeb80', 'LAW': '#ff8197', 'LANGUAGE': '#ff8197', 'WORK_OF_ART': '#f0d0ff', 'DATE': '#bfe1d9', 'TIME': '#bfe1d9', 'MONEY': '#e4e7d2', 'QUANTITY': '#e4e7d2', 'ORDINAL': '#e4e7d2', 'CARDINAL': '#e4e7d2', 'PERCENT': '#e4e7d2'}
def entname(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "1",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem"
    })


def entbox(children, color):
    return html.Mark(children, style={
        "background": color,
        "padding": "0.15em 0.15em",
        "margin": "0 0.25em",
        "line-height": "1",
        "border-radius": "0.35em",
    })


def entity(children, name):
    if type(children) is str:
        children = [children]

    children.append(entname(name))
    color = DEFAULT_LABEL_COLORS[name]
    return entbox(children, color)

def render(text,ents):
    children = []
    last_idx = 0
    for ent in ents:
        children.append(text[last_idx:ent[0]])
        children.append(
            entity(text[ent[0]:ent[1]], ent[2]))
        last_idx = ent[1]
    children.append(text[last_idx:])
    return children

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              Input('file_uploaded', 'data'))
def display_page(pathname,state):
    if pathname == '/settings':
         return setting_layout
    elif pathname == '/processing' and state==True and facade.current_doc is not None:
         return processing_layout
    else:
        return uploading_layout
@callback(Output('path', 'value'),
          Output('patterns', 'value'),
          Input('url', 'pathname'))
def display_settings(pathname):
    if pathname == '/settings':
         return facade.conf.model_path,str(facade.conf.patterns)
    else:
        raise PreventUpdate

@callback(Output("positioned-toast", "is_open"),
Output("positioned-toast", "icon"),
Output("positioned-toast", "children"),
          Input('update_button', 'n_clicks'),
          State('path', 'value'),
          State('patterns', 'value'))
def update_settings(n_clicks,new_path,new_patterns):
    if n_clicks is not None:
        if(facade.update(new_path,new_patterns)):
            return True,'success','Settings successfuly updated'
        else:
            return True,'danger','Something wrong happened, Please check the new settings'
    return False,dash.no_update,dash.no_update

@callback(Output('file_uploaded', 'data'),
          Output('url', 'pathname'),
          Input('upload-data', 'contents'))
def update_output(content):
    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        facade.set_document(decoded)
        return True,'/processing'
    else:
        return dash.no_update,dash.no_update


@callback(Output('original_text', 'children'),
           Input('file_uploaded', 'data'))
def set_text(state):
    if state is True:
        facade.run_model()
        return render(facade.current_doc.text,facade.current_doc.ents)
    else:
        dash.no_update
