import telebot
from telebot import types
from PIL import Image
import os
import string
import random
import os



API_TOKEN = '---------------------'

bot = telebot.TeleBot(API_TOKEN)
width=[]
height=[]

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@bot.message_handler(commands=['start'])
def send_welcome(message):
    width.clear()
    height.clear()
    msg = bot.reply_to(message, """\
    Hi these are photo size of almost social media
Facebook
profile picture size: 180 x 180
cover photo size: 820 x 312 
Story ad size: 1080 x 1920 
link image size: 1200 x 630  
image post size: 1200 x 630 
highlighted image size: 1200 x 717 
event image size: 1920 x 1005 
group cover image size: 1640 x 856 
image ad size: 1200 x 628 
Instagram
profile picture size: 110 x 110
photo sizes: 1080 x 1080
Stories size: 1080 x 1920
IGTV Cover Photo Size: 420 x 654 
Instagram Reels: 1080 x 1920  
Twitter  
profile picture size: 400 x 400
header size: 1500 x 500
post image size: 1200 x 675
image size for ads: 800 x 418
LinkedIn
company logo size: 300 x 300
cover photo size: 1128 x 191
Dynamic Ads size: 100 x 100 
Stories image size: 1080 x 1920
profile picture size: 400 x 400
background photo size: 1584 x 396
post image size: 1200 x 1200
YouTube
profile photo size: 800 x 800
Channel cover picture: 2560 x 1440 (desktop) 
Channel cover picture 1546 x 423 (smartphones)
Display ads: 300 x 250
Pinterest
Profile picture: 165 x 165
Board Display image: 222 x 150
Standard Pin size: Vertical images 1000 x 1500
Story Pins image size: 1080 x 1920
Tik Tok
Profile photo: 200 x 200
""")

    msg = bot.reply_to(message, ' please send me the width of the photo you want to resize.')
    bot.register_next_step_handler(msg, process_width_step)

def process_width_step(message):
    try:
        chat_id = message.chat.id
        if(message.text=='/stop' or message.text=='/start' ):
             return send_welcome(message)

        if message.text.isdigit()==False or int(message.text) < 1 or int(message.text) > 1200:
            msg = bot.reply_to(message, 'Send number between 1 - 1200')
            bot.register_next_step_handler(msg, process_width_step)
            return

        width.append(int(message.text))
        msg = bot.reply_to(message, 'Please send me the height of the photo you want to resize ')
        bot.register_next_step_handler(msg, process_height_step)
    except Exception as e:
        bot.reply_to(message, 'Something went wrong ')

def process_height_step(message):
    try:
        chat_id = message.chat.id
        if(message.text=='/stop' or message.text=='/start' ):
            return send_welcome(message)
        if message.text.isdigit()==False or int(message.text) < 1 or int(message.text) > 1200:
            msg = bot.reply_to(message, 'Send number between 1 - 1200')
            bot.register_next_step_handler(msg, process_height_step)
            return
        height.append(int(message.text))
        msg = bot.reply_to(message, 'Please send me the the photo you want to resize ')
        bot.register_next_step_handler(msg, process_send_file)
    except Exception as e:
        bot.reply_to(message, 'Something went wrong ')


def process_send_file(message):
    try: 
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        imageName=get_random_string(16)
        with open(imageName+".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, '10 second left ')
        image = Image.open(imageName+".jpg")
        # print(width)
        # print(height)
        new_image = image.resize((width[0], height[0]))
        new_image.save(imageName+".jpg")
        bot.reply_to(message, '5 second left ')
        chat_id = message.chat.id
        doc = open(imageName+".jpg", 'rb')
        bot.send_document(chat_id, doc)
        doc.close()
        msg = bot.reply_to(message, ' Thank you for useing my bot. Areeg Fahad ')
        os.remove(imageName+".jpg")
    except Exception as e:
        bot.reply_to(message, ' another time send photo ok')
        
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
bot.polling()
