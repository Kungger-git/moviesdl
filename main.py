from bs4 import BeautifulSoup as soup
import argparse
import colorama
import requests
import os


class Get_Connection:

    def __init__(self, search_query):
        for query in search_query:
            self.query = query

    def conn(self):
        try:
            url = f'https://yts.mx/browse-movies/{self.query}/all/all/0/rating/0/en'
            with requests.get(url) as response:
                response.raise_for_status()
                page_soup = soup(response.text, 'html.parser')
            
            return Get_Movies(self.query, page_soup).list_movies()
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)

class Get_Movies:

    def __init__(self, query, locator):
        self.query = query
        self.locator = locator

    def list_movies(self):
        data_set = {}
        for index, movie in enumerate(self.locator.findAll('a', {'class': 'browse-movie-title'}), start=1):
            data_set[index] = {movie.text: movie['href']}

        for index, title_index in enumerate(data_set, start=1):
            if index == title_index:
                for title in data_set[title_index]:
                    print(f'{index} : {title}')

        while True:
            selection = int(input('\n\nSelect the index of the movie to download: '))
            if not selection in data_set:
                print(colorama.Fore.RED,
                    f'[!!] {selection} is not a valid selection',
                    colorama.Style.RESET_ALL)
            else:
                for title in data_set[selection]:
                    print(colorama.Fore.YELLOW,
                        f'[!] {title} has been selected\n\n', colorama.Style.RESET_ALL)
                    print(colorama.Fore.GREEN,
                        f'[*] Getting Available Video Qualities for {title}', colorama.Style.RESET_ALL)
                    return Get_Movies(self.query, self.locator).find_torrent(data_set[selection][title])

    def find_torrent(self, url):
        try:
            with requests.get(url) as movie_response:
                movie_response.raise_for_status()
                page_soup = soup(movie_response.text, 'html.parser')
            
            quality_data = {}
            for quality in page_soup.findAll('p', {'class': 'hidden-xs hidden-sm'}):
                for index, download_link in enumerate(quality.findAll('a', {'rel': 'nofollow'}), start=1):
                    quality_data[index] = {download_link.text: download_link['href']}
                    print(f'{index} : {download_link.text}')

            while True:
                select_quality = int(input('\n\nSelect Index of Desired Quality: '))
                if not select_quality in quality_data:
                    print(colorama.Fore.RED,
                        f'[!!] {select_quality} is not a valid quality selection',
                        colorama.Style.RESET_ALL)
                else:
                    for torrent in quality_data[select_quality]:
                        for selected in quality_data[select_quality].keys():
                            print(colorama.Fore.YELLOW,
                                f'[!] {selected} quality has been selected\n\n',
                                colorama.Style.RESET_ALL)
                        print(colorama.Fore.GREEN,
                            f'[*] Downloading Torrent File')
                        return Get_Movies(self.query, self.locator).dl_torrent(quality_data[select_quality][torrent])
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)

    def dl_torrent(self, torrent_url):
        import re, traceback
        folder_name = 'torrents'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        try:
            origin = os.getcwd()
            with requests.get(torrent_url) as torrent_response:
                torrent_response.raise_for_status()

            disposition = torrent_response.headers['content-disposition']
            torrent_file = re.findall('filename="(.+)"', disposition)
            if torrent_file:
                os.chdir(os.path.join(origin, folder_name))
                with open(torrent_file[0], 'wb') as f_torrent:
                    f_torrent.write(torrent_response.content)

                print(colorama.Fore.YELLOW,
                    '[!] Torrent File Downloaded', colorama.Style.RESET_ALL)
                os.chdir(origin)
        except:
            print(colorama.Fore.RED,
                traceback.format_exc(), colorama.Style.RESET_ALL)

class Torrents:

    def movies_dl(self):
        import qbittorrent
        origin = os.getcwd()
        try:
            qbit = qbittorrent.Client('http://127.0.0.1:8080/')
            qbit.login('admin', 'adminadmin')

            os.chdir(os.path.join(origin, 'torrents'))
            if os.listdir() == []:
                print(colorama.Fore.YELLOW,
                    '[!] No Torrents Downloaded', colorama.Style.RESET_ALL)
            else:
                for torrent in os.listdir():
                    tor_dl = open(torrent, 'rb')
                    qbit.download_from_file(tor_dl, savefile=os.path.join(origin, 'torrents'))
                    Torrents().check_torrent_status()

                    os.remove(torrent)
            os.chdir(origin)
        except SystemError as syserr:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {syserr}',
                colorama.Style.RESET_ALL)
    
    def check_torrent_status(self):
        import qbittorrentapi
        try:
            client = qbittorrentapi.Client(host='localhost:8080', username='admin', password='adminadmin')

            for torrent in client.torrents_info():
                state_enum = qbittorrentapi.TorrentStates(torrent.state)
                print(colorama.Fore.YELLOW,
                    f'[!] {torrent.name}: {state_enum.value}', colorama.Style.RESET_ALL)
        except SystemError as syserr:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {syserr}', colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(description="Download Movies Through the terminal")

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help="Searches for the movie. (e.g. --search 'avengers')")

    parser.add_argument('-d', '--downloadtorrents',
                        action='store_true',
                        help='Downloads torrent files in the torrents directory')

    parser.add_argument('-c', '--checkstatus',
                        action='store_true',
                        help='Checks torrent status on qbittorrent localhost server')

    args = parser.parse_args()
    if args.search:
        Get_Connection([x for x in args.search]).conn()

    if args.downloadtorrents:
        Torrents().movies_dl()

    if args.checkstatus:
        Torrents().check_torrent_status()
