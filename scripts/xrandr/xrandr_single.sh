#!/bin/bash

xrandr --output HDMI-0 --off

/home/nix/.config/polybar/forest/launch.sh

#IPAD:
#xrandr --output DP-0 --mode 1280x960 --rate 144

#1080p:
xrandr --output DP-0 --mode 1920x1080 --rate 144

/home/nix/Scripts/wallpaper.sh
