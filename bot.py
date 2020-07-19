from telegram.ext import Updater, CommandHandler
from timerbot import MedicineTimerBot
from timezonebot import TimeZoneHandler
from database_handler import DatabaseHandler
import logging
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

c = json.load(open('creds.json'))

db_handler = DatabaseHandler(c)
updater = Updater(c['token'], use_context=True)
dispatcher = updater.dispatcher
medicine = MedicineTimerBot(updater, dispatcher, db_handler)
timezone = TimeZoneHandler(updater, dispatcher, db_handler)

def start(update, context):
    update.message.reply_text('Hi! Welcome to medicine reminder bot.\
                               \nUse /medicine name HOURS:MINUTES (09:40) to set a reminder\
                               \nUse /rmedicine name to remove the reminder\
                               \nUse /timezeone to select your timezone.')

dispatcher.add_handler(CommandHandler("start", start))

all_reminders = db_handler.get_all_reminder()
for reminder in all_reminders:
    user_id, timezone, reminder_name, reminder_time = reminder
    dtime = MedicineTimerBot.get_time_tzone(reminder_time, timezone)
    updater.job_queue.run_daily(MedicineTimerBot.medicing_alarm, dtime.time(), context=user_id)
    print(reminder)
#Start the Bot
updater.start_polling()

# Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
# SIGABRT. This should be used most of the time, since start_polling() is
# non-blocking and will stop the bot gracefully.
updater.idle()
