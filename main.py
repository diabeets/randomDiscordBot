import os
import discord
import requests
import json
import random

my_secret = os.environ['TOKEN']
client = discord.Client()
myList = []

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def getExist(item, myList):
  for i in range(len(myList)):
    if item == myList[i]:
      return True
  return False

def pick():
  return random.choice(myList)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('quote'):
        await message.channel.send(get_quote())

    if message.content.startswith('r!add'):
      item = message.content.split("r!add ", 1)[1]
      if getExist(item, myList) == False:
        myList.append(item)
        await message.channel.send("Added to list!")
      else:
        await message.channel.send("Already in list!")

    if message.content.startswith('r!remove'):
      item = message.content.split("r!remove ", 1)[1]
      if getExist(item, myList) == True:
        myList.remove(item)
        await message.channel.send("Removed from list!")
      else:
        await message.channel.send("Did not exist in list!")
    
    if message.content.startswith('r!pick'):
      await message.channel.send(pick())

    if message.content.startswith('r!display'):
        embedVar = discord.Embed(title="The List", description="items that are in the list", color=0x00ff00)
        embedVar.add_field(name="List", value=myList, inline=False)
        await message.channel.send(embed=embedVar)


client.run(my_secret)
