import discord
from discord.ext import commands

token = "YOUR DISCORD BOT TOKEN"

client = commands.Bot(intents=discord.Intents.all() , command_prefix= "!" , description='Sha256')

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!mod'):
        args = message.content.split()

        if not message.author.guild_permissions.administrator:
            await message.channel.send('You must be an administrator to use this command.')
            return

        if len(args) < 3:
            await message.channel.send('Not enough arguments. Use !mod [ban/kick/mute] [@user] [reason]')
            return

        user = message.mentions[0]

        reason = ' '.join(args[3:])

        if args[1].lower() == 'ban':
            await user.ban(reason=reason)
            await message.channel.send(f'{user.name} was banned for {reason}')

        elif args[1].lower() == 'kick':
            await user.kick(reason=reason)
            await message.channel.send(f'{user.name} was kicked for {reason}')

        elif args[1].lower() == 'mute':
            mute_role = discord.utils.get(message.guild.roles, name='Muted')

            if mute_role is None:
                mute_role = await message.guild.create_role(name='Muted')

                for channel in message.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False)

            await user.add_roles(mute_role, reason=reason)
            await message.channel.send(f'{user.name} was muted for {reason}')

        elif args[1].lower() == 'unmute':
            mute_role = discord.utils.get(message.guild.roles, name='Muted')

            if mute_role is None:
                mute_role = await message.guild.create_role(name='Muted')

            await user.remove_roles(mute_role, reason=reason)
            await message.channel.send(f'{user.name} was unmuted')

        else:
            await message.channel.send('Invalid action. Use !mod [ban/kick/mute] [@user] [reason]')


client.run(token)
