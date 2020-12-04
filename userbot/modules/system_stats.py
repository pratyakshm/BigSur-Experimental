# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version, uname
from shutil import which

from telethon import version

from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch", "--stdout", stdout=asyncPIPE, stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await sysd.edit("" + result + "")
        except FileNotFoundError:
            await sysd.edit("Install neofetch first!")


@register(outgoing=True, pattern=r"^\.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.edit(
        "**BigSur bot** is online.\n\n"
        f"Bot:  v0.2\n"
        f"Python:   {python_version()}\n"
        f"User:  {DEFAULTUSER}"
    )


@register(outgoing=True, pattern=r"^\.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = ".aliveu [new user without brackets] nor can it be empty"
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Successfully changed user to " + newuser + "!"
    await username.edit("" f"{output}" "")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """ For .resetalive command, reset the username in the .alive command. """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("" "Successfully reset user for alive!" "")


CMD_HELP.update({"alive": ">.alive"
                 "\nUsage: Type .alive to see wether your bot is working or not."
                 "\n\n>.aliveu <text>"
                 "\nUsage: Changes the 'user' in alive to the text you want."
                 "\n\n>.resetalive"
                 "\nUsage: Resets the user to default.",
                 })
