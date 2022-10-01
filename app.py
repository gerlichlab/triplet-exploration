import dash
from dash import dcc
from dash import html
import pandas as pd

# styling

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Triplet analysis"


# define layout

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Triplet Pixels",className="header-title"),
                html.P(
                    children="Analyze the distribution of triplet pixels around regions of interest",className="header-description"
                )
            ],
            className="header"
        )
    ]
)

# start app

if __name__ == "__main__":
    app.run_server(debug=True)