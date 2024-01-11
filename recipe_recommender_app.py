# Import Libraries
from dash import Dash, html, dcc, Output, Input, dash_table, State
import dash
import pandas as pd
import re

# Set the display options to show all columns and rows
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

# Data import
test_df = pd.read_csv("test_df.csv")

# RegEx to remove ', [ & ] from a string
# pattern = re.compile(r'[\'\[\]]')

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        # Left side of the layout
        html.Div(
            [
                html.H1("Recipe Recommender"),
                html.H2(
                    "Find the perfect recipe to prevent your leftovers from going to waste"
                ),
                # region multiple pages
                # html.Div([
                # html.Div(
                #         dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                #     ) for page in dash.page_registry.values()
                # ]),
                # dash.page_container
                # endregion
                # First filter - Ingredients dropdown
                html.Label("Enter your Ingredients:"),
                dcc.Dropdown(
                    id="ingredient-filter",
                    options=[
                        {"label": ingredient, "value": ingredient}
                        for ingredients_list in test_df[
                            "non_basic_ingredients"
                        ].str.split(", ")
                        for ingredient in ingredients_list
                    ],
                    multi=True,
                    placeholder="Select ingredients...",
                    style={"width": "100%"},  # Set the width to 100% of the container
                ),
                # Second Filter - Cuisine dropdown
                html.Label("Select a cuisine:"),
                dcc.Dropdown(
                    id="cuisine-filter",
                    options=[
                        {"label": cuisine, "value": cuisine}
                        for cuisine_list in test_df["cuisine"].str.split(", ")
                        if isinstance(
                            cuisine_list, list
                        )  # Check if cuisine_list is a list
                        for cuisine in cuisine_list
                    ],
                    multi=True,
                    placeholder="Select cuisine...",
                    style={"width": "100%"},  # Set the width to 100% of the container
                ),
                # Third Filter - Meal time dropdown
                html.Label("Choose time to make"),
                dcc.Dropdown(
                    id="time-to-make-filter",
                    options=[
                        {"label": time_to_make, "value": time_to_make}
                        for time_to_make_list in test_df["time-to-make"].str.split(", ")
                        if isinstance(
                            time_to_make_list, list
                        )  # Check if time-to-make is a list
                        for time_to_make in time_to_make_list
                    ],
                    multi=True,
                    placeholder="Select time to make...",
                    style={"width": "100%"},  # Set the width to 100% of the container
                ),
                # Button for search
                html.Button("Search Recipe", id="search-button"),
            ],
            style={
                "width": "30%",
                "float": "left",
                "padding": "20px",
                "background-color": "#dcdcdc",
            },
        ),
        # Right side of the layout
        html.Div(
            [
                # Display the filtered recipes in a DataTable
                dash_table.DataTable(
                    id="filtered-recipes-table",
                    columns=[
                        {"name": "Name", "id": "name", "presentation": "markdown"},
                        {"name": "Ingredients", "id": "ingredients"},
                        {"name": "Steps", "id": "steps"},
                    ],
                    style_table={"border": "thin lightgrey solid"},
                    style_header={"fontWeight": "bold"},
                    style_cell={"textAlign": "left"},
                    style_data_conditional=[
                        {"if": {"column_id": "Name"}, "display": "none"}
                    ],
                )
            ],
            style={"width": "70%", "float": "right", "padding": "20px"},
        ),
        # ])
    ]
)


# Define callback to update filtered recipes table and toggle visibility
@app.callback(
    [
        Output("filtered-recipes-table", "data"),
        Output("filtered-recipes-table", "style_data_conditional"),
    ],
    [Input("search-button", "n_clicks")],
    [State("ingredient-filter", "value"), State("cuisine-filter", "value")],
)
def filter_recipies_dataframe(
    recipies_data: pd.DataFrame,
    filter: list[str],
) -> pd.DataFrame:
    # implement filtering
    return


def filtered_recipes(
    recipies_data: pd.DataFrame,
    ingredients_selected: list[str] | None = None,
    cuisine_selected: list[str] | None = None,
    mealtime_selected: list[str] | None = None,
) -> pd.DataFrame:
    if ingredients_selected:
        recipies_data = filter_recipies_dataframe(recipies_data, ingredients_selected)
    if recipies_data.empty:
        return "No recipies were found for your selection"
    return


def update_filtered_recipes(n_clicks, ingredient_filter, cuisine_filter):
    try:
        print(f"n_clicks: {n_clicks}")
        print(f"ingredient_filter: {ingredient_filter}")
        print(f"cuisine_filter: {cuisine_filter}")

        if n_clicks is None or n_clicks == 0:
            return [], [{"if": {"column_id": "Name"}, "display": "none"}]

        # Convert all filter values to strings and handle None or float values
        ingredient_filter = [
            str(val) if val is not None and not isinstance(val, (float, int)) else ""
            for val in ingredient_filter
        ]

        # # Handle cuisine filter
        # if cuisine_filter is not None and not isinstance(cuisine_filter, (float, int)):
        #     cuisine_filter = [str(val) for val in cuisine_filter]
        # else:
        #     cuisine_filter = ""

        # Apply multiple filters
        filtered_recipes_df = test_df[
            test_df["ingredients"].apply(
                lambda x: any(ingredient in x for ingredient in ingredient_filter)
            )  # &
            # test_df['cuisine'].apply(lambda x: any(cuisine in x for cuisine in cuisine_filter))
        ]

        print(f"filtered_recipes_df: {filtered_recipes_df}")

        data = filtered_recipes_df.to_dict("records")

        # Show the DataTable when filters are applied
        return data, [{"if": {"column_id": "Name"}, "display": "table-cell"}]

    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return [], [{"if": {"column_id": "Name"}, "display": "none"}]


if __name__ == "__main__":
    app.run_server(debug=True)
