import asyncio
import aiohttp
import discord
import json
import random

from distutils.version import LooseVersion
__version__ = '0.2.5'

class Poke(discord.Client):
    def __init__(self, config_path: str, *args, **kwargs):
        self.config_path = config_path
        self.update_check = False
        self.channel = None

        with open(self.config_path) as f:
            self.configs = json.load(f)

        with open('pokemonrefs.json') as f:
            self.pokeref = json.load(f)
        super().__init__()

    def run(self):
        super().run(self.configs['token'], bot=False)
    
    @staticmethod
    def bordered(text):
        lines = text.splitlines()
        width = max(len(s) for s in lines)
        res = ['┌' + '─' * width + '┐']
        for s in lines:
            res.append('│' + (s + ' ' * width)[:width] + '│')
        res.append('└' + '─' * width + '┘')
        return '\n'.join(res)

    async def on_message(self, message):
        if self.configs['whitelist_channels'] and message.channel.id not in self.configs['whitelist_channels']:
            return
        if self.configs['blacklist_channels'] and message.channel.id in self.configs['blacklist_channels']:
            return
        if message.author.id == 365975655608745985 and message.embeds:
            emb = message.embeds[0]
            try:
                title = emb.title
            except AttributeError:
                return
            if title.startswith('A wild'):
                name = self.pokeref[emb.image.url.split('/')[-1].split('.')[0]]
                proc = random.randint(1, 100)
                if self.configs['priority_only'] and name not in self.configs['priority']:
                    return
                if name in self.configs['priority'] or (proc <= self.configs['catch_rate'] and
                                                        name not in self.configs['avoid_list']):
                    if name in self.configs['priority']:
                        self.configs['priority'].remove(name)
                    if name in self.configs['priority'] and not self.configs['delay_on_priority']:
                        pass
                    else:
                        await asyncio.sleep(self.configs['delay'])
                    pref = emb.description.split()[5]
                    def ping_check(m):
                        return self.user.mention in m.content and m.author.id == 365975655608745985
                    await message.channel.send(f"{pref} {name}")
                    self.channel = message.channel
                    print(message.channel)
                    try:
                        await self.wait_for('message', check=ping_check, timeout=5)
                    except asyncio.TimeoutError:
                        return print('Failed to catch {}{}'.format(name, f' in {message.guild.name}'
                                                                         f' in #{message.channel.name}.'
                                                                         if self.configs["verbose"] else "."))
                    print('Caught {}{}'.format(name, f' in {message.guild.name} in #{message.channel.name}.' if
                          self.configs["verbose"] else "."))
                elif self.configs['verbose']:
                    print(f"Skipped a {name}")

    async def on_ready(self):
        if not self.update_check:
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.get('http://api.github.com/repos/xKynn/PokecordCatcher/releases') as resp:
                    ver = await resp.json()
            ver_tag = ver[0]['tag_name']
            if LooseVersion(ver_tag) > LooseVersion(__version__):
                print(self.bordered(f'A new version is available! Please update ASAP.\n{ver[0]["name"]}\n{ver[0]["body"]}\n'
                                     'Visit http://www.github.com/xKynn/PokecordCatcher/releases/latest'))
            self.update_check = True

            await asyncio.sleep(self.configs['delay'])
        print("Logged in.\n---PokecordCatcher----\n"
              f"Priority: {', '.join(self.configs['priority'])}\n"
              f"Catch Rate: {self.configs['catch_rate']}%\n"
              f"Catch Delay: {self.configs['delay']} seconds\n"
              f"Delay On Priority: {'On' if self.configs['delay_on_priority'] == True else 'Off'}")
        if self.configs['findPokemon']:
            self.loop.create_task(self.background_findPokemon())
        if self.configs['whitelist_channels'] and self.configs['blacklist_channels']:
            print('------\nCan only have either blacklist__channels active or whitelist_channels active\n'
                  'Please clear one of the two lists to use the bot\n-----\nLogging out.')
            await self.logout()
    
    async def background_findPokemon(self):
        await self.wait_until_ready()
        while True:
            channel = self.get_channel(id=self.configs['findPokemon_channel'])
            print("finding pokemon in ", channel)
            await channel.send("Finding Pokemon...")
            await asyncio.sleep(self.configs['findPokemon_delay'])
