import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import lyricsgenius
import re
import json

class lyrics:
	
	### Get Bad Word Document ####
	with open("badwords.txt", "r") as f:
		curses = f.read().strip().split("\n")

	### Get API Keys ###
	with open("keys.txt", "r") as f:
		keys = json.load(f)
	
	def __init__(self, artist, track_album):
		self.artist = artist
		self.album = track_album
		self.track = track_album
		self.suggest = []
		self.tracklist = []
		self.results = []

	def get_tracklist(self):
		#### Spotify API Keys -> Memory ####
		os.environ['SPOTIPY_CLIENT_ID'] = self.keys['sp_client_id'] 
		os.environ['SPOTIPY_CLIENT_SECRET'] = self.keys['sp_client_secret']
		os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com'

		#### Authorize Spotify API Access ####
		auth_manager = SpotifyClientCredentials()
		sp = spotipy.Spotify(auth_manager=auth_manager)
		#### Search for Album ####
		search_results = sp.search(self.artist + " " + self.album, type='album')
		print("Searching Spotify...")
		album_found = False
		for idx, item in enumerate(search_results['albums']['items']):
			if item['artists'][0]['name']==self.artist and item['name']==self.album:
				print("Album Found: ", item['artists'][0]['name'], " – ", item['name'])
				album_found = True
				album_id = item['id']
				break
			if idx < 3:
				self.suggest.append([item['artists'][0]['name'], item['name']])

		#### If Album Isn't Found Exit ####
		if not album_found:
			print("Couldn't find album on spotify :(")
			return False
		#### Get Album Track Names from Spotify ####
		self.tracklist = sp.album_tracks(album_id)
		return True

	def get_track(self):
		#### Spotify API Keys -> Memory ####
		os.environ['SPOTIPY_CLIENT_ID'] = self.keys['sp_client_id'] 
		os.environ['SPOTIPY_CLIENT_SECRET'] = self.keys['sp_client_secret']
		os.environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com'

		#### Authorize Spotify API Access ####
		auth_manager = SpotifyClientCredentials()
		sp = spotipy.Spotify(auth_manager=auth_manager)
		#### Search for Track ####
		search_results = sp.search(self.artist + " " + self.track, type='track')
		print("Searching Spotify...")
		track_found = False
		for idx, item in enumerate(search_results['tracks']['items']):
			if item['artists'][0]['name']==self.artist and item['name']==self.track:
				print("Track Found: ", item['artists'][0]['name'], " – ", item['name'])
				track_found = True
				self.tracklist = {'items': [item]}
				break
			if idx < 3:
				self.suggest.append([item['artists'][0]['name'], item['name']])

		#### If Album Isn't Found Exit ####
		if not track_found:
			print("Couldn't find track on spotify :(")
			return False
		
		
		return True

	def get_lyrics(self):
		genius = lyricsgenius.Genius(self.keys['genius_token'])

		### Get Lyrics and Highlight Bad Words ####
		for idx, item in enumerate(self.tracklist['items']):
			title = item['name']
			artist = item['artists'][0]['name']
			### New song results will be formate [track info, is explicit, lyrics with bad words highlighted] #####
			new_result=[]
			#### Getting Track Lyrics from Genius ####
			try:
				song = genius.search_song(title, artist)
			except:
				print('Error contacting genius!')
				continue
			
			#### Check to See Lyrics Returned ####
			if not song:
				continue

			#### Add Song Result Title ####
			new_result.append(str(item['track_number']) + " " + artist + " – " + title)
			
			#### If track is marked explicit on spotify note it ####
			if item['explicit']:
				new_result.append(True)
			else:
				new_result.append(False)

			#### Highlight Bad Words ####
			song_scrub = song.lyrics
			for curse in self.curses:
				redata = re.compile(r"\b" + r'(' + curse + r')' + r"\b", re.IGNORECASE)
				song_scrub = redata.sub(r'<b>\1</b>', song_scrub)

			new_result.append(song_scrub)
			yield idx, new_result
		return
