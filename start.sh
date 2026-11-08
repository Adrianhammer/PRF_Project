#!/usr/bin/env bash
# Sets up the Python environment (first time only) and starts the Flask app.
# Usage: ./start.sh

set -e                      # stop if any command fails
cd "$(dirname "$0")"        # always run from the project folder

# Create the virtual environment the first time
if [ ! -d .venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate it and make sure all packages are installed
source .venv/bin/activate
pip install --quiet --disable-pip-version-check -r requirements.txt

# Start the app
cd app
flask --app app run --debug
