from dash import Dash, html, dcc, Output, Input, dash_table, State
import dash
import pandas as pd
import re

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

test_df = pd.read_csv("test_df01.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Recipe Recommender"),
                html.H2(
                    "Find the perfect recipe to prevent your leftovers from going to waste"
                ),
                # First filter
                html.Label("Enter your Ingredients:"),
                dcc.Dropdown(
                    id="ingredient-filter",
                    options=[
                        {"label": ingredient, "value": ingredient}
                        for ingredients_list in test_df["ingredients"].str.split(", ")
                        for ingredient in ingredients_list
                    ],
                    multi=True,
                    placeholder="Select ingredients...",
                    style={
                        "width": "100%",
                        "margin-top": "10px",
                        "margin-bottom": "10px",
                    },  # Add padding here
                ),
                html.Button("Search Recipe", id="search-button"),
            ],
            style={
                "width": "30%",
                "float": "left",
                "padding": "20px",
                "background-color": "#dcdcdc",
            },
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id="filtered-recipes-table",
                    columns=[
                        {"name": "Name", "id": "name", "presentation": "markdown"},
                        {"name": "Ingredients", "id": "ingredients"},
                        {"name": "Steps", "id": "steps"},
                    ],
                    style_table={
                        "border": "thin lightgrey solid",
                        "display": "none",
                    },  # Initially hide the table
                    style_header={"display": "none"},  # Initially hide the header
                    style_cell={"textAlign": "left"},
                    style_data_conditional=[
                        {
                            "if": {"filter_query": '{name} ne ""'},
                            "fontWeight": "bold",
                            "display": "table-cell",
                        }
                    ],
                )
            ],
            style={"width": "60%", "float": "right", "padding": "20px"},
        ),
    ]
)


@app.callback(
    [
        Output("filtered-recipes-table", "data"),
        Output("filtered-recipes-table", "style_data_conditional"),
        Output("filtered-recipes-table", "style_table"),
    ],
    [Input("search-button", "n_clicks")],
    [State("ingredient-filter", "value")],
)
def filter_recipes(n_clicks, ingredient_filter):
    try:
        if n_clicks is None or n_clicks == 0:
            return (
                [],
                [{"if": {"column_id": "Name"}, "display": "none"}],
                {"display": "none"},
            )

        filtered_recipes_df = test_df[
            test_df["ingredients"].apply(
                lambda x: any(ingredient in x for ingredient in ingredient_filter)
            )
        ]

        data = filtered_recipes_df.to_dict("records")

        return (
            data,
            [{"if": {"column_id": "Name"}, "display": "none"}],
            {"display": "table"},
        )

    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return (
            [],
            [{"if": {"column_id": "Name"}, "display": "none"}],
            {"display": "none"},
        )


if __name__ == "__main__":
    app.run_server(debug=True)
