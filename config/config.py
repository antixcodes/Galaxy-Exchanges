import json
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

# Load the JSON file
def load_role_mapping():
    with open('role_mapping.json', 'r') as file:
        return json.load(file)
    
def save_role_mapping(role_mapping):
    with open('role_mapping.json', 'w') as file:
        json.dump(role_mapping, file, indent=4)

class RoleMappingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def config_role_mapping(self, interaction: Interaction, exchange_key: str, role_id: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
            return
        
        # Load the existing role mapping
        role_mapping = load_role_mapping()

        # Update or add the role mapping entry
        role_mapping[exchange_key] = role_id

        # Save the updated mapping back to the file
        save_role_mapping(role_mapping)

        await interaction.response.send_message(f"Role mapping for `{exchange_key}` updated to `{role_id}`.", ephemeral=True)

# Add the cog to the bot
def setup(bot):
    bot.add_cog(RoleMappingCommand(bot))