# Discord Bot with Gemini AI

A Discord bot that answers questions about finance, product design, and other topics using Google's Gemini API.

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.8+ installed. Check by running:
```bash
python --version
```

### 2. Install Dependencies
Open your terminal/command prompt and navigate to this folder, then run:
```bash
pip install -r requirements.txt
```

### 3. Configure Your Bot
Open `discord_bot.py` and replace these placeholders:
- `your_discord_bot_token_here` - Your Discord bot token
- `your_gemini_api_key_here` - Your Gemini API key

**Better approach (more secure):** Use environment variables instead:
```bash
# On Windows (Command Prompt):
set DISCORD_TOKEN=your_token_here
set GEMINI_API_KEY=your_key_here

# On Mac/Linux:
export DISCORD_TOKEN=your_token_here
export GEMINI_API_KEY=your_key_here
```

Then modify the code to use:
```python
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

### 4. Run Your Bot
```bash
python discord_bot.py
```

## How to Use

### Method 1: Command
Type in any channel:
```
!ask What is the difference between stocks and bonds?
```

### Method 2: Mention
Mention the bot with your question:
```
@YourBot What are the principles of good product design?
```

## Features

✅ Responds to direct commands (`!ask`)
✅ Responds when mentioned
✅ Handles long responses (splits messages over 2000 characters)
✅ Shows "thinking" indicator
✅ Error handling

## Customization Ideas

1. **Limit to specific channels:**
   Add channel ID check in `on_message`:
   ```python
   ALLOWED_CHANNELS = [123456789, 987654321]
   if message.channel.id not in ALLOWED_CHANNELS:
       return
   ```

2. **Add different topics/modes:**
   Create separate commands like `!finance` or `!design`

3. **Add conversation history:**
   Store recent messages to provide context

4. **Rate limiting:**
   Prevent spam by limiting how often users can ask questions

## Troubleshooting

**Bot doesn't respond:**
- Check if "Message Content Intent" is enabled in Discord Developer Portal
- Make sure the bot has permissions to read and send messages
- Check the console for error messages

**API errors:**
- Verify your API keys are correct
- Check if you've hit API rate limits
- Ensure you have internet connection

## Safety Tips

🔒 **Never share your tokens/API keys publicly**
🔒 **Add discord_bot.py to .gitignore if using version control**
🔒 **Use environment variables for production**
