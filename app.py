from flask import Flask,request, redirect, url_for,render_template
import next_anime_episode as nae

app = Flask(__name__,
        static_url_path='', 
        static_folder='serving_static_',
        template_folder='serving_static_/templates')
base_url = ''
actual_episode = 0
option = 0

@app.route("/")
def root():
    return render_template('index.html',actual_episode=actual_episode)

@app.route("/add",methods=['POST'])
def add_anime():
    global actual_episode
    global base_url
    anime_url = request.form.get('anime_url').split('-')
    print(anime_url)
    actual_episode = anime_url.pop()
    base_url = '-'.join(anime_url)

    print(base_url+''+actual_episode)
    return app.redirect(url_for('root'))
    

@app.route('/next',methods=['POST'])
def next_episode():
    global actual_episode

    actual_episode = request.form.get('episode')
    try:
        print(base_url)
        print(actual_episode)
        print(request.form.get('option'))
        nae.next_episode(base_url,actual_episode,request.form.get('option'))
    except:
        print("ha ocurrido un error")

    return app.redirect(url_for('root'))


if __name__ == "__main__":
    app.run(debug=False)