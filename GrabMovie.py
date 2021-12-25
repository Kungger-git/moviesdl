## imports
from modules.error_handling import ErrorFunctions as ef
from bs4 import BeautifulSoup
import config as cfg
import traceback
import requests
import time
import re
import os


class MakeSoup():

    # errors that occur when trying to make a request
    communication_errors = []

    def __init__(self, query):
        self.query = query

        # configurations
        self.url = cfg.url
        self.header = cfg.header
        self.quality = cfg.quality
        self.genre = cfg.genre
        self.rating = cfg.rating
        self.order = cfg.order
        self.year = cfg.year
        self.lang = cfg.lang

    def searchResultsPageSoup(self):
        error_msg_prefix = "MakeSoup:searchResultsPageSoup; "

        error_msg = error_msg_prefix
        retry_flag = True
        rate_limit = 5

        while retry_flag:
            try:
                fmt_params = "{}/{}/{}/{}/{}/{}".format(
                        self.quality,
                        self.genre,
                        self.rating,
                        self.order,
                        self.year,
                        self.lang
                    )

                fmt_url = "{}/{}/{}/{}".format(
                        self.url,
                        self.header['browse'],
                        self.query,
                        fmt_params
                    )

                request_response = requests.get(fmt_url, timeout=5)
            except Exception as e:
                error_msg += ef.parseException('send get request', e, fmt_url)
                print(error_msg)
                self.communication_errors.append(error_msg)
                rate_limit -= 1
                time.sleep(3)

                if rate_limit == 0:
                    error_msg += " Rate limit reached."
                    return {'success': False, 'error_msg': error_msg}
                continue
            
            if request_response.status_code == 200:
                soup = BeautifulSoup(request_response.text, 'html.parser')
                return {'success': True, 'error_msg': error_msg, 'data': soup}


    def movieQualityPageSoup(self):
        error_msg_prefix = "MakeSoup:movieQualityPageSoup; "

        error_msg = error_msg_prefix
        retry_flag = True
        rate_limit = 5

        while retry_flag:
            try:
                fmt_url = "{}/{}/{}".format(
                        self.url,
                        self.header['movie-page'],
                        self.query
                    )

                request_response = requests.get(fmt_url, timeout=5)
            except Exception as e:
                error_msg += ef.parseException('send get request', e, fmt_url)
                print(error_msg)
                self.communication_errors.append(error_msg)
                rate_limit -= 1
                time.sleep(3)

                if rate_limit == 0:
                    error_msg += " Rate limit reached."
                    return {'success': False, 'error_msg': error_msg}
                continue
            
            if request_response.status_code == 200:
                soup = BeautifulSoup(request_response.text, 'html.parser')
                return {'success': True, 'error_msg': error_msg, 'data': soup}


class FindMovie():

    def listMovieResults(self, query_page_soup):
        return_msg = "FindMovie:list_results; "
        debug_data = []

        results = {}
        for index, movie in enumerate(query_page_soup.findAll('div', {'class': 'browse-movie-bottom'}), start=1):
            results[index] = {' '.join(movie.text.split()): movie.find('a')['href']}
            
        if results == {}:
            return_msg += "No Results Found. "
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}
        else:
            return_msg += "{} Results Found. ".format(len(results))
            return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': results}


    def listVideoQualities(self, movie_page_soup):
        return_msg = "FindMovie:listVideoQualities"
        debug_data = []

        quality_data = {}
        for qualities in movie_page_soup.findAll('p', {'class': 'hidden-xs hidden-sm'}):
            for index, dl_link in enumerate(qualities.findAll('a', {'rel': 'nofollow'}), start=1):
                quality_data[index] = {dl_link.text: dl_link['href']}

        if quality_data == {}:
            return_msg += "No Available Video Qualities Found. "
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}
        else:
            return_msg += "{} Video Qualities Found. ".format(len(quality_data))
            return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': quality_data}


    def downloadMovieTorrent(self, torrent_url):
        return_msg = "FindMovie:downloadMovieTorrent; "
        debug_data = []

        dir_name = 'torrents'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        
        try:
            origin = os.getcwd()
            with requests.get(torrent_url) as torrent_response:
                torrent_response.raise_for_status()

            disposition = torrent_response.headers['content-disposition']
            torrent_file = re.findall('filename="(.+)"', disposition)

            if torrent_file:
                os.chdir(os.path.join(origin, dir_name))
                with open(torrent_file[0], 'wb') as f_torrent:
                    f_torrent.write(torrent_response.content)

                os.chdir(origin)
        except Exception as e:
            return_msg += ef.parseException('downloading torrent file', traceback.format_exc(), torrent_url)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}
