from dotenv import load_dotenv as load
from os import getenv as get
import discord
from discord import app_commands
from discord.ext import commands, tasks
import functions.security
import functions.connect
from datetime import time, datetime
from time import sleep as s

load()

Token = get("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot("$", intents=intents)

@bot.event
async def on_ready():
  channel = bot.get_channel(1262107519686283305)
  await bot.change_presence(activity=(discord.Game('VsCode')), status=discord.Status.do_not_disturb)
  sinc = await bot.tree.sync()
  await channel.send(f'{len(sinc)} Comandos Sincronizados!', delete_after=5)
  print('✔ ON')

@bot.tree.command(name='clear', description='Limpa Todas as Mensagens do Canal!')
async def clear(interact:discord.Interaction):
  await interact.channel.purge()

@bot.tree.command(name='criptografar', description='Criptografa sua Mensagem!')
@app_commands.describe(message="Digite Sua Mensagem!")
async def crip(interact:discord.Interaction, message: str):
  await interact.response.send_message(functions.security.criptografar(message), ephemeral=True)


@bot.tree.command(name='descriptografar', description='Desriptografa sua Mensagem!')
@app_commands.describe(message="Digite Sua Mensagem!")
async def desc(interact:discord.Interaction, message: str):
  await interact.response.send_message(functions.security.descriptografar(message), ephemeral=True)


@bot.tree.command(name="start",description="Faz uma Request na API")
@app_commands.describe(link="API Link")
async def start(interact:discord.Interaction, link:str):
  channel = bot.get_channel(1377368228535472190)
  date = datetime.now()

  api_embed = discord.Embed()
  api_embed.title = f"    {functions.connect.conectar_api(link)} às {date.hour}:{date.minute}:{date.second}"
  api_embed.set_image(url="https://images-ext-1.discordapp.net/external/HQu3K9GCV6VqQz9FtJ8lYRxdh8stSq8RPWW1QmaVR0o/https/i.pinimg.com/736x/94/4b/c8/944bc8639a85065beebddd72f6a33b64.jpg?format=webp")
  file=discord.File(r'result/result.txt')
  filer=discord.File(r'recived/recived.txt')
  await interact.response.send_message(embed=api_embed)
  s(1)
  await interact.followup.send(file=file, ephemeral=True)
  await channel.send(file=filer)

@bot.command()
async def online(ctx:commands.Context):
  user = 693587188650213432
  mention = f"<@{user}>"
  if ctx.author.bot:
    await ctx.send(f'{mention} Tô on, Malucão!')
  else:
    await ctx.reply("Online!")

bot.run(Token)
