#!/bin/bash
COUNTER=30
while [ $COUNTER -lt 68 ]; do
python CherrySeek.py $COUNTER
let COUNTER=COUNTER+1 
done