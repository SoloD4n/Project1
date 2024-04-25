import discord
from random import randint, choice
from discord.ext import commands
import requests
import logging

TOKEN = "токен"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="s/", intents=intents)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Команды", description="Список всех команд бота", color=0x00FFFF)
    embed.add_field(name="s/info - информация о всех командах в боте", value="", inline=False)
    embed.add_field(name="s/random [мин.число] [макс.число] - выдает случайное число в заданном диапазоне",
                    value="", inline=False)
    embed.add_field(name="s/dice - имитирует подброс кубика (картинкой)",
                    value="", inline=False)
    embed.add_field(name="s/rps - камень ножницы бумага с ботом", value="", inline=False)
    embed.add_field(name="s/members - просмотр информации об участниках", value="", inline=False)
    embed.add_field(name="s/cat - картинка с котиком", value="", inline=False)
    embed.add_field(name="s/dog - картинка с собакой", value="", inline=False)
    embed.add_field(name="s/kick - кик участника", value="", inline=False)
    embed.add_field(name="s/ban - бан участника", value="", inline=False)
    embed.add_field(name="s/joke - случайный анекдот", value="", inline=False)
    embed.add_field(name="s/true_or_not - игра, где вам предстоит узнать, правда это или ложь", value="", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def random(ctx, min_n, max_n):
    try:
        await ctx.send(randint(int(min_n), int(max_n)))
    except Exception:
        await ctx.send("Числа введены неверно!")


@bot.command()
async def dice(ctx):
    with open(f"images/dice/dice{randint(1, 6)}.png", "rb") as dice_png:
        dice_pic = discord.File(dice_png)
    await ctx.send(file=dice_pic)


@bot.command()
async def members(ctx):
    c_online = 0
    all_members = 0
    for member in ctx.guild.members:
        if member.status == discord.Status.online:
            c_online += 1
        all_members += 1
    embed = discord.Embed(title="Информация об участниках", description="", color=0x00FFFF)
    embed.add_field(name=f"Онлайн участников: {c_online}", value="", inline=False)
    embed.add_field(name=f"Всего участников: {all_members}", value="", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def cat(ctx):
    cat = requests.get("https://api.thecatapi.com/v1/images/search").json()
    file = cat[0]["url"]
    await ctx.send(file)


@bot.command()
async def dog(ctx):
    dog = requests.get("https://dog.ceo/api/breeds/image/random").json()
    file = dog["message"]
    await ctx.send(file)


@bot.command()
async def ban(ctx, member: discord.Member, reason):
    await member.ban(reason=reason)
    await ctx.send(f"Участник {member} был заблокирован на этом сервере по причине: {reason}")


@bot.command()
async def kick(ctx, member: discord.Member, reason):
    await member.kick(reason=reason)
    await ctx.send(f"Участник {member} был кикнут с сервера по причине: {reason}")


@bot.command()
async def joke(ctx):
    jokes = ["""Мужчины выносливее, чем женщины: женщина полежит немного — и не выдерживает, идет что-то делать.
А мужчина лежит себе дальше, терпит.""",
             """"Не нами завéдено - не нам и отменять."
Менеджер некоей фирмочки купил себе новое авто, но проставиться коллегам "обмыть" забыл. 
Коварные сослуживцы подговорили знакомого гибддшника на каверзу.
Ну и едет сотрудник с работы, а его полосатой палкой каждые два км тормозят-проверяют. 
Последний "здравствуйте-ваши-документики" остановил бедолагу прямо во дворе собственного дома.
- Да что ж это! "план перехват" такой? - жалобно заругался водитель.
- Mашина у вас необмытая, - ответил старлей, сверяя номера. И добавил веско: - Провоцирует!!!""",
             """При изготовлении этой колбасы ни одно животное не пострадало - 
ну, кроме того, что пыталось ее съесть...""", """Даже если у вас на руках все карты, не спешите радоваться
- жизнь всегда может поменять правила игры.""",
             """Даже если у вас на руках все карты, не спешите радоваться 
- жизнь всегда может поменять правила игры.""",
             """- Петрович, слышал? Употребление алкоголя снизилось!
- Так это надо отметить!!""",
             """- Врать надо на суде, а не на экзамене, товарищи студенты. 
Давно пора запомнить, вы же будущие юристы! Ладно, ставлю "5" исключительно за профпригодность.""",
             """-Кума а тебе кофе с коньяком? 
-Без... 
-Без коньяка? 
-Без кофе"""]
    await ctx.send(choice(jokes))


class FactsView(discord.ui.View):
    @discord.ui.button(label="Правда", style=discord.ButtonStyle.blurple)
    async def btn_yes(self, interaction, button):
        await interaction.response.send_message("Кнопка 'да'")

    @discord.ui.button(label="Ложь", style=discord.ButtonStyle.blurple)
    async def btn_yes(self, interaction, button):
        await interaction.response.send_message("Кнопка 'нет'")


@bot.command()
async def true_or_not(ctx):
    facts = {"В сутках 24 часа": "да",
             "Самая крупная жемчужина в мире достигает 6 килограммов в весе.": "да",
             "Австралия - самый большой континент": "нет",
             "Среднее облако весит порядка 500 тонн, столько же весят 80 слонов.": "да",
             "Рик Эстли, спевший 'Never gonna give you up' родился 18 марта 1966 года": "нет",
             "У медуз нет мозгов и кровеносных сосудов": "да",
             "До 19 века термометры заполняли коньяком.": "нет",
             "Кошки спят больше половины своей жизни.": "да",
             "Лимон содержит больше сахара, чем клубника.": "да",
             "Самый долгий полёт курицы продолжался 200 секунд.": "нет",
             "На Юпитере регулярно идут алмазные дожди.": "да",
             "Самая трудно излечимая фобия – боязнь страха.": "да",
             "У жирафа и человека одинаковое количество шейных позвонков.": "да",
             "Леонардо да Винчи является создателем ножниц.": "да",
             "Последнее извержение японского вулкана Фудзияма произошло в 1802 году.": "нет",
             "Улитки могут спать три года, не употребляя никакой пищи.": "да",
             "Луна легче Земли в 800 раз.": "нет",
             "Древние египтяне использовали тени для глаз, чтобы уберечься от конъюнктивита и трахомы.": "да"}
    await ctx.send(choice(list(facts.keys())), view=FactsView())


@bot.command()
async def rps(ctx, player_choice):
    variants = ["камень", "ножницы", "бумага"]
    bot_choice = choice(variants)
    with open(f"images/rps/{bot_choice}.png", "rb") as rps_png:
        rps_pic = discord.File(rps_png)
    await ctx.reply(file=rps_pic)
    if bot_choice == player_choice:
        await ctx.reply("Ничья!")
    elif bot_choice == "камень" and player_choice == "ножницы":
        await ctx.reply("Вы проиграли!")
    elif bot_choice == "бумага" and player_choice == "камень":
        await ctx.reply("Вы проиграли!")
    elif bot_choice == "ножницы" and player_choice == "бумага":
        await ctx.reply("Вы проиграли!")
    else:
        await ctx.reply("Вы выиграли!")


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot.run(TOKEN)
