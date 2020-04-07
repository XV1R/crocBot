#!/bin/bash

#read HTML
ARTIST=$1
SONG=$2
HTML="https://www.azlyrics.com/lyrics/${ARTIST}/${SONG}.html"
cd ~/Documents/personalprojects/discordbots
wget --output-document=index.html ${HTML} -U firefox
python3 lyricParser.py 

