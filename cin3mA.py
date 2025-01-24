# Name: Cin3mA Bot
# Description: Discord bot for the New Lands server
# Author: Arthur Clemente Machado (d0pp3lg4nger)
# Version: 1.1

# Import the required libraries
import discord
import asyncio
import random
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Define the user ID exempt from the cooldown
EXEMPT_USER_ID = 424574968504909825

# Spotify API
load_dotenv("token.env")
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
guild_id = discord.Object(id=GUILD_ID)

class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"{self.user} está online e pronto!")

        try:
            guild = discord.Object(id=GUILD_ID)
            synced = await self.tree.sync(guild=guild)
            print(f"Comandos sincronizados: {synced}, para o servidor {guild}")
        except Exception as e:
            print(f"Erro ao sincronizar comandos: {e}")
            
# Define the intents for the bot
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.typing = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True
# Create the bot
bot = MyBot(command_prefix='!', intents=intents)

# Event to play a specific song when the bot is mentioned
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Verify if the bot was mentioned
    if bot.user in message.mentions:
        # Verify if the author is in a voice channel
        if message.author.voice:
            channel = message.author.voice.channel
            try:
                # Connect to the voice channel
                vc = await channel.connect()

                # Load the audio file
                audio_source = discord.FFmpegPCMAudio('intro.mp3')

                # Play the audio file
                if not vc.is_playing():
                    vc.play(audio_source)

                    # Wait until the audio file finishes playing
                    while vc.is_playing():
                        await asyncio.sleep(1)

                # Disconnect from the voice channel
                await vc.disconnect()
            except discord.ClientException:
                await message.channel.send('Já estou em um canal de voz.')
            except discord.InvalidArgument:
                await message.channel.send('Canal de voz inválido.')
            except Exception as e:
                await message.channel.send(f'Ocorreu um erro: {e}')
        else:
            await message.channel.send('Pilantra!')

    await bot.process_commands(message)

# Help command to display the bot's commands
bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Cin3mA Bot', description='Bot para o servidor New Lands', color=0x00ff00)
    embed.add_field(name='/status', value='Mostra o status do bot', inline=False)
    embed.add_field(name='/hello', value='Cumprimenta o usuário', inline=False)
    embed.add_field(name='/somar num num', value='Realiza a soma entre dois numeros', inline=False)    
    embed.add_field(name='/mover @membro', value='Move um membro para um canal de voz', inline=False)
    embed.add_field(name='/arrastao @membro', value='Bagunçar a vida de alguém', inline=False)
    embed.add_field(name='/bernometro @membro', value='Mostra a intenção de um membro', inline=False)
    embed.add_field(name='/iago', value='O que será que ele é?', inline=False)
    embed.add_field(name='/igor', value='O que será que ele é?', inline=False)
    embed.add_field(name='/bernie', value='O que será que ele é?', inline=False)
    await ctx.send(embed=embed)
 
# Simple command to display a message
@bot.tree.command(name='hello', description='Cumprimenta o usuário')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('Olá imbogno!')
    
@bot.tree.command(name='iago', description='O que será que ele é?')
async def iago(interaction: discord.Interaction):   
    await interaction.response.send_message('Iago gay')
    
@bot.tree.command(name='bernometro', description='Mostra a intenção de um membro')
async def bernometro(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'{member.mention} tem {random.randint(0, 100)}% de intenção.')
    
# Command to sum two numbers
@bot.tree.command(name='somar', description='Realiza a soma entre dois números')
async def somar(interaction: discord.Interaction, num1: int, num2: int):
    await interaction.response.send_message(f'O resultado da soma é: {num1 + num2}')
# Generate a random number
@bot.tree.command(name="igor", description="Como será que ele está hoje?")
async def igor(interaction: discord.Interaction):
    try:
        random_number = random.randint(0, 100)
        await interaction.response.send_message(f"Igor está {random_number}% 🐒 hoje!")
    except Exception as e:
        print(f"Erro no comando /igor: {e}")
        await interaction.response.send_message(f"Erro ao executar o comando: {e}")
    
@bot.tree.command(name="bernie", description="O que será que ele é?")
async def bernie(interaction: discord.Interaction):
    gif_url = "https://media1.giphy.com/media/h8sRbOtj55JACfGn8R/giphy.gif"
    await interaction.response.send_message(gif_url)
    
# Move a member to a voice channel
@bot.tree.command(name='mover', description='Move um membro para um canal de voz')
async def mover(interaction: discord.Interaction, member: discord.Member, channel: discord.VoiceChannel):
    if member.voice is None:
        await interaction.response.send_message(f'{member.mention} não está em um canal de voz.')
        return
    try:
        await member.move_to(channel)
    except discord.Forbidden:
        await interaction.response.send_message('Não tenho permissão para mover membros.')
    except discord.HTTPException:
        await interaction.response.send_message('Erro ao mover membro.')
        
@bot.tree.command(name='convocar', description='Convoca um membro para um lugar...')
async def convocar(interaction: discord.Interaction, member: discord.Member):
    if interaction.author.id is EXEMPT_USER_ID:
        try:
            # Remove the original message
            await interaction.response.delete_original_message()
        except discord.Forbidden:
            await interaction.response.send_message("Erro ao tentar apagar a mensagem.")
            return
        except discord.HTTPException:
            await interaction.response.send_message("Erro ao tentar apagar a mensagem.")
            return
        
        # Verify if the member is in a voice channel
        if member.voice is None:
            await interaction.response.send_message(f'{member.mention} não está em um canal de voz.')
            return
        
        # Search for the voice channel
        channel = discord.utils.get(interaction.guild.channels, name='🛋aA Alta Ordem!😈')
        if channel is None:
            await interaction.response.send_message('Canal de voz não encontrado.')
            return
        
        try:
            # Move the member to the voice channel
            await member.move_to(channel)
        except discord.Forbidden:
            await interaction.response.send_message('Não tenho permissão para mover membros.')
        except discord.HTTPException:
            await interaction.response.send_message('Erro ao mover membro.')

# Command to troll a member
@bot.tree.command(name='arrastao', description='Bagunçar a vida de alguém')
@commands.cooldown(1, 120, commands.BucketType.user)  # Cooldown: 1 uso a cada 120 segundos por usuário
async def arrastao(interaction: discord.Interaction, member: discord.Member):
    
    # Verify if the user is exempt from the cooldown
    if interaction.author.id is EXEMPT_USER_ID:
        # Reset the cooldown for the command
        arrastao.reset_cooldown(interaction)
    
    if member.voice is None:
        await interaction.response.send_message(f'{member.mention} não está em um canal de voz.')
        return
       
     
    # Get all the voice channels in the guild
    voice_channels = interaction.guild.voice_channels

    # Get the channel where the member is
    member_channel = member.voice.channel
    
    try:
        #for _ in range(3):
        for channel in voice_channels:
            if channel.name != '🛋aA Alta Ordem!😈':       
                if member.voice is not None:
                    await member.move_to(channel)
                    await asyncio.sleep(0.1)
                    
        for channel in reversed(voice_channels):
            if channel.name != '🛋aA Alta Ordem!😈':    
                if member.voice is not None:
                    await member.move_to(channel)
                    await asyncio.sleep(0.1)
        
        await member.move_to(member_channel)
    except discord.Forbidden:
        await interaction.response.send_message('Não tenho permissão para mover membros.')
    except discord.HTTPException:
        await interaction.response.send_message('Erro ao mover membro.')
        
# Handle cooldown errors
@arrastao.error
async def arrastao_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(f'Espere {error.retry_after:.2f} segundos antes de usar este comando novamente.')

    
@bot.command()
async def sync(ctx):
    try:
        await bot.tree.sync()
        await ctx.send("Slash commands sincronizados manualmente.")
    except Exception as e:
        await ctx.send(f"Erro ao sincronizar comandos: {e}")
    
# TOKEN
load_dotenv("token.env")
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)