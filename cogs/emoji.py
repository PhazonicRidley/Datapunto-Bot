from discord.ext import commands
import discord
import io


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def aiobytesfinalize(self, image):
        file_e = io.BytesIO()
        file_e.write(image)
        file_e.seek(0)
        return file_e.read()

    @commands.command(aliases=['nemoji'])
    async def nitroemoji(self, ctx, emojiname):
        emoji = discord.utils.get(self.bot.emojis, name=emojiname)
        if emoji:
            await ctx.send(emoji)
        else:
            return await ctx.send("No Emote Found!")

    @commands.group()
    async def emoji(self, ctx):
        """Emoji management commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @emoji.command()
    @commands.bot_has_permissions(manage_emojis=True)
    async def add(self, ctx, emoji_name, *, url):
        emoji_link = await self.bot.aiogetbytes(url)
        if emoji_link is not False:
            emoji_aio = self.aiobytesfinalize(emoji_link)
            try:
                finalized_e = await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_aio, 
                                                                  reason=f"Emoji Added by {ctx.author} "
                                                                  f"(ID: {ctx.author.id})")
            except Exception as ex:
               pass
               
            else:
                await ctx.send(f"Successfully created {finalized_e} `{finalized_e}`")
        else:
            return await ctx.send("Something went wrong trying to fetch the url. Try again later(?)")

    @emoji.command()
    @commands.bot_has_permissions(manage_emojis=True)
    async def copy(self, ctx, emoji: discord.PartialEmoji):
        """ "Copies" an emoji and adds it to the guild.
        
        Helpers+"""
        emoji_link = await self.bot.aiogetbytes(str(emoji.url))
        if emoji_link is not False:
            try:
                fe = await ctx.guild.create_custom_emoji(name=emoji.name, image=emoji_link,
                                                         reason=f"Emoji Added by {ctx.author} "
                                                         f"(ID: {ctx.author.id})")
            except Exception as ex:
                self.bot.log.error(ex)
                return await ctx.send("Something went wrong creating that emoji. Make sure this guild"
                                      " emoji\'s list isn\'t full and that emoji is under 256kb.")
            else:
                await ctx.send(f"Successfully created {fe} `{fe}`")
        else:
            return await ctx.send("Something went wrong trying to fetch the url. Try again later(?)")

    @emoji.command()
    @commands.bot_has_permissions(manage_emojis=True)
    async def delete(self, ctx, emote: discord.Emoji):
        """Deletes an emoji from the guild
        
        Moderators+"""
        if ctx.guild.id != emote.guild_id:
            return await ctx.send("This emoji isn't in this guild!")

        await emote.delete(reason=f"Emoji Removed by {ctx.author} (ID: {ctx.author.id})")
        await ctx.send("Emote is now deleted.")

def setup(bot):
    bot.add_cog(Emoji(bot))
