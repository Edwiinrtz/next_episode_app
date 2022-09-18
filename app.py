from flask import Flask,request, redirect, url_for,render_template
import next_anime_episode as nae
from pymongo import MongoClient
import re
import pprint

import bson





#connecting to database
client = MongoClient("mongodb+srv://asd:mTDSZLoMkaNeL6DL@nextepisodedb.pthngit.mongodb.net/?retryWrites=true&w=majority")
db = client['nextEpisodeDB']

app = Flask(__name__,
        static_url_path='', 
        static_folder='serving_static_',
        template_folder='serving_static_/templates')
base_url = ''
actual_episode = 0
option = 0
actual_anime_id = ''

def insertAnime():
    global actual_episode
    global base_url

    anime_name = base_url.split('ver/').pop().replace('-',' ').strip().upper()
    anime_name = re.sub('TV|HD','',anime_name).strip()

    anime = {
         'name': anime_name,
         'actual_episode':actual_episode,
         'base_url':base_url,
         'anime_url': base_url.replace('/ver/','/anime/')
    }
    db.favAnimes.insert_one(anime)

@app.route("/")
def root():
    #getting favorites animes

    favorites = db.favAnimes.find({})
    pprint.pprint(favorites)
    return render_template('index.html',id=actual_anime_id,actual_episode=actual_episode, favorites=favorites)

@app.route("/add",methods=['POST'])
def add_anime():
    global actual_episode
    global base_url
    anime_url = request.form.get('anime_url').split('-')
    print(anime_url)
    actual_episode = anime_url.pop()
    base_url = '-'.join(anime_url)

    print(base_url+''+actual_episode)
    insertAnime()
    return app.redirect(url_for('root'))
    

@app.route('/next',methods=['POST'])
def next_episode():
    global actual_episode
    global base_url
    global actual_anime_id

    actual_episode = request.form.get('episode')

    if(request.form.get('base_url')):
        base_url = request.form.get('base_url')
    
    if(request.form.get('id')):
        actual_anime_id = bson.objectid.ObjectId(request.form.get('id'))
        print(actual_anime_id)
        actual_anime = db.favAnimes.find_one({'_id':actual_anime_id})

        actual_episode = str(int(actual_anime['actual_episode'])+1)
        print(actual_anime)
        db.favAnimes.find_one_and_update({'_id':actual_anime_id}, {'$set':{'actual_episode':actual_episode}} )


    try:
        print(base_url)
        print(actual_episode)
        print(request.form.get('option'))
        nae.next_episode(base_url,actual_episode,request.form.get('option'))
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return app.redirect(url_for('root'))


if __name__ == "__main__":
    app.run(debug=False)