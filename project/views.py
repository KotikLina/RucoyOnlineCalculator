import disnake

from project import temporary_common_storage


class MobView(disnake.ui.View):
    def __init__(self, battle, command_sender: disnake.Member):
        super().__init__(timeout=None)
        self.mob_groups_dropdown = MobGroupsDropdown(battle=battle, command_sender=command_sender)
        self.add_item(self.mob_groups_dropdown)


class MobGroupsDropdown(disnake.ui.StringSelect):
    def __init__(self, battle, command_sender: disnake.Member):
        self.command_sender = command_sender

        self.battle = battle
        options = []

        for mob_groups, _ in temporary_common_storage.mobs_groups.items():
            options.append(disnake.SelectOption(label=mob_groups))

        super().__init__(
            placeholder="Select a group of mobs for further selection...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author == self.command_sender:
            selected_group = self.values[0]
            mobs_in_group = temporary_common_storage.mobs_groups[selected_group]

            mobs_dropdown = MobsInGroupsDropdown(battle=self.battle, mobs=mobs_in_group, command_sender=self.command_sender)

            for item in self.view.children:
                if isinstance(item, MobsInGroupsDropdown):
                    self.view.remove_item(item)

            self.view.add_item(mobs_dropdown)

            await inter.response.edit_message(view=self.view)
        else:
            await inter.response.send_message(content="Sorry, this string select is not for you!", ephemeral=True)


class MobsInGroupsDropdown(disnake.ui.StringSelect):
    def __init__(self, battle, mobs, command_sender: disnake.Member):
        self.command_sender = command_sender

        self.battle = battle
        options = [
            disnake.SelectOption(label=mob["name"], emoji=mob["emoji"], value=mob['name'])
            for mob in mobs
        ]

        super().__init__(
            placeholder="Choose a mob to count...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author == self.command_sender:
            embed = await self.battle.view(dropdown_option=self.values[0])
            await inter.response.edit_message(embed=embed)
        else:
            await inter.response.send_message(content="Sorry, this string select is not for you!", ephemeral=True)


class TrainView(disnake.ui.View):
    def __init__(self, battle, command_sender: disnake.Member):
        super().__init__(timeout=None)
        if battle.end_game:
            self.add_item(EndGameDropdown(battle=battle, command_sender=command_sender))

        if battle.trained_person is not None:
            self.add_item(MoreButton(battle=battle, command_sender=command_sender))


class EndGameDropdown(disnake.ui.StringSelect):
    def __init__(self, battle, command_sender: disnake.Member):
        self.command_sender = command_sender

        self.battle = battle
        options = []

        for mob in temporary_common_storage.high_hp_mobs:
            if battle.person.ctx.mob["defense"] == temporary_common_storage.low_hp_mobs[-1]["defense"]:
                options.append(disnake.SelectOption(label=mob["name"], emoji=mob["emoji"], value=mob["defense"]))
            elif mob["defense"] <= battle.person.ctx.mob["defense"]:
                options.append(disnake.SelectOption(label=mob["name"], emoji=mob["emoji"], value=mob["defense"]))

            super().__init__(
                placeholder="Select a mob for further training...",
                min_values=1,
                max_values=1,
                options=options,
            )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author == self.command_sender:
            embed = await self.battle.view(button=self.values[0])
            await inter.response.edit_message(embed=embed)
        else:
            await inter.response.send_message(content="Sorry, this string select is not for you!", ephemeral=True)


class MoreButton(disnake.ui.Button):
    def __init__(self, battle, command_sender: disnake.Member):
        self.command_sender = command_sender

        self.battle = battle
        super().__init__(label="More", style=disnake.ButtonStyle.green)

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author == self.command_sender:
            embed = await self.battle.view(self.battle.frontier_group[0]["defense"])
            await inter.response.edit_message(embed=embed)
        else:
            await inter.response.send_message(content="Sorry, this button is not for you!", ephemeral=True)