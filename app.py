import discord
import json
import random
import re
import os

if os.path.exists('token.txt'):
    with open('token.txt') as f:
        token = f.readlines()[0]
else:
    token = os.environ['TOKEN']

f = open('tweets.json')
twitter = json.load(f)

class Tosi(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if re.search(r'\btosi\b', message.content):
            choice = random.choice(list(twitter['tweet'].items()))
            text = re.sub('http\S+', '', choice[1].lower(), flags=re.MULTILINE)
            text = re.sub('@\w+', '', text, flags=re.IGNORECASE | re.MULTILINE)
            try:
                img = twitter['thumbnail'][choice[0]]
            except:
                img = ''
            if img != '':
                e = discord.Embed()
                e.set_image(url=img)
                return await message.channel.send(text, embed=e)
            return await message.channel.send(text)

client = Tosi()
client.run(token)