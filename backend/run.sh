#!/bin/bash

# Set the path to your desired directory
directoryPath="/home/oohben/aiLingo/backend/tempfront/ailingo-frontend"

# Run npm start with the specified directory path
cd $directoryPath && sudo npm start &

# Activate the virtual environment
venvPath="/home/oohben/aiLingo/backend/aiLingo/.venv/bin/activate"
source $venvPath

# Run the Django server
pythonPath="/home/oohben/aiLingo/backend/aiLingo/.venv/bin/python"
managePyPath="/home/oohben/aiLingo/backend/aiLingo/manage.py"
$pythonPath $managePyPath runserver