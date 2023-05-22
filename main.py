#Importing Libraries
from flask import Flask , render_template ,request,redirect,flash
import re
from pytube import Playlist,YouTube
import os

#App Configurations
app = Flask(__name__)
app.secret_key="Super Secret Key"

#Functions
def get_youtube_url_type(url):
    video_pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/watch\?v=([\w-]+)'
    playlist_pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com)/playlist\?list=([\w-]+)'
    short_video_pattern = r'(?:https?://)?(?:www\.)?youtu\.be/([\w-]+)'
    video_match = re.match(video_pattern, url)
    if video_match:
        return 'Video'
    playlist_match = re.match(playlist_pattern, url)
    short_video_match = re.match(short_video_pattern, url)
    if short_video_match:
        return 'Video'
    if playlist_match:
        return 'Playlist'
    return None

def is_valid_youtube_video(url):
    try:
        video = YouTube(url)
        return not video.age_restricted
    except Exception:
        return False

def is_valid_youtube_playlist(url):
    try:
        playlist = Playlist(url)
        return True
    except Exception:
        return False

def audio(url):
  try:
   destination ="static/Downloads/Audio"
   yt = YouTube(url)
   video = yt.streams.filter(only_audio=True).first()
   out_file = video.download(output_path = destination)
   base, ext = os.path.splitext(out_file)
   new_file = base + '.mp3'
   os.rename(out_file, new_file)
  except Exception as e:
    flash(f"Url's Video don't exist or is private. {url}","warning") 

def video(url):
  try:
    destination ="static/Downloads/Video"
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    out_file = video.download(output_path = destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp4'
    os.rename(out_file, new_file)
  except Exception as e:
    flash(f"Url's Video don't exist or is private. {url}","warning")


#Routes
@app.route("/",methods=["GET","POST"])
def home():
  if request.method == "POST":
    # try:
      file_type=request.form["file_type"]
      url=request.form["url"]

      a = get_youtube_url_type(url)

      if a ==None:
        flash(" Invalid Url , Please enter the url of a youtube video or playlist only","warning")

      elif a=="Video":
        if  is_valid_youtube_video(url)==True:
          if file_type=="Audio":
              audio(url)
          elif file_type=="Video":
              video(url)
        elif is_valid_youtube_video(url)==False:
          flash("Video don't exist or is private. :(","warning")
        else:
            flash(" Something Went Wrong :( ","danger")
      
      elif a=="Playlist":
        if  is_valid_youtube_playlist(url)==True:
          if file_type=="Audio":
              playlist = Playlist(url)
              for url in playlist:
                 audio(url)
          elif file_type=="Video":
              playlist = Playlist(url)
              for url in playlist:
                 video(url)
        elif is_valid_youtube_playlist(url)==False:
          flash(" Playlist don't exist or is private. :(","warning")
        else:
            flash(" Something Went Wrong :( ","danger")
        
      else:
        flash(" Something Went Wrong :( ","danger")
        
    # except Exception as e:
    #    flash(" Please choose Music/Video and Give a URL ","danger")

  return render_template("index.html")


#Running The App
if __name__ == "__main__":
  app.run(debug=True)