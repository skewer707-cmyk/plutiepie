import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Please set DISCORD_TOKEN and GEMINI_API_KEY in your .env file")

# Configure Gemini with current stable model
genai.configure(api_key=GEMINI_API_KEY)

# Try the latest stable models - will try multiple if one fails
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Using Gemini 2.5 Flash model")
except:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Using Gemini 2.0 Flash model")
    except:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        print("✅ Using Gemini 2.0 Flash model (explicit)")

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Updated system prompt for Plutus club
SYSTEM_CONTEXT = """You are PlutiPie, the helpful AI assistant for Plutus - a finance and entrepreneurship club.

About Plutus:
Plutus is a finance club focused on three main areas:
1. Creating and identifying products
2. Product design and development
3. Business pitching and presentation

Your Role:
- Help new members understand the club and its activities
- Answer questions about finance, product development, and business concepts
- Provide advice on projects and campaigns
- Guide members through their entrepreneurial journey
- Explain concepts related to product design, market analysis, and pitching

When answering:
- Be encouraging and supportive to new members
- Provide clear, practical, and actionable advice
- If a question is outside your expertise, acknowledge it and suggest resources
- Keep responses concise but informative
- Use examples relevant to student entrepreneurs when possible

Remember: You're here to help Plutus members grow their skills in finance, product creation, and business communication."""


async def get_gemini_response(question: str) -> str:
    """Get a response from Gemini API with error handling."""
    try:
        full_prompt = f"{SYSTEM_CONTEXT}\n\nQuestion: {question}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't generate a response: {str(e)}"


async def send_long_message(channel, content: str, reference=None):
    """Send a message, splitting it if it exceeds Discord's character limit."""
    max_length = 2000
    
    if len(content) <= max_length:
        if reference:
            await reference.reply(content)
        else:
            await channel.send(content)
        return
    
    # Split into chunks
    chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
    
    for i, chunk in enumerate(chunks):
        if i == 0 and reference:
            await reference.reply(chunk)
        else:
            await channel.send(chunk)


@bot.event
async def on_ready():
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'📊 Bot is active in {len(bot.guilds)} server(s)')
    print('🤖 Ready to answer questions!')


@bot.command(name='ask', help='Ask a question about Plutus, finance, or product design')
async def ask_question(ctx, *, question):
    """
    Usage: !ask What is compound interest?
    """
    async with ctx.typing():
        answer = await get_gemini_response(question)
        await send_long_message(ctx.channel, answer)


@bot.command(name='finance', help='Ask a finance-related question')
async def finance_question(ctx, *, question):
    """
    Usage: !finance What's the difference between stocks and bonds?
    """
    async with ctx.typing():
        finance_prompt = f"As a finance expert helping Plutus club members, answer this: {question}"
        answer = await get_gemini_response(finance_prompt)
        await send_long_message(ctx.channel, answer)


@bot.command(name='design', help='Ask a product design question')
async def design_question(ctx, *, question):
    """
    Usage: !design What are the principles of good UX design?
    """
    async with ctx.typing():
        design_prompt = f"As a product design expert helping Plutus club members, answer this: {question}"
        answer = await get_gemini_response(design_prompt)
        await send_long_message(ctx.channel, answer)


@bot.command(name='pitch', help='Get advice on business pitching')
async def pitch_question(ctx, *, question):
    """
    Usage: !pitch How do I structure a 3-minute pitch?
    """
    async with ctx.typing():
        pitch_prompt = f"As a business pitching expert helping Plutus club members, answer this: {question}"
        answer = await get_gemini_response(pitch_prompt)
        await send_long_message(ctx.channel, answer)


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Only respond to mentions if it's NOT a command
    # This prevents duplicate responses
    if message.content.startswith(bot.command_prefix):
        return
    
    # Check if bot is mentioned
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        question = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if question:
            async with message.channel.typing():
                answer = await get_gemini_response(question)
                await send_long_message(message.channel, answer, reference=message)


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please provide a question after the command!")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        print(f"Error: {error}")
        await ctx.send("❌ An error occurred while processing your command.")


# Run the bot
if __name__ == "__main__":
    print("🚀 Starting bot...")
    bot.run(DISCORD_TOKEN)
