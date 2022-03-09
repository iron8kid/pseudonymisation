"""
This file contains the back-end implementation of the dash web app.
"""

from dash import Input, Output, callback,State, html
import base64
from app import facade
from layouts import uploading_layout, processing_layout,setting_layout
from pylighter import Annotation
import dash
from dash.exceptions import PreventUpdate
DEFAULT_LABEL_COLORS={'ORG': '#7aecec', 'PRODUCT': '#bfeeb7', 'GPE': '#feca74', 'LOC': '#ff9561', 'PER': '#aa9cfc', 'NORP': '#c887fb', 'FAC': '#9cc9cc', 'EVENT': '#ffeb80', 'LAW': '#ff8197', 'LANGUAGE': '#ff8197', 'WORK_OF_ART': '#f0d0ff', 'DATE': '#bfe1d9', 'TIME': '#bfe1d9', 'MONEY': '#e4e7d2', 'QUANTITY': '#e4e7d2', 'ORDINAL': '#e4e7d2', 'CARDINAL': '#e4e7d2', 'PERCENT': '#e4e7d2'}

# entname, entbox, entity, and render are helper functions used to display the original text with identified entities#
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
######################################################################
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              Input('file_uploaded', 'data'))
def display_page(pathname,state):
    """ navigates between app interfaces.
    """
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
    """ displays configuration in the settting interface
    """
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
    """
    updates the config.ini file using the user input
    """
    if n_clicks is not None:
        if(facade.update(new_path,new_patterns)):
            return True,'success','Settings successfuly updated'
        else:
            return True,'danger','Something wrong happened, Please check the new settings'
    return False,dash.no_update,dash.no_update

@callback(Output('file_uploaded', 'data'),
          Output('url', 'pathname'),
          Output("modal-centered", "is_open"),
          Input('upload-data', 'contents'),
          Input("load_previous_results", "n_clicks"),
          Input("override_previous_results", "n_clicks"),)
def update_document(content,load,override):
    """
    reads the uploaded text file and updates facade current_doc attribute
    """
    ctx = dash.callback_context
    if content is None:
        return dash.no_update,dash.no_update,dash.no_update
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id=='upload-data' and content is not None:
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            facade.set_document(decoded)
            if (facade.is_file_in()):
                return dash.no_update,dash.no_update,True
            else:
                facade.writer.set_doc_instances(facade.current_doc,override=True)
                return True,'/processing',dash.no_update
        if trigger_id=="load_previous_results":
            facade.writer.set_doc_instances(facade.current_doc,override=False)
            return True,'/processing',dash.no_update
        if trigger_id=="override_previous_results":
            facade.writer.set_doc_instances(facade.current_doc,override=True)
            return True,'/processing',dash.no_update
        else:
            return dash.no_update,dash.no_update,dash.no_update

@callback(Output('original_text', 'children'),
Output('Orignal_text_rendred', 'data'),
           Input('file_uploaded', 'data'))
def set_text(state):
    """
    dispalys the orignal text
    """
    if state is True:
        facade.run_model()
        return render(facade.current_doc.text,facade.current_doc.ents),True
    else:
        dash.no_update,dash.no_update

@callback(Output('new_text', 'value'),
Output("standalone-checkbox", 'value'),
           Input('Orignal_text_rendred', 'data'))
def set_new_text(state):
    """
    displays the pseudonymized text
    """
    if state is True:
        facade.pseudonymise_doc()
        return facade.current_doc.pseudo_text,facade.current_doc.validated
    else:
        dash.no_update,dash.no_update

@callback(Output("saving-toast", "is_open"),
Output("saving-toast", "icon"),
Output("saving-toast", "children"),
Input('save_button', 'n_clicks'),
Input('new_text', 'value'),
Input('standalone-checkbox', 'value'))
def save_file(n_clicks,new_pseudo_text,new_validated):
    """
    saves files (original text and pseudonimzed text in corpus directory) and results (in results.csv file)
    """
    if new_pseudo_text is not None:
        facade.current_doc.set_pseudo_text(new_pseudo_text)
    if new_validated is not None:
        facade.current_doc.set_validated(new_validated)
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = 'No clicks yet'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if n_clicks is not None and trigger_id=='save_button':
        if(facade.save_doc()):
            return True,'success','File and resultats are successfuly saved'
        else:
            return True,'danger','Something wrong happened'
    return False,dash.no_update,dash.no_update
