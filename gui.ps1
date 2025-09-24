# Get the path to the python script
$scriptPath = "C:\NA\V3\gui_runner.py"

# Use the 'python' command to run the script
python $scriptPath

# Optional: Get the output from the python script
$output = python $scriptPath

# Display the output
Write-Host "The output from the python script is: $output"
