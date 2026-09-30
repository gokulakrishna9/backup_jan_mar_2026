"""DEPRECATED — Moved to app_validator/

This file is kept as a thin redirect. Use the standalone tool instead:

    py app_validator/validate.py frontend --url http://localhost:5173
    py app_validator/validate.py backend  --url http://localhost:8081
    py app_validator/validate.py all      --backend-url http://localhost:8081 --frontend-url http://localhost:5173

For backwards compatibility, running this script directly still works
by delegating to the new location.
"""

import os
import subprocess
import sys

def main():
    # Forward all args to the new validate.py with "frontend" subcommand
    validator_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "app_validator", "validate.py"
    )
    cmd = [sys.executable, validator_path, "frontend"] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
