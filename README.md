# LyricScrub

A web application that takes albums and quickly scrubs the lyrics for bad words.

### Prerequisites

Python 3 with the default libraries is required in addition to:
* flask
* spotipy
* lyricsgenius

A Genius access token and a Spotify client ID and secret are required to access the APIs. They should be places in file titled "keys.txt" in the primary directory in the following format:
```
{
	"genius_token": "insert Genius access token",
	"sp_client_id": "insert Spotify client ID",
	"sp_client_secret": "insert Spotify client secret"
}
```
Additionally, Flask requires a web session password; and there is a password to access the demo version of the site. This information should be stored in the same directory and be titled "web_secrets.txt" and follow this format:
```
{
	"secret_key": "insert session password (any randomly chosen string will work)",
	"password": "insert website access password"
}
```

### Usage
Run LyricScrub.py and access the development site at localhost:5000 in a web browser.
Users will be prompted to input an album and artist to find lyrics for.
If the album is found, the program will get the track list using Spotify API and then attempt to find the lyrics on Genius.
If lyrics are found, the program will cross reference the song lyrics with a list of potentially offensive words.
If the album is marked as explicit on Spotify, it will be noted in the final results. 

## Built With

* [LyricsGenius](https://pypi.org/project/lyricsgenius/) - Get lyrics from Genius.com
* [Spotipy](https://github.com/plamere/spotipy) - Interface with Spotify API


## Authors

* **Cameron Armand**

## License

All of the code original to this project is free to be used, reused, and edited in any capacity. The project, in its current form, should be for personal use only. The LyricsGenius library uses web scrapping and should be used at your own risk.