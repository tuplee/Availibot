import discord
from discord.ext import commands, tasks
import datetime

# State your intentions (enable message content intent)
intents = discord.Intents.all()
intents.messages = True

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# List to store RDP connections and their reservations
rdp_connections = {'bluestn1': None, 'bluestn2': None, 'purplestn1': None, 'purplestn2': None}

# Function to reserve an RDP connection
def reserve_connection(connection_name, user_id):
    rdp_connections[connection_name] = {'user_id': user_id, 'timestamp': datetime.datetime.now()}

# Function to release an RDP connection
def release_connection(connection_name):
    rdp_connections[connection_name] = None

# Command to select and mark an RDP connection as in use
@bot.command()
async def use(ctx, connection_name: str):
    if connection_name in rdp_connections:
        if rdp_connections[connection_name] is None:
            reserve_connection(connection_name, ctx.author.id)
            await ctx.send(f'{connection_name} is now in use by {ctx.author.display_name}.')
        else:
            await ctx.send(f'{connection_name} is already in use by {bot.get_user(rdp_connections[connection_name]["user_id"]).display_name}.')
    else:
        await ctx.send(f'Invalid RDP connection name.')

# Command to mark an RDP connection as available
@bot.command()
async def release(ctx, connection_name: str):
    if connection_name in rdp_connections:
        if rdp_connections[connection_name] is not None:
            release_connection(connection_name)
            await ctx.send(f'{connection_name} is now available.')
        else:
            await ctx.send(f'{connection_name} is already available.')
    else:
        await ctx.send(f'Invalid RDP connection name.')

# Command to extend an RDP reservation
@bot.command()
async def extend(ctx):
    for connection_name, reservation_info in rdp_connections.items():
        if reservation_info is not None and reservation_info['user_id'] == ctx.author.id:
            reservation_info['timestamp'] = datetime.datetime.now()
            await ctx.send(f'Your reservation for {connection_name} has been extended.')
            return
    await ctx.send('You do not have an active reservation to extend.')

# Command to explain how the bot works
@bot.command()
async def whoareyou(ctx):
    help = '''
    Use Availibot to check available RDP connections and reserve your workstation.
    This is a manual process right now, but there is a 3 hour auto-timeout for check-ins.
    V2 is in development for live RDP statuses-> https://github.com/tuplee/AvailibotV2

    Workstations To Choose From:
    {{bluestn1, bluestn2, purplestn1, purplestn2}}

    Commands:
    !connections                  -> list all RDP connections
    !use {{workstation_name}}     -> check into the workstation
    !release {{workstation_name}} -> checkout of the workstation)
    !extend                       -> reset the 3 hour timeout
    '''

    await ctx.send(help)

# Automatic release task
@tasks.loop(minutes=5)
async def automatic_release():
    now = datetime.datetime.now()
    for connection_name, reservation_info in rdp_connections.items():
        if reservation_info is not None:
            reservation_time = reservation_info['timestamp']
            if (now - reservation_time).total_seconds() >= 180 * 60:  # 3 hour timeout
                release_connection(connection_name)
                channel = await bot.fetch_channel("CHANNEL_ID_GOES_HERE")
                await channel.send(f'{connection_name} has been automatically released due to inactivity.')

# Start automatic release task
automatic_release.start()
    
# Run the bot
bot.run('BOT_TOKEN_GOES_HERE')