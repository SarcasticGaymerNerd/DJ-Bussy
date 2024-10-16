# DJ-Bussy

DJ-Bussy is a Discord bot designed to enhance your music experience in voice channels. With features like playing songs from YouTube and Spotify, managing playlists, and controlling playback, DJ-Bussy makes it easy to enjoy music with friends.

## Features

- **Join/Leave Voice Channels**: Easily connect and disconnect the bot from voice channels.
- **Play Music**: Play songs from YouTube and Spotify using simple commands.
- **Manage Playlists**: Create, add to, and play playlists.
- **Volume Control**: Adjust the volume of the bot to your liking.
- **Pause/Resume/Stop**: Control playback with pause, resume, and stop commands.
- **Help Command**: Get a list of available commands and their descriptions.

## Commands

Here are some of the commands you can use with DJ-Bussy:

- `-join`: Join the voice channel you're currently in.
- `-leave`: Leave the current voice channel.
- `-play <song name or URL>`: Play a song from YouTube.
- `-volume <0-100>`: Set the volume of the bot.
- `-pause`: Pause the currently playing song.
- `-resume`: Resume a paused song.
- `-stop`: Stop the current song and clear the queue.
- `-create_playlist <name>`: Create a new playlist with the given name.
- `-add_to_playlist <playlist_name> <song name or URL>`: Add a song to the specified playlist.
- `-play_playlist <name>`: Play all songs in the specified playlist.
- `-play_spotify <Spotify URL>`: Play a Spotify track or playlist.
- `-my_spotify_playlists`: List all your Spotify playlists.
- `-help`: Display this help message.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SarcasticGaymerNerd/DJ-Bussy.git
   ```
2. Navigate to the project directory:
   ```bash
   cd DJ-Bussy
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Make sure to set up your environment variables for the bot prefix and Spotify credentials. You can do this by creating a `.env` file in the project root with the following content:

## Usage

Run the bot using the following command:

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Discord.py](https://discordpy.readthedocs.io/en/stable/) for the Discord API wrapper.
- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) for Spotify API integration.
- [youtube-dl](https://github.com/ytdl-org/youtube-dl) for downloading audio from YouTube.
