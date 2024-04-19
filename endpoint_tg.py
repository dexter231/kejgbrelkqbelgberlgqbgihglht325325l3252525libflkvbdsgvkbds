import re
import os
import asyncio
from telegram import *
from telegram.ext import *
from llm import gemini as llm
token=os.getenv('TELEGRAM_BOT_TOKEN')
uname = os.getenv('BOT_NAME')

llm=llm("give detailed responses")
cid = None  # Initialize the "cid" variable

def print1(string):
    """Appends a string to a text file named "log.txt", creating the file if it doesn't exist.

    Args:
        string: The string to append to the log file.
    """

    with open("log.txt", "a") as file:  # Open in append mode
        file.write(string + "\n")  # Append string and a newline

def get_chat_id(update):
    global cid
    cid = update.effective_chat.id

def escape_markdown_v2(text):
    escape_chars = r'\_[]()~>\-\+=\|{}.!'
    escaped_text = ''.join('\\' + char if char in escape_chars else char for char in text)
    escaped_text = re.sub(r'\*+', '*', escaped_text)  # replace consecutive * with one *
    escaped_text = re.sub(r'(?<=\s)\*(?=\s)', ' ', escaped_text)  # remove single * marks
    escaped_text = re.sub(r'## (.*?)(?=\n)', r'*_\1_*', escaped_text)  # add __ to sentences starting with ##
    escaped_text = escaped_text.replace('#', '')  # remove all # marks
    escaped_text = re.sub(r'```', """```\n""", escaped_text)  # add new line at start of every ```
    return escaped_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="hey I'm up!")


async def setOneTime(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="mode set to oneTime repsponses")


async def setchat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="mode set to chat")


async def newchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    llm.reset()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="chat reset")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if cid == None:
        get_chat_id(update)
    req = update.message.text
    #print(req)
    resp =llm.get_response(req)
    # resp = resp.replace('!', '\\!')
    # resp = resp.replace('.', '\\.')
    #print(resp)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=resp, protect_content=True,parse_mode=constants.ParseMode.MARKDOWN_V2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=escape_markdown_v2(resp), parse_mode=constants.ParseMode.MARKDOWN_V2)
# handle erro


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    print1(f"Update {update} caused error {context.error}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="error occured")
# prevent server from sleeping


async def print_hi():
    while True:
        print("preventing timeout")
        print1("preventing timeout")
        await asyncio.sleep(60 * 5)  # Print "Hi" every 25 minutes


if __name__ == '__main__':

    while True:
        try:
            application = ApplicationBuilder().token(token).build()

            start_handler = CommandHandler('start', start)
            application.add_handler(start_handler)

            onetime = CommandHandler('onetimeresponse', setOneTime)
            application.add_handler(onetime)

            chattype = CommandHandler('chatresponse', setchat)
            application.add_handler(chattype)

            chatreset = CommandHandler('chatreset', newchat)
            application.add_handler(chatreset)

            message = MessageHandler(filters.Text() ,chat)  # message handler
            application.add_handler(message)

            application.run_polling()
        except:
            print("error")
            continue
