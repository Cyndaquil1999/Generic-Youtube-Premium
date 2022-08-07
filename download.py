from __future__ import unicode_literals
import youtube_dl
 
def main(url):
    ydl_opts = {'outtmpl': '$HOME/Downloads/%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download((url,))

if __name__ == "__main__":
    main(url)
