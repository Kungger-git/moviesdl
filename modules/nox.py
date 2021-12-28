import os


def startQbittorrent():
    os.system("qbittorrent-nox --daemon") 


def killQbittorrent():
    os.system("pkill qbittorrent-nox") 
