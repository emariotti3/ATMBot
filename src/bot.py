import sys
import telebot
from telebot import types
from geoloc import ATMFinder

#botToken = "667720183:AAGKnQxLDRbrHfGFw21G0Z2TuLndc-1tkTY"
bot = telebot.TeleBot(sys.argv[1])

MAX_DST = 500
K_NEIGHBOURS = 3
CANCEL = "Cancel"
USER_ACTIONS = {}

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.reply_to(message,"Hello! To search for ATMs you can try typing '/link' or '/banelco'.")

def atmNetworkCmd(msg):
	return msg.content_type=='text' and len(msg.text)>0 and (ATMFinder.isNetwork(msg.text[1:]))

@bot.message_handler(func=atmNetworkCmd)
def send_link_atms(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_geo_yes = types.KeyboardButton(text="Share my location!",request_location=True)
	button_geo_no = types.KeyboardButton(text=CANCEL,request_location=False)
	USER_ACTIONS[message.chat.id]=message.text[1:].upper()
	keyboard.add(button_geo_yes,button_geo_no)

	bot.send_message(message.chat.id, "Hey there! Want to see some "+message.text[1:].upper()+" ATMs?", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
	hideKb = types.ReplyKeyboardRemove()
	if not message.chat.id in USER_ACTIONS:
		bot.send_message(message.chat.id, "Please enter a command. Try '/help' for more information.",reply_markup=hideKb)
		return True
	atms = ATMFinder(K_NEIGHBOURS,MAX_DST).knn([message.location.latitude,message.location.longitude],USER_ACTIONS[message.chat.id])
	if len(atms)>0:
		for atm in atms:
			bot.send_venue(message.chat.id, atm.getLoc().latitude(),atm.getLoc().longitude(),atm.getBank(),atm.getAddress(),reply_markup=hideKb)
	else:
		#apparently this is due to a problem with numpy arrays. Exception should not be used to control non-exceptional flow.
		bot.send_message(message.chat.id, "Sorry! We found no "+str(USER_ACTIONS[message.chat.id])+" ATMs in your area!",reply_markup=hideKb)

@bot.message_handler(func=lambda message:message.text==CANCEL)
def handle_cancel(message):
	hideKb = types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "OK!", reply_markup=hideKb)

@bot.message_handler(content_types=['text'])
def handle_location(message):
	bot.send_message(message.chat.id, "Please enter a valid command. Try '/help' for more information.")

bot.polling(none_stop=True, interval=0)
