# Simple script to run the Flask app
Write-Host "Starting FlowChat..."
$prevLocation = Get-Location
Set-Location -Path "C:\Users\HP\Desktop\My Pride"
try {
    python app.py
} catch {
    Write-Host "Error: $_"
}
Set-Location -Path $prevLocation
