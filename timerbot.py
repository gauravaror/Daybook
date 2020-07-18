 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler
from datetime import datetime
from pytz import timezone
import pytz
from pytz.reference import UTC
#import datetime 

class MedicineTimerBot:
    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    #def start(update, context):
    #    update.message.reply_text('Hi! Use /set HOURS:MINUTES (09:40) to set a timer')

    @staticmethod
    def medicing_alarm(context):
        """Send the alarm message."""
        job = context.job
        context.bot.send_message(job.context, text='Time for medicine!')


    def set_timer(self, update, context):
        """Add a job to the queue."""
        chat_id = update.message.chat_id
        try:
            if 'timezone' in context.chat_data:
                tzone = pytz.timezone(context.chat_data['timezone'])
            else:
                update.message.reply_text('Please set timezone using /timezone command before setting reminder.')
                return
            # args[0] should contain the time for the timer in seconds
            reminder_name = str(context.args[0])
            dtime = datetime.strptime(context.args[1], '%H:%M')
            dtime  = dtime.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            dtime  = tzone.localize(dtime)
            dtime = dtime.astimezone(UTC)

            logging.info("Setting time for reminder" + str(dtime))
            #due = int(context.args[0])
            # Add job to queue and stop current one if there is a timer already
            if reminder_name in context.chat_data:
                old_job = context.chat_data[reminder_name]
                old_job.schedule_removal()
            new_job = context.job_queue.run_daily(MedicineTimerBot.medicing_alarm, dtime.time(), context=chat_id)
            context.chat_data[reminder_name] = new_job

            update.message.reply_text('Medicine reminder successfully set!')

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /medicine HOURS:MINUTES (09:40) [24 hours format]')

    def unset(self, update, context):
        """Remove the job if the user changed their mind."""
        reminder_name = str(context.args[0])
        if reminder_name not in context.chat_data:
            update.message.reply_text('You have no active medicine reminder with name ' + reminder_name)
            return

        job = context.chat_data[reminder_name]
        job.schedule_removal()
        del context.chat_data[reminder_name]

        update.message.reply_text('Medicine reminder: ' + reminder_name + ' successfully removed!')

    def __init__(self, updater, dispatcher, user_pickle, timezone_pickle):
        """Run bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.user_pickle = user_pickle
        self.timezone_pickle = timezone_pickle
        self.updater = updater
        #Updater("1115583820:AAHaMW-nuazjQvbuoovKQv8oRPVujwc2DAI", use_context=True)

        # Get the dispatcher to register handlers
        dp = dispatcher

        # on different commands - answer in Telegram
        #dp.add_handler(CommandHandler("start", start))
        #dp.add_handler(CommandHandler("help", start))
        dp.add_handler(CommandHandler("medicine", self.set_timer,
                                      pass_args=True,
                                      pass_job_queue=True,
                                      pass_chat_data=True))
        dp.add_handler(CommandHandler("rmedicine", self.unset, pass_chat_data=True))


#if __name__ == '__main__':
#    main()
