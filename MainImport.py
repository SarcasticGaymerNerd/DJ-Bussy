import subprocess
import sys
import platform

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def install_ffmpeg():
    system = platform.system().lower()
    if system == "windows":
        try:
            subprocess.check_call(["pip", "install", "ffmpeg-python"])
            print("FFmpeg installed successfully via pip.")
        except subprocess.CalledProcessError:
            print("Failed to install FFmpeg via pip. Please install it manually:")
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

print("Updating pip...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

print("Installing/Updating required packages...")

required_packages = [
    "discord.py[voice]",  # This installs discord.py with voice support
    "PyNaCl",             # Required for voice support
    "youtube_dl",         # For YouTube audio downloading
    "spotipy"             # For Spotify integration (if you're using it)
]

for package in required_packages:
    print(f"Installing/Updating {package}...")
    install(package)

print("All required packages have been installed/updated successfully!")

# Verify discord.py version
import discord
print(f"Installed discord.py version: {discord.__version__}")

print("\nAttempting to install FFmpeg...")
install_ffmpeg()

print("\nSetup complete!")
print("If FFmpeg installation was unsuccessful, please follow the provided instructions to install it manually.")
print("After ensuring FFmpeg is installed, your Discord bot should be ready for voice support.")