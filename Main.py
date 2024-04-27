from disnake.ext import commands
import disnake

import TrainModel
import Person_and_Mob

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.InteractionBot(intents=disnake.Intents.all())


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

        for mob in Person_and_Mob.high_hp_mobs:
            if battle.ctx.mob["defense"] == Person_and_Mob.low_hp_mobs[-1]["defense"]:
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


class DropdownView(disnake.ui.View):
    def __init__(self, battle):
        super().__init__()
        if battle.end_game:
            self.add_item(Dropdown(battle))

        if battle.trained_person is not None:
            self.add_item(Button(battle))


@bot.slash_command(name="train", description="online train")
async def train_slash_command(inter, lvl: int, stat: int, buffs: int = 0, weapon_atk: int = 5):
    battle = TrainModel.TrainModel(lvl, stat, buffs, weapon_atk)

    embed = await battle.view(False)
    view = DropdownView(battle)

    await inter.response.send_message(embed=embed, view=view)


bot.run('')
