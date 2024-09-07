from disnake.ext import commands
import disnake

import TrainModel
import PowerTrainModel
import Offline
import IndicatorsModel
import temporary_common_storage


command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.InteractionBot(intents=disnake.Intents.all())


@bot.slash_command(name="train", description="Online train")
async def train_slash_command(inter: disnake.ApplicationCommandInteraction,
                              lvl: commands.Range[int, 0, 1000],
                              stat: commands.Range[int, 0, 1000],
                              buffs: commands.Range[int, -100, 100] = 0,
                              weapon_atk: commands.Range[int, 4, 100] = 5):
    battle = TrainModel.BattleModel(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk)

    embed = await battle.view(False)
    view = View(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="ptrain", description="Online power train")
async def ptrain_slash_command(inter: disnake.ApplicationCommandInteraction,
                               lvl: commands.Range[int, 0, 1000],
                               stat: commands.Range[int, 0, 1000],
                               class_type: str = commands.Param(
                                   choices={"melee": "melee", "distance": "distance", "magic": "magic"}),
                               buffs: commands.Range[int, -100, 100] = 0,
                               weapon_atk: commands.Range[int, 4, 100] = 5,
                               tick: commands.Range[int, 1, 5] = 4):
    battle = PowerTrainModel.BattleModel(lvl=lvl, stat=stat, buffs=buffs, weapon_atk=weapon_atk, tick=tick,
                                         class_type=class_type)

    embed = await battle.view(False)
    view = View(battle)

    await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name="offline", description="Can only take **either** `stat2` or `hours`")
async def offline_slash_command(inter: disnake.ApplicationCommandInteraction,
                                current_stat: commands.Range[int, 1, 1000],
                                target_stat: commands.Range[int, 1, 1000] = None,
                                hours: commands.Range[int, 1, 1000] = None):

    if (target_stat is not None and hours is not None) or (target_stat is None and hours is None):
        await inter.response.send_message(
            "Invalid input. Please provide **either** a `target_stat` or `hours` value, but not both or neither.",
            ephemeral=True
        )

    elif target_stat is not None:
        if current_stat < target_stat:
            offline = Offline.OfflineModel(current_stat=current_stat, target_stat=target_stat)
            embed = await offline.calculate_time_to_target_stat()
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("Target stat must be higher than the current stat.", ephemeral=True)

    elif hours is not None:
        offline = Offline.OfflineModel(current_stat=current_stat, hours=hours)
        embed = await offline.calculate_new_stat_after_hours()
        await inter.response.send_message(embed=embed)


@bot.slash_command(name="lvl_info", description="Exp and skull")
async def level_info_slash_command(inter: disnake.ApplicationCommandInteraction,
                                   lvl: commands.Range[int, 1, 1000]):
    indicators = IndicatorsModel.IndicatorsModel(lvl=lvl)
    embed = indicators.view()
    await inter.response.send_message(embed=embed)


class Button(disnake.ui.Button):
    def __init__(self, battle):
        self.battle = battle
        super().__init__(label="More", style=disnake.ButtonStyle.green)

    async def callback(self, inter: disnake.MessageInteraction):
        embed = await self.battle.view(self.battle.frontier_group[0]["defense"])
        await inter.response.edit_message(embed=embed)


class Dropdown(disnake.ui.StringSelect):
    def __init__(self, battle):
        self.battle = battle
        options = []

        for mob in temporary_common_storage.high_hp_mobs:
            if battle.ctx.mob["defense"] == temporary_common_storage.low_hp_mobs[-1]["defense"]:
                options.append(disnake.SelectOption(label=mob["name"], emoji=mob["emoji"], value=mob["defense"]))
            elif mob["defense"] <= battle.ctx.mob["defense"]:
                options.append(disnake.SelectOption(label=mob["name"], emoji=mob["emoji"], value=mob["defense"]))

        super().__init__(
            placeholder="Select a mob for further training...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        embed = await self.battle.view(self.values[0])
        await inter.response.edit_message(embed=embed)


class View(disnake.ui.View):
    def __init__(self, battle):
        super().__init__()

        if battle.end_game:
            self.add_item(Dropdown(battle))

        if battle.trained_person is not None:
            self.add_item(Button(battle))


if __name__ == "__main__":
    bot.run("")
