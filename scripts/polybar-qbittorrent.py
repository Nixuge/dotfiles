#!/usr/bin/env python3
import qbittorrentapi
from functools import reduce
import argparse
import os

ICON_PLAY = ""
ICON_PAUSE = ""
ICON = ""
PATH=os.path.realpath(__file__)

# Config
username=''
password=''
host='localhost'
port='8080'


qbc: qbittorrentapi.Client
try:
    qbc = qbittorrentapi.Client(host=host,username=username,password=password, port=port, SIMPLE_RESPONSES=True)
    qbc.auth_log_in()
except Exception as e:
    print("")
    exit()

active = qbc.torrents.info.active()
parser = argparse.ArgumentParser()
parser.add_argument('--playpause', action="store_true")
parser.add_argument('--signonly', action="store_true")
args= parser.parse_args()
if args.playpause:
    if len(active):
        qbc.torrents_pause('all')
    else:
        qbc.torrents_resume('all')
    exit()

if args.signonly:
    ICON = ICON_PAUSE
    if len(active):
        ICON = ICON_PLAY
    print(f'{ICON}')
    exit()


if True:
    active = qbc.torrents.info.active()
    ICON = ICON_PAUSE
    if len(active):
        ICON = ICON_PLAY

    dlspeed = qbc.transfer.info['dl_info_speed']/1024
    dlunit = "KB/s"
    if dlspeed > 1024:
        dlunit = "MB/s"
        dlspeed = dlspeed/1024
    upspeed = qbc.transfer.info['up_info_speed']/1024
    upunit = "KB/s"
    if upspeed > 1024:
        upunit = "MB/s"
        upspeed = upspeed/1024
    cumulative_percentage = 0
    if len(active) > 0:
        cumulative_percentage = reduce(lambda a,b:a+b['progress'], active,0) / len(active)        
        
    print(f'{upspeed:.2f}{upunit} {ICON}%{{A}} {dlspeed:.2f}{dlunit}')
    #print(f'%{{A1: {PATH} --playpause:}}{ICON}%{{A}} {len(active)}  {cumulative_percentage:.2%} |  {upspeed:.2f}{upunit}  {dlspeed:.2f}{dlunit}')
