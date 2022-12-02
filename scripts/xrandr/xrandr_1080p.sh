#!/bin/bash

xrandr --auto
#xrandr --output HDMI-0 --right-of DP-0
#~/Scripts/wallpaper.sh
xrandr --output DP-0 --mode 1280x960 --rate 144

#polybar
sleep 1; /home/nix/.config/polybar/forest/launch.sh
