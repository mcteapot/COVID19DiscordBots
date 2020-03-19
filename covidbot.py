import requests
import json

import settings

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
        brief='(!ping, !p)A basic ping command',
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

    # Find Square Root
    @commands.command(
        name='square',
        description='Add a number after square command to get square root',
        brief='(!square, !s) Find square root of a numer',
        aliases=['s']
    )
    async def square(self, ctx, number):
        squared_value = int(number) * int(number)
        await ctx.send(str(number) + " sqared is " + str(squared_value))
        return

    # Get virus info for country
    # Data form https://github.com/nat236919/Covid2019API
    @commands.command(
        name='country',
        description='Get info of virus of country using ISO ALPHA-2',
        brief='(!country ISO2, !c ISO2) Stats per country ISO ALPHA-2',
        aliases=['c']
    )
    async def virus_country_info(self, ctx, isoalpha2code):
        isoalpha2code = isoalpha2code.lower()
        request_url = 'https://covid2019-api.herokuapp.com/country/' + isoalpha2code
        r = requests.get(url=request_url)
        info_null = 'Data Not Found' 
        settings.pings = settings.pings + 1
        if r.status_code == 200:
            # On scuess will get data on country 
            print('Success! ' + str(settings.pings))
            print(r.json())
            data = r.json()
            data_keys = list(data.keys())
            # Last check to see if real country
            if data_keys[0] == 'dt':
                await ctx.send(info_null)
            else:
                info_country =  'Country : ' + data_keys[0] + '\n'
                info_last_update = 'Last Update : ' + data[data_keys[1]]  + '\n'
                info_confirmed = 'Confirmed : ' + str(data[data_keys[0]]['confirmed'])  + '\n'
                info_deaths = 'Deaths : ' + str(data[data_keys[0]]['deaths']) + '\n' 
                info_recovered = 'Recovered : ' + str(data[data_keys[0]]['recovered']) + '\n' 
                await ctx.send(info_country + info_last_update + info_confirmed + info_deaths + info_recovered)
        elif r.status_code == 404:
            print(info_null)
            await ctx.send(info_null)
        return

    # Get virus info for US States
    # Data form https://github.com/axisbits/covid-api
    @commands.command(
        name='state',
        description='Get info of virus of country using  two letter statename',
        brief='(!state ca, !st ca)Stats per US two letter state',
        aliases=['st']
    )
    async def virus_state_info(self, ctx, state):
        state = state.upper()
        state_long = ''
        info_null = 'Data Not Found'
        settings.pings = settings.pings + 1

        try:
            state_long = settings.abbrev_us_state[state]
            print(settings.abbrev_us_state[state])
        except KeyError:
            await ctx.send(info_null)
            print('State Error')
            return

        state_long.replace(" ", "%20")
        request_url = 'https://covid-api.com/api/reports?iso=USA&region_province=' + state_long
        r = requests.get(url=request_url)

        if r.status_code == 200:
            # On scuess will get data on country 
            print('Success! ' + str(settings.pings))
            print(r.json())
            data = r.json()
            # Last check to see if real country
            if len(data['data']) == 0:
                await ctx.send(info_null)
            else:
                info_state =  data['data'][0]['region']['province'] + '\n'
                info_last_update = 'Last Update : ' + data['data'][0]['date']  + '\n'
                info_confirmed = 'Confirmed : ' + str(data['data'][0]['confirmed'])  + '\n'
                info_deaths = 'Deaths : ' + str(data['data'][0]['deaths'])  + '\n' 
                info_recovered = 'Recovered : ' + str(data['data'][0]['recovered']) + '\n' 
                info_new_confirmed = 'New Confirmed ' + str(data['data'][0]['confirmed_diff']) + '\n'
                await ctx.send(info_state + info_last_update + info_confirmed + info_deaths + info_recovered + info_new_confirmed)
        elif r.status_code == 404:
            print(info_null)
            await ctx.send(info_null)
        return

    # Get virus info of total worldwide
    # Data form https://github.com/nat236919/Covid2019API
    @commands.command(
        name='total',
        description='Get info of total effected by virus',
        brief='(!total, !t) Stats total of worldwide',
        aliases=['t']
    )
    async def virus_total_info(self, ctx):
        request_url = 'https://covid2019-api.herokuapp.com/total'
        r = requests.get(url=request_url)
        info_null = 'Data Not Found' 
        settings.pings = settings.pings + 1
        if r.status_code == 200:
            print('Success! ' + str(settings.pings))
            print(r.json())
            data = r.json()
            info_country =  'Total Worldwide' + '\n'
            info_last_update = 'Last Update : ' + data['dt']  + '\n'
            info_confirmed = 'Confirmed : ' + str(data['confirmed'])  + '\n'
            info_deaths = 'Deaths : ' + str(data['deaths']) + '\n' 
            info_recovered = 'Recovered : ' + str(data['recovered']) + '\n'
            await ctx.send(info_country + info_last_update + info_confirmed + info_deaths + info_recovered)
        elif r.status_code == 404:
            print(info_null)
            await ctx.send(info_null)
        return