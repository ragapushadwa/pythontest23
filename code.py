from telegram import Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import requests

# Set up logging

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = '7242947121:AAFrzm36RxqPbhChYseolosuekQu-8npan4'

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text('Hello! Send /getpost to get a dummy post.')


def get_cekpos(phoneNumber:str) -> str:
    url = f"http://localhost:9432/detail/{phoneNumber}"
    response = requests.get(url)
    
    if response.status_code==200:
     return response.json()
    else:
     return "not found"
def cekpos(update: Update, context: CallbackContext) -> None:
    if context.args:
        phoneNumber = " ".join(context.args)
        cekpos_info = get_cekpos(phoneNumber)
        sent_message=update.message.reply_text(cekpos_info)
        context.bot.send_message(chat_id='-1002214722819', text=cekpos_info)
        schedule_deletion(context, sent_message.chat_id, sent_message.message_id)

    else:
        update.message.reply_text("Please specify the phone number.")

def delete_message(context: CallbackContext) -> None:
    try:
        context.bot.delete_message(chat_id=context.job.context['chat_id'], message_id=context.job.context['message_id'])
    except Exception as e:
        print(f"Failed to delete message: {e}")

def schedule_deletion(context: CallbackContext, chat_id: int, message_id: int) -> None:
    context.job_queue.run_once(delete_message, 3, context={'chat_id': chat_id, 'message_id': message_id})


def get_post(update: Update, context: CallbackContext) -> None:
    """Fetch a dummy post from the JSONPlaceholder API and send it to the user."""
    url = 'http://localhost:9432/detail/{phoneNumber}'  # Dummy API URL
    
    try:
        response = requests.get(url)
        data = response.json()

        # Extracting data from the response
        post_id = data['id']
        title = data['title']
        body = data['body']
        
        # Sending a message back to the user
        update.message.reply_text(f"Post ID: {post_id}\nTitle: {title}\nBody: {body}")
        context.bot.send_message(chat_id='-1002214722819', text=update.message.reply_text(f"Post ID: {post_id}\nTitle: {title}\nBody: {body}"))
    
    except Exception as e:
        
        update.message.reply_text("An error occurred while fetching the data.")
       
    
 
def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getpost", get_post))
    
    dispatcher.add_handler(CommandHandler("cekpos", cekpos))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, cekpos))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()