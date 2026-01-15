#!/bin/sh
# Startup script for Railway deployment
PORT=${PORT:-8000}
echo "Starting server on port $PORT"
python -c "
import os
import sys
try:
    port = int('$PORT')
except ValueError:
    print('Invalid PORT value: $PORT. Using default port 8000.')
    port = 8000
os.environ['PORT'] = str(port)
sys.path.insert(0, '.')
from scripts.start_server import main
main()
"