#!/bin/bash
rm individual/*
cat *.har | grep avatar > messages.txt
split -l 1 messages.txt
mv x* individual
ls individual | xargs -I{} sh -c "cat individual/{} | cut -c 22- | rev | cut -c 2- | rev > individual/1{}.1"
rm individual/x*
python3 remove_smaller.py
ls individual | xargs -I{} sh sed.sh individual/{}
python3 organize.py > messages.txt
rm individual/*
