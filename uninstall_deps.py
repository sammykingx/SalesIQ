import sys
import subprocess

# Calls pip directly inside the active virtualenv to uninstall old dependencies
packages = ["weasyprint", "django-weasyprint"]

for pkg in packages:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", pkg],
        capture_output=True,
        text=True
    )
    print(f"Uninstalling {pkg}:")
    print(result.stdout)
    print(result.stderr)
