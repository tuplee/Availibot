import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True  # Enable the message content intent

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# List to store RDP connections and their statuses
rdp_connections = {'bluestn1': False, 'bluestn2': False, 'purplestn1': False, 'purplestn2': False}

# Function to update RDP connection status
def update_status(connection_name, status):
    rdp_connections[connection_name] = status

# Command to display available RDP connections
@bot.command()
async def connections(ctx):
    connections_list = '\n'.join([f'{name}: {"In Use" if status else "Available"}' for name, status in rdp_connections.items()])
    await ctx.send(f'Available RDP connections:\n{connections_list}')

# Command to select and mark an RDP connection as in use
@bot.command()
async def use(ctx, connection_name: str):
    if connection_name in rdp_connections:
        if not rdp_connections[connection_name]:
            update_status(connection_name, True)
            await ctx.send(f'{connection_name} is now in use.')
        else:
            await ctx.send(f'{connection_name} is already in use.')
    else:
        await ctx.send(f'Invalid RDP connection name.')

# Command to mark an RDP connection as available
@bot.command()
async def release(ctx, connection_name: str):
    if connection_name in rdp_connections:
        if rdp_connections[connection_name]:
            update_status(connection_name, False)
            await ctx.send(f'{connection_name} is now available.')
        else:
            await ctx.send(f'{connection_name} is already available.')
    else:
        await ctx.send(f'Invalid RDP connection name.')

@bot.command()
async def whoareyou(ctx):
    help = '''
    Use Availibot to check available RDP connections and reserve your workstation!

    !connections -> list all RDP connections
    !use {{bluestn1}} -> reserve the RDP connection
    !release {{bluestn1}} -> release the RDP reservation')
    '''

    await ctx.send(whoareyou)
    
# Run the bot
bot.run('')