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
trans_logs = Webhook(f"{tr_log}")
nocolor=0x2B2D31
tick="<:check:1305951941423009803>"
cross="<a:CrossXCross:1320006279376404550>"
#######################################################3
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
    # Ensure file path uses OS-independent separators
    file_name = os.path.join(*file_name.split('/')) if '/' in file_name else os.path.join(*file_name.split('\\'))

    new_data = {
        ticket_channel_id: [
            {
                "name": nom,
                "sendingcurrency": sendingcurrency,
                "receivingcurrency": receivingcurrency,
            }
        ]
    }

    try:
        # Try reading existing data
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            with open(file_name, "r") as file:
                data = json.load(file)
        else:
            data = {}
    except json.JSONDecodeError:
        print(f"Error: File {file_name} contains invalid JSON. Resetting data.")
        data = {}

    # Update data with the new entry
    if ticket_channel_id in data:
        data[ticket_channel_id].extend(new_data[ticket_channel_id])
    else:
        data.update(new_data)

    # Write updated data back to the file
    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # Ensure the directory exists
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

class ClaimButton(nextcord.ui.View):
    def __init__(self, client_name, client_id, sendingcurrency, receivingcurrency, embed, exchrolex, amount):
        super().__init__(timeout=None)
        self.client_name = client_name
        self.client_id = client_id
        self.exchrolex = exchrolex
        self.amount = amount
        self.sendingcurrency = sendingcurrency
        self.receivingcurrency = receivingcurrency
        self.embed = embed
        self.last_claim_pressed = None
        self.last_close_pressed = None
        self.last_change_amount_pressed = None
        self.claimer_name = None

    @nextcord.ui.button(label="Claim", emoji="<:thunder2:1305942208632983573>", style=nextcord.ButtonStyle.grey)
    async def claim_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.claimer_name = interaction.user.name
        current_time = asyncio.get_event_loop().time()
        if not any(role.id == exchangers_role_id for role in interaction.user.roles):
            await interaction.response.send_message("You do not have permission to claim this ticket.", ephemeral=True)
            return
        self.last_claim_pressed = current_time
        new_ticket_name = f"claimed-by-{interaction.user.name.replace(' ', '_')}・{self.client_name}"
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True, read_message_history=True),
            self.exchrolex: nextcord.PermissionOverwrite(view_channel=False),
            interaction.guild.get_member(self.client_id): nextcord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True, read_message_history=True)
        }
        await interaction.channel.edit(name=new_ticket_name, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket claimed and renamed to `{new_ticket_name}`.", ephemeral=True)
        em = nextcord.Embed()
        em.add_field(name="Ticket Claimed", value=f"> Before: {self.sendingcurrency}2{self.receivingcurrency}・{self.client_name}\n> After: {new_ticket_name}", inline=False)
        em.add_field(name="Channel ID", value=f"{interaction.channel.id}", inline=False)
        em.add_field(name="Client", value=f"{self.client_name} [{self.client_id}]", inline=False) 
        em.add_field(name="Exchanger", value=f"{interaction.user.name} [{interaction.user.id}]", inline=False)
        em.add_field(name="Purpose", value=f"{self.sendingcurrency}2{self.receivingcurrency}", inline=False) 
        await send_webhook_message(CLAIMED_WEBHOOK_URL, embed=em)
        button.disabled = True
        await interaction.message.edit(view=self)
        channel_id = str(interaction.channel.id)
        claimer_id = interaction.user.id
        try:
            with open("database/exchangedeals.json", "r") as file:
                exchange_data = json.load(file)
            
            if channel_id in exchange_data:
                if "exchanger" not in exchange_data[channel_id][0]:
                    exchange_data[channel_id][0]["client"] = self.client_id
                    exchange_data[channel_id][0]["exchanger"] = claimer_id
                    exchange_data[channel_id][0]["amount"] = self.amount
                else:
                    await interaction.response.send_message("This ticket is already claimed by another exchanger.", ephemeral=True)
                    return
            else:
                await interaction.response.send_message("No data found for this channel in exchangedeals.json.", ephemeral=True)
                return
            with open("database/exchangedeals.json", "w") as file:
                json.dump(exchange_data, file, indent=4)

        except FileNotFoundError:
            await interaction.response.send_message("The `exchangedeals.json` file was not found.", ephemeral=True)
        except json.JSONDecodeError:
            await interaction.response.send_message("There was an error reading the `exchangedeals.json` file. It might be corrupted.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {str(e)}", ephemeral=True)

    @nextcord.ui.button(label="Close", emoji="🔒", style=nextcord.ButtonStyle.grey)
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        current_time = asyncio.get_event_loop().time()
        if self.last_close_pressed is not None and (current_time - self.last_close_pressed) < 30:
            await interaction.response.send_message("This button is on cooldown. Please wait 30 seconds.", ephemeral=True)
            return
        if interaction.user.id == self.client_id:
            self.last_close_pressed = current_time
            confirmation_view = CloseConfirmationView(self.sendingcurrency, self.receivingcurrency, self.claimer_name)
            await interaction.response.send_message(embed=nextcord.Embed(description="<:QuestionBlock:1317257988851105795> | Are you sure you want to close this ticket?"), ephemeral=True, view=confirmation_view)
            await interaction.response.send_message("You have 15 seconds to confirm the closure of this ticket. Please interact with the buttons.", ephemeral=True)
            await asyncio.sleep(15)
            if not confirmation_view.is_finished():
                confirmation_view.disable_buttons()
                try:
                    await interaction.channel.send("The closure request has been cancelled due to inactivity.")
                except nextcord.NotFound:
                    print("The channel was not found or has already been deleted.")
                confirmation_view.stop()
        else:
            await interaction.response.send_message("Only Ticket Owner Can Close this Ticket", ephemeral=True)        

    @nextcord.ui.button(label="REQ MM", emoji="<:mm2:1320006751482806352>", style=nextcord.ButtonStyle.gray, custom_id="button_click")
    async def req_mm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel = interaction.channel
        role_id = 1315673156714762300
        role = interaction.guild.get_role(role_id)
        if interaction.user.id == self.client_id:
            if role:
                await channel.set_permissions(role, view_channel=True, read_message_history=True, send_messages=True)
                time.sleep(1)
                kyu = AllowedMentions(roles=True)
                await interaction.response.send_message(f"<@&{role_id}>", allowed_mentions=kyu)
            else:
                await interaction.response.send_message("Exchanger role not found.")
        else:
            await interaction.response.send_message("Only Ticket Owner Can Request for MM", ephemeral=True) 

class CloseConfirmationView(nextcord.ui.View):
    def __init__(self, sendingcurrency=None, receivingcurrency=None, claimer_name=None):
        super().__init__(timeout=None)  
        self.sendingcurrency = sendingcurrency
        self.receivingcurrency = receivingcurrency
        self.claimer_name = claimer_name

    def disable_buttons(self):
        for item in self.children:
            item.disabled = True

    @nextcord.ui.button(label="Confirm Closure", style=nextcord.ButtonStyle.grey)
    async def confirm_closure(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("This ticket will be deleted in 10 seconds.", ephemeral=True)
        purpose_with_two = f"{self.sendingcurrency}2{self.receivingcurrency}"
        await log_ticket_closure(interaction.user.name, interaction.channel.name, purpose_with_two, self.claimer_name)
        await asyncio.sleep(10)
        await interaction.channel.delete()
        print(f"Channel {interaction.channel.name} has been deleted after confirmation.")

    @nextcord.ui.button(label="Cancel Closure", style=nextcord.ButtonStyle.grey)
    async def cancel_closure(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Ticket close request has been cancelled.", ephemeral=True)
        self.stop()

async def send_webhook_message(webhook_url: str, content: str = None, embed: nextcord.Embed = None):
    async with aiohttp.ClientSession() as session:
        webhook = nextcord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(content=content, embed=embed)

async def log_ticket_closure(user: str, channel_name: str, purpose: str, claimer: str):
    embed = nextcord.Embed(title="Ticket Closed", color=rang)
    embed.add_field(name="Claimed by", value=claimer, inline=False)  
    embed.add_field(name="Deleted by", value=user, inline=False)
    embed.add_field(name="Channel", value=channel_name, inline=False)
    embed.add_field(name="Purpose", value=purpose, inline=False)
    await send_webhook_message(CLOSURE_WEBHOOK_URL, embed=embed)
    
class CurrencyExchangeView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.original_message = None
        self.sending_option = None
        self.last_select_pressed = None

    @nextcord.ui.select(
        placeholder="What will you be sending?",
        options=[
            nextcord.SelectOption(label="INR", value="inr", emoji="<:INR:1308674301406482463>"),
            nextcord.SelectOption(label="Crypto", value="crypto", emoji="<:Cryptotocrypto_official:1305994531585392692>"),
            nextcord.SelectOption(label="C2C", value="c2c", emoji="<:Cryptotocrypto_official:1305994531585392692>"),
            nextcord.SelectOption(label="Paypal", value="paypal", emoji="<:PAYPAL:1308674173333409895>"),
            nextcord.SelectOption(label="PKR", value="pkr", emoji="<:pkr:1315703040875167744>"),
            nextcord.SelectOption(label="IDR", value="idr", emoji="🇮🇩"),
            nextcord.SelectOption(label="BDT", value="bdt", emoji="<:BDTTT:1315702666504048754>")
        ]
    )
    async def select_callback(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        current_time = asyncio.get_event_loop().time()
        self.last_select_pressed = current_time
        if self.original_message is None:
            self.original_message = interaction.message
        self.sending_option = select.values[0]
        if self.sending_option == "c2c":
            await self.original_message.edit(content="‎")
            await interaction.response.send_modal(C2CAmountModal(self.sending_option))
        else:
            await self.original_message.edit(content="‎")
            amount_modal = Infomodal(self.sending_option)
            await interaction.response.send_modal(amount_modal)

class C2CAmountModal(nextcord.ui.Modal):
    def __init__(self, selected_crypto):
        super().__init__(title=f"Enter Amount to Exchange for {selected_crypto}")
        self.selected_crypto = selected_crypto
        self.sending = nextcord.ui.TextInput(
            label="Which Crypto will you send?",
            placeholder="(e.g., LTC, ETH)",
            required=True
        )
        self.receiving = nextcord.ui.TextInput(
            label="Which Crypto will you receive?",
            placeholder="(e.g., BTC, SOL)",
            required=True
        )
        self.amount_input = nextcord.ui.TextInput(
            label="Amount",
            placeholder="Enter amount (e.g., 100). Max 9999.",
            required=True
        )
        self.add_item(self.sending)
        self.add_item(self.receiving)
        self.add_item(self.amount_input)
    async def callback(self, interaction: nextcord.Interaction):
        try:
            amount = float(self.amount_input.value.strip())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            await interaction.response.send_message(
                "Invalid amount. Please enter a number greater than zero.", ephemeral=True
            )
            return
        ticket_name = f"c2c-{interaction.user.name.replace(' ', '_')}"
        category_id = EXCHANGE_CONFIG.get("category_mapping", {}).get("crypto_to_crypto")
        category = nextcord.utils.get(interaction.guild.categories, id=category_id)
        if category:
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.user: nextcord.PermissionOverwrite(
                    read_messages=True, send_messages=True, read_message_history=True
                ),
            }
            ticket_channel = await interaction.guild.create_text_channel(
                name=ticket_name, category=category, overwrites=overwrites
            )
            role_mapping = exchconfig.get("role_map", {})
            sending_currency = self.sending.value.upper().strip()
            receiving_currency = self.selected_crypto.upper().strip()
            role_mention = ""
            role_key = "crypto_exchanger"
            role_id = role_mapping.get(role_key)
            if role_id:
                role_mention = f"<@&{role_id}>"
            embed = nextcord.Embed(
                title=f"Exchange Request: {sending_currency} to {receiving_currency}",
                description=(
                    "> **Note:** Please be patient and wait for assistance as we might not always be available."
                ),
                color=0x808080
            )
            embed.set_thumbnail(url=interaction.guild.icon.url)
            embed.add_field(name="Deal Info:", value=f"Total Amount: {amount} {sending_currency}", inline=False)
            embed.add_field(name="Sending:", value=sending_currency, inline=False)
            embed.add_field(name="Receiving:", value=receiving_currency, inline=False)
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
            exchangedeal(
                ticket_channel_id=ticket_channel.id,
                nom=interaction.user.name.replace(' ', '_'),
                sendingcurrency="c",
                receivingcurrency="c"
            )
            claim_button = ClaimButton(
                client_name=interaction.user.name,
                client_id=interaction.user.id,
                sendingcurrency="c",
                receivingcurrency="b",
                embed=embed,
                exchrolex=interaction.guild.get_role(role_id),
                amount=amount
            )
            await ticket_channel.send(
                content=(
                    f"Welcome {interaction.user.mention}, please be patient. {role_mention} will assist you soon."
                ),
                embed=embed,
                view=claim_button
            )
            await interaction.response.send_message(embed=nextcord.Embed(description=f"{tick} | Ticket created successfully: <#{ticket_channel.id}>"), ephemeral=True)
        else:
            await interaction.response.send_message(embed=nextcord.Embed(description=f"{cross} | No category available for C2C exchanges. Please contact an admin.", ephemeral=True))

class Infomodal(nextcord.ui.Modal):
    def __init__(self, sending_option, receiving_option=None):
        super().__init__(title="Amount to Exchange")
        self.sending_option = sending_option
        self.receiving_option = receiving_option
        self.amount_input = nextcord.ui.TextInput(
            label="Amount (e.g., 100$, 50€)", 
            placeholder="Enter amount (max 9999)", 
            required=True)
        self.receivingcurrency = nextcord.ui.TextInput(
            label="What will you be receiving?", 
            placeholder="(e.g. PayPal, Crypto)", 
            required=True
        )
        self.add_item(self.receivingcurrency)
        self.add_item(self.amount_input)
    
    async def callback(self, interaction: Interaction):
        category_mapping = EXCHANGE_CONFIG.get("category_mapping", {})
        role_mapping = exchconfig["role_map"]
        allowed_receiving_options = EXCHANGE_CONFIG.get("allowed_receiving_options", {})
        sendingcurrency = self.sending_option.lower()
        receivingcurrency = self.receivingcurrency.value.strip().lower()
        if receivingcurrency not in allowed_receiving_options.get(sendingcurrency, []):
            eg = ', '.join(f"`{option}`" for option in allowed_receiving_options.get(sendingcurrency, []))
            emxx = nextcord.Embed()
            emxx.add_field(name=f"{cross} | Please select any of the options below to receive", value=f"{eg}")
            await interaction.response.send_message(embed=emxx, ephemeral=True)
            return
        exchange_key = f"{sendingcurrency}_to_{receivingcurrency}"
        category_id = category_mapping.get(exchange_key)
        if not category_id:
            await interaction.response.send_message("Error: No category available for this exchange type. Please contact an admin.", ephemeral=True)
            return
        match = re.match(r"^(\d+(\.\d+)?)([$€]?)$", self.amount_input.value.strip())
        if match:
            channel_role_map = {
                    "paypal2crypto": "paypal_exchanger",
                    "crypto2paypal": "paypal_exchanger",
                    "inr2crypto": "inr_exchanger",
                    "crypto2inr": "inr_exchanger",
                    "crypto2crypto": "crypto_exchanger",
                    "pkr2crypto": "pkr_exchanger",
                    "crypto2pkr": "pkr_exchanger",
                    "crypto2idr": "idr_exchanger",
                    "idr2crypto": "idr_exchanger",
                    "bdt2crypto": "bdt_exchanger",
                    "crypto2bdt": "bdt_exchanger",
                } 
            amount = float(match.group(1))
            currency_sign = match.group(3) or "$"
            ticket_channel_name = f"{sendingcurrency}2{receivingcurrency}・{interaction.user.name.replace(' ', '_')}" 
            role_mention = ""
            for prefix, role_key in channel_role_map.items():
                if ticket_channel_name.startswith(prefix):
                    role_id = role_mapping.get(role_key)
                    if role_id:
                        role_mention = f"<@&{role_id}>"
                    break
            category = nextcord.utils.get(interaction.guild.categories, id=category_id)
            if category:
                if len(category.channels) >= 50:
                    await interaction.response.send_message("Cannot create more channels in this category.", ephemeral=True)
                    return
                exchrolex = interaction.guild.get_role(role_id)
                overwrites = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                    interaction.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
                    exchrolex: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
                }
                nom = interaction.user.name.replace(' ', '_')
                ticket_channel = await interaction.guild.create_text_channel(ticket_channel_name, category=category, overwrites=overwrites)
                exchangedeal(ticket_channel.id, nom, sendingcurrency, receivingcurrency)
                embed = nextcord.Embed(title=f"{sendingcurrency} 2 {receivingcurrency}", description="> Note: Please be patient and wait for a reply as we are not always available.", color=808080)
                embed.set_thumbnail(url=interaction.guild.icon.url)
                embed.add_field(name="Deal Info:", value=f"Total Amount: {amount}{currency_sign}", inline=False)
                embed.add_field(name="Sending: ", value=f"{sendingcurrency}", inline=False)
                embed.add_field(name="Receiving: ", value=f"{receivingcurrency}", inline=False)
                embed.set_footer(text=f"{interaction.user}", icon_url=interaction.user.avatar)
                client_name = interaction.user.name
                client_id = interaction.user.id        
                claim_button = ClaimButton(client_name, client_id, sendingcurrency, receivingcurrency, embed, exchrolex, amount)
                wlc = await ticket_channel.send(
                    f"Welcome {interaction.user.mention}, be patient {role_mention} will be here soon...",
                    embed=embed,
                    view=claim_button)
                await wlc.pin()
                await interaction.response.send_message(embed=nextcord.Embed(description=f"{tick} | Ticket created successfully: <#{ticket_channel.id}>"), ephemeral=True)
        else:
            await interaction.response.send_message("Invalid amount format. Please enter a valid amount (e.g., 100$, 50€ or just 100).", ephemeral=True)

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_task = None  

    async def update_exchange_message(self):
        print("Exchange bot activated! Powered by @server.py")
        state = load_state()
        if state.get("setup_channel_id") and state.get("setup_message_id"):
            try:
                channel = self.bot.get_channel(state["setup_channel_id"])
                setup_message = await channel.fetch_message(state["setup_message_id"])
                view = CurrencyExchangeView()
                embed = nextcord.Embed(title=f"{name} Service", color=rang)
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
                guild = channel.guild
                embed.set_thumbnail(url=guild.icon.url)
                embed.set_footer(text=f"{name} | MM | Exchange", icon_url=guild.icon.url)
                await setup_message.edit(embed=embed, view=view)
                print("Successfully restored the setup message.")
                if self.update_task is None or self.update_task.done():
                    self.update_task = asyncio.create_task(self.update(setup_message, embed, view))
            except nextcord.NotFound:
                print("Setup message not found, it might have been deleted.")
            except nextcord.Forbidden:
                print("Bot does not have permission to access the channel or message.")

    async def update(self, setup_message, embed, view):
        print("Starting the update function.")
        while True:
            await asyncio.sleep(540)
            try:
                await setup_message.edit(embed=embed, view=view)
                print("Successfully updated the setup message.")
            except nextcord.NotFound:
                print("The setup message could not be found, it might have been deleted.")
                break
            except nextcord.Forbidden:
                print("Bot does not have permission to access the message.")
                break
            except Exception as e:
                print(f"Error while updating message: {e}")

def setup(bot):
    bot.add_cog(MainCog(bot))
