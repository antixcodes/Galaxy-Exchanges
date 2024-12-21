import nextcord, string
from nextcord.ext import commands
import random, json, os

with open('config.json', 'r') as f:
    config = json.load(f)
rang = config['rang']
name = config['embedname']

role_map_file = "database\rolemap.json"
def rolemap():
    if os.path.exists(role_map_file):
        try:
            with open(role_map_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON in role_map_file. Initializing a new role map.")
            return initialize_rolemap()
    else:
        return initialize_rolemap()

def initialize_rolemap():
    return {
        "role_map": {
            "crypto_exchanger": None,
            "paypal_exchanger": None,
            "inr_exchanger": None,
            "pkr_exchanger": None,
            "idr_exchanger": None,
            "bdt_exchanger": None,
            "mm_id": None,
            "admin_id": None,
            "staff": None
        }
    }


exchconfig = rolemap()  

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=35))

def load_staff_data():
    try:
        with open("database\staff.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_staff_data(data):
    with open("database\staff.json", "w") as file:
        json.dump(data, file, indent=4)

role_mapping = exchconfig.get("role_map", {})
adminrole = role_mapping.get("admin_id")
majdur = role_mapping.get("staff")

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx, member: nextcord.Member):
        role = nextcord.utils.get(ctx.guild.roles, id=majdur)
        if any(role.id == adminrole for role in ctx.author.roles):
            staff_data = load_staff_data()
            key = generate_key()
            if str(member.id) in staff_data:
                if "key" not in staff_data[str(member.id)]:
                    staff_data[str(member.id)]["key"] = key
                    save_staff_data(staff_data)
                    await member.add_roles(role)
                    await ctx.send(embed = nextcord.Embed(description=f"<:check:1305951941423009803> | Successfully Added {member.mention} to staff",color=rang))
                    embed = nextcord.Embed(title=f"Welcome to {name}'s Staff",color=rang)
                    embed.add_field(name=f"Token: {key}", value="Copy it and keep it safe! It will backup your deals and roles if your main id is termed")
                    await member.send(embed=embed)
                else:
                    embed = nextcord.Embed(title=f"Welcome to {name}'s Staff",color=rang)
                    embed.add_field(name=f"Token: {key}", value="Copy it and keep it safe! It will backup your deals and roles if your main id is termed")
                    await ctx.send(f"{member.mention} is already a staff member with an existing key.")
                    await member.send(embed=embed)
            else:
                staff_data[str(member.id)] = {"key": key}
                save_staff_data(staff_data)
                await member.add_roles(role)
                await ctx.send(embed = nextcord.Embed(description=f"<:check:1305951941423009803> | Successfully Added {member.mention} to staff",color=rang))
                embed = nextcord.Embed(title=f"Welcome to {name}'s Staff",color=rang)
                embed.add_field(name=f"Token: {key}", value="Copy it and keep it safe! It will backup your deals and roles if your main id is termed")
                await member.send(embed=embed)
        else:
            print("idk")
            return
        
    @commands.command()
    async def rstaff(self, ctx, member: nextcord.Member):
        if any(role.id == adminrole for role in ctx.author.roles):
            staff_data = load_staff_data()
            if str(member.id) in staff_data:
                staff_data[str(member.id)].pop("key", None)
                save_staff_data(staff_data)
                role = nextcord.utils.get(ctx.guild.roles, id=majdur)
                if role:
                    await member.remove_roles(role)
                await ctx.send(f"{member.mention}'s key has been removed, but their deal details remain.")
            else:
                await ctx.send(f"{member.mention} is not a staff member.")
        else:
            print("idk")
            return
        
    @commands.command()
    async def login(self, ctx, key: str):
        staff_data = load_staff_data()
        found = False
        if str(ctx.author.id) in staff_data:
            await ctx.send(f"You are already part of the staff team. Login denied.")
            return
        for staff_id, staff_info in staff_data.items():
            if isinstance(staff_info, dict) and staff_info.get("key") == key:
                staff_data[str(ctx.author.id)] = {"key": key}
                del staff_data[staff_id]  
                found = True
                save_staff_data(staff_data) 
                role = nextcord.utils.get(ctx.guild.roles, id=majdur)
                if role:
                    await ctx.author.add_roles(role)
                await ctx.send(f"Login successful! Your staff member ID has been updated to {ctx.author.id}.")
                break
            elif isinstance(staff_info, list):
                continue
        if not found:
            await ctx.send("Invalid key or the key does not exist in the staff records.")
        
    @commands.command()
    async def delete(self, ctx):
        channel=ctx.channel
        if any(role.id == adminrole for role in ctx.author.roles):
            await channel.delete()
        else:
            print("idk")
            return

def setup(bot):
    bot.add_cog(admin(bot))