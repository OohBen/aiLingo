#!/bin/bash
# Navigate to the script directory
cd "$(dirname "$0")"

# Django setup
cd backend/aiLingo
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
echo "Starting Django server..."
python manage.py runserver & # Start the Django server in the background

# Next.js setup
cd ../../frontend/aiLingo
echo "Starting Next.js server..."
if ! command -v npm &> /dev/null
then
    echo "npm could not be found, please install it."
    exit
fi
npm install
npm run dev & # Start the Next.js development server in the background

# Wait for all background jobs to complete
wait
