#!/bin/bash

if ! command -v ngrok &> /dev/null
then
    echo "🌐 Installing ngrok CLI..."
    npm install -g ngrok
fi

echo "🚀 [SEED-MCP] Starting ngrok tunnel using custom domain..."
ngrok http --domain=seed-mcp.ngrok.app 8080
