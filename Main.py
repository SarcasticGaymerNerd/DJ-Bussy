##Import Subprocess V3 ##
import subprocess
import sys
import platform
import pkg_resources

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def install_ffmpeg():
    system = platform.system().lower()
    if system == "windows":
        try:
            install("ffmpeg-python")
            print("FFmpeg-python installed successfully via pip.")
            print("Note: This package provides Python bindings for FFmpeg, but you may still need to install FFmpeg separately.")
        except subprocess.CalledProcessError:
            print("Failed to install ffmpeg-python. Please install FFmpeg manually:")
            print("1. Download FFmpeg from https://ffmpeg.org/download.html")
            print("2. Add FFmpeg to your system PATH")
    elif system == "darwin":  # macOS
        print("To install FFmpeg on macOS, use Homebrew:")
        print("1. Install Homebrew from https://brew.sh/ if you haven't already")
        print("2. Run: brew install ffmpeg")
    elif system == "linux":
        print("To install FFmpeg on Linux, use your distribution's package manager.")
        print("For Ubuntu or Debian, run: sudo apt-get install ffmpeg")
        print("For Fedora, run: sudo dnf install ffmpeg")
    else:
        print("Unsupported operating system. Please install FFmpeg manually.")

# ... (rest of the script remains the same)