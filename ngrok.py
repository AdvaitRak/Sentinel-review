import subprocess


def main():
    subprocess.run([
        "ngrok", "http",
        "--domain=cartographic-felisa-compliable.ngrok-free.dev",
        "8000"
    ])


if __name__ == "__main__":
    main()