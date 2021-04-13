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
            url = f'https://yts.mx/browse-movies/{self.query}/all/all/0/rating/0/all'
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
            print(f'{index} : {movie.text}')

        if not data_set == {}:
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
        else:
            print(colorama.Fore.YELLOW,
                f'[!] There are no results for {self.query}',
                colorama.Style.RESET_ALL)

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
        import qbittorrent, platform
        origin = os.getcwd()
        try:
            qbit = qbittorrent.Client('http://127.0.0.1:8080/')
            qbit.login('admin', 'adminadmin')

            if not os.path.exists('movies'):
                os.mkdir('movies')

            if os.listdir(os.path.join(os.getcwd(), 'torrents')) == []:
                print(colorama.Fore.YELLOW,
                    '[!] No Torrents Downloaded', colorama.Style.RESET_ALL)
            else:
                torrents_dir = os.path.join(os.getcwd(), 'torrents')
                for filename in os.listdir(torrents_dir):
                    if filename.endswith('.torrent'):
                        with open(os.path.join(torrents_dir, filename), 'rb') as tor_dl:
                            qbit.download_from_file(tor_dl, save_path=os.path.join(origin, 'movies'))
                    os.remove(os.path.join(torrents_dir, filename))
                Torrents().check_torrent_status()
        except SystemError as syserr:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {syserr}',
                colorama.Style.RESET_ALL)
    
    def check_torrent_status(self):
        import qbittorrentapi
        try:
            client = qbittorrentapi.Client(host='localhost:8080', username='admin', password='adminadmin')
            print(colorama.Fore.GREEN,
                f'[*] You have {len(client.torrents_info())} Torrent{String_Converters().plural_s(len(client.torrents_info()))}',
                colorama.Style.RESET_ALL)

            torrent_data = {}
            for torrent_index, torrent in enumerate(client.torrents_info(), start=1):
                torrent_data[torrent_index] = {torrent.name : torrent.hash}                
                if args.downloadtorrents or args.checktorrentstatus:
                    if torrent.state_enum.is_errored:
                        print(colorama.Fore.YELLOW,
                            f'[!] Deleting {torrent.name}, because its current state is errored',
                            colorama.Style.RESET_ALL)
                        client.torrents_delete(delete_files=True, torrent_hashes=[torrent.hash])
                    
                    elif torrent.state_enum.is_complete:
                        print(colorama.Fore.YELLOW, f'[!] {torrent.name} complete.', colorama.Style.RESET_ALL)                           
                        print(colorama.Fore.YELLOW, f'[!] Deleting saved torrent: {torrent.name}, because current state is complete\n',
                            colorama.Style.RESET_ALL)
                        client.torrents_delete(delete_files=False, torrent_hashes=[torrent.hash])
                    
                    elif torrent.state_enum.is_downloading:
                        data_set = {'Torrent': torrent.name, 'Progress': '{:.2%}'.format(torrent.progress), 'Seeders': torrent.num_seeds, 'Peers': torrent.num_leechs,
                                    'Downloaded': f'{String_Converters().format_bytes(torrent.downloaded)} / {String_Converters().format_bytes(torrent.total_size)}',
                                    'Download Speed': f'{String_Converters().format_bytes(torrent.dlspeed)}p/s', 'ETA': String_Converters().convert(torrent.eta)}
                        for data in data_set:
                            print(colorama.Fore.YELLOW, f'[!] {data}: {data_set[data]}', colorama.Style.RESET_ALL)
                
                if args.removetorrent:
                    print(f'{torrent_index} : {torrent.name}')

            if args.removetorrent:        
                if not torrent_data == {}:
                    while True:
                        remove_selection = int(input('\n\nEnter Index/Indices of which to delete: '))
                        if not remove_selection in torrent_data:
                            print(colorama.Fore.RED,
                                f'[!!] {remove_selection} is not a valid selection',
                                colorama.Style.RESET_ALL)
                        else:
                            for element in torrent_data[remove_selection]:
                                print(colorama.Fore.GREEN,
                                    f'[!] Deleted {element}', colorama.Style.RESET_ALL) 
                                return client.torrents_delete(delete_files=True, torrent_hashes=[torrent_data[remove_selection][element]])
        except SystemError as syserr:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {syserr}', colorama.Style.RESET_ALL)


class String_Converters:

    def plural_s(self, v):
        return 's' if not abs(v) == 1 else ''

    def convert(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return "%d:%02d:%02d" % (hours, mins, secs)

    def format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f'{round(size, 2)} {power_labels[n]}b'


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(description="Download Movies Through the terminal")

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help="Searches for the movie. (e.g. --search 'avengers')")

    parser.add_argument('-dlt', '--downloadtorrents',
                        action='store_true',
                        help='Downloads torrent files in the torrents directory')

    parser.add_argument('-cts', '--checktorrentstatus',
                        action='store_true',
                        help='Checks torrent status on qbittorrent localhost server')

    parser.add_argument('-rmt', '--removetorrent',
                        action='store_true',
                        help='Deletes torrents')

    args = parser.parse_args()
    if args.search:
        Get_Connection([x for x in args.search]).conn()

    if args.downloadtorrents:
        Torrents().movies_dl()

    if args.checktorrentstatus or args.removetorrent:
        Torrents().check_torrent_status()
