"""Copy application definitions to the output directory so generate_application finds them."""
import shutil
from pathlib import Path

src = Path("application_definitions/job_portal")
dst = Path("generated_application/job_portal")

for f in src.glob("webflux_*.json"):
    shutil.copy2(f, dst / f.name)
    print(f"  Copied {f.name}")

print("Done!")
