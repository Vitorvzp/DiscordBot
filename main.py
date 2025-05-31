from dotenv import load_dotenv as load
from os import getenv as get
from os import path as p
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

@bot.event
async def on_member_join(member: discord.Member):
    list_users = [1038983303555977297]
    user_id = member.id
    guild = member.guild
    viwer = discord.utils.get(guild.roles, id=1377349468902395904)
    admin = discord.utils.get(guild.roles, id=1263291925386231990)
    if user_id in list_users:
        await member.add_roles(admin)
    else:
        await member.add_roles(viwer)

@bot.tree.command(name='help', description='Mostra Todos os Comandos')
async def ajuda(interact:discord.Interaction):
   ch1 = bot.get_channel(1262107519686283305)
   ch2 = bot.get_channel(1377355498852188250)
   await interact.response.send_message(f"# EXEMPLOS:```/clear``````/criptografar Olá``````/descriptografar zMá```Usado em {ch1.mention}", ephemeral=True)
   await interact.followup.send(f"# EXEMPLOS: ```/start https://api-c783.onrender.com/Usuarios``````/start https://api-c783.onrender.com/Nomes```Usado em {ch2.mention}", ephemeral=True)

@bot.tree.command(name='clear', description='Limpa Todas as Mensagens do Canal!')
async def clear(interact:discord.Interaction):
  channel = bot.get_channel(1377783988353241218)
  roles = interact.user.roles
  role = discord.utils.get(interact.guild.roles, id=1377302864350675024)
  not_delete = [1376737654749528135, 1377368228535472190, 1377402614404223076, 1377783988353241218]
  if role in roles and interact.channel_id not in not_delete:
    await interact.channel.purge()
    await channel.send(f'<@693587188650213432> {interact.user.mention} Apagou as Mensagens de {interact.channel.mention}')
  elif interact.user.id == 693587188650213432 :
    await interact.channel.purge()
    await channel.send(f'<@693587188650213432> {interact.user.mention} Apagou as Mensagens de {interact.channel.mention}')
  elif role not in roles:
     await interact.response.send_message("Seu Cargo Não Tem Permissão Suficiente!", ephemeral=True)
  elif interact.channel_id in not_delete:
     await interact.response.send_message("As Mensagens Deste Canal Só Podem Ser Apagadas Pelo Dono!", ephemeral=True)
  else:
     await interact.response.send_message("ERRO!")

@bot.tree.command(name='criptografar', description='Criptografa sua Mensagem!')
@app_commands.describe(message="Digite Sua Mensagem!")
async def crip(interact:discord.Interaction, message: str):
  channel = bot.get_channel(1377783988353241218)
  mention = bot.get_channel(1262107519686283305)
  roles = interact.user.roles
  role = discord.utils.get(interact.guild.roles, id=1377302864350675024)
  if role in roles and interact.channel_id == 1262107519686283305 or interact.user.id == 693587188650213432:
    await interact.response.send_message(functions.security.criptografar(message), ephemeral=True)
    await channel.send(f"<@693587188650213432>, {interact.user.mention} Criptografou a Mensagem: ```{message}``` (no canal {interact.channel.mention})")
  elif role not in roles:
     await interact.response.send_message("Seu Cargo Não Tem Permissão Suficiente!", ephemeral=True)
  elif interact.channel_id != 1262107519686283305:
     await interact.response.send_message(f"Neste Canal Não Fucina, Tente em {mention.mention}", ephemeral=True)
  else:
     await interact.response.send_message("ERRO!", ephemeral=True)

@bot.tree.command(name='descriptografar', description='Desriptografa sua Mensagem!')
@app_commands.describe(message="Digite Sua Mensagem!")
async def desc(interact:discord.Interaction, message: str):
  channel = bot.get_channel(1377783988353241218)
  mention = bot.get_channel(1262107519686283305)
  roles = interact.user.roles
  role = discord.utils.get(interact.guild.roles, id=1377302864350675024)
  if role in roles and interact.channel_id == 1262107519686283305 or interact.user.id == 693587188650213432:
    await interact.response.send_message(functions.security.descriptografar(message), ephemeral=True)
    await channel.send(f"<@693587188650213432>, {interact.user.mention} Desriptografou a Mensagem: ```{message}``` (no canal {interact.channel.mention})")
  elif role not in roles:
     await interact.response.send_message("Seu Cargo Não Tem Permissão Suficiente!", ephemeral=True)
  elif interact.channel_id != 1262107519686283305:
     await interact.response.send_message(f"Neste Canal Não Fucina, Tente em {mention.mention}", ephemeral=True)
  else:
     await interact.response.send_message("ERRO!", ephemeral=True)

@bot.tree.command(name="start",description="Faz uma Request na API")
@app_commands.describe(link="API Link")
async def start(interact:discord.Interaction, link:str):
  channel = bot.get_channel(1377368228535472190)
  mention = bot.get_channel(1262107519686283305)
  roles = interact.user.roles
  role = discord.utils.get(interact.guild.roles, id=1377302864350675024)
  if role in roles and interact.channel_id == 1262107519686283305 or interact.user.id == 693587188650213432:
    date = datetime.now()
    api_embed = discord.Embed()
    api_embed.title = f"    {functions.connect.conectar_api(link)} às {date.hour}:{date.minute}:{date.second}"
    api_embed.set_image(url="https://images-ext-1.discordapp.net/external/HQu3K9GCV6VqQz9FtJ8lYRxdh8stSq8RPWW1QmaVR0o/https/i.pinimg.com/736x/94/4b/c8/944bc8639a85065beebddd72f6a33b64.jpg?format=webp")
    paths = ['result', 'recived']
    file=discord.File(p.join(paths[0], "result.txt"))
    filer=discord.File(p.join(paths[1], "recived.txt"))
    await interact.response.send_message("Aguarde", ephemeral=True)
    await interact.followup.send(embed=api_embed, ephemeral=True)
    s(1)
    await interact.followup.send(file=file, ephemeral=True)
    await channel.send(file=filer)
    ch = bot.get_channel(1377783988353241218)
    ch2 = bot.get_channel(1377368228535472190)
    await ch.send(f"<@693587188650213432>, {interact.user.mention} usou /start no link ```{link}``` Verifique {ch2.mention}")
  elif role not in roles:
     await interact.response.send_message("Seu Cargo Não Tem Permissão Suficiente!", ephemeral=True)
  elif interact.channel_id != 1262107519686283305:
     await interact.response.send_message(f"Neste Canal Não Fucina, Tente em {mention.mention}", ephemeral=True)
  else:
     await interact.response.send_message("ERRO!", ephemeral=True)
@start.autocomplete('link')
async def complete(interact:discord.Interaction, recived:str):
  links = ['https://api-c783.onrender.com/Usuarios', 'https://api-c783.onrender.com/Nomes']
  options = []
  for link in links:
    option = app_commands.Choice(name=link, value=link)
    options.append(option)
  return options[:]

@bot.command()
async def online(ctx:commands.Context):
  user = 693587188650213432
  mention = f"<@{user}>"
  await ctx.reply(f'{mention} Tô on Malucão!')



bot.run(Token)
