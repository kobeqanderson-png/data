# Run analysis (PowerShell)
# Activate venv if present and run the cleaning example
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    Write-Host "Activating venv..."
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host ".venv not found; ensure you created a virtual environment or run from an env with dependencies installed."
}

Write-Host "Running quick test script..."
python src/quick_test.py

