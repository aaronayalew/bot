import logging
from time import sleep
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Share Contact", request_contact=True)]])
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please share your contact to request a ride", reply_markup=reply_markup)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Please select what kind of ride you want to book"
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Book a Private Ride")], [KeyboardButton("Book a Shared(Pool) Ride")]])
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text=message, reply_markup=reply_markup)

async def pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("POOOOOOL")
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("1"), KeyboardButton("2")]])
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="How many seats do you want?", reply_markup=reply_markup)

async def private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Share current location", request_location=True)]])
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="Please Share your pick up location", reply_markup=reply_markup)

async def loc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="Please enter your destination address", reply_markup=ReplyKeyboardRemove())

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Bole international airport")],[KeyboardButton("Bole international hotel")],[KeyboardButton("Bole, Addis Ababa")],])
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="Please select from the listed addresses", reply_markup=reply_markup)

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Confirm")], [KeyboardButton("Cancel")]])
    Message = "You have ordered: \nFrom: *Your Location* \nTo: Bole international airport\nEstimated Cost: 212.45 Br.\nETA: 10 minutes\n*Confirm?*"
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text=Message, reply_markup=reply_markup, parse_mode="Markdown")

async def accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="Looking for drivers...", reply_markup=ReplyKeyboardRemove())
    sleep(2)
    driver = "A driver has accepted your request\nDriver: Abebe Bikila\nPhone no. +251900112233\nThank you for using this service"
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text=driver)

if __name__ == '__main__':
    application = ApplicationBuilder().token('5869755832:AAFrMuHvyC3mypl0GYPx9z52sqLRJJ9kDCY').build()
    
    start_handler = CommandHandler('start', start)
    pool_handler = MessageHandler(filters=filters.Regex("Book a Shared\(Pool\) Ride"), callback=pool)
    private_handler = MessageHandler(filters=filters.Regex("Book a Private Ride"), callback=private)
    contact_handler = MessageHandler(filters=filters.CONTACT, callback=register)
    seats_handler = MessageHandler(filters=filters.Regex("1") | filters.Regex("2"), callback=private)
    loc_handler = MessageHandler(filters=filters.LOCATION, callback=loc)
    address_handler = MessageHandler(filters=filters.Regex("bole"), callback=address)
    accept_handler = MessageHandler(filters=filters.Regex(r"Confirm"), callback=accept)
    confirm_handler = MessageHandler(filters=filters.Regex("Bole international airport"), callback=confirm)

    # msg_handler = MessageHandler(filters=filters.TEXT, callback=msg)
    application.add_handlers([pool_handler, private_handler, seats_handler, loc_handler, address_handler, confirm_handler, accept_handler])
    application.add_handler(start_handler)
    application.add_handler(contact_handler)
    
    application.run_polling()
