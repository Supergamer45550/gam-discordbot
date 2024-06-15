import discord
import os
from googleapiclient.discovery import build
from discord.ext import commands
from discord.utils import get
import logging


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Bot(command_prefix='', intents=intents)


#Bot console messages
@bot.event
async def on_ready():
    print(f'{bot.user.name} ist gestartet')

@bot.after_invoke
async def after_any_command(ctx):
    print(f"Command {ctx.command} wurde gerade genutzt.")

#Join/leave-messages
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(858267391665111052)
    await channel.send(f'Willkommen {member.mention} auf unserem Server!')
    print(f"{member.name} ist gejoint.")
    role_name = "unverifiziert"
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        print(f"{member} hat die Rolle {role.name} erhalten.")
    
    role_name2 = "------Verwarnungen------"
    role = discord.utils.get(member.guild.roles, name=role_name2)
    if role:
        await member.add_roles(role)
        print(f"{member} hat die Rolle {role.name} erhalten.")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(858267391665111052)
    await channel.send(f'{member.mention}, hat den Server verlassen')
    print(f"{member.name} hat den server verlassen")


#Bot-Activity
@bot.command()
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity: str):
    await bot.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"Activity set to {activity}")
    
@activity.error
async def activity_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Du hast hierfür keine Rechte")

#Bot Commands
@bot.command()
async def hi(ctx):
    await ctx.send('Hello! I am a Discord bot.')

@bot.command()
async def hilfe(ctx):
    await ctx.send("""
Vor jeden command muss ein !
    > hello
    > hi
    > hilfe
    > multiline (nur experimentell)
    """)

@bot.command()
async def multiline(ctx):
    await ctx.send("""
    > Hi
 UwU
    """)

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title='Test', description='Test beschreibung', color=discord.Color.red())
    embed.add_field(name='Test 1', value='test1', inline=False)
    embed.add_field(name='Test 2', value='test2', inline=False)

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def rules(ctx):
    await ctx.send("**Das sind unsere Regeln**")
    embed = discord.Embed(title='Regeln', description='Die Serverregeln', color=discord.Color.red())
    embed.add_field(name='Regel 1', value='Keine Beleidigungen, Rassismus o.ä \nJede Person hat Gefühle', inline=False)
    embed.add_field(name='Regel 2', value='Respektvoller Umgang mit jedem \nHier soll sich jeder wohlfühlen', inline=False)
    embed.add_field(name='Regel 3', value='Auf Mods/Admins hat man zu hören \n Sie müssen sich nicht rechtfertigen \nEs sind auch nur Menschen, die Zeit in diesen Server investieren', inline=False)
    embed.add_field(name='Regel 4', value='Keine (Eigen-)Werbung \nWerbung nervt nur und wird nicht toleriert', inline=False)
    embed.add_field(name='Regel 5', value='Kein Spielverderber sein \nRuiniert Leuten nicht den Spaß auf dem Server', inline=False)
    embed.add_field(name='Regel 6', value='Keine unnötigen Pings \nEs nervt einfach nur, wenn man unnötige Nachrichten bspw aufs Handy kriegt', inline=False)
    embed.add_field(name='Regel für Mods o.ä', value='Nutzt eure Rechte gescheit \nSolltet ihr sie falsch benutzen, so wird euch die Rolle weggenommen \nund ihr werdet auf eine Blacklist gesetzt', inline=False)
    await ctx.send(embed=embed)
    embed = discord.Embed(title='Verwarnungen', description='Infos, was die Verwarnungen machen', color=discord.Color.green())
    embed.add_field(name='Verwarnung 1', value='Man steht zwar unter Beobachtung, mehr aber nicht', inline=False)
    embed.add_field(name='Verwarnung 2', value='Zuerst behält man nur einen Timeout \nZudem steht man noch mehr unter Beobachtung', inline=False)
    embed.add_field(name='Verwarnung', value='Sobald du Verwarnung 3 hast, bist du direkt gebannt', inline=False)
    await ctx.send(embed=embed)
    embed = discord.Embed(title='Bestrafungen', color=discord.Color.blue())
    embed.add_field(name='Verwarnung 1', value='Regeln 2,4,5 und 6 geben dir die Verwarnung 1', inline=False)
    embed.add_field(name='Verwarnung 2', value='Regeln 1 (Nur, wenn leichte Beleidigungen o.ä) und 3 geben dir Verwarnung 2', inline=False)
    embed.add_field(name='Verwarnung 3', value='Solltet ihr bei Regel 1 übertreiben oder andere schlimme Dinge machen, \nkriegt ihr Verwarnung 3 und werdet direkt gebannt', inline=False)
    await ctx.send(embed=embed)
    await ctx.send("Verifiziere dich [hier](<https://discord.com/channels/1079786484296589322/1240293444782657567>), in dem du !verifizierung eingibst \nDu stimmst damit automatisch den Regeln zu")

@rules.error
async def rules_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Du hast hierfür keine Rechte")

@bot.slash_command(name='test', description='Nur ein test')
async def ping(ctx):
    await ctx.respond('Stiftung warentest bestanden I guess')

@bot.slash_command(name='ping', description='Nur ein test')
async def ping(ctx):
    await ctx.respond('pong')


@bot.slash_command(name='socials', description='Zeigt die Socials')
async def socials(ctx):
    await ctx.respond("""
> [Youtube](https://www.youtube.com/@gamesandmore_)
> [Twitch](https://www.twitch.tv/bestergameryoutube)                    
    """)

@bot.slash_command(name='invite', description='Zeigt den Discord invite')
async def invite(ctx):
    await ctx.respond('https://discord.gameandmore.eu')

#custom vc
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == 1112487455661236294:
        guild = member.guild
        category = guild.get_channel(1240413921832337499)
        custom_voice_channel = await guild.create_voice_channel(name=f"{member.name}'s channel", category=category)
        
        await member.move_to(custom_voice_channel)

        def check(a, b, c):
            return len(custom_voice_channel.members) == 0

        await bot.wait_for('voice_state_update', check=check)
        await custom_voice_channel.delete()

#verifizierung
@bot.command()
async def verifizierung(ctx):
    verified_role_name = "verifiziert"
    unverified_role_name = "unverifiziert"
     
    verified_role = discord.utils.get(ctx.guild.roles, name=verified_role_name)
    unverified_role = discord.utils.get(ctx.guild.roles, name=unverified_role_name)
    
    if verified_role in ctx.author.roles:
        print(f"person bereits verifiziert")
        return  
    
    if verified_role:
        await ctx.author.add_roles(verified_role)
        await ctx.send("Du wurdest verifiziert")
        print(f"{ctx.author} wurde verifiziert.")
    
    if unverified_role:
        await ctx.author.remove_roles(unverified_role)

@bot.slash_command(name='songrequest', description='Schlage ein Song vor (Nur YouTube Links)')
async def whitelist(ctx, url: str):
    channel = discord.utils.get(bot.get_all_channels(), id=1250197363792937093)

    message = f'{ctx.author.display_name} wünscht sich {url}'

    await channel.send(message)

    await ctx.respond(f'Dein Song Request wurde gesendet')
    print(f'{ctx.author.display_name} hat folgenden Song Request eingereicht {url}')



bot.run('bot-token')