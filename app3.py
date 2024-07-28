

from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__,template_folder='template')

# Read anime data from CSV file
anime = pd.read_csv('anime_preprocessed.csv')
indices = pd.read_csv('anime_prediction.csv')
anime['name']=anime['name'].str.lower()

def get_id_from_partial_name(partial):
    for name1 in anime['name']:
        if partial in name1:
           return name1



def get_index_from_name(name):
    for i in range(anime.shape[0]):
        if anime["name"][i] == name:
            return i
    return None

def print_similar_animes(query):
    found_id = get_index_from_name(get_id_from_partial_name(query.lower()))
    if found_id is not None:
        similar_animes = []
        for id in indices.iloc[found_id, 1:]:
            similar_animes.append(anime.iloc[id]["name"].title())
        return similar_animes
    else:
        return []

# @app.route('/')
# def hello_world():
#     return render_template('web3.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    query='k'
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        recommendations = print_similar_animes(query)
        query=get_id_from_partial_name(query.lower())
    
    return render_template('web3.html', recommendations=recommendations,query1=query.title())
if __name__ == '__main__':
    app.run(debug=True)
