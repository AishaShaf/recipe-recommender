from dash import Dash, html, dcc, Output, Input, dash_table, State
import dash
import pandas as pd
import re

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

test_df = pd.read_csv("test_df.csv")

# Drop rows with null values in the cuisine column
test_df = test_df.dropna(subset=['cuisine'])

# Create a set to store unique non_basic_ingredients
unique_non_basic_ingredients_set = set()
for ingredients_list in test_df['non_basic_ingredients'].str.split(','):
    unique_non_basic_ingredients_set.update(ingredients_list)
unique_non_basic_ingredients_list = list(unique_non_basic_ingredients_set)

# Create a set to store unique cuisines
unique_cuisines_set = set()
for cuisines_list in test_df['cuisine'].str.split(', '):
    unique_cuisines_set.update(cuisines_list)
unique_cuisines_list = list(unique_cuisines_set)

# Create a set to store unique meal_times
unique_meal_times_set = set()
for meal_times_list in test_df['meal_time'].str.split(', '):
    unique_meal_times_set.update(meal_times_list)
unique_meal_times_list = list(unique_meal_times_set)

# Create a set to store unique sweet_or_savoury
unique_sweet_or_savoury_set = set()
for sweet_or_savoury_list in test_df['sweet_or_savoury'].str.split(', '):
    unique_sweet_or_savoury_set.update(sweet_or_savoury_list)
unique_sweet_or_savoury_list = list(unique_sweet_or_savoury_set)

# Create a set to store unique time_to_make
unique_time_to_make_set = set()
for time_to_make_list in test_df['time_to_make'].str.split(', '):
    unique_time_to_make_set.update(time_to_make_list)
unique_time_to_make_list = list(unique_time_to_make_set)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Recipe Recommender'),
        html.H2('Find the perfect recipe to prevent your leftovers from going to waste'),

        # First dropdown for non_basic_ingredients
        html.Label('Select your Ingredients:'),
        dcc.Dropdown(
            id='ingredient-filter',
            options=[
                {'label': ingredient, 'value': ingredient}
                for ingredient in unique_non_basic_ingredients_list
            ],
            multi=True,
            placeholder='Select ingredients...',
            style={'width': '100%', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),

        # Second dropdown for cuisine
        html.Label('Select Cuisine:'),
        dcc.Dropdown(
            id='cuisine-filter',
            options=[
                {'label': cuisine, 'value': cuisine}
                for cuisine in unique_cuisines_list
            ],
            multi=True,
            placeholder='Select cuisine...',
            style={'width': '100%', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),

        # Third dropdown for meal_time
        html.Label('Select Meal Time:'),
        dcc.Dropdown(
            id='meal-time-filter',
            options=[
                {'label': meal_time, 'value': meal_time}
                for meal_time in unique_meal_times_list
            ],
            multi=True,
            placeholder='Select meal time...',
            style={'width': '100%', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),

        # Fourth dropdown for sweet_or_savoury
        html.Label('Select Sweet or Savoury:'),
        dcc.Dropdown(
            id='sweet-or-savoury-filter',
            options=[
                {'label': sweet_or_savoury, 'value': sweet_or_savoury}
                for sweet_or_savoury in unique_sweet_or_savoury_list
            ],
            multi=True,
            placeholder='Select sweet or savoury...',
            style={'width': '100%', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),
        # Fifth dropdown for time_to_make
        html.Label('Select Time to Make:'),
        dcc.Dropdown(
            id='time-to-make-filter',
            options=[
                {'label': time_to_make, 'value': time_to_make}
                for time_to_make in unique_time_to_make_list
            ],
            multi=True,
            placeholder='Select time to make...',
            style={'width': '100%', 'margin-top': '10px', 'margin-bottom': '10px'}
        ),

        html.Button('Search Recipe', id='search-button'),

    ], style={'width': '30%', 'float': 'left', 'padding': '20px', 'background-color': '#dcdcdc'}),

    html.Div([
        dash_table.DataTable(
            id='filtered-recipes-table',
            columns=[
                {'name': 'Name', 'id': 'name', 'presentation': 'markdown'},
                {'name': 'Ingredients', 'id': 'non_basic_ingredients'},
                {'name': 'Steps', 'id': 'steps'}
            ],
            style_table={'border': 'thin lightgrey solid', 'display': 'none'},
            style_header={'display': 'none'},
            style_cell={'textAlign': 'left'},
            style_data_conditional=[
                {'if': {'filter_query': '{name} ne ""'},
                 'fontWeight': 'bold',
                 'display': 'table-cell'
                 }
            ]
        ),
        html.Div(id='no-results-message', style={'margin-top': '20px', 'color': 'red'}),
    ], style={'width': '60%', 'float': 'right', 'padding': '20px'}),
])


@app.callback(
    [Output('filtered-recipes-table', 'data'),
     Output('filtered-recipes-table', 'style_data_conditional'),
     Output('filtered-recipes-table', 'style_table'),
     Output('no-results-message', 'children')],
    [Input('search-button', 'n_clicks')],
    [State('ingredient-filter', 'value'),
     State('cuisine-filter', 'value'),
     State('meal-time-filter', 'value'),
     State('sweet-or-savoury-filter', 'value'),
     State('time-to-make-filter', 'value')]
)
def filter_recipes(n_clicks, ingredient_filter, cuisine_filter, meal_time_filter, sweet_or_savoury_filter, time_to_make_filter):
    try:
        if n_clicks is None or n_clicks == 0:
            return [], [{'if': {'column_id': 'Name'}, 'display': 'none'}], {'display': 'none'}, ''

        # Apply filters using logical AND operation
        filtered_recipes_df = test_df
        if ingredient_filter:
            filtered_recipes_df = filtered_recipes_df[
                filtered_recipes_df['non_basic_ingredients'].apply(lambda x: any(ingredient in x for ingredient in ingredient_filter))
            ]
        if cuisine_filter:
            filtered_recipes_df = filtered_recipes_df[
                filtered_recipes_df['cuisine'].apply(lambda x: any(cuisine in x for cuisine in cuisine_filter))
            ]
        if meal_time_filter:
            filtered_recipes_df = filtered_recipes_df[filtered_recipes_df['meal_time'].isin(meal_time_filter)]
        if sweet_or_savoury_filter:
            filtered_recipes_df = filtered_recipes_df[
                filtered_recipes_df['sweet_or_savoury'].apply(lambda x: any(sweet_or_savoury in x for sweet_or_savoury in sweet_or_savoury_filter))
            ]
        if time_to_make_filter:
            filtered_recipes_df = filtered_recipes_df[filtered_recipes_df['time_to_make'].isin(time_to_make_filter)]

        data = filtered_recipes_df.to_dict('records')

        # Check if there are no results
        if len(data) == 0:
            return data, [{'if': {'column_id': 'Name'}, 'display': 'none'}], {'display': 'none'}, 'No recipes were found for your selected criteria.'

        return data, [{'if': {'column_id': 'Name'}, 'display': 'none'}], {'display': 'table'}, ''

    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return [], [{'if': {'column_id': 'Name'}, 'display': 'none'}], {'display': 'none'}, ''



if __name__ == '__main__':
    app.run_server(debug=True)














