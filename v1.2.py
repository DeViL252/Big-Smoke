import requests 
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import Intents
import json


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

prefix = "bg-"

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=Intents.all())
bot.remove_command('help')

# ----- COMMANDS -----



# --- ping ---
@bot.command()
async def ping(ctx):
    return await ctx.send(f'Ping is {round(bot.latency * 1000)}ms')



# --- help ---
@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Help Command", colour=ctx.bot.user.colour)
  embed = embed.add_field(name=f"{prefix}ping", value="to check bot ping", inline=False)
  embed = embed.add_field(name=f"{prefix}invite", value="to get bot invite link", inline=False)
  embed = embed.add_field(name=f"{prefix}servers", value="to search online or offline servers", inline=False)
  embed = embed.add_field(name=f"{prefix}players", value="to check online players of a server", inline=False)
  embed = embed.add_field(name=f"{prefix}imginfo", value="to get info banner of a server", inline=False)
  embed = embed.add_field(name=f"{prefix}info", value="to get info of a server", inline=False)
  return await ctx.send(embed=embed)



# --- !invite ---
@bot.command()
async def invite(ctx):
  return await ctx.send("Click:- https://discord.com/api/oauth2/authorize?client_id=910434347365064714&permissions=1511828880448&scope=bot")



# --- !servers ---
@bot.command()
async def servers(ctx, *,server:str):

  msg = await ctx.send("`Searching...`")

  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0

  embed = discord.Embed(title="Online Server", description=f"Server found with name {server}, Bot can only send first 25 matching servers.", colour=ctx.bot.user.colour)

  for a in soup.find_all('a', href=True):
    
    if str(server.lower()) in str((a.get_text()).lower()):
      total_server = total_server + 1
      server_ip_info = a['href']
      # server_raw = server_ip_info[1:-1].split(':')
      server_ip = server_ip_info[1:-1]
      embed = embed.add_field(name=f"{str(a.get_text())}", value=f"IP = {server_ip}", inline=False)
     
  if total_server <= 0:
    await msg.delete()
    return await ctx.send(f"There is no server online with name `{server}`")

  
  else:
    await msg.delete()
    embed = embed.add_field(name="Total Servers", value=total_server, inline=True)
    embed = embed.set_footer(text="Big Smoke", icon_url=ctx.bot.user.avatar_url)
    return await ctx.send(embed=embed)



# --- !players ---
@bot.command()
async def players(ctx, *,server:str):
  
  msg = await ctx.send("`Searching...`")

  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    await msg.delete()
    return await ctx.send(f"There are two or too many servers online with a name `{server}`, Use `!servers` to check right server name.")

  elif total_online_servers(server) == False:
    await msg.delete()
    return await ctx.send(f"There are no server found with name `{server}`")

  player_list = ""
    
  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text()).lower()):

      su = requests.get(f"https://www.game-state.com{a['href']}", headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')
      playerslist = soupurl.find(id='playerslist')
      tp = 0

      for player in playerslist.find_all('td'):
        
        if tp%2 == 0:
          tp = tp + 1
          player_list = player_list + f"{str(player.get_text())}"

        elif tp%2 == 1:
          tp = tp + 1
          player_list = player_list + f"  -  {str(player.get_text())}\n"

      if tp <= 2:
        await msg.delete()
        return await ctx.send("There are no player online or unable to retrive player data due to server having 100+ members.")


      await msg.delete()
      embed = discord.Embed(title=f"{str(a.get_text())}", description=player_list, colour=ctx.bot.user.colour)
      embed.add_field(name="Total Players", value=str((soupurl.find(id='players')).get_text()), inline=True)
      embed = embed.set_footer(text="Big Smoke", icon_url=ctx.bot.user.avatar_url)
      
      return await ctx.send(embed=embed)

  else:
    await msg.delete()
    return await ctx.send(f"Server not found with name {server}.")
  


# --- !imginfo ---
@bot.command()
async def imginfo(ctx, *,server:str):

  msg = await ctx.send("`Searching...`")

  url = f'https://www.game-state.com/index.php?search={server}&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    await msg.delete()
    return await ctx.send(f"There are two or too many servers online with name `{server}`")

  elif total_online_servers(server) == False:
    await msg.delete()
    return await ctx.send(f"There are no server found with name `{server}`")

  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text()).lower()):
      await msg.delete()
      return await ctx.send(f"http://www.game-state.com/{a['href']}/560x95_FFFFFF_FF9900_000000_000000.png")



# --- info ---
@bot.command()
async def info(ctx, *, server:str):

  msg =  await ctx.send(f"`Searching...`")

  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    await msg.delete()
    return await ctx.send(f"There are two or too many servers online with name `{server}`")
  
  elif total_online_servers(server) == False:
    await msg.delete()
    return await ctx.send(f"There are no server found with name `{server}`")

  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text()).lower()):

      su = requests.get(f"https://www.game-state.com{a['href']}", headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      embed = discord.Embed(title="Server Info", colour=ctx.bot.user.colour)

      embed = embed.add_field(name="Server Name", value=f"{str((soupurl.find(id='hostname')).get_text())}", inline=True)
      embed = embed.add_field(name="State", value=f"{str((soupurl.find(id='state')).get_text())}", inline=True)
      embed = embed.add_field(name="Total Players", value=f"{str((soupurl.find(id='players')).get_text())}", inline=True)
      embed = embed.add_field(name="IP", value=f"{str(a['href'][1:-1])}", inline=True)
      embed = embed.add_field(name="Game Mode", value=f"{str((soupurl.find(id='gamemode')).get_text())}", inline=True)
      embed = embed.add_field(name="Map Name", value=f"{str((soupurl.find(id='mapname')).get_text())}", inline=True)

      servervar = soupurl.find(id='var')
      varcout = 0
      var1 = ""
      var2 = ""
      for link in servervar.find_all('td'):
        varcout = varcout + 1

        if varcout%2 == 1:
          var1 = str(link.get_text())

        elif varcout%2 == 0:
          var2 = str(link.get_text())
          embed = embed.add_field(name=var1, value=var2, inline=True)
        # if not found td or loop won't add new fields :)

      await msg.delete()
      embed = embed.set_footer(text="Big Smoke", icon_url=ctx.bot.user.avatar_url)
      return await ctx.send(embed=embed)
    




# ----- EVENTS -----

@bot.event
async def on_ready():

  # --- Bot Rich Presence ---
  game = discord.Game("Created by DeViL#7091") 
  await bot.change_presence(status=discord.Status.online, activity=game)

  print(f'Bot is online.\n Bot Name: {bot.user}!')


# ----- COMMAND ERRORS -----

@players.error
async def players_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `{prefix}players [Server Name]`")

@players.error
async def servers_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `{prefix}servers [Server Name]`")

@imginfo.error
async def imginfo_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `{prefix}imginfo [Server Name]`")

@info.error
async def info_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
    await ctx.send(f"{ctx.author.mention} Correct Usage: `{prefix}imginfo [Server Name]`")



# ----- FUNCTIONS -----

# --- Total Online Servers ---
def total_online_servers(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  serverlist = soup.find(id='serverlist')
  if serverlist == None:
    return False
  for cs in serverlist.find_all('a', href=True):

    if server.lower() in str((cs.get_text().lower())):
      print(server.lower())
      total_server = total_server + 1
  return total_server
  


with open('./config.json', 'r') as configFile:
  configdata = json.load(configFile)
  token = configdata['TOKEN']

bot.run(token)


"""

# --- Total Online Servers ---
def total_online_servers(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  serverlist = soup.find(id='serverlist')

  for cs in serverlist.find_all('a', href=True):

    if str(server.lower()) in str((cs.get_text().lower())):
      total_server = total_server + 1

  return total_server


# --- Servers ---
def find_online_servers(server:str):

  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  total_server_string = ""

  serverlist = soup.find(id='serverlist')

  for a in serverlist.find_all('a', href=True):

    if str(userserver.lower()) in str((a.get_text().lower())):

      total_server = total_server + 1
      server_ip_info = a['href']
      # server_raw = server_ip_info[1:-1].split(':')
      server_ip = server_ip_info[1:-1]
      total_server_string = total_server_string + f"Server: {str(a.get_text())} IP: {server_ip}\n"
     
  if total_server <= 0:
    return f"There is no server online with name {server}"
  
  else:
    return total_server_string



# ----- Server Image -----
def find_online_server_img(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    return f"There are two or too many servers online with name {server}"

  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text().lower())):
      return f"http://www.game-state.com/{a['href']}/560x95_FFFFFF_FF9900_000000_000000.png"



# ----- Online Players -----
def find_online_server_players(server:str):
    
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    return f"There are two or too many servers online with name {server}"


  player_list = ""
    
  for a in soup.find_all('a', href=True):

    if str(userserver.lower()) in str((a.get_text().lower())):

      serverurl = f"https://www.game-state.com{a['href']}"

      su = requests.get(serverurl, headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      playerslist = soupurl.find(id='playerslist')
      tp = 0

      for player in playerslist.find_all('td'):


        if tp%2 == 0:
          player_list = player_list + f"{str(player.get_text())}"
          tp = tp + 1

        elif tp%2 == 1:
          tp = tp + 1
          player_list = player_list + f"  -  {str(player.get_text())}\n"

      
      if (tp-2) <= 2:
        return f"There are no players online or not retrive players data due to server having more 100+ player"

      return player_list



# ----- Server Info -----
def find_online_server_info(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:
    return f"There are two or too many servers online with name {server}"


  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text().lower())):

      serverurl = f"https://www.game-state.com{a['href']}"

      su = requests.get(serverurl, headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      print(f"Server Name: {(soupurl.find(id='hostname')).get_text()}")
      print(f"State: {(soupurl.find(id='state')).get_text()}")
      print(f"Total Players: {(soupurl.find(id='players')).get_text()}")
      print(f"IP: {a['href'][1:-1]}")
      print(f"Game Mode: {(soupurl.find(id='gamemode')).get_text()}")
      print(f"Map Name: {(soupurl.find(id='mapname')).get_text()}")

      servervar = soupurl.find(id='var')
      varcout = 0
      var = ""
      for link in servervar.find_all('td'):
        varcout = varcout + 1
        if varcout%2 == 1:
          var = var + str(link.get_text())

        elif varcout%2 == 0:
          var = var + f"{str(link.get_text())}\n"

      
      return var


"""
