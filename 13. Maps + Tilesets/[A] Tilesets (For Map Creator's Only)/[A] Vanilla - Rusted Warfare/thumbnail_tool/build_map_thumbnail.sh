#!/bin/bash
set -e

#You may need linux or cygwin to use this tool
#run 'apt-get install python-imaging' if you are missing the image module
#and tiled is required for tmxrasterizer

cd "`dirname "$0"`"

yell() { echo "$0: $*" >&2; }
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

forceupdate=true

showSpawns=true


if [ "$#" -ne 1 ]; then
  echo "Usage: $0 MapPath"
  exit 1  
fi

#paths=("assets/maps/skirmish/")
#for path in ${paths[@]}; do
#  echo path:$path
  #for file in $path/*.tmx;  do
files=("$1")
  
  for file in "$files";  do
    echo file:$file
    
    ls -l "$file"
    
    raw=$(echo "$file" | grep -oP '.*(?=\.tmx)')
    
    png_map="${raw}_map.png"
    png_unit="${raw}_unit.png"
    
    linkedMap=$(readlink "$file" || echo "$file")
    
    echo "linkedMap:$linkedMap"
    
    if [ ! -f "$png_map" ] || [ $forceupdate = true ]; then
    
    tmxrasterizer -a --ignore-visibility --hide-layer set -s 0.5 "$linkedMap" "$png_map" && convert "$png_map" -resize 160 "$png_map"
    
    if [[ $path == *"skirmish"* || $showSpawns = true ]]
    then
      echo "draw unit positions"
    
      tmxrasterizer -a --ignore-visibility --hide-layer set \
                                           --hide-layer ground \
                                           --hide-layer ground2 \
                                           --hide-layer items \
                                           -s 0.25 "$linkedMap" "$png_unit" #&& convert "$png_unit" -resize 600 "$png_unit"
      
      ./draw_spawn_points.py "$png_map" "$png_unit"
      rm "$png_unit"
    else
      
      ./remove_alpha.py "$png_map"
    fi

    fi

  done
  
#done
