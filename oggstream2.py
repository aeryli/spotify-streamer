import http
import time
import socket
import requests
import webbrowser
from pathlib import Path as pathy
from librespot.core import Session
from librespot.metadata import TrackId
from spotify_scraper import SpotifyClient
from http.server import BaseHTTPRequestHandler, HTTPServer
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

def gimmeIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception: ip = '127.0.0.1'
    finally: s.close()
    return ip
class mergle:
    def __init__(self):          self.track_uri = "spotify:track:2FpEXjGqe2dJJ9oB8c8Io2"
    def auth_url_callback(url):  webbrowser.open(url)
    def login(self):
        success_page = "<html><body><h1>Login Successful.</h1><p>You can close this window now.</p><script>setTimeout(() => {window.close()}, 100);</script></body></html>"
        self.session = Session.Builder().oauth(self.auth_url_callback, success_page).create()
    def getStrem(self, trackURI):
        track_id = TrackId.from_uri(trackURI)
        content_stream = self.session.content_feeder().load(track_id, VorbisOnlyAudioQuality(AudioQuality.NORMAL), False, None)
        self.raw_stream = content_stream.input_stream.stream()
    def verbose():
        print(self.raw_stream)
        print(type(self.raw_stream))
    def stremchunk(self, chsize):
        
        chunk = self.raw_stream.read(chsize)
        return chunk
    def headers(write, mime):
        if mime:
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            write()
class MI(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path.startswith("/music/")):
            stuffs = self.path.split("/music/")[1].split("/")
            track_uri = stuffs[0]
            if track_uri:
                print(track_uri)
                mergel = mergle()
                mergel.login()
                mergel.getStrem(track_uri)

                self.send_response(200)
                self.send_header("Content-Type", "audio/ogg")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                try:
                    while True:
                        chunk = mergel.stremchunk(1024*4)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        self.wfile.flush()
                except Exception as e:
                    print(e)
            
        elif (self.path.startswith("/cover/")):
            stuffs = self.path.split("/cover/")[1].split("/")[0].split("spotify:track:")[1]
            
            with SpotifyClient() as client:
                track = client.get_track(stuffs)
                response = requests.get(track.to_dict()["images"][0]["url"])
            
            self.send_response(200)
            self.send_header("Content-Type", response.headers.get('Content-Type'))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(response.content)
            self.wfile.flush()
            
        elif (self.path.startswith("/data/")):
            stuffs = self.path.split("/data/")[1].split("/")
            with SpotifyClient() as client:
                track = client.get_track(stuffs[0].split("spotify:track:")[1]).to_dict()
            
            pathys = stuffs[1:(len(stuffs)-1)]
            for i in range(len(pathys)):
                track = track[pathys[i]]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            
            self.wfile.write(str(track).encode())
            self.wfile.flush()
        else:
            self.send_error(404)
    
print(f"HTTP is here: {hasattr(http, 'HTTPStatus')}")
print(f"Connect to: http://{gimmeIP()}:8000/music/spotify:track:xxxxxxxxxxxxxxxxxxxxxx")
print(f"Example: http://{gimmeIP()}:8000/music/spotify:track:2FpEXjGqe2dJJ9oB8c8Io2")
print(f"Example: http://{gimmeIP()}:8000/cover/spotify:track:2FpEXjGqe2dJJ9oB8c8Io2")
print(f"Example: http://{gimmeIP()}:8000/data/spotify:track:2FpEXjGqe2dJJ9oB8c8Io2")
try:
    httpd = HTTPServer(('', 8000), MI)
    httpd.serve_forever()
except Exception as e:
    print(e)




