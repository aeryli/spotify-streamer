import http
import time
import webbrowser
from pathlib import Path as pathy
from librespot.core import Session
from librespot.metadata import TrackId
from http.server import BaseHTTPRequestHandler, HTTPServer
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

class mergle:
    def __init__(self):
        self.track_uri = "spotify:track:2FpEXjGqe2dJJ9oB8c8Io2"
        if (self.track_uri == ""):
            self.track_uri = input("Set the track uri(spotify:track:[trackID]): ")
    def auth_url_callback(url):
        webbrowser.open(url)
    def login(self):
        success_page = "<html><body><h1>Login Successful.</h1><p>You can close this window now.</p><script>setTimeout(() => {window.close()}, 100);</script></body></html>"
        self.session = Session.Builder().oauth(self.auth_url_callback, success_page).create()
    def getStrem(self, trackURI):
        track_id = TrackId.from_uri(trackURI)
        content_stream = self.session.content_feeder().load(track_id, VorbisOnlyAudioQuality(AudioQuality.HIGH), False, None)
        self.raw_stream = content_stream.input_stream.stream()
    def verbose():
        print(self.raw_stream)
        print(type(self.raw_stream))
    def strem(strem):
        #wawa to 3ds / other thing (meaning stream to self)
        while True:
            chunk = self.raw_stream.read(4096)
            if not chunk:
                break
            #streeeeeeeeeeeeeeeeeeeeeeeeeeeeeemmmmmmmmmmmmm
    def stremchunk(self):
        chunk = self.raw_stream.read(4096)
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
            track_uri = self.path.split("/music/")[1].split("/")[0]
            if track_uri:
                print(track_uri)
                mergel = mergle()
                mergel.login()
                mergel.getStrem(track_uri)

                self.send_response(200)
                self.send_header("Content-Type", "audio/ogg")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                
                while True:
                    chunk = mergel.stremchunk()
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
                
        elif (self.path.startswith("/source/")):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            
            try:
                chunk = open(r"C:\Users\alixc\3ds\spotify\spotify.c", "r", encoding="utf-8")
                print(chunk.read())
                self.wfile.write(chunk.read().encode())
                self.wfile.flush()
            except Exception as e:
                print("Error: " + str(e))
        else:
            self.send_error(404)
    
print(f"HTTP is here: {hasattr(http, 'HTTPStatus')}")
httpd = HTTPServer(('', 8000), MI)
httpd.serve_forever()