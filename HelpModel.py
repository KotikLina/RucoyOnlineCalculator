import disnake
from abc import ABC, abstractmethod


class AbstractHelpModel(ABC):
    @abstractmethod
    def view(self) -> disnake.Embed:
        ...


class HelpModel(AbstractHelpModel):
    def view(self) -> disnake.Embed:

        mini_slime_emoji = "<:mini_slime:1194708281319510017>"

        title = f"Commands{mini_slime_emoji}"

        description = '''
**/train [lvl] [stat] [buffs] [weapon atk]**
Calculates the mob that you can train effectively on.
Buff default is 0. Weapon atk default is 5.

**/ptrain [lvl] [stat] [buffs] [weapon atk] [class type] [ticks]**
Calculates the mob that you can power-train effectively on.
Buff default is 0. Weapon atk default is 5. Ticks default is 4.

**/offline [current stat] [target stat] [hours]**
Calculates the offline training time needed for stat2, or stat gain from hours of offline training.

**/dmg [lvl] [stat] [buffs] [weapon atk] [class type]**
Calculates the damage you do to certain mobs.

**/oneshot [lvl] [stat] [buffs] [weapon atk] [attack type] [consistency]**
Calculates whether you already one-shot a mob, or the stat level needed to one-shot a certain mob.
Buff default is 0. Consistency default is 80%.

**/lvl_info [lvl]**
Calculates the experience at a certain base level.
Calculates the amount of gold needed to skull for a certain base level.

**/help**
Displays the command list, but it looks like you already know how to use this!

**/info**
Shows more information about the bot.

**/invite**
Shows the invite link to add the bot to your server.
*Make sure you give the bot ALL of the permissions requested.

**/github**
Displays the github link containing the source code for the bot!
'''

        footer = "If you have suggestions or bugs to report, message me: kotiklinok#0000"

        return disnake.Embed(title=title, description=description).set_footer(text=footer, icon_url=None)
