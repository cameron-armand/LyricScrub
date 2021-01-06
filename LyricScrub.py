from flask import Flask, render_template, request, session, redirect, url_for, Response, stream_with_context
import time
import lyrics
import json

app = Flask(__name__)

with open("web_secrets.txt", 'r') as f:
	secrets = json.load(f)

app.secret_key = secrets['secret_key']
password = secrets['password']

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		attempt = request.form['password']
		if attempt == password:
			session["password"] = attempt
			return redirect(url_for('index'))
		else:
			return render_template('login.html', badpassword=True)
	else:
		return render_template('login.html')

@app.route('/', methods=['GET','POST'])
def index():

	### Handle form post ####
	if not 'password' in session:
		return redirect(url_for('login'))
	elif request.method == 'POST' and session['password'] == password:
		### Get input from form ####
		artist = request.form['artist']
		album_track = request.form['album']
		session['mode'] = request.form.get('mode')

		### Validate response ####
		if not artist or not album_track:
			return render_template('index.html', badartist=not artist, badalbum=not album_track, isdark=session.get('mode'))

		### Initialize results object ####
		item = lyrics.lyrics(artist,album_track)

		### Return if album isn't found on spotify ####
		if request.form['action'] == "track":
			if not item.get_track():
				return render_template('index.html', isdark=session.get('mode'), notfound="Couldn't find that track &#x1F614", len=len(item.suggest), suggest=item.suggest, tracksearch=True)
		else:
			if not item.get_tracklist():
				return render_template('index.html', isdark=session.get('mode'), notfound="Couldn't find that album &#x1F614", len=len(item.suggest), suggest=item.suggest)

		rows = item.get_lyrics()
		return Response(stream_with_context(stream_template('results.html', rows=rows, isdark=session.get('mode'), len=len(item.tracklist['items']))))

	### Handle initial load ####
	else:
		return render_template('index.html', isdark=session.get('mode'))

if __name__ == '__main__':
	app.run()
