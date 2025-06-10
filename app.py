from flask import Flask,request, redirect, url_for,render_template
import next_anime_episode as nae
from pymongo import MongoClient
import threading
import re
import bson
import os
from dotenv import load_dotenv
load_dotenv()






#connecting to database
client = MongoClient(os.getenv('MONGO_URI_NE'))


app = Flask(__name__,
        static_url_path='', 
        static_folder='serving_static_',
        template_folder='serving_static_/templates')
base_url = ''
actual_episode = 0
option = 0
actual_anime_id = ''
db = ''
actual_user = ''
last_player_option = 0
paused = False

def insertAnime():
    global actual_episode
    global base_url

    anime_name_url = base_url.split('ver/').pop()
    img = nae.getting_image(anime_name_url)
    anime_name = re.sub('TV|HD','',anime_name_url).replace('-',' ').upper().strip()
    anime_url = base_url.replace('/ver/','/anime/')
    print(anime_name)
    
    anime = {
         'name': anime_name,
         'actual_episode':actual_episode,
         'base_url':base_url,
         'anime_url': anime_url,
         'image':img
    }
    db.favAnimes.insert_one(anime)


@app.route("/select_user", methods=['POST'])
def select_user():
    global actual_user, db

    actual_user = request.form.get("user")    
    db = client['nextEpisodeDBHome_'+actual_user]

    return app.redirect(url_for('root'))



@app.route("/")
def user():
    return render_template("select_user.html")

@app.route("/home")
def root():
    global db, actual_user
    #getting favorites animes

    if(actual_user==''):
        return redirect(url_for('user'))
    favorites = db.favAnimes.find({})
    return render_template('index.html',id=actual_anime_id,actual_episode=actual_episode, favorites=favorites,player_option = last_player_option)

@app.route("/add",methods=['POST'])
def add_anime():
    global actual_episode
    global base_url
    anime_url = request.form.get('anime_url').replace('m.animeflv.net','www3.animeflv.net').split('-')
    actual_episode = anime_url.pop()
    base_url = '-'.join(anime_url)

    insertAnime()
    return app.redirect(url_for('root'))


@app.route("/deleteFavorites",methods=['POST'])
def delete_favorite():
    global actual_episode
    global base_url
    global option 
    global actual_anime_id

    id = bson.ObjectId(request.form.get('id'))
    db.favAnimes.find_one_and_delete({'_id':id})

    base_url = ''
    actual_episode = ''
    option = ''
    actual_anime_id = ''

    return app.redirect(url_for('root'))
    

@app.route('/next',methods=['POST'])
def next_episode():
    global actual_episode
    global base_url
    global actual_anime_id
    global last_player_option

    actual_episode = int(request.form.get('episode'))

    if(request.form.get('base_url')):
        base_url = request.form.get('base_url')

    if(request.form.get('id')):
        actual_anime_id = bson.objectid.ObjectId(request.form.get('id'))
        
    if(request.form.get('next_episode')):        
        actual_episode+=1

    actual_episode = str(actual_episode)
    db.favAnimes.find_one_and_update({'_id':actual_anime_id}, {'$set':{'actual_episode':actual_episode}} )

    last_player_option = request.form.get('option')

    try:
        print(base_url)
        print(actual_episode)
        print(request.form.get('option'))
        threading.Thread(target=nae.next_episode, args=(base_url,actual_episode,last_player_option)).start()
        #threading.main_thread(app.redirect(url_for('root')))
        #app.redirect(url_for('root'))

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return app.redirect(url_for('root'))


#CONTROLS SESSION
@app.route('/omitirOpening',methods=['POST'])
def omitirOpening():
    nae.omitirOpening()
    return app.redirect(url_for('root'))

@app.route('/adelantar',methods=['POST'])
def adelantar():
    nae.forward()
    return app.redirect(url_for('root'))

@app.route('/atrasar',methods=['POST'])
def atrasar():
    nae.backward()
    return app.redirect(url_for('root'))

@app.route('/volumen',methods=['POST'])
def volumen():
    nae.volumen(request.form.get('action'))
    return app.redirect(url_for('root'))

@app.route('/pause',methods=['POST'])
def pause():
    nae.pause()
    return app.redirect(url_for('root'))


@app.route('/shutdown',methods=['POST'])
def shutdown():
    global actual_user
    if(actual_user==''):
        return redirect(url_for('user'))
    os.system("shutdown now -h")
    return render_template('shutdown.html')

if __name__ == "__main__":
    app.run(debug=False)