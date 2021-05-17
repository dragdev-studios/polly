#!/usr/bin/sh

# Clone from git
echo "Downloading latest release of polly..."
git clone git@github.com:dragdev-studios/polly.git polly && git checkout production && git pull && cd polly

# Create virtual environment
echo "Creating virtual environment..."
/usr/bin/python3 -m venv venv
source venv/bin/activate

# Install deps
echo "Installing dependencies..."
pip install -Ur requirements.txt pip

# Minimal config
echo "Creating config.json..."
echo '{"token": "INSERT_TOKEN_HERE", "cogs": "AUTO"}' > config.json

echo "Installed polly."
echo "Please edit config.json to your heart's content."
echo "Once you've set that up, just run main.py to get the bot running!" 
