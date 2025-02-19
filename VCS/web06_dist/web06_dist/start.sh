#!/bin/bash

cd /app || exit
exec python app.py &
cd /bot || exit
exec python bot.py