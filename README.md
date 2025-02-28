# Rucoy Online Calculator
#### Для русской версии, см. [README_RU.md](README_RU.md).

Rucoy Online Calculator is a Discord bot created to help players with calculations related to gameplay in the game Rucoy Online. The bot provides various commands to analyze training efficiency, damage, level and other parameters.

## Discord bot server
Join the official bot server:  
[Server Link](https://discord.gg/wJuydcvG6p)

## Add Discord bot to your server
If you want to use a bot on your server or have any questions about the project, contact the author via Discord: #kotiklinok#0000

<br>

## Bot Commands

<details>
<summary>Click to expand list of commands</summary>
  
#### 💠 `/train [lvl] [stat] [buffs] [weapon atk]`
Calculates the mob that you can train effectively on.

---

#### 💠 `/ptrain [lvl] [stat] [buffs] [weapon atk] [class type] [ticks]`
Calculates the mob that you can power-train effectively on.

---

#### 💠 `/offline [current stat] [target stat] [hours]`
Calculates the offline training time needed for stat2, or stat gain from hours of offline training.

---

#### 💠 `/dmg [lvl] [stat] [buffs] [weapon atk] [class type]`
Calculates the damage you do to certain mobs.

---

#### 💠 `/oneshot [lvl] [stat] [buffs] [weapon atk] [attack type] [consistency]`
Calculates whether you already one-shot a mob, or the stat level needed to one-shot a certain mob.

---

#### 💠 `/lvl_info [lvl]`
Calculates the experience at a certain base level.
Calculates the amount of gold needed to skull for a certain base level.

---

#### 💠 `/help`
Displays the command list.

</details>

<br>

## Technologies
The bot is written in **Python** using [disnake](https://github.com/DisnakeDev/disnake) library.

## Installation and customization
The bot is currently running and supported by the developer. 
The current version of the repository is missing key files such as `__main__.py` and `.env`, making it impossible to run the bot on its own. 

Please note that this project is distributed under the GNU Affero General Public License v3.0 (AGPL). Any use of the code must comply with the terms of the license, including mandatory disclosure of the source code of derivative works and prohibition of commercial use without explicit permission from the author.

## License
This project is distributed under the [GNU Affero General Public License v3.0 (AGPL)](LICENSE) license.  
This means:
- You are free to use and modify the code for non-commercial purposes.
- Any commercial use is possible only with the written permission of the author.
- If you use this code in your project, you are obliged to make your project open source and provide the source code.
- It is forbidden to use the code in proprietary (closed) projects without explicit permission.
- When using the code, you must indicate authorship.

## Acknowledgements
I would like to extend a huge thank you to the following people who played a key role in the creation and development of this project:

* LightmanLP and mikk357 :

  These two people were indispensable helpers in writing and improving the code. Without their support and valuable advice this project would not have reached its current level. Thank you for your patience!
* Mimsqueeze (Mims) :
  
  Author of the [`Mims-Rucoy-Calculator`](https://github.com/Mimsqueeze/Mims-Rucoy-Calculator) project, which has been a source of inspiration for me. Thanks to his work, I got ready-made formulas for calculations, which formed the basis of my bot.
* Rozieal :
  
  Author of the original project from which Mimsqueeze took the formulas. His work laid the foundation for all subsequent work related to calculations on Rucoy Online game.