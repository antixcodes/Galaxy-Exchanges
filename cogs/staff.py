import nextcord, requests, string
from nextcord.ext import commands
from nextcord.ui import View, Select
from nextcord.ui import Button, View
import random, asyncio, json, os, re, qrcode, io
from dhooks import Webhook
from googletrans import Translator, LANGUAGES
translator = Translator()
from typing import Optional
import io
from chat_exporter.construct.transcript import Transcript
from chat_exporter.ext.discord_import import discord
from chat_exporter.construct.attachment_handler import AttachmentHandler

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
claimed_channels = {}
#######################################################3
VOUCHES_FILE = "database/vouches.json"

if not os.path.exists(VOUCHES_FILE):
    with open(VOUCHES_FILE, 'w') as f:
        json.dump({}, f) 

def load_walletdb():
    try:
        with open('database\wallet.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  
    
def save_walletdb(data):
    with open('database\wallet.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_state():
    if os.path.exists('database\state.json'):
        with open('database\state.json', 'r') as file:
            return json.load(file)
    return {}

def save_state(state):
    with open('database\state.json', 'w') as file:
        json.dump(state, file)

def exchangedeal(ticket_channel_id, nom, sendingcurrency, receivingcurrency, file_name="database\exchangedeals.json"):
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

CONFIG_FILE_PATH = "database\categorydb.json"
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
def fukc(file_name="database\exchangedeals.json"):
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
    if os.path.exists('database\state.json'):
        with open('database\state.json', 'r') as file:
            return json.load(file)
    return {}

def save_state(state):
    with open('database\state.json', 'w') as file:
        json.dump(state, file)

state = load_state()

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

def fukc(file_name="database\exchangedeals.json"):
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
    
with open('config.json', 'r') as f:
    config = json.load(f)
rang = config['rang'] 
name = config['embedname']

BLOCKCHAIN_API_URL = "https://api.blockcypher.com/v1/ltc/main/txs/"
BLOCKCHAIN_API_KEY = "1e79c185c3824cc79bf354c0ff13f8a9"
PRICE_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"

class ConfirmationView(nextcord.ui.View):
    def __init__(self, client_id):
        super().__init__(timeout=None)
        self.client_id = int(client_id)
        self.confirmed = False
        self.confirmed_by = None
        self.interaction_completed = asyncio.Event()
    @nextcord.ui.button(label="Confirm Deal", style=nextcord.ButtonStyle.grey)
    async def confirm_deal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.client_id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
        self.confirmed = True
        self.confirmed_by = interaction.user
        await interaction.response.send_message("Deal confirmed!", ephemeral=True)
        button.disabled = True
        for item in self.children:
            if isinstance(item, nextcord.ui.Button):
                item.disabled = True
        await interaction.message.edit(view=self)
        self.interaction_completed.set()
    @nextcord.ui.button(label="Cancel Deal", style=nextcord.ButtonStyle.grey)
    async def cancel_deal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.client_id:
            await interaction.response.send_message("You cannot use this button.", ephemeral=True)
            return
        await interaction.response.send_message("Deal cancelled.", ephemeral=True)
        button.disabled = True
        for item in self.children:
            if isinstance(item, nextcord.ui.Button):
                item.disabled = True
        await interaction.message.edit(view=self)
        self.interaction_completed.set()  


role_mapping = exchconfig.get("role_map", {})
admin = role_mapping.get("admin_id")
mmrole = role_mapping.get("mm_id")
majdur = role_mapping.get("staff")
exchrole = 1315652262210830420

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reclaim(self, ctx):
        if any(role.id == exchrole for role in ctx.author.roles):
            channel_id = str(ctx.channel.id)
            channel = ctx.guild.get_channel(int(channel_id))
            data = fukc()
            if channel_id in data:
                ticket_info = data[channel_id][0]
                name = ticket_info.get("name")
                if "exchanger" in ticket_info:
                    await ctx.send("This ticket is already claimed.")
                else:
                    ticket_info["exchanger"] = ctx.author.id
                    ticket_name = f"claimed-by-{ctx.author.name.replace(' ', '_')}・{name}"
                    if channel:
                        print(f"Channel found: {channel.name}")
                        await channel.edit(name=ticket_name)
                    else:
                        await ctx.send("Channel not found")
                    try:
                        with open('database/exchangedeals.json', 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        await ctx.send(f"Ticket successfully claimed by {ctx.author.mention}.")
                    except Exception as e:
                        await ctx.send(f"An error occurred while saving the data: {str(e)}")
            else:
                await ctx.send("Ticket ID not found in the database.")

    @commands.command()
    async def transcript(self, ctx: commands.Context, limit: Optional[int] = None, tz_info="UTC", military_time=True, fancy_times=True):
        if any(role.id == exchrole for role in ctx.author.roles):
            channel = ctx.channel
            channel_id = str(ctx.channel.id)
            edit = await ctx.send("Generating Transcript <a:load:1305941958967169054>")
            if os.path.exists('database/exchangedeals.json'):
                try:
                    with open('database/exchangedeals.json', 'r') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}
            if channel_id not in data:
                await ctx.send(f"No data found for channel ID: {channel_id}")
                return
            deal = data[channel_id][0]
            sendingcurrency = deal.get("sendingcurrency")
            receivingcurrency = deal.get("receivingcurrency")
            amount = deal.get("amount")
            exchanger = deal.get("exchanger")
            client = deal.get("client")
            user = bot.get_user(client)
            transcript = (await Transcript(
                channel=channel,
                limit=limit,
                messages=None,
                pytz_timezone=tz_info,
                military_time=military_time,
                fancy_times=fancy_times,
                before=None,
                after=None,
                support_dev=False,
                bot=bot,
                attachment_handler=None
            ).export()).html

            if not transcript:
                await ctx.send("Error: Could not generate the transcript.")
                return
            transcript = re.sub(r"<!--.*?-->", "", transcript, flags=re.DOTALL)
            transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html")
            await ctx.send("Transcript saved to transcript logs")
            message = await ctx.send(file=transcript_file)
            transcript_link = f"https://mahto.id/chat-exporter?url={message.attachments[0].url}"
            embed = discord.Embed()
            if user is None:
                await ctx.send("Could not find the user. Please make sure the client ID is correct.")
                return
            embed.add_field(name="Ticket Owner", value=f"{user.mention}", inline=False)
            embed.add_field(name="Ticket Name", value=f"{channel.name}", inline=False)
            embed.add_field(name="Exchange Of", value=f"{sendingcurrency} To {receivingcurrency}", inline=False)
            embed.add_field(name="Exchanger ID", value=f"{exchanger}", inline=False)
            embed.add_field(name="Amount", value=f"{amount}", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=f"{user.name}", icon_url=f"{ctx.author.avatar.url}")
            button = discord.ui.Button(label="Direct Link", style=discord.ButtonStyle.link, url=f"{transcript_link}")
            view = discord.ui.View()
            view.add_item(button)
            embed.add_field(name="Download Transcript", value=f"[Click Here to Download]({transcript_link})", inline=False)
            try:
                await user.send(embed=embed, view=view)
                await edit.edit(f"Transcript successfully sent to {user.mention}")
            except discord.Forbidden:
                await ctx.send(f"Could not send a DM to {user.mention}. They may have DMs disabled.")

    @commands.command()
    async def close(self, ctx):
        if any(role.id == exchrole for role in ctx.author.roles):
            channel_id = str(ctx.channel.id)
            data = fukc()
            if channel_id in data:
                ticket_info = data[channel_id][0]
                exchanger_id = ticket_info.get("exchanger")
                if exchanger_id:
                    ticket_info.pop("exchanger", None)
                    sendingcurrency = ticket_info.get("sendingcurrency")
                    receivingcurrency = ticket_info.get("receivingcurrency")
                    name = ticket_info.get("name")
                    ticket_name = f"{sendingcurrency}2{receivingcurrency}・{name}"
                    channel = ctx.guild.get_channel(int(channel_id))
                    if channel:
                        try:
                            await channel.edit(name=ticket_name)
                            await ctx.send(f"Channel {channel.mention} has been renamed to {ticket_name}.")
                            with open('database/exchangedeals.json', 'w') as f:
                                json.dump(data, f, indent=4)
                        except Exception as e:
                            await ctx.send(f"An error occurred while renaming the channel or saving data: {str(e)}")
                    else:
                        await ctx.send("Channel not found.")
                else:
                    await ctx.send("This ticket is not claimed (no exchanger ID).")
            else:
                await ctx.send("Ticket ID not found in the database.")
        else:
            return
        
    @commands.command()
    async def unclaim(self, ctx):
        if any(role.id == exchrole for role in ctx.author.roles):
            channel_id = str(ctx.channel.id)
            data = fukc()
            if channel_id in data:
                ticket_info = data[channel_id][0]
                exchanger_id = ticket_info.get("exchanger")
                if exchanger_id:
                    ticket_info.pop("exchanger", None)
                    sendingcurrency = ticket_info.get("sendingcurrency")
                    receivingcurrency = ticket_info.get("receivingcurrency")
                    name = ticket_info.get("name")
                    ticket_name = f"{sendingcurrency}2{receivingcurrency}・{name}"
                    channel = ctx.guild.get_channel(int(channel_id))
                    if channel:
                        try:
                            await channel.edit(name=ticket_name)
                            await ctx.send(f"Channel {channel.mention} has been renamed to {ticket_name}.")
                            with open('database/exchangedeals.json', 'w') as f:
                                json.dump(data, f, indent=4)
                        except Exception as e:
                            await ctx.send(f"An error occurred while renaming the channel or saving data: {str(e)}")
                    else:
                        await ctx.send("Channel not found.")
                else:
                    await ctx.send("This ticket is not claimed (no exchanger ID).")
            else:
                await ctx.send("Ticket ID not found in the database.")
        else:
            return
        
    @commands.command()
    async def remind(self, ctx, user: nextcord.User, time: str, *, note="None"):
        if any(role.id == exchrole for role in ctx.author.roles):
            time_multipliers = {"s": 1, "m": 60, "h": 3600}
            unit = time[-1]
            if unit not in time_multipliers:
                await ctx.send("Invalid time format. Use 's', 'm', 'h'.")
                return
            try:
                duration = int(time[:-1]) * time_multipliers[unit]
            except ValueError:
                await ctx.send("Invalid time format.")
                return
            embed = nextcord.Embed(color=0x00FF00)
            embed.add_field(name=f"Reminder set for {user.display_name}", value=f"Time: {time}\nNote: {note}.")
            embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "")
            await ctx.send(embed=embed)
            await asyncio.sleep(duration)
            embed = nextcord.Embed(title="<a:alert:1316152948560101509> Reminder!", color=0xFF0000)
            embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
            embed.add_field(name="Note", value=note, inline=False)
            try:
                await user.send(embed=embed)
                await ctx.send(f"{user.mention} has been reminded via DM.")
            except nextcord.Forbidden:
                await ctx.send(f"Unable to send a DM to {user.mention}.")
        else:
            return
        
    @commands.command()
    async def claim(self, ctx):
        if any(role.id == mmrole for role in ctx.author.roles):
            member = ctx.author
            role_mapping = exchconfig.get("role_map", {})
            role_key = "mm_id"
            role_id = role_mapping.get(role_key)
            middleman_role = nextcord.utils.get(ctx.guild.roles, id=role_id)
            if middleman_role not in member.roles:
                await ctx.send("You need the middleman role to claim this ticket!")
                return
            ticket_channel = ctx.channel
            if ticket_channel.id in claimed_channels:
                await ctx.send(nextcord.Embed(description=f"MM for this ticket is {claimed_channels[ticket_channel.id]}.", color=0x00FF00))
                return
            claimed_channels[ticket_channel.id] = member.mention
            await ticket_channel.set_permissions(middleman_role, view_channel=True, read_message_history=True, send_messages=True)
            await ticket_channel.set_permissions(member, view_channel=True, read_message_history=True, send_messages=True)
            await ticket_channel.set_permissions(middleman_role, overwrite=None)
            await ctx.send(f"{member.mention} has successfully claimed the ticket!")
        else:
            return
        
    @commands.command(aliases=["ts"])
    async def translate(self, ctx):
        if any(role.id == majdur or exchrole for role in ctx.author.roles):
            try:
                if ctx.message.reference:
                    referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                    translation = translator.translate(referenced_message.content, dest='en')
                    await ctx.reply(f"**Translated**: {translation.text}")
                else:
                    await ctx.reply("You need to reply to a message to translate it.")
            except Exception as e:
                await ctx.send("Sorry, something went wrong with the translation.")
                print(e)
        else:
            return
        
    @commands.command()
    async def txid(self, ctx, txid: str):
        if any(role.id == majdur for role in ctx.author.roles):
            try:
                response = requests.get(f"{BLOCKCHAIN_API_URL}{txid}?token={BLOCKCHAIN_API_KEY}")
                if response.status_code != 200:
                    await ctx.send("Could not fetch transaction information. Please check the TXID.")
                    return
                tx_data = response.json()
                inputs = tx_data.get("inputs", [])
                outputs = tx_data.get("outputs", [])
                input_addresses = [inp["addresses"] for inp in inputs if "addresses" in inp]
                segwit_output_addresses = [
                    out["addresses"] for out in outputs if "addresses" in out and out["addresses"][0].startswith('ltc1')
                ]
                total_sent_ltc = sum(out["value"] for out in outputs) / 1e8
                price_response = requests.get(PRICE_API_URL)
                if price_response.status_code != 200:
                    await ctx.send("Could not fetch Litecoin price. Try again later.")
                    return
                ltc_price_usd = price_response.json()["litecoin"]["usd"]
                total_sent_usd = total_sent_ltc * ltc_price_usd
                embed = nextcord.Embed(color=rang)
                embed.add_field(name="<:linked:1305952731072168007> Transaction ID", value=txid, inline=False)
                embed.add_field(
                    name="<:Cryptotocrypto_official:1305994531585392692> Total Sent", 
                    value=f"Total LTC: {total_sent_ltc:.8f} LTC\nTotal USD: {total_sent_usd:.2f} USD", 
                    inline=False
                )
                embed.add_field(
                    name="<:remove:1315770686181998734> From Address",
                    value="\n".join(addr[0] for addr in input_addresses),
                    inline=False,
                )
                if segwit_output_addresses:
                    embed.add_field(
                        name="<:Add:1315769240724443186> To Address",
                        value="\n".join(addr[0] for addr in segwit_output_addresses),
                        inline=False,
                    )
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            return
        
    @commands.command(aliases=['bal', 'ltcbal'])
    async def getbal(self, ctx, ltcaddress):
        if any(role.id == majdur for role in ctx.author.roles):
            try:
                response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
                if response.status_code == 200:
                    data = response.json()
                    balance = data['balance'] / 10**8  
                    total_balance = data['total_received'] / 10**8
                    unconfirmed_balance = data['unconfirmed_balance'] / 10**8
                else:
                    await ctx.send("Failed to retrieve balance. Please check the Litecoin address.")
                    return
                cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
                if cg_response.status_code == 200:
                    usd_price = cg_response.json()['litecoin']['usd']
                else:
                    await ctx.send("Failed to retrieve the current price of Litecoin.")
                    return
                usd_balance = balance * usd_price
                usd_total_balance = total_balance * usd_price
                usd_unconfirmed_balance = unconfirmed_balance * usd_price
                embed = nextcord.Embed(
                    title="<a:ltc:1305940882582802472> WALLET INFO <a:ltc:1305940882582802472>", 
                    color=rang
                )
                embed.add_field(name="<:LTC:1305994660073963530> Litecoin Address", value=f'`{ltcaddress}`', inline=False)
                embed.add_field(name="<:prices:1305942191629271120> Current Balance", value=f"${usd_balance:.2f} USD", inline=False)
                embed.add_field(name="<:Cryptotocrypto_official:1305994531585392692> Total LTC Received", value=f"${usd_total_balance:.2f} USD", inline=False)
                embed.add_field(name="<a:load:1305941958967169054> Unconfirmed Balance", value=f"${usd_unconfirmed_balance:.2f} USD", inline=False)
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            return
          
    @commands.command()
    async def mybal(self, ctx):
        if any(role.id == majdur for role in ctx.author.roles):
            user_id = str(ctx.author.id)
            ltc_data = load_walletdb()
            if user_id not in ltc_data:
                await ctx.send("You have not set a Litecoin address yet. Please use `/setltc` to set one.")
                return
            ltcaddress = ltc_data[user_id]["ltc"]
            response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

            if response.status_code == 200:
                data = response.json()
                balance = data['balance'] / 10**8
                total_balance = data['total_received'] / 10**8
                unconfirmed_balance = data['unconfirmed_balance'] / 10**8
            else:
                await ctx.send("Failed to retrieve balance. Please check your Litecoin address.")
                return

            cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

            if cg_response.status_code == 200:
                usd_price = cg_response.json()['litecoin']['usd']
            else:
                await ctx.send("Failed to retrieve the current price of Litecoin.")
                return

            usd_balance = balance * usd_price
            usd_total_balance = total_balance * usd_price
            usd_unconfirmed_balance = unconfirmed_balance * usd_price

            embed = nextcord.Embed(title="<a:ltc:1305940882582802472> WALLET INFO <a:ltc:1305940882582802472>", color=0x3498db)
            embed.add_field(name="<:LTC:1305994660073963530> Litecoin Address", value=f'`{ltcaddress}`', inline=False)
            embed.add_field(name="<:prices:1305942191629271120> Current Balance", value=f"${usd_balance:.2f} USD", inline=False)
            embed.add_field(name="<:Cryptotocrypto_official:1305994531585392692> Total LTC Received", value=f"${usd_total_balance:.2f} USD", inline=False)
            embed.add_field(name="<a:load:1305941958967169054> Unconfirmed Balance", value=f"${usd_unconfirmed_balance:.2f} USD", inline=False)

            await ctx.send(embed=embed)
        else:
            return
        
    @commands.command()
    async def addy(self, ctx):
        if any(role.id == majdur for role in ctx.author.roles):
            user_id = str(ctx.author.id)
            ltc_data = load_walletdb()
            if user_id not in ltc_data:
                await ctx.send("You have not set a Litecoin address yet. Please use `/setltc` to set one.")
                return

            ltcaddress = ltc_data[user_id]["ltc"]
            qr_data = f"litecoin:{ltcaddress}"
            qr = qrcode.make(qr_data)
            img_byte_arr = io.BytesIO()
            qr.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            embed = nextcord.Embed(
                description=f"{ctx.author.mention} | LTC Info",
                color=0x3498db
            )
            embed.set_footer(text="Your Wallet Details", icon_url=ctx.author.avatar.url)
            embed.add_field(name="Litecoin Address", value=f"```{ltcaddress}```", inline=False)

            copy_button = Button(label="Copy Address", style=nextcord.ButtonStyle.gray)
            scanner_button = Button(label="QR Code", style=nextcord.ButtonStyle.gray)

            async def copy(interaction: nextcord.Interaction):
                await interaction.response.send_message(content=f"{ltcaddress}", ephemeral=True)

            async def scanner(interaction: nextcord.Interaction):
                file = nextcord.File(img_byte_arr, filename="qr.png")
                qr_embed = nextcord.Embed(
                    title=f"{ctx.author.display_name}'s QR Code",
                    description="Scan this QR code to access the Litecoin address.",
                    color=0x3498db
                )
                qr_embed.set_image(url=f"attachment://qr.png")
                await interaction.response.send_message(embed=qr_embed, file=file, ephemeral=True)

            copy_button.callback = copy
            scanner_button.callback = scanner

            view = View()
            view.add_item(copy_button)
            view.add_item(scanner_button)

            await ctx.send(embed=embed, view=view)
        else:
            return
        
    @commands.command()
    async def upi(self, ctx):
        if any(role.id == majdur for role in ctx.author.roles):
            user_id = str(ctx.author.id)
            ltc_data = load_walletdb()

            if user_id not in ltc_data:
                await ctx.send("You have not set a Litecoin address yet. Please use `/setltc` to set one.")
                return

            upi_addy = ltc_data[user_id]
            ltcaddress = ltc_data[user_id]

            qr_data = f"litecoin:{ltcaddress}"
            qr = qrcode.make(qr_data)
            ltc_qr_buffer = io.BytesIO()
            qr.save(ltc_qr_buffer, format='PNG')
            ltc_qr_buffer.seek(0)

            uqr_data = f"upi://pay?pa={upi_addy}"
            uqr = qrcode.make(uqr_data)
            upi_qr_buffer = io.BytesIO()
            uqr.save(upi_qr_buffer, format='PNG')
            upi_qr_buffer.seek(0)

            embed = nextcord.Embed(
                description=f"{ctx.author.mention} | UPI Info",
                color=0x3498db
            )
            embed.set_footer(text="Your Wallet Details", icon_url=ctx.author.avatar.url)
            embed.add_field(name="Litecoin Address", value=f"```{ltcaddress}```", inline=False)
            copy_button = Button(label="Copy Address", style=nextcord.ButtonStyle.gray)
            scanner_button = Button(label="UPI QR", style=nextcord.ButtonStyle.gray)

            async def copy(interaction: nextcord.Interaction):
                await interaction.response.send_message(content=f"{upi_addy}", ephemeral=True)

            async def scanner(interaction: nextcord.Interaction):
                file = nextcord.File(upi_qr_buffer, filename="upi_qr.png")
                qr_embed = nextcord.Embed(
                    title=f"{ctx.author.display_name}'s UPI QR Code",
                    description="Scan this QR code to access the UPI address.",
                    color=0x3498db
                )
                qr_embed.set_image(url="attachment://upi_qr.png")
                await interaction.response.send_message(embed=qr_embed, file=file, ephemeral=True)

            copy_button.callback = copy
            scanner_button.callback = scanner

            view = View()
            view.add_item(copy_button)
            view.add_item(scanner_button)

            await ctx.send(embed=embed, view=view)
        else:
            return

    @commands.command()
    async def done(self, ctx: commands.Context, limit: Optional[int] = None, tz_info="UTC", military_time=True, fancy_times=True):
        if any(role.id == exchrole for role in ctx.author.roles):
            channel = ctx.channel
            await ctx.message.delete()
            channel_id = str(ctx.channel.id)
            if os.path.exists('database/exchangedeals.json'):
                try:
                    with open('database/exchangedeals.json', 'r') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}

            if channel_id not in data:
                await ctx.send(f"No data found for channel ID: {channel_id}")
                return

            deal = data[channel_id][0]
            sendingcurrency = deal.get("sendingcurrency")
            receivingcurrency = deal.get("receivingcurrency")
            amount = deal.get("amount")
            exchanger = deal.get("exchanger")
            client = deal.get("client")

            embed = discord.Embed(
                title="Deal Pending Confirmation",
                description=f"<@{client}>, only click Confirm once you have received the funds!",
                color=0x00FF00
            )
            embed.add_field(name="Exchanger", value=f"<@{exchanger}>", inline=False)
            embed.add_field(name="Amount", value=f"{amount}", inline=False)
            embed.add_field(name="Deal Details", value=f"{sendingcurrency}2{receivingcurrency}", inline=False)

            confirmation_view = ConfirmationView(client)
            await ctx.send(embed=embed, view=confirmation_view)
            await confirmation_view.interaction_completed.wait()

            if confirmation_view.confirmed:
                try:
                    await ctx.send(f"Deal confirmed! Amount: `{amount}`. Thank you.")
                    sax = await ctx.send(f"+rep {exchanger} LEGIT | EXCHANGED {sendingcurrency} TO {receivingcurrency} [ {amount} ] • TYSM")
                    await sax.reply(f"Vouch please <@{client}>")
                    user = ctx.guild.get_member(client)  
                    if user is None:
                        await ctx.send("Could not find the user. Please make sure the client ID is correct.")
                        return
                    edit_message = await ctx.send("Generating Transcript <a:load:1305941958967169054>")
                    try:
                        transcript_data = await Transcript(
                            channel=channel,
                            limit=limit,
                            messages=None,
                            pytz_timezone=tz_info,
                            military_time=military_time,
                            fancy_times=fancy_times,
                            before=None,
                            after=None,
                            support_dev=False,
                            bot=self.bot,
                            attachment_handler=None
                        ).export()
                    except Exception as e:
                        await edit_message.edit(content=f"Transcript generation failed: {str(e)}")
                        return

                    if not transcript_data or not transcript_data.html:
                        await edit_message.edit(content="Error: Could not generate the transcript.")
                        return

                    transcript = re.sub(r"<!--.*?-->", "", transcript_data.html, flags=re.DOTALL)
                    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html")
                    message = await ctx.send(file=transcript_file)
                    transcript_link = f"https://mahto.id/chat-exporter?url={message.attachments[0].url}"
                    embed = discord.Embed()
                    embed.add_field(name="Ticket Owner", value=f"{user.mention}", inline=False)
                    embed.add_field(name="Ticket Name", value=f"{channel.name}", inline=False)
                    embed.add_field(name="Exchange Of", value=f"{sendingcurrency} To {receivingcurrency}", inline=False)
                    embed.add_field(name="Exchanger ID", value=f"{exchanger}", inline=False)
                    embed.add_field(name="Amount", value=f"{amount}", inline=False)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    embed.set_footer(text=f"{user.name}", icon_url=ctx.author.avatar.url)
                    button = discord.ui.Button(label="Direct Link", style=discord.ButtonStyle.link, url=transcript_link)
                    view = discord.ui.View()
                    view.add_item(button)
                    adminrole = ctx.guild.get_role(1317225312031084634)
                    client_role = ctx.guild.get_role(1315652271048101930)
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        adminrole: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True, read_message_history=True)
                    }
                    await channel.edit(name="Close")
                    if client_role:
                        await user.add_roles(client_role)
                    try:
                        await user.send(embed=embed, view=view)
                        em = discord.Embed()
                        em.add_field(name="Ticket Owner", value=f"{user.mention}", inline=False)
                        em.add_field(name="Ticket Name", value=f"{channel.name}", inline=False)
                        em.add_field(name="Exchange Of", value=f"{sendingcurrency} To {receivingcurrency}", inline=False)
                        em.add_field(name="Exchanger ID", value=f"{exchanger}", inline=False)
                        em.add_field(name="Amount", value=f"{amount}", inline=False)
                        em.add_field(name="Ticket Link", value=f"[Direct Link]({transcript_link})")
                        em.set_thumbnail(url=ctx.guild.icon.url)
                        trans_logs.send(embed=em)#, file=transcript_file)
                        await edit_message.edit(content=f"Transcript successfully sent to {user.mention}")
                    except discord.Forbidden:
                        await ctx.send(f"Could not send a DM to {user.mention}. They may have DMs disabled.")
                    data.pop(channel_id, None)
                    with open('database/exchangedeals.json', 'w') as f:
                        json.dump(data, f, indent=4)

                except Exception as e:
                    await ctx.send(f"An error occurred while processing the deal: {str(e)}")
            else:
                await ctx.send("Deal was canceled by the user.")
        else:
            return

        
    @commands.command()
    async def ticketinfo(self, ctx, channel_id: str = None):
        if any(role.id == majdur for role in ctx.author.roles):
            if channel_id is None:
                channel_id = str(ctx.channel.id)
            try:
                data = fukc() 
                if channel_id in data:
                    deal = data[channel_id][0]
                    sendingcurrency = deal.get("sendingcurrency")
                    receivingcurrency = deal.get("receivingcurrency")
                    nom = deal.get("name")
                    exchanger = deal.get("exchanger")
                    amount = deal.get("amount")

                    embed = discord.Embed(color=rang)
                    embed.add_field(name="<:TextChannel:1317199100604715030> Channel ID", value=f"```{channel_id}```", inline=True)
                    embed.add_field(name="<:memberblack:1317198609112109056> Client", value=f"```{nom}```", inline=True)
                    embed.add_field(name="<:exchange2:1314633645692026891> Exchanger", value=f"<@{exchanger}>", inline=True)
                    embed.add_field(name="<:payy:1317198611188285552> Amount", value=f"```{amount}$```", inline=True)
                    embed.add_field(name="<:remove:1315770668868046889> Sending", value=f"```{sendingcurrency}```", inline=True)
                    embed.add_field(name="<:Add:1315769240724443186> Receiving", value=f"```{receivingcurrency}```", inline=True)
                    embed.set_footer(text=f"{name} | MM | Exchange")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"No data found for channel ID: {channel_id}")

            except FileNotFoundError:
                await ctx.send("The file `exchangedeals.json` was not found.")
            except json.JSONDecodeError:
                await ctx.send("There was an error decoding the JSON file.")
            except Exception as e:
                await ctx.send(f"An unexpected error occurred: {e}")
        else:
            return
            
    @commands.command()
    async def wallet(self, ctx):
        if any(role.id == majdur for role in ctx.author.roles):
            user_id = str(ctx.author.id)
            ltc_data = load_walletdb()
            if user_id not in ltc_data:
                await ctx.send("You have not set a Litecoin address yet. Please use `/setwallet` to set one.")
                return

            user_info = ltc_data[user_id]
            upi_addy = user_info.get("upi", "Not Set")
            paypal_addy = user_info.get("paypal", "Not Set")
            bdt_addy = user_info.get("bdt", "Not Set")
            idr_addy = user_info.get("idr", "Not Set")
            pkr_addy = user_info.get("pkr", "Not Set")
            ltcaddress = user_info.get("ltc", "Not Set")

            qr_data = f"litecoin:{ltcaddress}"
            qr = qrcode.make(qr_data)
            ltc_qr_buffer = io.BytesIO()
            qr.save(ltc_qr_buffer, format='PNG')
            ltc_qr_buffer.seek(0)

            uqr_data = f"upi://pay?pa={upi_addy}"
            uqr = qrcode.make(uqr_data)
            upi_qr_buffer = io.BytesIO()
            uqr.save(upi_qr_buffer, format='PNG')
            upi_qr_buffer.seek(0)

            embed = nextcord.Embed(description=f"{ctx.author.mention} | Wallet Info", color=0x3498db)
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)

            if ltcaddress != "Not Set":
                embed.add_field(name="<:LTC:1305994660073963530> Litecoin Address", value=f"```{ltcaddress}```", inline=False)
            if paypal_addy != "Not Set":
                embed.add_field(name="<:PAYPAL:1308674173333409895> PayPal Address", value=f"```{paypal_addy}```", inline=False)
            if upi_addy != "Not Set":
                embed.add_field(name="<:INR:1308674301406482463> UPI Address", value=f"```{upi_addy}```", inline=False)
            if bdt_addy != "Not Set":
                embed.add_field(name="<:BDT:1315702666504048754> BDT Address", value=f"```{bdt_addy}```", inline=False)
            if idr_addy != "Not Set":
                embed.add_field(name="<:IDR:1315702666504048754> IDR Address", value=f"```{idr_addy}```", inline=False)
            if pkr_addy != "Not Set":
                embed.add_field(name="<:PKR:1315703040875167744> PKR Address", value=f"```{pkr_addy}```", inline=False)

            copy_button = Button(label="Copy Address", style=nextcord.ButtonStyle.gray)
            upi_button = Button(label="UPI QR", style=nextcord.ButtonStyle.gray)
            scanner_button = Button(label="LTC QR", style=nextcord.ButtonStyle.gray)

            async def copy(interaction: nextcord.Interaction):
                select = Select(
                    placeholder="Choose an address to copy",
                    options=[]
                )
                if ltcaddress != "Not Set":
                    select.options.append(nextcord.SelectOption(label="LTC", emoji="<a:ltc:1305940882582802472>"))
                if paypal_addy != "Not Set":
                    select.options.append(nextcord.SelectOption(label="Paypal", emoji="<:PAYPAL:1308674173333409895>"))
                if upi_addy != "Not Set":
                    select.options.append(nextcord.SelectOption(label="UPI", emoji="<:INR:1308674301406482463>"))
                if bdt_addy != "Not Set":
                    select.options.append(nextcord.SelectOption(label="BDT", emoji="<:BDTTT:1315702666504048754>"))
                if idr_addy != "Not Set":
                    select.options.append(nextcord.SelectOption(label="IDR", emoji="🇮🇩"))
                if pkr_addy != "Not Set":
                    select.options.append(nextcord.SelectOption(label="PKR", emoji="<:pkr:1315703040875167744>"))

                async def select_callback(interaction: nextcord.Interaction):
                    selected_option = select.values[0]
                    address_mapping = {
                        "LTC": ltcaddress,
                        "Paypal": paypal_addy,
                        "UPI": upi_addy,
                        "BDT": bdt_addy,
                        "IDR": idr_addy,
                        "PKR": pkr_addy
                    }
                    await interaction.response.send_message(content=address_mapping[selected_option], ephemeral=True)

                select.callback = select_callback
                view = View()
                view.add_item(select)
                await interaction.response.send_message(content="Choose an address to copy:", view=view, ephemeral=True)

            async def scanner(interaction: nextcord.Interaction):
                file = nextcord.File(ltc_qr_buffer, filename="ltc_qr.png")
                qr_embed = nextcord.Embed(
                    title=f"{ctx.author.display_name}'s LTC QR Code",
                    description="Scan this QR code to access the Litecoin address.",
                    color=0x3498db
                )
                qr_embed.set_image(url="attachment://ltc_qr.png")
                await interaction.response.send_message(embed=qr_embed, file=file, ephemeral=True)

            async def upi(interaction: nextcord.Interaction):
                file = nextcord.File(upi_qr_buffer, filename="upi_qr.png")
                qr_embed = nextcord.Embed(
                    title=f"{ctx.author.display_name}'s UPI QR Code",
                    description="Scan this QR code to access the UPI address.",
                    color=0x3498db
                )
                qr_embed.set_image(url="attachment://upi_qr.png")
                await interaction.response.send_message(embed=qr_embed, file=file, ephemeral=True)

            copy_button.callback = copy
            scanner_button.callback = scanner
            upi_button.callback = upi

            view = View()
            view.add_item(copy_button)
            view.add_item(scanner_button)
            view.add_item(upi_button)

            await ctx.send(embed=embed, view=view)
        else:
            return

'''@bot.slash_command(name="vouch")
async def vouch(
    interaction: Interaction,
    seller: nextcord.User = SlashOption(description="The user to vouch for"),
    product: str = SlashOption(description="The name of the product"),
    price: float = SlashOption(description="The price of the product"),
    feedback: int = SlashOption(description="1 to 10", choices={str(i): i for i in range(1, 11)})
):
    if interaction.user == bot.user:
        await interaction.response.send_message("The bot cannot be vouched for.", ephemeral=True)
        return
    if interaction.user == seller:
        await interaction.response.send_message("You cannot vouch for yourself.", ephemeral=True)
        return    
    has_client_role = any(role.id == CLIENT_ROLE_ID for role in interaction.user.roles)
    if not has_client_role:
        await interaction.response.send_message("You don't have the required role to vouch.", ephemeral=True)
        return
    if feedback < 1 or feedback > 10:
        await interaction.response.send_message("Feedback must be between 1 and 10.", ephemeral=True)
        return
    with open(VOUCHES_FILE, 'r') as f:
        vouches_data = json.load(f)
    if str(seller.id) not in vouches_data:
        vouches_data[str(seller.id)] = []
    vouch_entry = {
        "customer": str(interaction.user.id),
        "product": product,
        "price": price,
        "feedback": feedback
    }
    vouches_data[str(seller.id)].append(vouch_entry)
    with open(VOUCHES_FILE, 'w') as f:
        json.dump(vouches_data, f, indent=4)
    embed = nextcord.Embed(description=f"Customer: {interaction.user.mention}", color=rang)
    embed.add_field(name="<:memberblack:1306361652584648779> User", value=seller.mention, inline=True)
    embed.add_field(name="<:stock:1306361654279409834> Product", value=f"```{product}```", inline=True)
    embed.add_field(name="<:prices:1306173627518947329> Price", value=f"```${price:.2f}```", inline=True)
    embed.add_field(name="<:white_star:1306361657454493696> Feedback", value=f"```{feedback}/10```", inline=True)
    embed.set_footer(text=f"{name} Exchange Service")
    await interaction.response.send_message(embed=embed)
    vouchlog.send(embed=embed)
    try:
        dm_embed = nextcord.Embed(description=f"# You have received a vouch from {interaction.user.mention} for the product `{product}`.", color=rang)
        dm_embed.add_field(name="<:memberblack:1306361652584648779> User", value=seller.mention, inline=True)
        dm_embed.add_field(name="<:stock:1306361654279409834> Product", value=f"```{product}```", inline=True)
        dm_embed.add_field(name="<:prices:1306173627518947329> Price", value=f"```${price:.2f}```", inline=True)
        dm_embed.add_field(name="<:white_star:1306361657454493696> Feedback", value=f"```{feedback}/10```", inline=True)
        dm_embed.set_footer(text=f"{name} Exchange Service")
        await seller.send(embed=dm_embed)
    except nextcord.errors.Forbidden:
        await interaction.followup.send(f"Could not send a DM to {seller.mention}, they might have DMs disabled.", ephemeral=True)
'''


def setup(bot):
    bot.add_cog(staff(bot))