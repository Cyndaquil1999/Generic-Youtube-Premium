# Generic Youtube Premium
YoutubePremiumの一部機能（DL, 動画視聴）をTwitterIDを入力することで可能にしたアプリ
なお、DLについては問題ない（https://japan.zdnet.com/article/35162547/）

## 環境
- Python 3.8.10
- flask 2.2.1
- youtube-dl 2021.12.17
- requests 2.22.0

### 動作確認済み
- Ubuntu 20.04
- MacOS 12.2.1

### 構成

```
.
├── README.md
├── download.py
├── run.py
├── static
│   └── css
│       └── styles.css
├── templates
│   ├── index.html
│   ├── movies.html
│   └── test.html
├── twitterAPI.py
└── twitterAPI2.py
```

