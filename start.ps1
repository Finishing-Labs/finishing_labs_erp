# Finishing Labs ERP - Quick Start Script
# Run this to start the Flask development server

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Finishing Labs ERP - Starting..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[✓] Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "[!] No virtual environment found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    Write-Host "[✓] Installing dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "Starting Flask development server..." -ForegroundColor Green
Write-Host "Navigate to: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run the Flask app
python app.py
