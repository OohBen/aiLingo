#!/bin/bash

# Start the Django server
cd backend/aiLingo           # Navigate to the Django project directory
source venv/bin/activate     # Activate the virtual environment
echo "Starting Django server..."
python manage.py runserver & # Start the Django server in the background

# Start the Next.js server
cd ../../frontend/ailingo    # Navigate to the Next.js project directory
echo "Starting Next.js server..."
npm run dev                  # Start the Next.js development server

# Wait for all background jobs to complete
wait
