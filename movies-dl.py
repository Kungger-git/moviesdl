#!/bin/env python

# imports
from modules import nox
from modules import colors as c
from modules.run_once import run_once
from modules.clear import clear
from modules.convert_string import StringConverter as sc
from modules.error_handling import ErrorFunctions as ef
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from GrabMovie import MakeSoup, FindMovie, Torrent
from time import sleep
import os


class MoviesDl():

    def __init__(self, search_query):
        self.search_query = search_query


    def selectMovie(self):
        clear()

        result_movie = MakeSoup(self.search_query).searchResultsPageSoup()
        fm = FindMovie()

        if result_movie['success'] != True:
            print(result_movie['error_msg'])
            exProc() 
        elif result_movie['success'] == True:
            movie_results = fm.listMovieResults(result_movie['data'])

        if not 'data' in movie_results:
            print(movie_results['return_msg'])
            exProc() 
        elif 'data' in movie_results:
            res = movie_results['data']
            for movie in res:
                print("[{}{}{}] {}-->{} {}{}{}".format(
                      c.GREEN, movie, c.RESET,
                      c.RED, c.RESET,
                      c.BLUE, ''.join(res[movie]), c.RESET))

        movie_selected = {}
        try:
            retry_flag = True

            while retry_flag == True:
                selection = int(input("\n{}Enter Choice: {}".format(c.RED, c.RESET)))

                if not selection in res:
                    print("\n{}Invalid Range.{}\n".format(c.RED, c.RESET))
                    exProc() 
                elif selection in res:
                    for title in res[selection]:
                        clear()

                        retry_flag = False
                        return {'title': title, 'movie_page_url': res[selection][title]}
        except KeyboardInterrupt:
            print('\nStopped!')
            exProc() 

    
    def selectQuality(self, movie):
        clear()

        print("{}\"{}\"{} has been selected.\n".format(
              c.GREEN, movie['title'], c.RESET))

        fmt_mpage_query = movie['movie_page_url'].split('/')[-1]
        result_quality = MakeSoup(fmt_mpage_query).movieQualityPageSoup()
        fm = FindMovie()

        if result_quality['success'] != True:
            print(result_quality['error_msg'])
            exProc() 
        elif result_quality['success'] == True:
            quality_results = fm.listVideoQualities(result_quality['data'])
            
        if not 'data' in quality_results:
            print(quality_results['return_msg'])
            exProc() 
        elif 'data' in quality_results:
            res = quality_results['data']
            for quality in res:
                print("[{}{}{}] {}-->{} {}{}{}".format(
                      c.GREEN, quality, c.RESET,
                      c.RED, c.RESET,
                      c.BLUE, ''.join(res[quality]), c.RESET))
        
        quality_selected = {}
        try:
            retry_flag = True

            while retry_flag == True:
                selection = int(input("\n{}Enter Choice: {}".format(c.RED, c.RESET)))

                if not selection in res:
                    print("\n{}Invalid Range.{}\n".format(c.RED, c.RESET))
                    exProc() 
                elif selection in res:
                    for quality in res[selection]:
                        clear()

                        retry_flag = False
                        return {'quality': quality, 'torrent_url': res[selection][quality]}
        except KeyboardInterrupt:
            print('\nStopped!')
            exProc() 


    def getTorrent(self, torrent_info):
        clear()

        fm = FindMovie()
        print("{}\"{}\"{} has been selected.\n".format(
              c.GREEN, torrent_info['quality'], c.RESET))
        
        torrent_download = fm.downloadMovieTorrent(torrent_info['torrent_url'])
        if torrent_download['success'] != True:
            print(torrent_download['return_msg'])
            exProc() 
        elif torrent_download['success'] == True:
            clear()
            
            torrent_path = torrent_download['data']

   
    def downloadMovies(self):
        clear()

        trnt = Torrent()
        dl_dir = os.path.expanduser("~/Downloads")
        src_dir = os.path.join(dl_dir, "torrents")
        
        auth = trnt.loginQbitClient()
        if not 'data' in auth:
            print(auth['return_msg'])
            exProc() 
        elif 'data' in auth:
            auth = auth['data']
            
        for torrent_file in os.listdir(src_dir):
            if torrent_file.endswith('.torrent'):
                path = os.path.join(src_dir, torrent_file)
                trnt.downloadMovie(auth, path)
        
        api_auth = trnt.authorizeAPIAccess()
        if not 'data' in api_auth:
            print(api_auth['return_msg'])
            exProc() 
        elif 'data' in api_auth:
            api_auth = api_auth['data']

        try:
            tmp = 0
            torrent_name = ""
            while tmp < 1:
                status = trnt.statusCheck(api_auth)
                if not 'data' in status:
                    print(status['return_msg'])
                    exProc() 
                elif 'data' in status:
                    status = status['data']
                
                if status == 1:
                    tmp += status
                    successMessage(torrent_name)
                    trnt.cleanUp(api_auth)
                    break

                if status == 2:
                    tmp += status
                    errorMessage(torrent_name)
                    trnt.cleanUp(api_auth)
                    break

                torrent_name = status['torrent_name']
                titleTorrent(torrent_name)
                print("{}[Progress]{}: {}{}{} at {}{}{} on {}{}{} in {}{}{}".format(
                    c.MAGENTA, c.RESET,
                    c.GREEN, status['progress'], c.RESET,
                    c.YELLOW, status['downloaded'],c.RESET,
                    c.RED, status['download_speed'], c.RESET,
                    c.BLUE, status['eta'], c.RESET),
                    end='\r')
                sleep(0.25)
        except KeyboardInterrupt:
            print('\nStopped!')
            trnt.deleteTorrents(api_auth)


@run_once
def titleTorrent(name):
    print("{}Downloading: {}{}{}".format(
            c.RED,
            c.BLUE, name, c.RESET))


def successMessage(name):
    clear()
    print("{}Download Successful: {}{}".format(
        c.RED,
        c.BLUE, name, c.RESET))


def errorMessage(name):
    clear()
    print("{}Download Unsuccessful: {}{}".format(
        c.RED,
        c.BLUE, name, c.RESET))


def exProc():
    nox.killQbittorrent()
    exit(0)


def main(query):
    nox.startQbittorrent()
    md = MoviesDl(query)

    movie = md.selectMovie()
    quality = md.selectQuality(movie)
    torrent = md.getTorrent(quality)

    md.downloadMovies()
    exProc()


if __name__ == '__main__':
    parser = ArgumentParser(description="Download Movies For Free From The Terminal",
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help="Searches for the movie. (e.g. --search 'avengers')")

    args = parser.parse_args()
    if args.search:
        main(''.join(args.search)) 
