echo y|winget uninstall --id Microsoft.Onedrive 
start-sleep -seconds 10
echo y|winget install --id Microsoft.Onedrive --source winget
exit
