from __future__ import unicode_literals
import youtube_dl

def main(link):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)

if __name__ == "__main__":
    main(link)
