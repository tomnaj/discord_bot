Here's a `README.md` file for your Discord music bot repository:

```markdown
# Discord Music Bot 🎶

A simple Discord bot that joins a voice channel and plays music from YouTube based on search queries. The bot supports a music queue, looping, pausing, resuming, and stopping playback.

## Features

- Play audio from YouTube based on search queries
- Music queue support to add multiple songs
- Looping option to repeat the current song
- Pause and resume audio playback
- Stop playback and leave the voice channel
- Display the current queue

## Requirements

- Python 3.8+
- `discord.py` library
- `yt-dlp` library
- FFmpeg (for audio playback)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/discord-music-bot.git
   cd discord-music-bot
   ```

2. Install dependencies:

   ```bash
   pip install discord.py yt-dlp
   ```

3. Download and set up FFmpeg:

   - Download FFmpeg from [FFmpeg's website](https://ffmpeg.org/download.html) and add it to your system's PATH.
   - On Windows, you can place the FFmpeg executable in `C:\ffmpeg\bin\`.

## Configuration

1. Open `discord_bot.py` and replace `bot_token` with your own Discord bot token:

   ```python
   bot_token = "YOUR_BOT_TOKEN"  # Replace with your bot token
   ```

2. Save the file.

## Usage

Run the bot with:

```bash
python discord_bot.py
```

### Bot Commands

- `!join` - Bot joins the voice channel of the user who invoked the command.
- `!play <title>` - Adds the specified song to the queue and starts playback if the bot is idle.
- `!queue` - Shows the list of songs currently in the queue.
- `!loop` - Toggles looping of the current song.
- `!pause` - Pauses the current audio playback.
- `!resume` - Resumes paused audio playback.
- `!stop` - Clears the queue, stops the audio, and disconnects the bot from the voice channel.
- `!leave` - Forces the bot to leave the voice channel.

## Example

In Discord, you can control the bot using the commands listed above:

```text
!join           # Bot joins the user's voice channel
!play song name # Adds "song name" to the queue and plays it
!queue          # Displays the current queue
!pause          # Pauses playback
!resume         # Resumes playback
!stop           # Stops and disconnects the bot
```

## Requirements

1. Ensure `discord.py` and `yt-dlp` libraries are installed:

   ```bash
   pip install discord.py yt-dlp
   ```

2. Make sure FFmpeg is installed and in your PATH.

## Notes

- Ensure your bot has permission to join and speak in voice channels.
- FFmpeg must be correctly installed and accessible by the bot for audio playback to work.

## License

This project is licensed under the MIT License.

---

Happy listening! 🎧
```

Replace `"YOUR_BOT_TOKEN"` with your bot’s token, and make sure to update the clone URL in the installation instructions with your GitHub repository URL once you upload it.
