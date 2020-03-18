# Import libs
import settings
import covidbot

import asyncio
import discord

from discord.ext import commands


def get_prefix(client, message):

    prefixes = ['=', '==', '!']    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['==']   # Only allow '==' as a prefix when in DMs, this is optional

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='Bot tracking COVID-19 \n ISO2 Country Codes : https://www.iban.com/country-codes',  # Set a description for the bot
    owner_id=374886124126208000,            # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)

# case_insensitive=True is used as the commands are case sensitive by default

@bot.event
async def on_ready():                                       # Do this when the bot is logged in
    print("COVID-19 Bot is spreading!")
    print(f'Logged in as {bot.user.name} - {bot.user.id}')  # Print the name and ID of the bot logged in.
    print('------')
    return


bot.add_cog(covidbot.Commands(bot))

# Finally, login the bot
bot.run(settings.token, bot=True, reconnect=True)