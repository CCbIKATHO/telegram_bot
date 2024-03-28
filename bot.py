#!/usr/bin/python
import config 
import telegram
import os
import subprocess
import sys
import shlex
import datetime
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload 

#bot = telegram.Bot(token = config.token)
#Bot verification
#print(bot.getMe())
from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I'm a bot, waiting for a command")


def help(bot, update):
    reload(config)
    bot.sendMessage(chat_id=update.message.chat_id, text='''list of available commands:
    /id - User ID
    /ifconfig - network settings
    /df - disk space information (df -h)
    /free - memory information
    /mpstat - CPU load information
    /dir1 - folder volume''' + config.dir1 + '''
    /dirbackup - backup file size for the current day in the folder ''' + config.dir_backup + '''

    ''')

#command function id
def myid(bot, update):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)


#command function ifconfig
def ifconfig(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        run_command("ifconfig")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#command function df
def df(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        run_command("df -h")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#command function free
def free(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        run_command("free -m")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#command function mpstat
def mpstat(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        run_command("mpstat")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#command function dir1
def dir1(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        dir1_command = "du -sh "+ config.dir1
        run_command(dir1_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#command function dirbackup - checks the presence of a file by date
def dirbackup(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #if the user id is in the list admin then the command is executed
        now_date = datetime.date.today() # The current date
        cur_year = str(now_date.year) # Current year
        cur_month = now_date.month # Current month
        if cur_month < 10:
            cur_month = str(now_date.month)
            cur_month = '0'+ cur_month
        else:
            cur_month = str(now_date.month)
        cur_day = str(now_date.day) # Current day
        filebackup = config.dir_backup + cur_year + '-' + cur_month + '-' + cur_day + '.03.00.co.7z'  #form the file name to search
        print (filebackup)
        filebackup_command = "ls -lh "+ filebackup
        run_command(filebackup_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

ifconfig_handler = CommandHandler('ifconfig', ifconfig)
dispatcher.add_handler(ifconfig_handler)

df_handler = CommandHandler('df', df)
dispatcher.add_handler(df_handler)

free_handler = CommandHandler('free', free)
dispatcher.add_handler(free_handler)

mpstat_handler = CommandHandler('mpstat', mpstat)
dispatcher.add_handler(mpstat_handler)

dir1_handler = CommandHandler('dir1', dir1)
dispatcher.add_handler(dir1_handler)

dirbackup_handler = CommandHandler('dirbackup', dirbackup)
dispatcher.add_handler(dirbackup_handler)

myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


updater.start_polling()