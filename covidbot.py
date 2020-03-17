from discord.ext import commands
from datetime import datetime as d

# New - The Cog class must extend the commands.Cog class
class Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # Define a new command
    @commands.command(
        name='ping',
        description='The ping command',
        brief='A basic ping command',
        aliases=['p']
    )
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
        # Gets the timestamp when the command was used

        msg = await ctx.send(content='Pinging')
        # Sends a message to the user in the channel the message with the command was received.
        # Notifies the user that pinging has started

        await msg.edit(content=f'Pong!\nOne message round-trip took {( d.timestamp( d.now() ) - start ) * 1000 }ms.')
        # Ping completed and round-trip duration show in ms
        # Since it takes a while to send the messages
        # it will calculate how much time it takes to edit an message.
        # It depends usually on your internet connection speed
        return

    @commands.command(
        name='square',
        description='Add a number after square command to get square root',
        brief='Find square root of a numer',
        aliases=['s']
    )
    async def square(self, ctx, number):
        squared_value = int(number) * int(number)
        await ctx.send(str(number) + " sqared is " + str(squared_value))
        return