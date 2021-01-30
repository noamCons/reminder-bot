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
        msg = await client.wait_for('message', check=check, timeout = 86400)
        print("Here the msg we have:", msg)
      except asyncio.exceptions.TimeoutError:
        await channel.send("Reply timed out!")
  
      #if the user replied
      try:
        if msg:
          if msg.content == "Y":
            await channel.send('THE LESSON IS ON!')
          else:
            await channel.send("Rescheduling :-|")
      except:
          await channel.send('NO REPLY')



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
