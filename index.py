from keep_alive import keep_alive
import nextcord, requests, time#, chat-exporter#, jishaku
from nextcord.ext import commands
from nextcord import Interaction, ui
from nextcord import File
from nextcord.ui import View, Select
from nextcord import SlashOption
from nextcord.ui import Button, View
import datetime, random, asyncio, aiohttp, json, os, re, aiofiles, qrcode, io
from dhooks import Webhook
from datetime import datetime
from googletrans import Translator, LANGUAGES
#from cogs.staff.py import staff
from nextcord import AllowedMentions
translator = Translator()
from typing import Optional
import io
from chat_exporter.construct.transcript import Transcript
from chat_exporter.ext.discord_import import discord
from chat_exporter.construct.attachment_handler import AttachmentHandler
from cogs import exchange

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None, owner_ids={955721842675560462})
#bot.add_cog(staff(bot))
with open('config.json', 'r') as f:
    config = json.load(f)
tkn = config['token']    
CLOSURE_WEBHOOK_URL = config['logs']
CLAIMED_WEBHOOK_URL = config['claim_logs']
tr_log = config['transcript_logs']
bot_thumbnail = config['bot_thumbnail']
rang = config['rang']
exchangers_role_id = config['exchangers_role_id']
CLIENT_ROLE_ID = config['client_role_id']
name = config['embedname']
vlx = config['vouchlogs']
vouchlog = Webhook(f"{vlx}")
trans_logs = Webhook(f"{tr_log}")
prefix="."
nocolor=0x2B2D31
tick="<:GreenCheck:1317254690676936816>"
#######################################################3

def load_walletdb():
    file_path = 'database/wallet.json'
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Warning: {file_path} contains invalid JSON. Returning an empty dictionary.")
        return {}

def save_walletdb(data):
    file_path = 'database/wallet.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving wallet database: {e}")

VOUCHES_FILE = "database/vouches.json"

if not os.path.exists(VOUCHES_FILE):
    with open(VOUCHES_FILE, 'w') as f:
        json.dump({}, f) 

def load_walletdb():
    try:
        with open('database/wallet.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  
    
def save_walletdb(data):
    with open('database/wallet.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_state():
    if os.path.exists('database/state.json'):
        with open('database/state.json', 'r') as file:
            return json.load(file)
    return {}

def save_state(state):
    with open('database/state.json', 'w') as file:
        json.dump(state, file)

def exchangedeal(ticket_channel_id, nom, sendingcurrency, receivingcurrency, file_name="database/exchangedeals.json"):
    new_data = {
        ticket_channel_id: [
            {   "name": nom,
                "sendingcurrency": sendingcurrency,
                "receivingcurrency": receivingcurrency
            }
        ]
    }

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    if ticket_channel_id in data:
        data[ticket_channel_id].extend(new_data[ticket_channel_id])
    else:
        data.update(new_data)
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {file_name}")

CONFIG_FILE_PATH = "database/categorydb.json"
def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as file:
            return json.load(file)
    else:
        return {
            "category_mapping": {
                "crypto_to_inr": None,
                "inr_to_crypto": None,
                "crypto_to_crypto": None,
                "paypal_to_crypto": None,
                "crypto_to_paypal": None,
                "pkr_to_crypto": None,
                "crypto_to_pkr": None,
                "crypto_to_idr": None,
                "idr_to_crypto": None,
                "crypto_to_bdt": None,
                "bdt_to_crypto": None
            },
            "allowed_receiving_options": {
                "crypto": ["pkr", "paypal", "idr", "inr", "bdt"],
                "inr": ["crypto"],
                "paypal": ["crypto"],
                "pkr": ["crypto"],
                "idr": ["crypto"],
                "bdt": ["crypto"]
            }
        }

role_map_file = "database/rolemap.json"
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

def rolemapsave(config):
    os.makedirs(os.path.dirname(role_map_file), exist_ok=True)
    with open(role_map_file, "w") as file:
        json.dump(config, file, indent=4)

exchconfig = rolemap()  
def fukc(file_name="database/exchangedeals.json"):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file {file_name}.")
        return {}
    
EXCHANGE_CONFIG = load_config()
if not os.path.exists('tickets'):
    os.makedirs('tickets')

def load_state():
    if os.path.exists('database/state.json'):
        with open('database/state.json', 'r') as file:
            return json.load(file)
    return {}

def save_state(state):
    with open('database/state.json', 'w') as file:
        json.dump(state, file)

state = load_state()

def load_staff_data():
    try:
        with open("database/staff.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_staff_data(data):
    with open("database/staff.json", "w") as file:
        json.dump(data, file, indent=4)

def fukc(file_name="database/exchangedeals.json"):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file {file_name}.")
        return {}

def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as file:
        json.dump(config, file, indent=4)    

role_mapping = exchconfig.get("role_map", {})
admin = role_mapping.get("admin_id")
mmrole = role_mapping.get("mm_id")
majdur = role_mapping.get("staff")
exchrole = [
    role_mapping.get("crypto_exchanger"),
    role_mapping.get("paypal_exchanger"),
    role_mapping.get("inr_exchanger"),
    role_mapping.get("pkr_exchanger"),
    role_mapping.get("idr_exchanger"),
    role_mapping.get("bdt_exchanger")
]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}!")
    try:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Galaxy Exchanges"))
        print("[+] Status Set")
        bot.load_extension("cogs.staff")
        print("[+] Loaded staff.py")
        bot.load_extension("cogs.exchange")
        print("[+] Loaded exchange.py")
        bot.load_extension("cogs.admin")
        print("[+] Loaded admin.py")
        bot.load_extension("cogs.general")
        print("[+] Loaded general.py")
        bot.load_extension("cogs.events")
        print("[+] Loaded events.py")
    except Exception as e:
        print(f"Error loading Cogs: {e}")
    exchange_cog = bot.get_cog("MainCog")
    if exchange_cog:
        try:
            await exchange_cog.update_exchange_message()
        except Exception as e:
            print(f"Error updating exchange message: {e}")
    else:
        print("ExchangeBot Cog not found!")

'''@bot.command(pass_context=True)
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    #print(f'Ping {int(ping)}ms')'''

'''@bot.command()
async def d(ctx):
    channel = ctx.channel
    await channel.delete()'''
#category_id=1315684490324086845: str = None)
'''@bot.command()
async def fuk(ctx, cat: str):
    guild = ctx.guild
    category_id = int(cat)
    category = nextcord.utils.get(guild.categories, id=category_id)
    if category is None:
        await ctx.send(f"Category '{category}' not found.")
        return
    for channel in category.text_channels:
        try:
            await channel.delete()
            print(f"deleted {channel.name}")
        except nextcord.Forbidden:
            print(f"Permission error: Could not send message to {channel.name}")'''

@bot.slash_command(description="Setup you payment details")
async def setwallet(
    interaction: nextcord.Interaction, 
    ltcaddress: str = None, 
    paypal: str = None, 
    upi: str = None, 
    bdt: str = None, 
    idr: str = None, 
    pkr: str = None):
    if any(role.id == majdur for role in interaction.user.roles):
        try:
            user_id = str(interaction.user.id)
            ltc_data = load_walletdb()
            if user_id in ltc_data:
                del ltc_data[user_id]
                save_walletdb(ltc_data)
            if user_id not in ltc_data:
                ltc_data[user_id] = {}
            if ltcaddress:
                ltc_data[user_id]["ltc"] = ltcaddress
            if paypal:
                ltc_data[user_id]["paypal"] = paypal
            if upi:
                ltc_data[user_id]["upi"] = upi
            if bdt:
                ltc_data[user_id]["bdt"] = bdt
            if idr:
                ltc_data[user_id]["idr"] = idr
            if pkr:
                ltc_data[user_id]["pkr"] = pkr
            save_walletdb(ltc_data)
            embed = nextcord.Embed(
                description="<:check:1305951941423009803> Config Successful:",
                color=rang
            )
            if ltcaddress:
                embed.add_field(name="<a:ltc:1305940882582802472> LTC", value=ltcaddress, inline=False)
            if paypal:
                embed.add_field(name="<:PAYPAL:1308674173333409895> PayPal", value=paypal, inline=False)
            if upi:
                embed.add_field(name="<:INR:1308674301406482463> UPI", value=upi, inline=False)
            if bdt:
                embed.add_field(name="<:BDTTT:1315702666504048754> BDT", value=bdt, inline=False)
            if idr:
                embed.add_field(name="🇮🇩 IDR", value=idr, inline=False)
            if pkr:
                embed.add_field(name="<:pkr:1315703040875167744> PKR", value=pkr, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")
    else:
        await interaction.response.send_message("You Can't Use this Slash Cmd.", ephemeral=True) 

@bot.slash_command(description="Setup exchange panel")
async def setup(interaction: nextcord.Interaction, channel: nextcord.TextChannel):
    if any(role.id == admin for role in interaction.user.roles):
        state = load_state()
        if not isinstance(state, dict):
            state = {}
        state.setdefault('setup_channel_id', None)
        state.setdefault('setup_message_id', None)
        if state["setup_channel_id"] is not None:
            await interaction.response.send_message("The setup has already been completed in another channel.", ephemeral=True)
            return
        em = nextcord.Embed(color=rang)
        view = exchange.CurrencyExchangeView()
        em = nextcord.Embed(color=rang)
        em.set_image(url="https://media.discordapp.net/attachments/1314881227878174782/1315664991357108296/Purple_Aquamarine_Art_Pixel_Art_Discord_Profile_Banner_1.png?ex=67583c01&is=6756ea81&hm=5d36e392796ea18030809c15b19ba4cb2a31491f4f7f1fd22890ed423458bb93&=&format=webp&quality=lossless&width=412&height=165")
        await channel.send(embed=em)
        embed = nextcord.Embed(title=f"{name} Service", color=rang)#, url="")
        embed.add_field(name="<:exchange2:1314633645692026891> Exchanges <:exchange2:1314633645692026891>", value="""
<:INR:1308674301406482463> Crypto to INR 
<:b_:1315699244182540373> BELOW 50$ 87/$
<:b_:1315699244182540373> ABOVE 50$ 87.5/$

<:INR:1308674301406482463> INR To Crypto 
<:b_:1315699244182540373> 91/$ | ANY AMOUNT

<:Cryptotocrypto_official:1305994531585392692> Crypto to Crypto
<:b_:1315699244182540373> 3% | ANY AMOUNT

<:PAYPAL:1308674173333409895> PAYPAL TO CRYPTO
<:b_:1315699244182540373> 10% | ANY AMOUNT

<:PAYPAL:1308674173333409895> CRYPTO TO PAYPAL
<:b_:1315699244182540373> 1% | ANY AMOUNT""")
        embed.add_field(name="<:exchange2:1314633645692026891> Rate of Foreign Currency:", value="""
<:pkr:1315703040875167744>  Pkr to Crypto
<:b_:1315699244182540373> 293/$ | ANY AMOUNT

<:pkr:1315703040875167744>  Crypto to Pkr
<:b_:1315699244182540373> 278/$ | ANY AMOUNT

🇮🇩  Crypto to IDR
<:b_:1315699244182540373> 15100/$

🇮🇩  IDR to Crypto
<:b_:1315699244182540373>16000/$

<:BDTTT:1315702666504048754> Crypto to BDT
<:b_:1315699244182540373>124/$

<:BDTTT:1315702666504048754> BDT to Crypto
<:b_:1315699244182540373>129/$
    """, inline=False)
        embed.set_thumbnail(url=bot_thumbnail)
        setup_message = await channel.send(embed=embed, view=view)
        state["setup_channel_id"] = channel.id
        state["setup_message_id"] = setup_message.id
        save_state(state)
        await interaction.response.send_message(f"Setup message has been sent in {channel.mention}.", ephemeral=True)
    else:
        await interaction.response.send_message("You Can't Use this Slash Cmd.", ephemeral=True) 
        
@bot.slash_command(description="unsetups exchange panel")
async def unsetup(interaction: nextcord.Interaction):
    if any(role.id == admin for role in interaction.user.roles):
        if os.path.exists('database/state.json'):
            with open('database/state.json', 'r') as file:
                state = json.load(file)
            state.pop('setup_channel_id', None)
            state.pop('setup_message_id', None)
            save_state(state)
            await interaction.response.send_message("Setup channel and message IDs have been removed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("No state.json file found.", ephemeral=True)
    else:
        await interaction.response.send_message("You Can't Use this Slash Cmd.", ephemeral=True) 

@bot.slash_command(description="Setup Exchange category")
async def csetup(
    interaction: nextcord.Interaction,
    category: str = SlashOption(description="Select an exchange category", choices=[
        "crypto2inr", "inr2crypto", "crypto2crypto", "paypal2crypto", "crypto2paypal", "pkr2crypto", "crypto2pkr", "crypto2idr", "idr2crypto", "crypto2bdt", "bdt2crypto"
    ]),
    category_id: str = SlashOption(description="Enter the category ID")
):
    if any(role.id == admin for role in interaction.user.roles):
        try:
            category_id = int(category_id)
        except ValueError:
            await interaction.response.send_message("Invalid category ID format. Please provide a valid category ID.", ephemeral=True)
            return

        category_key_map = {
            "crypto2inr": "crypto_to_inr",
            "inr2crypto": "inr_to_crypto",
            "crypto2crypto": "crypto_to_crypto",
            "paypal2crypto": "paypal_to_crypto",
            "crypto2paypal": "crypto_to_paypal",
            "pkr2crypto": "pkr_to_crypto",
            "crypto2pkr": "crypto_to_pkr",
            "crypto2idr": "crypto_to_idr",
            "idr2crypto": "idr_to_crypto",
            "crypto2bdt": "crypto_to_bdt",
            "bdt2crypto": "bdt_to_crypto"
        }

        if category not in category_key_map:
            await interaction.response.send_message("Invalid category selection. Please choose a valid exchange category.", ephemeral=True)
            return

        category_key = category_key_map[category]
        EXCHANGE_CONFIG["category_mapping"][category_key] = category_id
        save_config(EXCHANGE_CONFIG)
        await interaction.response.send_message(embed=nextcord.Embed(description=f"{tick} | Successfully stored Category ID for '{category}'."), ephemeral=True)
    else:
        await interaction.response.send_message("You Can't Use this Slash Cmd.", ephemeral=True) 

@bot.slash_command(description="Setup Exchangers Role")
async def rsetup(
    interaction: Interaction,
    role: str = SlashOption(
        description="Select an exchange category",
        choices=[
            "Crypto Exchanger",
            "Paypal Exchanger",
            "INR Exchanger",
            "PKR Exchanger",
            "IDR Exchanger",
            "BDT Exchanger",
            "Middle Man",
            "Admin",
            "Staff"
        ]
    ),
    role_id: str = SlashOption(description="Enter the category ID")
):
    if any(role.id == admin for role in interaction.user.roles):
        try:
            role_id = int(role_id) 
        except ValueError:
            await interaction.response.send_message(
                "Invalid category ID format. Please provide a valid integer ID.",
                ephemeral=True
            )
            return
        randmap = {
            "Crypto Exchanger": "crypto_exchanger",
            "Paypal Exchanger": "paypal_exchanger",
            "INR Exchanger": "inr_exchanger",
            "PKR Exchanger": "pkr_exchanger",
            "IDR Exchanger": "idr_exchanger",
            "BDT Exchanger": "bdt_exchanger",
            "Middle Man": "mm_id",
            "Admin": "admin_id",
            "Staff": "staff"
        }

        if role not in randmap:
            await interaction.response.send_message(
                "Invalid category selection. Please choose a valid exchange category.",
                ephemeral=True
            )
            return
        role_key = randmap[role]
        exchconfig["role_map"][role_key] = role_id
        rolemapsave(exchconfig)
        await interaction.response.send_message(embed=nextcord.Embed(description=f"{tick} | Successfully stored role id of {role} in DB.", ephemeral=True))
    else:
        await interaction.response.send_message("You Can't Use this Slash Cmd.", ephemeral=True) 

@bot.command()
async def help(ctx, helpcategory="none"):
    guild = ctx.guild
    helpcategory = helpcategory.lower().replace("[", "").replace("]", "")
    eheh = bot.commands
    fuk = len(eheh)
    timestamp = datetime.utcnow().strftime('%H:%M:%S')
    if helpcategory == "none":
        embed = nextcord.Embed(
            title="Help Command Overview :",
            description=f"```The prefix for this server is {prefix}\nType {prefix}help <category>```", color=0x2B2D31)
        embed.add_field(name="Category", value="""
        <:settings:1306221127126880256> `:` System
        <:HeadMod:1306221130654154796> `:` Admins
        <:MOD:1308128124172500992> `:` Mods
        <:head_mod:1315773327444279427> `:` Staff
        <:Crypto_Exchange:1306307580687028345> `:` Crypto
        <:Members:1305993106457497612> `:` Clients""", inline=False)
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"Requested by {ctx.author.name} | {timestamp}", icon_url=f"{ctx.author.avatar.url}")
    elif "system" in helpcategory:
        embed = nextcord.Embed(
        title="<:settings:1306221127126880256> System Cmds",
        description=f"""
{prefix}help
{prefix}ping
{prefix}uptime
{prefix}restart
{prefix}shutdown
        """, color=0x2B2D31)
        embed.set_thumbnail(url=bot_thumbnail)
        embed.set_footer(text=f"Requested by {ctx.author.name} | {timestamp}", icon_url=f"{ctx.author.avatar.url}")
    elif "staff" in helpcategory:
        embed = nextcord.Embed(
        title="<:settings:1306221127126880256> Staff Cmds",
        description=f"""
<:SlashCommand:1315825649188999249> Slash Cmds:    
`/setwallet` | set staff's wallet info
`/login`     | backup cmd for staff
<:imagec:1315825552363622461> Cmds:
`{prefix}done`        | Confirms a exchange deal
`{prefix}ticketinfo`  | Shows info of exchange ticket
`{prefix}a2t @member` | Add a member to ticket
`{prefix}rft @member` | Removes a member from ticket
`{prefix}claim`       | claims ticket for middleman
`{prefix}reclaim`     | reclaims a ticket after exchanger unclaims it
`{prefix}umclaim`     | unclaims ticket
`{prefix}wallet`      | Shows wallet info
`{prefix}bal <addy>`  | Shows given addy's bal
`{prefix}mybal <addy>`| Shows your wallet bal
        """, color=0x2B2D31)
        embed.set_thumbnail(url=bot_thumbnail)
        embed.set_footer(text=f"Requested by {ctx.author.name} | {timestamp}", icon_url=f"{ctx.author.avatar.url}")
    elif "admins" in helpcategory:
        embed = nextcord.Embed(
        title="<:settings:1306221127126880256> Admins Cmds",
        description=f"""
<:SlashCommand:1315825649188999249> Slash Cmds:        
/setup
/unsetup
/csetup
/rsetup
/vanityrole
<:imagec:1315825552363622461> Cmds:    
{prefix}staff @member
{prefix}rstaff @member

        """, color=0x2B2D31)
        embed.set_thumbnail(url=bot_thumbnail)
        embed.set_footer(text=f"Requested by {ctx.author.name} | {timestamp}", icon_url=f"{ctx.author.avatar.url}") 
    elif "mods" in helpcategory:
        embed = nextcord.Embed(
        title="<:settings:1306221127126880256> Mods Cmds",
        description=f"""
{prefix}ban @member
{prefix}unban @member
{prefix}timeout @member
{prefix}untimeout @member
{prefix}unbanall
{prefix}roleall
        """, color=0x2B2D31)
        embed.set_thumbnail(url=bot_thumbnail)
        embed.set_footer(text=f"Requested by {ctx.author.name} | {timestamp}", icon_url=f"{ctx.author.avatar.url}")       
    '''elif "admins" in helpcategory:
    elif "mods" in helpcategory:
    elif "crypto" in helpcategory: 
    elif "clients" in helpcategory: 
    elif "exchangers" in helpcategory:   '''                     
    await ctx.send(embed=embed)

keep_alive()
async def main():
  #await load()
  await bot.start(tkn)
asyncio.run(main())
