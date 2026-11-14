<h1 align="center">Nano-BD</h1>
<p align="center">
A daughter that is also a Discord Bot, Website, and Database
</p>
<p align="center">
<sub>More info about the first three badges to come later~!</sub>
<br>
<img alt="Contains Nano-DCv3" src="https://img.shields.io/badge/DC-v3-FAD">
<img alt="Contains Nano-WSv0" src="https://img.shields.io/badge/WS-v0-AFD">
<img alt="Contains Nano-DBv1" src="https://img.shields.io/badge/DB-v1-ADF">
<br>
<img alt="Discord.py Badge" src="https://img.shields.io/badge/discord-.py-306998?logo=discord&logoColor=fff&logoSize=auto&labelColor=5865F2">
<img alt="Django Badge" src="https://img.shields.io/badge/django-092E20?logo=django&logoColor=fff&logoSize=auto">
<img alt="MySql Badge" src="https://img.shields.io/badge/my-sql-F29111?logo=mysql&logoColor=fff&logoSize=auto&labelColor=00758F">
<br>
<img alt="License Badge" src="https://img.shields.io/github/license/MiXenia/Nano-BDv0">
</p>

## Current Features

Nano-BD is currently in the process of migrating from Nano-DCv2, and has very barebones features at the moment.
It's okay if you don't know what that means. For now, here's what she's got:

* MySQL Database support with Django Models for users that involves all Discord-related data DCv2 needed to play with users.
* A Django management command to import data from certain pkl files DCv2 used into BD's database.
* A Django management command to start BD's integrated Discord Bot.
* A Discord text command, `+sync`, that syncs slash commands to the command tree in the current guild or globally, with the added option to clear guild syncs.
* A Discord slash command, `/mydata`, that shows what data Nano-BD has on the user, if any.

## Planned Features

* A port of most of DCv2's features.
* A fully functional website that has a side dedicated to the discord bot, and another side that isn't.
* And more...

## Setup

Nano-BD currently runs on Python 3.14 and MySQL 8.0.16+
She also needs a Discord Application with the Server Members and Message Content intents turned on.
If you want to set up your own copy of Nano-BD, get the above and then follow the steps below:
1. Make a clone of this repository, then create and activate an environment as needed.
2. Run the following to install the remainder of her prerequisites.
   ```bash
   pip install -r requirements.txt
   ```
3. Create a MySQL database with `utf8mb4`. Go ahead and make a user too while you're at it, if you don't have one set up already.
   ```sql
   CREATE USER 'NANO-BDv00-Username-Here'@'localhost' IDENTIFIED BY 'Insert-Better-Password-Than-This-One-Here';
   CREATE DATABASE DatabaseName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   GRANT ALL PRIVILEGES ON DatabaseName.* TO 'NANO-BDv00-Username-Here'@'localhost';
   ```
4. Make a copy of `.env.example` and rename it to `.env`, then follow the Environment Variable Guide. To get the secure Django key, run the following:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
   ```
5. Run Django migration with the following:
   ```bash
   python manage.py migrate
   ```
6. Then create a Django superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. From there, to start the Django website, run the usual:
   ```bash
   python manage.py runserver
   ```
8. To start up the Discord Bot, you instead run:
   ```bash
   python manage.py rundc
   ```
9. To get the Discord bot actually on a server, head back to the Discord Developer Portal, select the App, then navigate to the OAuth2 page on the side bar. Scroll down to the URL Generator, check the `bot` and `applications.commands` scopes. For Bot Permissions, tick the following:
   * View Channels
   * Send Messages
   * Send Messages in Threads
   * Embed Links
   * Attach Files
   * Read Message History
   * Use External Emojis
   * Add Reactions

   Make sure Integration Type is set to Guild Install, then Copy the link below and open it. This will pull you to either a webpage or directly into discord to add your copy of Nano-BD to a Discord server of your choosing!
10. If all was set up correctly, you should be able to send `+sync` in a Discord Server with Nano-BD in it to have her add her commands to that server. (Note: You can only run `+sync` if you're the owner of the app in the developer portal!)

### Environment Variable Guide
| Key          | Value                                                                                                                         |
|--------------|-------------------------------------------------------------------------------------------------------------------------------|
| `DISCORDKEY` | The Discord Bot Token for the Discord App. Get this by going to Discord's Developer Portal -> your app -> Bot -> Reset Token. |
| `SITEKEY`    | The secure Django key.                                                                                                        |
| `DEBUG`      | Setting this to `1` runs the website in Debug Mode. Any other value runs it normally.                                         |
| `DBNAME`     | The name of the MySQL Database used for calls.                                                                                |
| `DBUSERNAME` | The Username both the website and the Discord bot will use when accessing the Database.                                       |
| `DBPASSWORD` | The Password that matches the above Username.                                                                                 |
| `DBHOST`     | The Host/Address of the Database. (Usually just `localhost`)                                                                  |
| `DBPORT`     | The Port of the Database. (Usually just `3306`)                                                                               |

## Project Structure
```text
Nano-BD
├──config                  # Main Django directory.
├──catplush                # Django App for the main part of the website.
└──nano                    # Django App for the Nano-Focused part of the website.
   │  models.py            # All Models used by both the website and the Discord bot.
   ├──DCv3                 # Base Directory for the Discord Bot
   │  └──Cogs              # Cogs used by the Discord bot, loaded automatically.
   │     │  dccore.py      # Fundamental Cog that will soon have user signups and administration.
   │     │  testy.py       # Cog used for testing.
   └──management
      └──commands
         │  importpkl.py   # Used to import DCv2 *.pkl files.
         │  rundc.py       # Runs the Discord Bot.
```

## Misc
You can support my endeavors on Ko-fi!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M63090Z)

Nano-BD is licensed under the [GNU AGPL v3.0](LICENSE).
