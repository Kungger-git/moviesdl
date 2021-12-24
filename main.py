#!/bin/env python

# imports
from modules import colors, convert_string
from modules.error_handling import ErrorFunctions as ef
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from GrabMovie import MakeSoup, FindMovie


def main(query):
    soup = MakeSoup(query).searchResultsPageSoup()['data']
    fm = FindMovie()

    res = fm.listMovieResults(soup)['data']
    for movie in res:
        print("{} : {}".format(movie, ''.join(res[movie])))

    movie_selected = {}
    try:
        retry_flag = True

        while retry_flag:
            selection = int(input('\n\nSelect the index of the movie to download: '))
            
            if selection in res:
                for title in res[selection]:
                    print('{} has been selected.'.format(title))
                    movie_selected = {'title': title, 'movie_page_url': res[selection][title]}
                    
                    retry_flag = False
    except KeyboardInterrupt:
        print('\nStopped!')

    fmt_mpage_query = movie_selected['movie_page_url'].split('/')[-1]
    mpage = MakeSoup(fmt_mpage_query).movieQualityPageSoup()['data']

    qualities = fm.listVideoQualities(mpage)['data']
    for quality in qualities:
        print("{} : {}".format(quality, ''.join(qualities[quality])))

    quality_selected = {}
    try:
        retry_flag = True

        while retry_flag:
            selection = int(input('\n\nSelect the quality of the movie: '))
            
            if selection in qualities:
                for element in qualities[selection]:
                    print('{} has been selected.'.format(element))
                    quality_selected = {'quality': element, 'torrent_url': qualities[selection][element]}

                    retry_flag = False
    except KeyboardInterrupt:
        print('\nStopped!')

    fm.downloadMovieTorrent(quality_selected['torrent_url'])



if __name__ == '__main__':
    parser = ArgumentParser(description="Download Movies For Free From The Terminal",
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help="Searches for the movie. (e.g. --search 'avengers')")

    parser.add_argument('-d', '--download',
                        action='store_true',
                        help='Downloads torrent files in the torrents directory')

    parser.add_argument('-c', '--checkstatus',
                        action='store_true',
                        help='Checks torrent status on qbittorrent localhost server')

    parser.add_argument('-r', '--remove',
                        action='store_true',
                        help='Deletes torrents')

    args = parser.parse_args()
    if args.search:
        main(' '.join(args.search)) 
