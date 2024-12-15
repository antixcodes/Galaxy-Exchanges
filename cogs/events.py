import nextcord, json
from nextcord.ext import commands

with open('config.json', 'r') as f:
    config = json.load(f)
rang = config['rang']
name = config['embedname']
channel_id = 1315351763871596606 
class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(f"Welcome to Galaxy Exchanges, {member.mention}")
        '''try:
            await member.send(f"Hello {member.name}, welcome to the server! Please check out the rules and have fun!")
        except nextcord.Forbidden:
            pass''' 
        
def setup(bot):
    bot.add_cog(events(bot))