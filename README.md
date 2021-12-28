<h1 align="center"> movies-dl </h1>
<p align="center">Download Movie Torrents as easy as 1, 2, 3
<img src="img/movies-dl.gif" />
</p>


### Requirements:
- `requests`
- `bs4`
- `colorama`
- `python-qbittorrent`
- `qbittorrent-api`

### Package Requirements:
- `qbittorrent` - An advanced BitTorrent client.
- `qbittorrent-nox`- qbittorrent but without gui

# Setup:
```
# installing qbittorrent packages
sudo pacman -S qbittorrent qbittorrent-nox

# clone repository & change directory
git clone --depth=1 https://github.com/Kungger-git/movies-dl.git
cd movies-dl/

# install dependency libraries
pip install -r requirements.txt
```

# Usage:
```
# search for a Movie
./movies-dl -s "Spider-man"
---------------------------------------------------

# select a Movie
[1] --> Spider-Man: Into the Spider-Verse 2018
[2] --> Spider-Man: Far from Home 2019
[3] --> Spider-Man: Homecoming 2017
[4] --> The Amazing Spider-Man 2 2014
[5] --> Spider-Man 2 2004
[6] --> Spider-Man 3 2007
[7] --> The Amazing Spider-Man 2012
[8] --> Spider-Man 2002

Enter Choice:
---------------------------------------------------

# select Video Quality
"Spider-Man: Into the Spider-Verse 2018" has been selected.

[1] --> 3D.BluRay
[2] --> 720p.BluRay
[3] --> 1080p.BluRay
[4] --> 2160p.BluRay
[5] --> 720p.WEB
[6] --> 1080p.WEB

Enter Choice:
---------------------------------------------------
```
