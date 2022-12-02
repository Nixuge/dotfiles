
search_dir=~/Static/Wallpapers
image=$(find $search_dir -maxdepth 1 -type f | shuf -n 1)

echo $image
feh --bg-scale $image
