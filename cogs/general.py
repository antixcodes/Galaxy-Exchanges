import nextcord, json
from nextcord.ext import commands

with open('config.json', 'r') as f:
    config = json.load(f)
rang = config['rang']
name = config['embedname']

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def calc(self, ctx, *, expression: str):
        try:
            if "%" in expression:
                number, percent = expression.split('-')
                number = float(number.strip())
                percent = float(percent.replace('%', '').strip())
                result = number - (number * (percent / 100))
            else:
                result = eval(expression)
            embed = nextcord.Embed(title="<:calculator:1315718760530706503> Calculator", color=rang)
            embed.add_field(name="Input:", value=f"```{expression}```", inline=False)
            embed.add_field(name="Output:", value=f"```{result}```", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
            #embed.set_thumbnail(url=bot_thumbnail)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @commands.command()
    async def staffreq(self, ctx):
            await ctx.message.delete() 
            embed = nextcord.Embed(title="Galaxy Exchange Staff Req", color=rang)
            embed.add_field(name="<:alert:1321168458016358448> Req:", value=f"<:arrow_downright:1305955462700863498> 30+ vouches = 2$ Exchange/mm limit\n<:arrow_downright:1305955462700863498> 50+ vouches = 4$ Exchange/mm limit\n**TOS: Must have to add our vanity in your status/about\nYou must agree to exchange at our exchange rate > <#1320005089343307868>**", inline=False)
            embed.add_field(name="Want more exchange/mm limit", value=f"> Deposite Security Amount Above your Limit\n> Eg: Your limit is 2$ and you want limit of 4$ then deposit 2$ as security", inline=False)
            embed.set_footer(text=f"Galaxy Exchanges | MM | Exchanges")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))
