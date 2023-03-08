import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbset, dbget


class messagefunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            if len(message.content) <= 1500:
                msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                if channel:
                    await channel.send(f"Message from {message.author.name} in channel {message.channel.mention} deleted: {message.content}")
            else:
                msgchnl = await dbget(message.guild.id, self.bot.user.name, "messagechannelid")
                channel = discord.utils.get(message.guild.channels, id=msgchnl[0])
                if channel:
                    await channel.send(
                         f"Message from {message.author.name} in channel {message.channel.mention} deleted: content too long to send.")
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        try:
            msgsum = sum([len(message_before.content), len(message_after.content)])
            if msgsum <= 1500:
                msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                if channel:
                    await channel.send(f"Message from {message_before.author.name} in channel {message_before.channel.mention} edited from {message_before.content} to {message_after.content}")
            else:
                msgchnl = await dbget(message_before.guild.id, self.bot.user.name, "messagechannelid")
                channel = discord.utils.get(message_before.guild.channels, id=msgchnl[0])
                if channel:
                    await channel.send(
                        f"Message from {message_before.author.name} in channel {message_before.channel.mention} edited: content too long to send.")
        except Exception as e:
            print(e)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="resetmessagechannel", description="Command to reset your server's message log channel.")
    async def resetwelcomechannel(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, self.bot.user.name, "messagechannelid", 0)
            await interaction.response.send_message(f"Message log channel config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)


async def setup(bot: commands.Cog):
    await bot.add_cog(messagefunctions(bot))
