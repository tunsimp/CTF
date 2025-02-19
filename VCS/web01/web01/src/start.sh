#!/bin/sh

echo "$FLAG1" > /flag1.txt
unset FLAG1

echo "$FLAG2" > /flag2.txt
unset FLAG2

echo "$FLAG3"

python3 /app/app.py