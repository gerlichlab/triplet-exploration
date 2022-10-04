from cProfile import label
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
from utils.parse import parse_directory
import plotly.express as px

# parse data

data = parse_directory("./data/pileups")
regions = list(data.keys())
binsizes = list(data[regions[0]].keys())
offsets = sorted(list(data[regions[0]][binsizes[0]].keys()), key=lambda x: int(x))

initial_iccf = data[regions[0]][binsizes[0]][offsets[0]]["iccf"]
initial_obsexp = data[regions[0]][binsizes[0]][offsets[0]]["obsexp"]

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
        ),
        html.Div(
            children=[
                html.Div(children="Region", className="menu-title"),
                dcc.Dropdown(
                    id="region-filter",
                    options=[
                        {"label": region, "value": region}
                        for region in regions
                    ],
                    value=regions[0],
                    clearable=False,
                    className="dropdown",
                ),
                html.Div(children="Binsize [kb]", className="menu-title"),
                dcc.Dropdown(
                    id="binsize-filter",
                    options=[
                        {"label": binsize, "value": binsize}
                        for binsize in binsizes
                    ],
                    value=binsizes[0],
                    clearable=False,
                    className="dropdown",
                ),
                html.Div(children="Offset [kb]", className="menu-title"),
                dcc.RadioItems(
                    id="offset-radio",
                    options=[
                        {"label": offset, "value": offset}
                        for offset in offsets
                    ],
                    value="0", inline=True)
            ],
            className="menu"
        )
    ,
    html.Div(
        children=[
                html.Div(
                    children=[
                        dcc.Graph(id="iccf"),
                        dcc.RangeSlider(0, 20, value=[5, 15], id='iccf-slider',
                        tooltip={"placement": "bottom", "always_visible": True},
                        dots=False),],
                    className="card"
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="obsexp"),
                        dcc.RangeSlider(0, 20, value=[5, 15], id='obsexp-slider',
                        tooltip={"placement": "bottom", "always_visible": True},
                        dots=False,),
                        ],
                    className="card"
                )
        ],
        className="wrapper"
    )

    ]
)


@app.callback(
    Output("iccf-slider", "min"),
    Output("iccf-slider", "max"),
    Output("iccf-slider", "value"),
    Output("iccf-slider", "marks"),
    Input("region-filter", "value"),
    Input("binsize-filter", "value"),
    Input("offset-radio", "value")
)
def update_iccf_slider_values(region, binsize, offset):
    subset = np.log10(data[region][binsize][offset]["iccf"].values.flatten())
    range_min = np.nanmin(subset)
    range_max = np.nanmax(subset)
    pos_min = np.percentile(subset, 1)
    pos_max = np.percentile(subset, 99)
    marks = {i: str(np.round(i,2)) for i in np.linspace(range_min, range_max, 5)}
    return range_min, range_max, [pos_min, pos_max], marks

@app.callback(
    Output("obsexp-slider", "min"),
    Output("obsexp-slider", "max"),
    Output("obsexp-slider", "value"),
    Output("obsexp-slider", "marks"),
    Input("region-filter", "value"),
    Input("binsize-filter", "value"),
    Input("offset-radio", "value")
)
def update_obsexp_slider_values(region, binsize, offset):
    subset = np.log2(data[region][binsize][offset]["obsexp"].values.flatten())
    range_min = np.nanmin(subset)
    range_max = np.nanmax(subset)
    pos_min = np.percentile(subset, 1)
    pos_max = np.percentile(subset, 99)
    marks = {i: str(np.round(i,2)) for i in np.linspace(range_min, range_max, 5)}
    return range_min, range_max, [pos_min, pos_max], marks

@app.callback(
    Output("iccf", "figure"),
    Input("region-filter", "value"),
    Input("binsize-filter", "value"),
    Input("offset-radio", "value"),
    Input("iccf-slider", "value")
)
def update_iccf(region, binsize, offset, slider_val):
    subset = data[region][binsize][offset]["iccf"]
    fig = px.imshow(np.log10(subset), title="Raw counts [log10]", zmin=slider_val[0], zmax=slider_val[1])
    return fig

@app.callback(
    Output("obsexp", "figure"),
    Input("region-filter", "value"),
    Input("binsize-filter", "value"),
    Input("offset-radio", "value"),
    Input("obsexp-slider", "value")
)
def update_obsexp(region, binsize, offset, slider_val):
    subset = data[region][binsize][offset]["obsexp"]
    fig = px.imshow(np.log2(subset), color_continuous_scale="RdBu_r",
                    color_continuous_midpoint=0, title="Obs/exp [log2]",
                    zmin=slider_val[0], zmax=slider_val[1])
    return fig

# start app

if __name__ == "__main__":
    app.run_server(port=8050, host="0.0.0.0")