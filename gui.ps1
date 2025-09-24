# --- Configuration ---
# The name of your Python script. It should be in the same folder as this PowerShell script.
$pythonScriptName = "Gui_runner4.py"

# The URL for the official Python installer.
# This example uses Python 3.12.4. You can change this to any other version.
$pythonDownloadUrl = "https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
$installerFileName = "python_installer.exe"
$installerPath = Join-Path $env:TEMP $installerFileName

# --- Main Logic ---

# Step 1: Check if Python is installed and available in the PATH
Write-Host "Checking for Python installation..." -ForegroundColor Yellow
$pythonExe = Get-Command python -ErrorAction SilentlyContinue

if ($pythonExe) {
    Write-Host "Python is already installed at: $($pythonExe.Source)" -ForegroundColor Green
} else {
    Write-Host "Python not found. Starting download and installation process..." -ForegroundColor Cyan

    # Step 2: Download the Python installer
    Write-Host "Downloading Python from $pythonDownloadUrl..."
    try {
        Invoke-WebRequest -Uri $pythonDownloadUrl -OutFile $installerPath
        Write-Host "Download complete." -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to download the Python installer. Check the URL or your connection." -ForegroundColor Red
        # Pause the script so the user can see the error before the window closes.
        Read-Host "Press Enter to exit"
        exit 1
    }

    # Step 3: Run the installer silently
    Write-Host "Installing Python silently... This may take a few minutes."
    # Installer arguments:
    # /quiet               - No UI is displayed.
    # InstallAllUsers=1    - Install for all users (requires admin rights).
    # PrependPath=1        - Adds Python to the system PATH environment variable.
    $installArgs = "/quiet InstallAllUsers=1 PrependPath=1"
    
    try {
        # Start the process and wait for it to complete.
        Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -NoNewWindow
        Write-Host "Python installation successful!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Python installation failed. You may need to run this script as an Administrator." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    # IMPORTANT: The PATH in the current PowerShell session will not be updated automatically.
    # We will tell the user to restart the terminal for the 'python' command to work everywhere.
    Write-Host "Installation is complete. For the 'python' command to be available system-wide, please close and reopen this terminal." -ForegroundColor Yellow
    
    # For this script to continue, we'll use the default install location directly.
    $pythonExe = "C:\Program Files\Python312\python.exe"
    if (-not (Test-Path $pythonExe)) {
        Write-Host "ERROR: Could not find python.exe at its default install location." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Step 4: Run the Python script
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath $pythonScriptName

if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: The Python script '$pythonScriptName' was not found in this directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "--- Running Python script: $pythonScriptName ---" -ForegroundColor Yellow
try {
    # Use the '&' call operator to execute the command
    & $pythonExe $scriptPath
    Write-Host "-------------------------------------------" -ForegroundColor Yellow
    Write-Host "Python script finished." -ForegroundColor Green
} catch {
    Write-Host "ERROR: An error occurred while running the Python script." -ForegroundColor Red
    Write-Host $_.Exception.Message
}

# Optional: Clean up the downloaded installer file
if (Test-Path $installerPath) {
    Remove-Item $installerPath -Force
}

# Pause at the end
Read-Host "Process complete. Press Enter to exit"