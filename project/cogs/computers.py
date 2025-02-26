import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Range, Param

import logging

from project.bot import bot
from project.computers import train, power_train, offline_train, damage, oneshot, indicators
from project.cogs import help
from project.temporary_common_storage import Context
from project.structures import Person
from project import views

logger = logging.getLogger(__name__)


@bot.slash_command(name="train", description="Online train")
async def train_slash_command(inter: ApplicationCommandInteraction,
                              lvl: Range[int, 1, 1000],
                              stat: Range[int, 1, 1000],
                              buffs: Range[int, -100, 100] = 0,
                              weapon_atk: Range[int, 4, 100] = 5):
    ctx = Context()
    person = Person(ctx=ctx,
                    lvl=lvl,
                    stat=stat,
                    buffs=buffs,
                    weapon_atk=weapon_atk)
    battle = train.BattleModel(person=person)
    embed = await battle.view(False)
    view = views.TrainView(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="ptrain", description="Online power train")
async def ptrain_slash_command(inter: ApplicationCommandInteraction,
                               lvl: Range[int, 1, 1000],
                               stat: Range[int, 1, 1000],
                               buffs: Range[int, -100, 100] = 0,
                               weapon_atk: Range[int, 4, 100] = 5,
                               class_type: str = Param(
                                   choices={"melee": "melee", "distance": "distance", "magic": "magic"}),
                               tick: Range[int, 1, 5] = 4):
    ctx = Context()
    person = Person(ctx=ctx,
                    lvl=lvl,
                    stat=stat,
                    buffs=buffs,
                    weapon_atk=weapon_atk,
                    class_type=class_type)
    battle = power_train.BattleModel(person=person,
                                     tick=tick)
    embed = await battle.view(False)
    view = views.TrainView(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="offline", description="Can only take EITHER `stat2` or `hours`")
async def offline_slash_command(inter: ApplicationCommandInteraction,
                                current_stat: Range[int, 1, 1000],
                                target_stat: Range[int, 1, 1000] = None,
                                hours: Range[int, 1, 1000] = None):
    if (target_stat is not None and hours is not None) or (target_stat is None and hours is None):
        await inter.response.send_message(
            "Invalid input. Please provide **either** a `target_stat` or `hours` value, but not both or neither.",
            ephemeral=True)

    elif target_stat is not None:
        if current_stat < target_stat:
            offline = offline_train.OfflineModel(current_stat=current_stat, target_stat=target_stat)
            embed = await offline.view()
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("Target stat must be higher than the current stat.", ephemeral=True)

    elif hours is not None:
        offline = offline_train.OfflineModel(current_stat=current_stat, hours=hours)
        embed = await offline.view()
        await inter.response.send_message(embed=embed)


@bot.slash_command(name="dmg", description="damage calc")
async def damage_slash_command(inter: ApplicationCommandInteraction,
                               lvl: Range[int, 1, 1000],
                               stat: Range[int, 1, 1000],
                               buffs: Range[int, -100, 100] = 0,
                               weapon_atk: Range[int, 4, 100] = 5,
                               class_type: str = Param(
                                   choices={"melee": "melee", "distance": "distance", "magic": "magic"})):
    ctx = Context()
    person = Person(ctx=ctx,
                    lvl=lvl,
                    stat=stat,
                    buffs=buffs,
                    weapon_atk=weapon_atk,
                    class_type=class_type)
    battle = damage.BattleModel(person=person)
    embed = await battle.view(False)
    view = views.MobView(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="oneshot", description="oneshot calc")
async def oneshot_slash_command(inter: ApplicationCommandInteraction,
                                lvl: Range[int, 1, 1000],
                                stat: Range[int, 1, 1000],
                                buffs: Range[int, -100, 100] = 0,
                                weapon_atk: Range[int, 4, 100] = 5,
                                class_type: str = Param(
                                    choices={"melee": "melee", "distance": "distance", "magic": "magic"}),
                                consistency: Range[int, 1, 100] = 80):
    ctx = Context()
    person = Person(ctx=ctx,
                    lvl=lvl,
                    stat=stat,
                    buffs=buffs,
                    weapon_atk=weapon_atk,
                    class_type=class_type)
    battle = oneshot.OneshotModel(person=person,
                                  consistency_need=consistency)
    embed = await battle.view(False)
    view = views.MobView(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="lvl_info", description="Exp and skull")
async def level_info_slash_command(inter: ApplicationCommandInteraction,
                                   lvl: Range[int, 1, 1000]):
    indicator = indicators.IndicatorsModel(lvl=lvl)
    embed = await indicator.view()

    await inter.response.send_message(embed=embed)


@bot.slash_command(name="help", description="Brief description of all commands")
async def help_slash_command(inter: disnake.ApplicationCommandInteraction):
    help_model = help.HelpModel()
    embed = help_model.view()

    await inter.response.send_message(embed=embed)


@bot.slash_command(name="github", description="link to the my github")
async def github_slash_command(inter: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(title="<:mini_slime:1194708281319510017> Kotiklina' Rucoy Calculator",
                          description="""Here is the code for this bot: 
                          https://github.com/KotikLina/RucoyOnlineCalculator 
                          
                          <:mini_slime:1194708281319510017>
                          I deleted `__main__.py` and it cannot be run without me. It wasn't necessary, but I decided to do so for some reason.""")
    await inter.response.send_message(embed=embed)
