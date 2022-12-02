#/!bin/sh
vnstati -d -i enp34s0 -o /tmp/network-log-d.png
vnstati -s -i enp34s0 -o /tmp/network-log-s.png

feh /tmp/network-log-d.png & 
feh /tmp/network-log-s.png &
