from discord import Color, Embed, Interaction, Member, Role, TextChannel, app_commands
from discord.ext import commands
from data.config import COLOR_CODE, MANAGEMENT, PERMISSION_ERR

COLOR = Color.from_str(COLOR_CODE)


def check_role(roles: list) -> bool:
    for role in roles:
        if role.id in MANAGEMENT:
            return True
    return False


class ModerationCommands(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kicks Member")
    async def kick(self, ctx: Interaction, member: Member, reason: str = None):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            name = member.name
            await member.kick(reason=reason)
            await ctx.followup.send(
                f"{name} is kicked from the server. Reason: {reason}"
            )
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="ban", description="Bans Member")
    async def ban(self, ctx: Interaction, member: Member, reason: str = None):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            name = member.name
            await member.ban(reason=reason)
            await ctx.followup.send(
                f"{name} is banned from the server. Reason: {reason}"
            )
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="mute", description="Mutes Member")
    async def mute(self, ctx: Interaction, member: Member, reason: str = None):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    await member.add_roles(role)
                    return await ctx.followup.send(
                        f"{member.name} is muted. Reason: {reason}"
                    )
            await ctx.followup.send("Error: Muted Role was mot found in you Server.")
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="unmute", description="Unmutes Member")
    async def unmute(self, ctx: Interaction, member: Member):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            for role in ctx.guild.roles:
                if role.name == "Muted":
                    await member.remove_roles(role)
                    return await ctx.followup.send(f"{member.name} is unmuted now.")
            await ctx.followup.send("Error: Muted Role was mot found in you Server.")
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="addrole", description="Adds Role")
    async def addrole(self, ctx: Interaction, member: Member, new_role: Role):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            for role in ctx.guild.roles:
                if role == new_role:
                    await member.add_roles(role)
                    return await ctx.followup.send(
                        f"{new_role.mention} role is added to {member.mention}."
                    )
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="removerole", description="Removes Role")
    async def removerole(self, ctx: Interaction, member: Member, new_role: Role):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            for role in ctx.guild.roles:
                if role == new_role:
                    await member.remove_roles(role)
                    return await ctx.followup.send(
                        f"{new_role.mention} role is removed from {member.mention}."
                    )
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="warn", description="Warns Member")
    async def warn(self, ctx: Interaction, member: Member, reason: str = None):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            desc = f"{member.mention} have been warned. Reason: {reason}"
            embed = Embed(title="Warning", description=desc, color=Color.red())
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            await ctx.followup.send(embed=embed)
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(
        name="purge", description="Deletes Previous Unpinned Messages"
    )
    async def purge(self, ctx: Interaction, limit: int):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            if limit > 50 or limit < 1:
                return await ctx.followup.send(
                    "Error: Purge limit must be between 1 and 50"
                )
            await ctx.channel.purge(limit=limit, check=lambda msg: not msg.pinned)
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="dm", description="Sends Member a DM")
    async def dm(self, ctx: Interaction, member: Member, message: str):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            try:
                await member.send(message)
                await ctx.followup.send(
                    f"New DM is sent to Server Member: {member.name}."
                )
            except Exception as err:
                await ctx.followup.send(err)
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="ann", description="Sends Announcement")
    async def ann(self, ctx: Interaction, channel: TextChannel, title: str, desc: str):
        try:
            await ctx.response.defer()
            if not check_role(ctx.user.roles):
                return await ctx.followup.send(PERMISSION_ERR)
            embed = Embed(title=title, description=desc, color=COLOR)
            await channel.send(embed=embed)
            await ctx.followup.send(
                f"New announcement has been sent to {channel.mention}."
            )
        except Exception as err:
            await ctx.followup.send(err)


async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
