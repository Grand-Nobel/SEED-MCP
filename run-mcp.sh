#!/bin/bash

echo "🔧 [SEED-MCP] Building Docker container..."
docker build -t seed-mcp .

echo "🚀 [SEED-MCP] Running container on port 8080..."
docker run -d -p 8080:80 --name seed-mcp-container seed-mcp

echo "✅ [SEED-MCP] Running at http://localhost:8080"

#!/bin/bash

echo "🛠️  [SEED-MCP] Building Docker container..."
docker build -t seed-mcp .

echo "🧼  [SEED-MCP] Cleaning any existing container..."
docker rm -f seed-mcp-container &>/dev/null

echo "🚀  [SEED-MCP] Running on port 8080..."
docker run -d -p 8080:80 --name seed-mcp-container seed-mcp

echo "✅  [SEED-MCP] Ready at http://localhost:8080"
