# Set the path to your desired directory
$directoryPath = "D:\aiLingo\backend\tempfront\ailingo-frontend"

# Run npm start with the specified directory path
Start-Job -ScriptBlock {
    npm start --prefix $using:directoryPath
}

# Activate the virtual environment
$venvPath = "D:\aiLingo\backend\.venv\Scripts\Activate.ps1"
& $venvPath

# Run the Django server
$pythonPath = "D:\aiLingo\backend\.venv\Scripts\python.exe"
$managePyPath = "D:\aiLingo\backend\aiLingo\manage.py"
& $pythonPath $managePyPath runserver