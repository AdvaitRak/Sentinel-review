import subprocess
import sys


def main():
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--reload",
        "--port", "8000",
    ])


if __name__ == "__main__":
    main()