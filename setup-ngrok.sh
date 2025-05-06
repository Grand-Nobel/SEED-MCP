#!/bin/bash

if ! command -v ngrok &> /dev/null
then
    echo "🌐 Installing ngrok CLI..."
    npm install -g ngrok
fi

echo "🚀 Starting ngrok tunnel on port 8080..."
ngrok http 8080
