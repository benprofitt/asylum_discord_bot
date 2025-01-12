import os
import discord
from discord.ext import commands
import requests
import aiohttp
import json

from config import discord_bot_token
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = discord_bot_token
intents = discord.Intents.default()
intents.message_content = True  # Make sure message_content is enabled if you're using text commands

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command(name="coverletter")
async def coverletter(ctx):
    """
    !coverletter some file here
    This command will capture "some text here" as the 'message' argument.
    """
    print("Command received: coverletter")

    message = "Error in receiving message. "
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    # Decode the bytes to a string (assuming UTF-8)
                    text_content = data.decode("utf-8")
                    message = text_content

                    # Send (some or all) content back to the channel
                    # NOTE: If the file is large, sending everything might exceed Discord’s character limit
                    await ctx.send(f"Received File Contents")
                    await ctx.send(f"Processing...")
                else:
                    await ctx.send(f"Failed to download file. Status: {resp.status}")
  

    try:
        url = "https://asylum-aged-mountain-7254.fly.dev/coverletter"
        data = {"body": message}

        response = requests.post(url, json=data)
        data = response.json()

        evaluation = data.get("evaluation", {
            "irrelevant_info": False,
            "missing_info": False,
            "reasoning": "Evaluation failed",
            "rule_violation": False,
            "said_too_much": False
        })

        await ctx.send(
            (
            f"**Evaluation:**\n"
            f"{evaluation.get('reasoning')}\n"
            f"**Too much information:** {evaluation.get('said_too_much')}\n"
            f"**Missing information:** {evaluation.get('missing_info')}\n"
            f"**Rule violation:** {evaluation.get('rule_violation')}\n"
            f"**Irrelevant information:** {evaluation.get('irrelevant_info')}\n"
            )
            )
    except Exception as e:
        await ctx.send(f"Could not retrieve evaluation. Error: {e}")


@bot.command(name="gradequestions")
async def grade_questions(ctx, *, message: str):
    """
    !gradequestions some text here
    This command will capture "some text here" as the 'message' argument.
    """
    print("Command received: grade qs")
    url = "https://asylum-aged-mountain-7254.fly.dev/gradequestions"

    try:
        data = json.loads(message)

        response = requests.post(url, json=data)
        data = response.json()

        for answer in data:
            evaluation = answer.get("evaluation", {
                "irrelevant_info": False,
                "missing_info": False,
                "reasoning": "Evaluation failed",
                "rule_violation": False,
                "said_too_much": False
            })
            await ctx.send(
                (
                f"**Evaluation:**\n"
                f"{evaluation.get('reasoning')}\n"
                f"**Too much information:** {evaluation.get('said_too_much')}\n"
                f"**Missing information:** {evaluation.get('missing_info')}\n"
                f"**Rule violation:** {evaluation.get('rule_violation')}\n"
                f"**Irrelevant information:** {evaluation.get('irrelevant_info')}\n"
                )
                )
    except Exception as e:
        await ctx.send(f"Could not retrieve evaluation. Error: {e}")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)