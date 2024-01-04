from dash import Dash, html, dcc, Output, Input, dash_table
import pandas as pd

# Sample data
recipes_df = pd.read_csv('recipes_w_search_terms.csv')
recipes_df_short = recipes_df.head(500)

app = Dash(__name__)

app.layout = html.Div([
    # Left side of the layout
    html.Div([
        html.H1('Recipe Analytics'),

        # First filter - Ingredients dropdown
        html.Label('Filter by Ingredients:'),
        dcc.Dropdown(
            id='ingredient-filter',
            options=[
                {'label': ingredient, 'value': ingredient}
                for ingredients_list in recipes_df_short['ingredients'].str.split(', ')
                for ingredient in ingredients_list
            ],
            multi=True,
            placeholder='Select ingredients...'
        ),

        # Add more filters as needed

    ], style={'width': '30%', 'float': 'left', 'padding': '20px'}),

    # Right side of the layout
    html.Div([
        # Display the filtered recipes in a DataTable
        dash_table.DataTable(
            id='filtered-recipes-table',
            columns=[
                {'name': 'Name', 'id': 'name', 'presentation': 'markdown'},
                {'name': 'Ingredients', 'id': 'ingredients'},
                {'name': 'Steps', 'id': 'steps'}
            ],
            style_table={'border': 'thin lightgrey solid'},
            style_header={'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )
    ], style={'width': '70%', 'float': 'right', 'padding': '20px'}),
])

# Define callback to update filtered recipes table
@app.callback(
    Output('filtered-recipes-table', 'data'),
    [Input('ingredient-filter', 'value')]
)
def update_filtered_recipes(ingredient_filter):
    # Filter recipes based on ingredient filter
    if not ingredient_filter:
        return []

    filtered_recipes_df = recipes_df_short[recipes_df_short['ingredients'].apply(lambda x: any(ingredient in x for ingredient in ingredient_filter))]
    data = filtered_recipes_df.to_dict('records')
    return data

if __name__ == '__main__':
    app.run_server(debug=True)

















