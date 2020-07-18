from telegram.ext import Updater, CommandHandler
from timerbot import MedicineTimerBot
from timezonebot import TimeZoneHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater("1115583820:AAHaMW-nuazjQvbuoovKQv8oRPVujwc2DAI", use_context=True)
dispatcher = updater.dispatcher
medicine = MedicineTimerBot(updater, dispatcher, 'medicine.df', 'timezone.df')
timezone = TimeZoneHandler(updater, dispatcher, 'timezone.df')

def start(update, context):
    update.message.reply_text('Hi! Welcome to medicine reminder bot.\
                               \nUse /medicine name HOURS:MINUTES (09:40) to set a reminder\
                               \nUse /rmedicine name to remove the reminder\
                               \nUse /timezeone to select your timezone.')

dispatcher.add_handler(CommandHandler("start", start))


#Start the Bot
updater.start_polling()

# Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
# SIGABRT. This should be used most of the time, since start_polling() is
# non-blocking and will stop the bot gracefully.
updater.idle()
