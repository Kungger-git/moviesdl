# Configuration file for quick & easy access to values.

# This is used for establishing connection
# with the qbittorrent client.
host = "localhost"
port = "8080"
client = "http://{}:{}/".format(host, port)

# user credentials.
username = "admin"
password = "adminadmin"

# main search configuration
"""
Avaliable Video Quality options:
- all (default)
- 720p
- 1080p
- 2160p
- 3D
"""
quality = "all"

"""
Available Movie Genre options:
- all (default)
- Action
- Adventure
- Animation
- Biography
- Comedy
- Crime
- Documentary
- Drama
- Family
- Fantasy
- Film-Noir
- Game-Show
- History
- Horror
- Music
- Musical
- Mystery
- News
- Reality-TV
- Romance
- Sci-Fi
- Sport
- Talk-Show
- Thriller
- War
- Western
"""
genre = "all"

"""
Available Movie Rating options:
- 0 (default for all)
- 1 - 9
"""
rating = 0

"""
Available Sorting options:
- latest(default)
- oldest
- featured
- seeds
- peers
- year
- rating
- likes
- alphabetical
- downloads
"""
order = "latest"

""" 
Available Year options:
- 0 (default for all)
- 2021
- 2020
- 2019
- 2015-2018
- 2010-2014
- 2000-2009
- 1990-1999
- 1980-1989
- 1970-1979
- 1900-1969
"""
year = "0"

""" Language """
lang = "all"

header = {'browse': 'browse-movies', 'movie-page': 'movies'}
url = "https://yts.mx/"
