import discord
import os
import asyncio
import random

client = discord.Client()
version = "0.1"

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

def apagado(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print (client.user.name)
    print (client.user.id)
    print(f"Bot Version: {version}")
    print("=================================")
    await client.change_presence(game=discord.Game(name="no betamc.com.br"))
@client.event
async def on_message(message):
#MODERATION
    ##MODERAÇÃO
    if message.content.lower().startswith('/moderação'):
        role = discord.utils.get(message.server.roles, name='💎 Staff')
        if not role in message.author.roles:
            return await client.send_message(message.channel, "Você precisa ter o cargo `💎 Staff` para executar este comando!")
        embed = discord.Embed(
            title="Comandos de moderação:",
            color=0x0d488a,
            description="\n"
                        "/ban <usuário> » Banimento permanentemente do discord.\n"
                        "/kick <usuário> » Expulsão do discord.\n"
                        "/mute <usuário> » Mute permanentemente do discord\n"
                        "/unmute <usuário> » Unmute do discord\n"
                        "\n"
                        "**Bugs ou sugestões contate o Bruno no privado.**"
        )
        embed.set_author(
            name="BetaMC",
            icon_url=client.user.avatar_url
        )
        embed.set_footer(
            text="Copyright © 2018 Beta Servidores",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/180796040708882432/d18bacdc9165e7fcf47ab746ceacdc44.webp?size=1024')

        await client.send_message(message.channel, "Olá {}, foi enviado todos os comandos de moderação no seu privado!".format(message.author.mention))
        await client.send_message(message.author, embed=embed)
    ##BAN
    elif message.content.lower().startswith('/ban'):
        role = discord.utils.get(message.server.roles, name='💎 Staff')
        if not role in message.author.roles:
            return await client.send_message(message.channel, ":x: Você deverá possuir o cargo `💎 Staff` para executar este comando!")
        membro = message.mentions[0]
        embedmsg = discord.Embed(
            title="⚠ Punição!"
                  "",
            description="O membro {} foi punido do servidor!".format(membro.name),
            color=0x0d488a,
        )
        embedmsg.set_thumbnail(url=membro.avatar_url)

        await client.send_message(message.channel, embed=embedmsg)
        await client.ban(membro)
    ##KICK
    elif message.content.lower().startswith('/kick'):
        role = discord.utils.get(message.server.roles, name='💎 Staff')
        if not role in message.author.roles:
            return await client.send_message(message.channel,
                                             ":x: Você deverá possuir o cargo `💎 Staff` para executar este comando!")
        membro = message.mentions[0]
        embedmsg = discord.Embed(
            title="⚠ Punição!"
                  "",
            description="O membro {} foi expulso do servidor!".format(membro.name),
            color=0x0d488a,
        )
        embedmsg.set_thumbnail(url=membro.avatar_url)
        await client.kick(membro)
        await client.send_message(message.channel, embed=embedmsg)
    ##MUTE
    elif message.content.lower().startswith('/mute'):
        role = discord.utils.get(message.server.roles, name='💎 Staff')
        if not role in message.author.roles:
            return await client.send_message(message.channel,
                                             ":x: Você deverá possuir o cargo `💎 Staff` para executar este comando!")
        membro = message.mentions[0]
        embedmsg = discord.Embed(
            title="⚠ Punição!"
                  "",
            description="O membro {} foi mutado!".format(membro.name),
            color=0x0d488a,
        )
        embedmsg.set_thumbnail(url=membro.avatar_url)

        await client.send_message(message.channel, embed=embedmsg)
        cargo = discord.utils.get(message.author.server.roles, name='Muted')
        await client.add_roles(membro, cargo)
    ##UNMUTE
    elif message.content.lower().startswith('/unmute'):
        role = discord.utils.get(message.server.roles, name='💎 Staff')
        if not role in message.author.roles:
            return await client.send_message(message.channel,
                                             ":X: Você deverá possuir o cargo `💎 Staff` para executar este comando!")
        membro = message.mentions[0]
        embedmsg = discord.Embed(
            title="✔ Impunição!"
                  "",
            description="O membro {} foi desmutado!".format(membro.name),
            color=0x0d488a,
        )
        embedmsg.set_thumbnail(url=membro.avatar_url)

        await client.send_message(message.channel, embed=embedmsg)
        cargo = discord.utils.get(message.author.server.roles, name='Muted')
        await client.remove_roles(membro, cargo)
#SUPERIORES
    if message.content.lower().startswith('/administração'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        embed = discord.Embed(
            title="Comandos de administração:",
            color=0x0d488a,
            description="\n"
                        "``/ban <usuário>`` » Banimento permanentemente do discord.\n"
                        "``/kick <usuário>`` » Expulsão do discord.\n"
                        "``/mute <usuário>`` » Mute permanentemente do discord\n"
                        "``/unmute <usuário>`` » Unmute do discord\n"
                        "``/apagar <quantidade>`` » Apague de 1 a 100 mensagens\n"
                        "``/jogando <nome>`` » Atualize o status jogando do bot\n"
                        "``/transmitindo <nome>`` » Atualize o status de transmissão do bot\n"
                        "``/assistindo <nome>`` » Atualize o status assistindo do bot\n"
                        "``/bc <mensagem>`` » Bot repete o que foi dito\n"
                        "``/aviso <mensagem>`` » Comando próprio para aviso\n"
                        "``/votar <mensagem>`` » Bot repete a mensagem e reage automaticamente com like/deslike\n"
                        "``/sorteio`` » Inicia um sorteio de 1 a 500\n\n"
                        "**CARGOS:**\n\n"
                        "``/groupadd <cargo> <usuário>`` » Adicione um cargo a alguém\n"
                        "``/groupremove <cargo> <usuário>`` » Remova um cargo de alguém\n"
                        "``/demotar <usuário>`` » Demote alguém (MOD, TRIAL E AJUDANTE)\n"
                        "``/newmod <usuário>`` » Seta a tag mod, staff e remove a membro\n"
                        "``/newtrial <usuário>`` » Seta a tag trial, staff e remove a membro\n"
                        "``/newhelper <usuário>`` » Seta a tag ajudante, staff e remove a membro\n"
                        "\n"
                        "======================================================"
                        "\n\n"
                        "**Bugs ou sugestões contate o Bruno no privado.**")
        embed.set_author(
            name="BetaMC",
            icon_url=client.user.avatar_url)
        embed.set_footer(
            text="Copyright © 2018 Beta Servidores",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1")
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/180796040708882432/d18bacdc9165e7fcf47ab746ceacdc44.webp?size=1024')
        await client.send_message(message.channel, "Olá {}, foi enviado todos os comandos de administração no seu privado!".format(message.author.mention))
        await client.send_message(message.author, embed=embed)
    ##APAGAR
    if message.content.lower().startswith('/apagar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        deletados = message.content.strip('/apagar ')
        deletados = apagado(deletados)
        if message.author.top_role:
            if deletados <= 1000:
                msg_author = message.author.mention
                await client.delete_message(message)
                await asyncio.sleep(1)
                deleted = await client.purge_from(message.channel, limit=deletados)
                botmsgdelete = await client.send_message(message.channel, 'Foi deletado total de {} mensagens!'.format(len(deleted), msg_author))
                await asyncio.sleep(5)
                await client.delete_message(botmsgdelete)

            else:
                botmsgdelete = await client.send_message(message.channel, 'Use /apagar <1 a 1000>')
                await asyncio.sleep(5)
                await client.delete_message(message)
                await client.delete_message(botmsgdelete)
    ##JOGANDO
    if message.content.startswith('/jogando'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Status de jogo alterado para: " + game + " ")
    ##TRANSMITINDO
    if message.content.startswith('/transmitindo'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        game = message.content[14:]
        await client.change_presence(game=discord.Game(name=game, url='https://twitch.tv/TheDiretor', type=1))
        await client.send_message(message.channel, "Status de transmissão alterado para: " + game + " ")
    ##ASSISTINDO
    if message.content.startswith('/assistindo'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        game = message.content[11:]
        await client.change_presence(game=discord.Game(name=game, type=3), status=discord.Status.dnd)
        await client.send_message(message.channel, "Status assistindo alterado para: " + game + " ")
    ##BC
    if message.content.lower().startswith("/bc"):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        msg = message.content[4:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    ##AVISO
    if message.content.startswith('/aviso'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        await client.delete_message(message)
        try:
            user = message.author
            msg = message.content[7:]

            embed = discord.Embed(
                title="⚠ AVISO!",
                description="{}".format(msg),
                color=0x003aff
            )
            embed.set_footer(
                text="Enviado pelo: " + user.name,
                icon_url=user.avatar_url
            )

            await client.send_message(message.channel, "@everyone")
            await client.send_message(message.channel, embed=embed)
        finally:
            pass
    ##SORTEIO
    if message.content.lower().startswith('/sorteio'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        choice = random.randint(1, 500)
        embedsorteio = discord.Embed(title='🎉 Sorteio', description='O ganhador do sorteio foi o número {}, Parabéns! Aguarde um superior te chamar no privado para receber seu prêmio! (Não fique floodando nenhum membro da equipe, apenas aguarde)'.format(choice), colour=0x003afff)
        await client.send_message(message.channel, embed=embedsorteio)
    ##VOTAR
    elif message.content.lower().startswith('/votar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        msg = message.content[7:2000]
        botmsg = await client.send_message(message.channel, msg)
        await client.add_reaction(botmsg, '👍')
        await client.add_reaction(botmsg, '👎')
        await client.delete_message(message)
#GRUPOS
    elif message.content.lower().startswith('/groupadd staff'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='💎 Staff')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `staff` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove staff'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='💎 Staff')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `staff` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd trial'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎓 Trial-Mod')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `trial` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove trial'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎓 Trial-Mod')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `trial` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd ajudante'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🔹Ajudante')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `ajudante` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove ajudante'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🔹Ajudante')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `ajudante` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd mod'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🍀Moderador')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `moderador` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove mod'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🍀Moderador')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `moderador` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd builder'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🔨 Construtor')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `construtor` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove builder'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🔨 Construtor')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `construtor` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd dzn'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎨 Designer')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `designer` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove dzn'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎨 Designer')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `designer` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd yt+'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='📹 Youtuber+')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `youtuberplus` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove yt+'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='📹 Youtuber+')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `youtuberplus` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd yt'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='📹 Youtuber')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `youtuber` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove yt'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='📹 Youtuber')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `youtuber` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd beta'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🏆 Beta')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `beta` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove beta'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🏆 Beta')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `beta` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd titan'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='⚡ Titan')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `titan` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove titan'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='⚡ Titan')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `titan` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd elite'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎲 Elite')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `elite` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove elite'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎲 Elite')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `elite` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd legend'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎈 Legend')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `legend` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove legend'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='🎈 Legend')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `legend` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd hero'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='👾 Hero')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `hero` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove hero'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='👾 Hero')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `hero` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd passe livre'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='♣ Passe livre')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `passe livre` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove passe livre'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='♣ Passe livre')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `passe livre` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd verificado'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='✔ Verificado')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `verificado` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove verificado'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='✔ Verificado')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `verificado` do membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupadd membro'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='👤 Membro')
        await client.add_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi adicionado o grupo `membro` ao membro {}!'.format(user.mention))

    elif message.content.lower().startswith('/groupremove membro'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='👤 Membro')
        await client.remove_roles(user, cargo)
        await client.send_message(message.channel, '✔ Foi removido o grupo `membro` do membro {}!'.format(user.mention))
    ##DEMOTAR
    elif message.content.lower().startswith('/demotar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')

        user = message.mentions[0]

        cargo = discord.utils.get(message.author.server.roles, name='👤 Membro')
        await client.add_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='💎 Staff')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='👮 ModPlus')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='💥 Gerente')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='🍁 Diretor')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='🍀Moderador')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='🎓 Trial-Mod')
        await client.remove_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='🔹Ajudante')
        await client.remove_roles(user, cargo)

        await client.send_message(message.channel, '✔ {} foi demotado hihihihihi'.format(user.mention))

    ##NEW-MOD
    elif message.content.lower().startswith('/newmod'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui acesso à este comando!')
        user = message.mentions[0]

        cargo = discord.utils.get(message.author.server.roles, name='🍀Moderador')
        await client.add_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='💎 Staff')
        await client.add_roles(user, cargo)

        cargo = discord.utils.get(message.author.server.roles, name='👤 Membro')
        await client.remove_roles(user, cargo)

        await client.send_message(discord.Object(id='444996049522655264'), '**{}** Integra a equipe ocupando o cargo Moderador!'.format(user.name))
    ##VERIFICADO
    elif message.content.lower().startswith('!ativartag verificado'):
        await client.delete_message(message)
        user = message.author
        cargo = discord.utils.get(message.author.server.roles, name='✔ Verificado')
        await client.add_roles(user, cargo)
        await client.send_message(message.author, '✔ Sua tag `verificado` foi ativada com sucesso {}!'.format(user.name))
        await client.send_message(discord.Object(id='420086372167319562'),'**AVISO!**\n\n{} ativou a tag verificado!'.format(user.mention))

#OTHERS
    ##SERVERINFO
    if message.content.lower().startswith('/serverinfo'):
        server = message.server
        embedserver = discord.Embed(
            title='Informaçoes do Servidor',
            color=0x003aff,
            descripition='Essas são as informaçoes\n')
        embedserver = discord.Embed(name="{} Server ".format(message.server.name), color=0x551A8B)
        embedserver.add_field(name="Nome:", value=message.server.name, inline=True)
        embedserver.add_field(name="Dono:", value=message.server.owner.mention)
        embedserver.add_field(name="ID:", value=message.server.id, inline=True)
        embedserver.add_field(name="Cargos:", value=len(message.server.roles), inline=True)
        embedserver.add_field(name="Membros:", value=len(message.server.members), inline=True)
        embedserver.add_field(name="Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"))
        embedserver.add_field(name="Emojis:", value=f"{len(message.server.emojis)}/100")
        embedserver.add_field(name="Região:", value=str(message.server.region).title())
        embedserver.set_thumbnail(url=message.server.icon_url)
        embedserver.set_footer(text="By: brunoqq")
        await client.send_message(message.channel, embed=embedserver)
    ##USERINFO
    if message.content.startswith('/user'):
            try:
                user = message.mentions[0]
                userjoinedat = str(user.joined_at).split('.', 1)[0]
                usercreatedat = str(user.created_at).split('.', 1)[0]

                userembed = discord.Embed(
                    title="Nome",
                    description=user.name,
                    color=0x003aff
                )
                userembed.set_thumbnail(url=user.avatar_url)
                userembed.set_author(
                    name="Informações do usuário {}".format(user.name)
                )
                userembed.add_field(
                    name="Entrou no servidor em",
                    value=userjoinedat
                )
                userembed.add_field(
                    name="Jogando",
                    value=user.game
                )
                userembed.add_field(
                    name="Criou seu Discord em",
                    value=usercreatedat
                )
                userembed.add_field(
                    name="TAG",
                    value=user.discriminator
                )

                await client.send_message(message.channel, embed=userembed)
            except IndexError:
                await client.send_message(message.channel, "Usuário não encontrado!")
            except:
                await client.send_message(message.channel, "Erro, desculpe. ")
            finally:
                pass
    ##AVATAR
    elif message.content.lower().startswith('/avatar'):
        try:
            membro = message.mentions[0]
            avatarembed = discord.Embed(
                title="",
                color=0x003aff,
                description="**[Clique aqui](" + membro.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed.set_author(name=membro.name)
            avatarembed.set_image(url=membro.avatar_url)
            await client.send_message(message.channel, embed=avatarembed)
        except:
            avatarembed2 = discord.Embed(
                title="",
                color=0x003aff,
                description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed2.set_author(name=message.author.name)
            avatarembed2.set_image(url=message.author.avatar_url)
            await client.send_message(message.channel, embed=avatarembed2)
    ##AJUDA
    if message.content.lower().startswith('/ajuda'):
        embed = discord.Embed(
            title="",
            color=0x003aff,
            description="Olá, obrigado por fazer parte de nosso discord BetaMC! Segue abaixo algumas informações da rede que pode te ajudar! 😉\n"
                        "\n"
                        "IP: betamc.com.br\n"
                        "\n"
                        "Site: [clique aqui!](https://betamc.com.br/)\n"
                        "\n"
                        "Loja: [clique aqui!](https://loja.betamc.com.br/)\n"
                        "\n"
                        "Twitter da rede: [clique aqui!](https://twitter.com/BetaServidores)\n"
                        "\n"
                        "Fórum: [clique aqui!](https://forum.betamc.com.br/)\n"
                        "\n"
                        "Caso precise de outro tipo de ajuda contate um membro da equipe!"
        )
        embed.set_author(
            name="BetaMC",
            icon_url=client.user.avatar_url
        )
        embed.set_footer(
            text="Copyright © 2018 BetaMC",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei umas informações no privado! 😘".format(
            message.author.mention))
        await client.send_message(message.author, embed=embed)
@client.event
async def on_member_join(member):
    grupo = discord.utils.find(lambda g: g.name == "👤 Membro", member.server.roles)
    await client.add_roles(member, grupo)

    embed = discord.Embed(
        title="",
        color=0x0d488a,
        description="**Seja bem-vindo ao nosso Discord, divirta-se.**\n"
                                        "\n"
                                        "**IP: betamc.com.br**\n"
                                        "**Site:** [Clique aqui](https://betamc.com.br/)\n"
                                        "**Loja:** [Clique aqui](https://loja.betamc.com.br/)\n"
                                        "**Fórum:** [Clique aqui](https://forum.betamc.com.br/)\n"
                                        "**Twitter da rede:** [Clique aqui](https://twitter.com/BetaServidores)"
    )
    embed.set_author(
        name="Beta Servidores",
        icon_url=client.user.avatar_url
    )
    embed.set_footer(
        text="Copyright © 2018 BetaMC",
        icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
    )

    await client.send_message(member, embed=embed)

client.run(token)
