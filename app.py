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

admin_ids = os.environ['IDS'].split(",")

f = open('tweets.json')
twitter = json.load(f)
def clearTweet(text):
    text = re.sub('http\S+', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub('@\w+', '', text, flags=re.IGNORECASE | re.MULTILINE)
    return text

class Tosi(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if re.search(r'((hadi\s?)?((uykuya)|(uyu)|(yat)|(git))\s?[t]+[o]+[s]+[i]+)|([t]+[o]+[s]+[i]+\s?(hadi\s?)?((uykuya)|(uyu)|(yat)|(git)))', message.content, flags=re.IGNORECASE | re.MULTILINE):
            await self.shutdown(message)

        elif re.search(r'((hadi\s?)?((uy[a]+n)|(kalk)|(gel))\s?[t]+[o]+[s]+[i]+)|([t]+[o]+[s]+[i]+\s?(hadi\s?)?((uy[a]+n)|(kalk)|(gel)))', message.content, flags=re.IGNORECASE | re.MULTILINE):
            await self.wakeup(message)

        elif message.guild.get_member(self.user.id).status != discord.Status.online:
            return

        elif re.search(r'(\s?[t]+[o]+[s]+[i]+){2}', message.content, flags=re.IGNORECASE | re.MULTILINE):
            choice = twitter['tweet']["1643"]
            text = clearTweet(choice)
            img = twitter['thumbnail']["1643"]
            e = discord.Embed()
            e.set_image(url=img)
            return await message.channel.send(text, embed=e)

        elif re.search(r'\b[t]+[o]+[s]+[i]+\b', message.content, flags=re.IGNORECASE | re.MULTILINE):
            choice = random.choice(list(twitter['tweet'].items()))
            text = clearTweet(choice[1])
            try:
                img = twitter['thumbnail'][choice[0]]
            except:
                img = ''
            if img != '':
                e = discord.Embed()
                e.set_image(url=img)
                return await message.channel.send(text, embed=e)
            return await message.channel.send(text)

    async def shutdown(self, message):
        if str(message.author.id) in admin_ids:
            await message.channel.send("üşdakka uyuyim madem")
            await self.change_presence(status=discord.Status.idle)

    async def wakeup(self, message):
        if str(message.author.id) in admin_ids:
            await message.channel.send("üşdakka uyumuşdum nevar")
            await self.change_presence(status=discord.Status.online)

client = Tosi()
client.run(token)