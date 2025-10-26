"""Portable dev runner for linkedin-skill-analyzer.

This script creates a venv in `.venv` (if missing), installs requirements,
and launches the backend which also serves the frontend static files.

Usage:
  python run.py           # creates venv (if needed), installs deps, and runs backend in venv
  python run.py --no-venv # runs backend in the current Python environment (no venv actions)
  python run.py --reinstall # force reinstall requirements in the venv

The script avoids shell-specific helpers and Windows execution policy issues
because it is a pure-Python entrypoint — run it with the system Python.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys


ROOT = os.path.dirname(__file__)
VENV_DIR = os.path.join(ROOT, ".venv")
REQUIREMENTS = os.path.join(ROOT, "requirements.txt")


def venv_python(venv_dir: str) -> str:
    if sys.platform.startswith("win"):
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")


def ensure_venv(venv_dir: str) -> None:
    if os.path.isdir(venv_dir):
        print(f"Using existing venv at {venv_dir}")
        return
    print(f"Creating virtual environment at {venv_dir}...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])


def install_requirements(python_exe: str) -> None:
    print("Upgrading pip and installing requirements...")
    subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"]) 
    subprocess.check_call([python_exe, "-m", "pip", "install", "-r", REQUIREMENTS])


def run_in_venv(venv_dir: str) -> None:
    python_exe = venv_python(venv_dir)
    if not os.path.exists(python_exe):
        raise RuntimeError(f"Python executable not found in venv: {python_exe}")
    # Replace current process with the venv-backed Python running the backend module
    os.execv(python_exe, [python_exe, "-u", "-m", "backend.main"])


def run_no_venv() -> None:
    # Run the backend in the current interpreter (useful for CI or existing envs)
    print("Running backend in current Python environment...")
    # Import and run app directly — this blocks until stopped.
    import backend.main as backend_main  # type: ignore

    # The backend's main module starts the Flask app when executed as __main__.
    # We call app.run here to avoid import-time side effects.
    backend_main.app.run(host="0.0.0.0", port=5000, debug=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-venv", action="store_true", help="Run without creating/using a virtualenv")
    parser.add_argument("--reinstall", action="store_true", help="Reinstall requirements into the venv")
    args = parser.parse_args(argv)

    if args.no_venv:
        return run_no_venv()

    # Ensure venv exists and install requirements
    ensure_venv(VENV_DIR)
    py = venv_python(VENV_DIR)
    if args.reinstall:
        install_requirements(py)
    else:
        # Try importing Flask to see if requirements are available; if not, install
        try:
            # run a tiny subprocess that imports Flask using the venv python
            subprocess.check_call([py, "-c", "import flask"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Requirements appear to be installed in the venv.")
        except subprocess.CalledProcessError:
            install_requirements(py)

    # Finally run the backend from the venv
    run_in_venv(VENV_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
