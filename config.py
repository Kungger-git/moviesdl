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
- rating (default)
- oldest
- featured
- seeds
- peers
- year
- latest
- likes
- alphabetical
- downloads
"""
order = "rating"

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

""" Available Language Options:
- en (English, default)
- all
- foreign
- fr (French)
- ja (Japanese)
- it (Italian)
- es (Spanish)
- de (German)
- zh (Chinese)
- ko (Korean)
- cn (Cantonese)
- hi (Hindi)
- ru (Russian)
- sv (Swedish)
- pt (Portuguese)
- pl (Polish)
- th (Thai)
- da (Danish)
- nl (Dutch)
- no (Norwegian)
- ta (Tamil)
- te (Telugu)
- vi (Vietnamese)
- fi (Finnish)
- cs (Czech)
- tr (Turkish)
- id (Indonesian)
- fa (Persian)
- el (Greek)
- tl (Tagalog)
- hu (Hungarian)
- ar (Arabic)
- he (Hebrew)
- ro (Romanian)
- et (Estonian)
- bn (Bangla)
- ur (Urdu)
- ms (Malay)
- is (Icelandic)
- ml (Malayalam)
- uk (Ukrainian)
- sr (Serbian)
- xx (xx)
- ca (Catalan)
- sk (Slovak)
- pa (Punjabi)
- af (Afrikaans)
- wo (Wolof)
- ka (Georgian)
- mr (Marathi)
- eu (Basque)
- lv (Latvian)
- bo (Tibetan)
- kn (Kannada)
- am (Amharic)
- gl (Galician)
- la (Latin)
- bs (Bosnian)
- ak (Akan)
- sh (Serbo-Croatian)
- lt (Lithuanian)
- mn (Mongolian)
- nb (Norwegian Bokmal)
- sw (Swahili)
- iu (Inuktitut)
- so (Somali)
- cy (Welsh)
- st (Southern Sotho)
- lg (Ganda)
- be (Belarusian)
- hy (Armenian)
- hr (Croatian)
- zu (Zulu)
- ig (Igbo)
- ku (Kurdish)
- ab (Abkhazian)
- az (Azerbaijani)
- ht (Haitian Creole)
- ky (Kyrgyz)
- ps (Pashto)
- lb (Luxembourgish)
- ga (Irish)
- mi (Maori)
- aa (Afar)
- km (Khmer)
- yi (Yiddish)
- mk (Macedonian)
- os (Ossetic)
"""
lang = "en"

header = {'browse': 'browse-movies', 'movie-page': 'movies'}
url = "https://yts.mx/"
