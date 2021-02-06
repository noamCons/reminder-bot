import discord
import threading
import datetime
from discord.ext import commands, tasks
import asyncio
import os
from pytz import timezone
import pytz

token = os.environ.get('BOT_TOKEN')

#parameters are thing that goes into a function
client = discord.Client() # object 

#This function runs once every 1 hour to check the time
@tasks.loop(seconds=3600)
async def name_change():
    print("Task is looping")
    weekday = datetime.datetime.now(tz=pytz.utc)
    weekday = weekday.astimezone(timezone('US/Pacific'))
    #if its Tues at 7pm or thursday at 7pm
    if ( weekday.strftime("%a") == "Tue" and weekday.strftime("%-H") == "19") or (weekday.strftime("%a") == "Thu" and weekday.strftime("%-H") == "19"):
      channel = client.get_channel(802297661091872780)
      noamid = "<@485451366307725352>"
      await channel.send(f"{noamid} you got class tommorrow don't forget lmao. Y to confirm or N to reschedule ")
      #check if message came from the alarm channel
      def check(m):
          return channel == m.channel

      #wait reply, you'll have one day of time to reply 
      try:
        msg = await client.wait_for('message', check=check, timeout = 90000)
        print("Here the msg we have:", msg)
      except asyncio.exceptions.TimeoutError:
        await channel.send("Reply timed out!")
  
      #if the user replied
      try:
        if msg:
          verifiers = ["y","ye","yes","yess","sure","k","ok","ayy the bot works","nice"]
          
          if msg.content.lower() in verifiers:
            await channel.send('THE LESSON IS ON!')
          else:
            #try and see if there are errors
            try: 

              jackyid = "<@139270518153936896>"
              jacky_user =client.get_user(139270518153936896)

              weekday = datetime.datetime.now(tz=pytz.utc)
              weekday = weekday.astimezone(timezone('US/Pacific'))
              day = weekday.strftime("%a")
              if jacky_user.dm_channel:
                await jacky_user.dm_channel.send(f"{jackyid} Noam would like to reschedule lesson on {day}")
              else:
                dm_channel = jacky_user.create_dm()
                await dm_channel.send(f"{jackyid} Noam would like to reschedule lesson on {day}")

            except Exception as e:
              await channel.send(f'ERROR!{e}')
            else:
              await channel.send(f'DONE!')

      except:
          await channel.send('NO REPLY')


@client.event
async def on_message(message):
  if message.author != client.user:
    
    #split msg into parts
    try :
      symbol = message.content.split()[0] # seperate string into a list by spaces
      command = message.content.split()[1] 
    except:
      pass
      
    else:
      if symbol == "!": 
        if command == "status":
          await message.channel.send("I'm alive!")


@client.event
async def on_ready():
  print("DISCORD.PY VER:",discord.__version__)
  print("im up and runnin dawg")
  print("Emojis:",client.emojis)
  print("guild:",client.guilds)
  channel = client.get_channel(802297661091872780)
  weekday = datetime.datetime.now(tz=pytz.utc)
  weekday = weekday.astimezone(timezone('US/Pacific'))
  await channel.send("howdy! :french_bread: \nIt's {}".format(weekday.strftime("%a")))
  name_change.start()


client.run(token)
