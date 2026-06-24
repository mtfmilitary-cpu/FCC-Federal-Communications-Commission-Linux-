#!/bin/bash
# Install local packages if missing
pip install -r requirements.txt

# Launch Flask on the local loopback network
python3 app.py &

# Wait for server initialization, then open default Mint browser
sleep 2
xdg-open http://127.0.0.1:5000
