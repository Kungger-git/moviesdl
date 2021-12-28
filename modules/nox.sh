startQbittorrent() {
    qbittorrent-nox --daemon
}

killQbittorrent() {
    if pgrep qbittorrent-nox; then
        pkill qbittorrent-nox
    fi
}

if [[ "$1" == "start" ]]; then
    startQbittorrent

elif [[ "$1" == "kill" ]]; then
    killQbittorrent
fi
