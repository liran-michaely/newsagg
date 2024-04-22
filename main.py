import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = html.Div([
    dcc.Input(id='topic-input', type='text', placeholder='Enter a topic...', value='', style={'margin': 10}),  # Set initial value to an empty string
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='news-cards', children=[])
])


# API key and base URL for NewsAPI
API_KEY = '978e623a86df429f9d2b2eb36606207a '
BASE_URL = "https://newsapi.org/v2/everything"


# Callback to update the news cards based on the topic input
@app.callback(
    Output('news-cards', 'children'),
    Input('search-button', 'n_clicks'),
    State('topic-input', 'value')
)
def update_output(n_clicks, input_value):
    if n_clicks > 0 and input_value:
        params = {
            'q': input_value,
            'apiKey': API_KEY,
            'language': 'en',
            'sortBy': 'publishedAt',  # Ensure articles are sorted by publication date
        }
        response = requests.get(BASE_URL, params=params)
        articles = response.json().get('articles', [])

        # Sort articles by date in descending order (most recent first)
        articles = sorted(articles, key=lambda x: x['publishedAt'], reverse=True)

        # Generate a card for each article
        cards = []
        for article in articles:
            image_url = article['urlToImage'] if article[
                'urlToImage'] else "https://via.placeholder.com/150"  # Placeholder if no image
            card_content = [
                dbc.CardHeader(article['source']['name'] + " - " + article['publishedAt'][:10]),
                # Include date in header
                dbc.CardImg(src=image_url, top=True,
                            style={'width': '80%', 'height': 'auto', 'object-fit': 'contain', 'display': 'block',
                                   'margin-left': 'auto', 'margin-right': 'auto'}),  # Adjusted image styling
                dbc.CardBody([
                    html.H5(article['title'], className="card-title"),
                    html.P(article['description'], className="card-text"),
                    dbc.Button("Read More", href=article['url'], color="primary", target="_blank")
                ])
            ]
            card = dbc.Card(card_content, style={'margin': '10px'})
            cards.append(card)

        return cards
    return []


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
