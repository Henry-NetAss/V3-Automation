# Define connection details (User and Password are the same for all servers)
$User = "Na-Tech"# Replace with your actual user name (use format: Domain\Username or local machine name\Username)
$Password = "Supp0rtn@007!" # Replace with the actual password

# Define a list of servers to update credentials for
# IMPORTANT: Replace the example servers below with your actual remote computer names or IP addresses
$Servers = @(
    "Invictus.networkassociates.co.za", 
    "Dibashe.networkassociates.co.za", 
    "himoinsa.networkassociates.co.za",
    "rocketseed.networkassociates.co.za",
    "adlock.networkassociates.co.za",
    "3rdgen.networkassociates.co.za",
    "eclipse.networkassociates.co.za",
    "chemchamp.networkassociates.co.za",
    "topcar.networkassociates.co.za",
    "selective.networkassociates.co.za",
    "dotcom.networkassociates.co.za",
    "kell.networkassociates.co.za",
    "chumile.networkassociates.co.za",
    "outsource.networkassociates.co.za",
    "obl.networkassociates.co.za",
    "exchale.networkassociates.co.za",
    "finedetails.networkassociates.co.za",
    "fibretronics.networkassociates.co.za",
    "glowlighting.networkassociates.co.za",
    "ohsoboho.networkassociates.co.za"

    # Add all new server details here as strings
)

# 1. Loop through the list of servers and store the credentials for each
# The target for RDP connections must be prefixed with 'TERMSRV/'
foreach ($Server in $Servers) {
    Write-Host "--- Attempting to store credentials for: $Server ---"
    
    # Run cmdkey command to store credentials
    cmdkey /generic:TERMSRV/$Server /user:$User /pass:$Password
    
    # Check the result of the cmdkey command (Exit code 0 means success)
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully stored credentials for $Server." -ForegroundColor Green
    } else {
        Write-Host "Failed to store credentials for $Server (cmdkey error code: $LASTEXITCODE). Check server name/IP." -ForegroundColor Red
    }
}

Write-Host "`nCredential update complete for $($Servers.Count) servers."