import subprocess
import sys
import os


def main():
    login_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "login.py"
    )

    subprocess.run([sys.executable, login_file])


if __name__ == "__main__":
    main()