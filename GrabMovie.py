## imports
from modules.error_handling import ErrorFunctions as ef
from modules.convert_string import StringConverter as sc
from bs4 import BeautifulSoup
import config as cfg
import traceback
import requests
import time
import re
import os

# qbittorrent libs
import qbittorrent
import qbittorrentapi

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
        return_msg = "FindMovie:listVideoQualities; "
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

        try:
            origin_dir = os.getcwd()
            dest_dir = os.path.expanduser("~/Downloads/torrents")
            
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)

            with requests.get(torrent_url) as torrent_response:
                torrent_response.raise_for_status()

            disposition = torrent_response.headers['content-disposition']
            torrent_file = re.findall('filename="(.+)"', disposition)

            if torrent_file:
                os.chdir(dest_dir)
                with open(torrent_file[0], 'wb') as f_torrent:
                    f_torrent.write(torrent_response.content)

                os.chdir(origin_dir)
        except Exception as e:
            return_msg += ef.parseException('downloading torrent file', traceback.format_exc(), torrent_url)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        torrent = ''.join(torrent_file)
        if not os.path.exists(os.path.join(dest_dir, torrent)):
            return_msg += "cannot confirm file location."
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}
        else:
            torrent_path = os.path.join(dest_dir, torrent)
            return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': torrent_path}

class Torrent:

    def __init__(self, username=cfg.username, password=cfg.password):
        self.client = cfg.client
        self.username = username
        self.password = password
        self.host = "{}:{}".format(cfg.host, cfg.port)


    def loginQbitClient(self):
        return_msg = "Torrent:loginQbitClient; "
        debug_data = []

        try:
            qbit = qbittorrent.Client(self.client)
            qbit.login(self.username, self.password)
        except Exception as e:
            return_msg += ef.parseException(
                    'logging into qbittorrent server client.', e, 
                    [self.username, self.password]
                )
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': qbit}

    def downloadMovie(self, qbit_client_auth, torrent_path):
        return_msg = "Torrent:downloadMovie; "
        debug_data = []
 
        dl_dir = os.path.expanduser('~/Downloads')
        dest_dir = os.path.join(dl_dir, 'movies')
       
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        
        try:
            with open(torrent_path, 'rb') as tor:
                qbit_client_auth.download_from_file(tor, save_path=dest_dir)
            os.remove(torrent_path)
        except Exception as e:
            return_msg += ef.parseException("downloading movie from torrent file.", e, torrent_path)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data}

  
    def authorizeAPIAccess(self):
        return_msg = "Torrent:authorizeAPIAccess; "
        debug_data = []

        try:
            api_client = qbittorrentapi.Client(
                    host=self.host,
                    username=self.username,
                    password=self.password
                )
        except Exception as e:
            return_msg += ef.parseException('Connection to Local qbit Server Failed', e, "")
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': api_client}


    def statusCheck(self, api_auth):
        return_msg = "Torrent:statusCheck; "
        debug_data = []

        try:
            torrent_data = {}
            for torrent in api_auth.torrents_info():
                torrent_data = {
                    'torrent_name': torrent.name,
                    'progress': '{:.1%}'.format(torrent.progress),
                    'seeders': torrent.num_seeds,
                    'peers': torrent.num_leechs,
                    'downloaded': "{}/{}".format(sc.formatBytes(torrent.downloaded), sc.formatBytes(torrent.total_size)),
                    'download_speed': "{}/s".format(sc.formatBytes(torrent.dlspeed)),
                    'eta': sc.convertTime(torrent.eta)
                }
                if torrent.state_enum.is_complete:
                    return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': 1}
                elif torrent.state_enum.is_errored:
                    return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data, 'data': 2}
        except Exception as e:
            return_msg += ef.parseException('retrieving movie download info', e, api_auth)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data, 'data': torrent_data}


    def cleanUp(self, api_auth):
        return_msg = "Torrent:cleanUp; "
        debug_data = []

        try:
            for torrent in api_auth.torrents_info():
                if torrent.state_enum.is_errored:
                    api_auth.torrents_delete(
                        delete_files=True,
                        torrent_hashes=[torrent.hash]
                    )
                elif torrent.state_enum.is_complete:
                    api_auth.torrents_delete(
                        delete_files=False,
                        torrent_hashes=[torrent.hash]
                    )
        except Exception as e:
            return_msg += ef.parseException('clean up clutter in Qbittorrent', e, api_auth)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}

        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data}


    def deleteTorrents(self, api_auth):
        return_msg = "Torrent:deleteTorrents; "
        debug_data = []

        try:
            for torrent in api_auth.torrents_info():
                api_auth.torrents_delete(
                    delete_files=True,
                    torrent_hashes=[torrent.hash]
                )
        except Exception as e:
            return_msg += parseException('delete all torrents', e, api_auth)
            return {'success': False, 'return_msg': return_msg, 'debug_data': debug_data}
        
        return {'success': True, 'return_msg': return_msg, 'debug_data': debug_data}
