#!/bin/bash
oldtitle=""
oldrunning=""

while :
do
sleep 0.5
title=$(xtitle)

if [ "$title" == "$oldtitle" ]; then
  echo "same title, continuing"
  continue
fi
oldtitle=$title

running="0"
#for value in "Minecraft" "Java" "Lunar Client"
for value in "Lunar Client" "Minecraft 1.8.9"
do

  if [[ "$title" == *$value* ]]; then
    if ! [ -z "$(ps -A | grep java)" ]; then
      running="1"
    fi
  fi
done

if [ "$running" == "$oldrunning" ]; then
  echo "same running, continuing"
  continue
fi
oldrunning=$running

echo "changing smth"
if [ "$running" == "1" ]; then
  xmodmap ~/.xmodmap-mc
else
  setxkbmap -layout fr
fi
done
