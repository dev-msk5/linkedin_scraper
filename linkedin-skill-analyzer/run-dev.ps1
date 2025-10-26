param(
    [switch] $Reinstall
)

Write-Host "Running dev helper..."

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}
Write-Host "Installing requirements into the venv (if needed)..."
# Use the venv python.exe so we don't need to activate the venv in this script
$py = Join-Path -Path (Join-Path -Path $PWD -ChildPath '.venv') -ChildPath 'Scripts\python.exe'
if (-not (Test-Path $py)) {
    # for non-Windows shells fallback to bin/python
    $py = Join-Path -Path (Join-Path -Path $PWD -ChildPath '.venv') -ChildPath 'bin/python'
}

if ($Reinstall) {
    & $py -m pip install --upgrade pip
    & $py -m pip install -r requirements.txt
} else {
    # quick check if Flask is importable in the venv; if not, install
    $check = & $py -c "import sys
try:
    import flask
    print('OK')
except Exception:
    print('MISSING')" 2>$null
    if ($check -notlike '*OK*') {
        & $py -m pip install -r requirements.txt
    }
}

Write-Host "Starting backend (serves API + frontend) on http://127.0.0.1:5000"
& $py .\backend\main.py
