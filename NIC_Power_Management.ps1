$adapters = Get-NetAdapter | Get-NetAdapterPowerManagement
foreach ($adapter in $adapters)
{
$adapter.AllowComputerToTurnOffDevice = 'Disabled'
$adapter | Set-NetAdapterPowerManagement
}