#!/bin/python3

import requests
import time
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PI_BASE_URL = "http://192.168.1.28"

PORTS = {
    "Sonarr": "8989",
    "Radarr": "7878",
    "qBittorrent": "8080",
    "Jellyfin": "8096",
    "Jackett": "9117",
    "FlareSolverr": "8191"
}

done = []

while len(done) < len(PORTS):
    os.system("clear")
    fullString = ""
    for port in PORTS:
        if port in done: 
            fullString += f"{port}: {bcolors.OKGREEN}Success !{bcolors.ENDC}\n"
            continue

        try:
            r = requests.get(f"{PI_BASE_URL}:{PORTS[port]}")
            if r.status_code == 200:
                fullString += f"{port}: {bcolors.OKGREEN}Success !{bcolors.ENDC}\n"
                done.append(port)
                continue
        except: pass
        fullString += f"{port}: {bcolors.FAIL}Error !{bcolors.ENDC}\n"

    print(fullString)
    time.sleep(1)

            

