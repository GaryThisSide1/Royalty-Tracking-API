import requests
import discord
import os
import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands
import json
import webbrowser
import random
import csv
import os
pp = PrettyPrinter()
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

game = ''
total=0
Hadeswap=0
MagicEden_V2=0
totals=0
Royalty=0
def fetchAPOD():
  response = requests.get(
    'https://api.coralcube.cc/0dec5037-f67d-4da8-9eb6-97e2a09ffe9a/inspector/getMintActivities?update_authority=yootn8Kf22CQczC732psp7qEqxwPGSDQCFZHkzoXp25&collection_symbol=y00ts'
  ).json()
  global game
  global Hadeswap
  global MagicEden_V2
  global total
  global totals
  global Royalty
  Royalty=0
  total=0
  totals=0
  Hadeswap=0
  MagicEden_V2=0
  game = requests.get(response[random.randint(0,len(response))]["metadata"]["uri"]).json()
  game = game['image']
  data_file = open('hello.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  count = 0
  # for data in response:
  #     if count == 0:
  #         header = data.keys()
  #         csv_writer.writerow(header)
  #         count += 1
  #     csv_writer.writerow(data.values())

  data_file.close()
  d = []
  for x in range(len(response)):
    d.append({})
    for y in range(len(response[x])):
      if (y == 0):
        totals+=1
        d[x]["mint"] = response[x]["metadata"]["mint"]
        d[x]["pubkey"] = response[x]["metadata"]["pubkey"]
        d[x]["name"] = response[x]["metadata"]["name"]
        d[x]["symbol"] = response[x]["metadata"]["symbol"]
        d[x]["seller_fee_basis_points"] = response[x]["metadata"][
          "seller_fee_basis_points"]
      else:
        d[x]["price"] = ((response[x]["price"])/1000000000)
        d[x]["royalty_fee"] = response[x]["royalty_fee"]/1000000000
        Royalty+=d[x]["royalty_fee"]
        if(d[x]["royalty_fee"]!=0):
            total+=1
        d[x]["buyer"] = response[x]["buyer"]
        d[x]["seller"] = response[x]["seller"]
        d[x]["marketplace"] = response[x]["marketplace"]
        if(d[x]["marketplace"]=="Hadeswap"):
          Hadeswap+=1
        elif(d[x]["marketplace"]=="MagicEden V2"):
          MagicEden_V2+=1
        d[x]["signature"] = response[x]["signature"]

  # 0.metadata.mint
  # response[x][0]["metadata"]["mint"]
  # 0.metadata
  data_file = open('hello.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  count = 0
  for data in d:
    if count == 0:
      header = data.keys()
      csv_writer.writerow(header)
      count += 1
    csv_writer.writerow(data.values())
  return 0
def fetch(a,b):
  response = requests.get(
    "https://api.coralcube.cc/0dec5037-f67d-4da8-9eb6-97e2a09ffe9a/inspector/getMintActivities?update_authority="+a+"&collection_symbol="+b
  ).json()
  global game
  global Hadeswap
  global MagicEden_V2
  global total
  global totals
  global Royalty
  Royalty=0
  total=0
  totals=0
  Hadeswap=0
  MagicEden_V2=0
  game = requests.get(response[random.randint(0,len(response))]["metadata"]["uri"]).json()
  game = game['image']
  data_file = open('hello.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  count = 0
  # for data in response:
  #     if count == 0:
  #         header = data.keys()
  #         csv_writer.writerow(header)
  #         count += 1
  #     csv_writer.writerow(data.values())

  data_file.close()
  d = []
  for x in range(len(response)):
    d.append({})
    for y in range(len(response[x])):
      if (y == 0):
        totals+=1
        d[x]["mint"] = response[x]["metadata"]["mint"]
        d[x]["pubkey"] = response[x]["metadata"]["pubkey"]
        d[x]["name"] = response[x]["metadata"]["name"]
        d[x]["symbol"] = response[x]["metadata"]["symbol"]
        d[x]["seller_fee_basis_points"] = response[x]["metadata"][
          "seller_fee_basis_points"]
      else:
        d[x]["price"] = ((response[x]["price"])/1000000000)
        d[x]["royalty_fee"] = response[x]["royalty_fee"]/1000000000
        Royalty+=d[x]["royalty_fee"]
        if(d[x]["royalty_fee"]!=0):
            total+=1
        d[x]["buyer"] = response[x]["buyer"]
        d[x]["seller"] = response[x]["seller"]
        d[x]["marketplace"] = response[x]["marketplace"]
        if(d[x]["marketplace"]=="Hadeswap"):
          Hadeswap+=1
        elif(d[x]["marketplace"]=="MagicEden V2"):
          MagicEden_V2+=1
        d[x]["signature"] = response[x]["signature"]

  # 0.metadata.mint
  # response[x][0]["metadata"]["mint"]
  # 0.metadata
  data_file = open('hello.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  count = 0
  for data in d:
    if count == 0:
      header = data.keys()
      csv_writer.writerow(header)
      count += 1
    csv_writer.writerow(data.values())
  return 0

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.command()
async def data(ctx):
  fetchAPOD()

  await ctx.send(file=discord.File(r'hello.csv'))
#   await ctx.send(game)
  embed=discord.Embed(title="Lily", color=0xFF5733)
  embed.add_field(name="Owners", value=totals, inline=True)
  embed.add_field(name="Royalty payers", value=total, inline=True)
  embed.add_field(name="Total Royalty paid", value=str(Royalty)+"sol", inline=True)
  embed.set_image(url=game)
  await ctx.send(embed=embed)
  plt.cla()
  g=[]
  g.append(Hadeswap)
  g.append(MagicEden_V2)
  y = np.array(g)
  mylabels = ["Hadeswap", "MagicEden_V2"]
  
  plt.title("Marketplaces")
  plt.pie(y, labels = mylabels)
  plt.legend()
  plt.savefig("output.jpg")
  await ctx.send(file=discord.File(r'output.jpg'))
  os.remove("output.jpg")
  plt.cla()
  f=[]
  f.append((total/totals)*100)
  f.append(100-((total/totals)*100))
  z=np.array(f)
  labelss=["people gave royalty","Total people who buyed"]
  
  plt.title("royalty pie chart")
  plt.pie(z,labels=labelss)
  plt.legend()
  plt.savefig("out.jpg")
  await ctx.send(file=discord.File(r'out.jpg'))
  os.remove("out.jpg")
@client.command()
async def specific(ctx,arg1,arg2):
  fetch(arg1,arg2)
  await ctx.send(file=discord.File(r'hello.csv'))
  embed=discord.Embed(title=arg2, color=0xFF5733)
  embed.add_field(name="Owners", value=totals, inline=True)
  embed.add_field(name="Royalty payers", value=total, inline=True)
  embed.add_field(name="Total Royalty paid", value=str(Royalty)+"sol", inline=True)
  embed.set_image(url=game)
  await ctx.send(embed=embed)
  plt.cla()
  g=[]
  if(Hadeswap==0):
    g.append(MagicEden_V2)
    y = np.array(g)
    mylabels = ["MagicEden_V2"]
  elif(MagicEden_V2==0):
    g.append(Hadeswap)
    y = np.array(g)
    mylabels = ["Hadeswap"]
  else:
    g.append(Hadeswap)
    g.append(MagicEden_V2)
    y = np.array(g)
    mylabels = ["Hadeswap", "MagicEden_V2"]
  
  plt.title("Marketplaces")
  plt.pie(y, labels = mylabels)
  plt.legend()
  plt.savefig("output.jpg")
  await ctx.send(file=discord.File(r'output.jpg'))
  plt.cla()
  os.remove("output.jpg")
  f=[]
  f.append((total/totals)*100)
  f.append(100-((total/totals)*100))
  z=np.array(f)
  labelss=["people gave royalty","Total people who buyed"]
  
  plt.title("royalty pie chart")
  plt.pie(z,labels=labelss)
  plt.legend()
  plt.savefig("out.jpg")
  await ctx.send(file=discord.File(r'out.jpg'))
  os.remove("out.jpg")
@client.command()
async def Help(ctx):
    await ctx.send("For seeing the predefined nft colllection data use ```!data``` For a specific collection data use ```!specific  then write Update Authority then write the collection name```")
client.run('MTA1MTA1MDY5MDM5MjM3NTMyNg.GqvIQ7.5Lvn6JlLtj98zZDeRw5hzb9ApovXur-zqSSvuA')


    