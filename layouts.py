from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import  html

#============== Uploading Layout ================#
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("File content already traited"), close_button=False),
                dbc.ModalBody("Do you want to load previous results ?"),
                dbc.ModalFooter([
                    dbc.Button(
                        "Yes",
                        id="load_previous_results",color="dark", className="me-1",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        "No",
                        id="override_previous_results",color="dark", className="me-1",
                        n_clicks=0,
                    )
                    ]
                ),
            ],
            id="modal-centered",
            backdrop="static",
            centered=True,
            is_open=False,
        ),
    ]
)

NAVBAR = dbc.Navbar(
    dbc.Container(children=[
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Pseudonymization App", className="ml-auto"))
                ],
                align="center"),
                dbc.Row(
                    [
                        dbc.Col(dcc.Link(dbc.Button(html.I(className="bi bi-gear"), outline=True, color="light"),href='/settings'), className="mr-auto")
                    ],
                    align="center"),

    ],fluid=True),
    color="dark",
    dark=True,
    sticky="top",
)
upload=dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a .txt file',style={'font-weight': 'bold',})
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    )

upload_file_card = [
    dbc.CardHeader(html.H5("Upload document")),
    dbc.CardBody(
        [
            dcc.Loading(upload,
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]
uploading_layout = html.Div([
    NAVBAR,
     dbc.Container(
        [
        modal,
            dbc.Row([dbc.Col(dbc.Card(children=upload_file_card)),], style={"marginTop": 30}),
        ],
        className="mt-12",
    ),
])
#============== Setting Layout ================#
model_path_input =html.Div([
        dbc.Label("Path to NER model", html_for="path"),
        dbc.Input(type="text", id="path"),
        ],className="mb-3")



patterns_input =html.Div([
        dbc.Label("Patterns", html_for="patterns"),
        dbc.Input(
            type="text",
            id="patterns",),dbc.FormText(html.P(["Check ",html.A("this link",href='https://spacy.io/api/matcher',target="_blank")," to learn more about patterns format."])),
        ],className="mb-3")

form = dbc.Form([model_path_input, patterns_input, dbc.Row(dbc.Button("Update Settings", outline=True, color="dark",className="mr-auto",id='update_button'),className="d-grid gap-2 col-3 mx-auto")])


setting_card = [
    dbc.CardHeader(html.H5("App Settings")),
    dbc.CardBody(
        [
            dcc.Loading(form ,
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

Setting_NAVBAR = dbc.Navbar(
    dbc.Container(children=[
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Pseudonymization App", className="ml-auto"))
                ],
                align="center"),
                dbc.Row(
                    [
                        dbc.Col(dcc.Link(dbc.Button(html.I(className="bi bi-file-earmark-arrow-up"), outline=True, color="light"),href='/'), className="mr-auto"),
                        dbc.Col(dcc.Link(dbc.Button(html.I(className="bi bi-play"), outline=True, color="light"),href='/processing'), className="mr-auto")
                    ],
                    align="center"),

    ],fluid=True),
    color="dark",
    dark=True,
    sticky="top",
)

toast = html.Div(
    [
        dbc.Toast(
            id="positioned-toast",
            header="Settings updated",
            is_open=False,
            dismissable=True,
            icon="danger",
            duration=1000,
            style={"position": "fixed", "top": 66, "right": 10, "width": 350,"z-index":'auto'},
        ),
    ]
)

setting_layout = html.Div([
dcc.Store(id='setting_void', storage_type='local'),
Setting_NAVBAR,
 dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(children=setting_card)),toast], style={"marginTop": 30,"z-index": 1}),
    ],
    className="mt-12",
),
])


#============== Processing Layout ================#


save_toast = html.Div(
    [
        dbc.Toast(
            id="saving-toast",
            header="Saving file and results",
            is_open=False,
            dismissable=True,
            icon="danger",
            duration=1000,
            style={"position": "fixed", "top": 66, "right": 10, "width": 350,"z-index":'auto'},
        ),
    ]
)

new_text =html.Div([

        dcc.Textarea(id="new_text",className="new_text",style={'width':"100%"},rows=10),
        ],className="mb-3")
new_text_form = dbc.Form([new_text, dbc.Checkbox(
                    id="standalone-checkbox",
                    label="Validate resultats",
                    value=False,
                ), dbc.Row(dbc.Button("Save the file and results", id='save_button',outline=True, color="dark",className="mr-auto"),className="d-grid gap-2 col-3 mx-auto")])
original_text_card = [
    dbc.CardHeader(html.H5("Original Text")),
    dbc.CardBody(
        [
            dcc.Loading(html.P(id='original_text',style={'whiteSpace': 'pre-wrap'}) ,
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]
new_text_card = [
    dbc.CardHeader(html.H5("Pseudonymised Text")),
    dbc.CardBody(
        [save_toast ,
            dcc.Loading(new_text_form ,
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

Body=dbc.Container(
dbc.Row(
[dbc.Col(dbc.Card(original_text_card),md=6,style={"marginBottom": 10}),dbc.Col(dbc.Card(new_text_card),md=6)],style={"marginTop": 30}),fluid=True
)


Processing_NAVBAR = dbc.Navbar(
    dbc.Container(children=[
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Pseudonymization App", className="ml-auto"))
                ],
                align="center"),
                dbc.Row(
                    [
                        dbc.Col(dcc.Link(dbc.Button(html.I(className="bi bi-file-earmark-arrow-up"), outline=True, color="light"),href='/'), className="mr-auto"),
                        dbc.Col(dcc.Link(dbc.Button(html.I(className="bi bi-gear"), outline=True, color="light"),href='/settings'), className="mr-auto")
                    ],
                    align="center"),

    ],fluid=True),
    color="dark",
    dark=True,
    sticky="top",
)
processing_layout = html.Div([

dcc.Store(id='Orignal_text_rendred', storage_type='local'),
Processing_NAVBAR,
Body
])
