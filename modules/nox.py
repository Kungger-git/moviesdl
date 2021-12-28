import os


nox_file = 'nox.sh'

def startQbittorrent():
    os.system("./modules/{} start".format(nox_file)) 


def killQbittorrent():
    os.system("./modules/{} kill".format(nox_file)) 
