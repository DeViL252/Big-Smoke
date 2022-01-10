import requests 
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import Intents
import json


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

prefix = "!"

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=Intents.all())

# ----- COMMANDS -----

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

  embed = discord.Embed(title="Online Server", description=f"Server found with name {server}, Bot can only send first 25 matching servers.", colour=ctx.author.colour)

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

  # elif total_server >= 49:
  #   await msg.delete()
  #   return await ctx.send(f"There are more than 50+ servers online with name `{server}`")
  
  else:
    await msg.delete()
    embed = embed.add_field(name="Total Servers", value=total_server, inline=True)
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

  totalplayer = 0
  servername = ""
  playerlist = ""
    
  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text()).lower()):
      cp = 0
      servername = str(a.get_text())
      
      # server_url = 

      su = requests.get(f"https://www.game-state.com{a['href']}", headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      real_cp = 0 
      for id in soupurl.find_all('td'):
        real_cp = real_cp + 1
        if id.get_text() == "Score":
          break

      for id in soupurl.find_all('td'):
        cp = cp + 1
        if cp > real_cp:

          if totalplayer < 90:
            if cp%2 == 1:
              playerlist = playerlist + f"{id.get_text()}"

            elif cp%2 == 0:

              totalplayer = totalplayer + 1
              playerlist = playerlist + f" - {id.get_text()}\n"

      await msg.delete()
      embed = discord.Embed(title=servername, description=playerlist, colour=ctx.author.colour)
      embed.add_field(name="Total Players", value=totalplayer, inline=True)

      if totalplayer == 0:
        embed.add_field(name="Server Unbound Issue", value="Unable to retrive server player data cause server across 100+ player or server having zero player connected!", inline=True)
      embed.set_footer(text="Big Smoke", icon_url=ctx.bot.user.avatar_url)
      
      return await ctx.send(embed=embed)

  else:
    await msg.delete()
    return await ctx.send(f"There is no server online with name `{server}`")
  

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

  for a in soup.find_all('a', href=True):

    if str(server.lower()) in str((a.get_text()).lower()):
      await msg.delete()
      return await ctx.send(f"http://www.game-state.com/{a['href']}/560x95_FFFFFF_FF9900_000000_000000.png")

  else:
    await msg.delete()
    return await ctx.send(f"Server not found with name {server}.")



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




# ----- FUNCTIONS -----

# --- Total Online Servers ---
def total_online_servers(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  for a in soup.find_all('a', href=True):
    if server in str(a.get_text()):
      total_server = total_server + 1
  return total_server


# --- Total Online Players ---
def total_online_players(server:str):
    
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(server) >= 2:

    return f"There are two or too many servers online with name {server}"


    
  for a in soup.find_all('a', href=True):

    if server in str(a.get_text()):
      cp = 0
      totalplayer = 0

      serverurl = f"https://www.game-state.com{a['href']}"

      su = requests.get(serverurl, headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      for id in soupurl.find_all('td'):
        cp = cp + 1

        if cp > 48:

          if cp%2 == 1:
            pass

          elif cp%2 == 0:

            totalplayer = totalplayer + 1

      return totalplayer

with open('./config.json', 'r') as configFile:
  configdata = json.load(configFile)
  token = configdata['TOKEN']

bot.run(token)




"""
import requests 
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}



def total_online_servers(server:str):
  url = f'https://www.game-state.com/index.php?search={userserver}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  for a in soup.find_all('a', href=True):
    if userserver in str(a.get_text()):
      total_server = total_server + 1
  return total_server



def find_online_servers(server:str):

  url = f'https://www.game-state.com/index.php?search={userserver}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  total_server = 0
  total_server_string = ""

  if total_online_servers(userserver) >= 2:
    
    print(f"There are two or too many servers online with name {server}")
    return 0

  for a in soup.find_all('a', href=True):
    if userserver in str(a.get_text()):
      total_server = total_server + 1
      server_ip_info = a['href']
      # server_raw = server_ip_info[1:-1].split(':')
      server_ip = server_ip_info[1:-1]
      total_server_string = total_server_string + f"Server: {str(a.get_text())} IP: {server_ip}\n"
     
  if total_server == 0:
    return f"There is no server online with name {server}"
  
  else:
    print("---------- Online Servers ----------")
    return total_server_string

def find_server_info(server:str):
  url = f'https://www.game-state.com/index.php?search={server}&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(userserver) >= 2:
    print(f"There are two or too many servers online with name {server}")
    return 0
  for a in soup.find_all('a', href=True):

    if userserver in str(a.get_text()):
      return f"http://www.game-state.com/{a['href']}/560x95_FFFFFF_FF9900_000000_000000.png"



def find_online_players(server:str):
    
  url = f'https://www.game-state.com/index.php?search={server}&spp=50&game=samp'

  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  if total_online_servers(userserver) >= 2:

    print(f"There are two or too many servers online with name {server}")

    return 0

    
  for a in soup.find_all('a', href=True):

    if userserver in str(a.get_text()):
      cp = 0
      totalplayer = 0

      players = f"Server Name:- {str(a.get_text())}"
      serverurl = f"https://www.game-state.com{a['href']}"

      su = requests.get(serverurl, headers=headers)

      soupurl = BeautifulSoup(su.text, 'html.parser')

      for id in soupurl.find_all('td'):
        cp = cp + 1

        if cp > 48:

          if cp%2 == 1:
            players = players + f"{id.get_text()}"

          elif cp%2 == 0:

            totalplayer = totalplayer + 1
            players = players + f"  {id.get_text()}\n"

      print(f"{players}\nTotal Online Players: {totalplayer}")



if __name__ == "__main__":

  userinput = str(input("What do you wanna search for?\n Type:-\n 'player' - to find online players!\n 'find' - to find a server info\n 'servers' - to find online servers\n"))

  if userinput == 'player':

    userserver = str(input("Enter the server name!\n"))

    find_online_players(userserver)

  elif userinput == "find":
    userserver = str(input("Enter the server name!\n"))
    print(f"{find_server_info(userserver)}")

  elif userinput == "servers":

    userserver = str(input("Enter the server name!\n"))

    print(f"{find_online_servers(userserver)}")
"""
