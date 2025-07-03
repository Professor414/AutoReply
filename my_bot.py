# my_bot.py

import os
import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# --- ផ្នែករៀបចំ Menu ---
# បង្កើតប៊ូតុងសម្រាប់ Menu របស់យើង (អាចដាក់ Emoji បាន)
button_products = KeyboardButton(text="🛍️ ផលិតផល")
button_location = KeyboardButton(text="📍 ទីតាំង & ទំនាក់ទំនង")
button_about_us = KeyboardButton(text="ℹ️ អំពីយើង")

# រៀបចំប៊ូតុងជាแถว (Row)
# នៅទីនេះយើងដាក់ ២ ប៊ូតុងក្នុងមួយแถว និង ១ ប៊ូតុងនៅแถวទីពីរ
main_menu_layout = [
    [button_products, button_location],
    [button_about_us]
]
# បង្កើត Menu Keyboard
main_menu_keyboard = ReplyKeyboardMarkup(main_menu_layout, resize_keyboard=True)


# --- ផ្នែក Handlers (មុខងារឆ្លើយតប) ---

def start(update, context):
    """ផ្ញើសារស្វាគមន៍ និងបង្ហាញ Menu នៅពេលអ្នកប្រើប្រាស់វាយ /start"""
    user = update.effective_user
    update.message.reply_html(
        f"សួស្ដីបាទ {user.mention_html()}! ខ្ញុំបាទ តេង សម្បត្តិ (ADMIN PAGE TS MEDIA)  \n\n
        - តើខ្ញុំអាចជួយអ្វីបានដែរ? សូមជ្រើសរើសពី Menu ខាងក្រោម៖",
        reply_markup=main_menu_keyboard  # បង្ហាញ Menu
    )

def handle_products(update, context):
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'ផលិតផល'"""
    reply_text = "នេះគឺជាបញ្ជីផលិតផលរបស់យើង៖\n- ផលិតផល A: តម្លៃ $10\n- ផលិតផល B: តម្លៃ $20\n- ផលិតផល C: តម្លៃ $30"
    update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

def handle_location(update, context):
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'ទីតាំង & ទំនាក់ទំនង'"""
    reply_text = "📍 ហាងយើងខ្ញុំមានទីតាំងនៅផ្ទះលេខ 25, ផ្លូវ 123, សង្កាត់បឹងកេងកង, រាជធានីភ្នំពេញ។\n\n📞 លេខទូរសព្ទទំនាក់ទំនង៖ 012 345 678"
    update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

def handle_about_us(update, context):
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'អំពីយើង'"""
    reply_text = "ℹ️ យើងខ្ញុំគឺជាហាងដែលផ្តល់ជូនផលិតផលដែលមានគុណភាពខ្ពស់ និងសេវាកម្មល្អបំផុតជូនអតិថិជន។"
    update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

def handle_unknown_messages(update, context):
    """ឆ្លើយតបទៅសារដែលមិនស្គាល់ (Auto-Reply ទូទៅ)"""
    reply_text = "ขออภัยครับ ខ្ញុំមិនយល់ពីអ្វីដែលអ្នកចង់បានទេ។ សូមសាកល្បងជ្រើសរើសពី Menu ដែលមានស្រាប់។"
    update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)


def main():
    """ចាប់ផ្តើមដំណើរការ Bot"""
    # យក TOKEN ពី Environment Variable ដើម្បីសុវត្ថិភាព
    # យើងនឹងកំណត់វានៅលើ Render.com
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("!!! សូមកំណត់ TELEGRAM_TOKEN ជា Environment Variable ជាមុនសិន។")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # ចុះឈ្មោះ Handlers
    # 1. Command Handler សម្រាប់ /start
    dp.add_handler(CommandHandler("start", start))

    # 2. Message Handlers សម្រាប់ប៊ូតុងនីមួយៗ
    dp.add_handler(MessageHandler(Filters.regex('^🛍️ ផលិតផល$'), handle_products))
    dp.add_handler(MessageHandler(Filters.regex('^📍 ទីតាំង & ទំនាក់ទំនង$'), handle_location))
    dp.add_handler(MessageHandler(Filters.regex('^ℹ️ អំពីយើង$'), handle_about_us))
    
    # 3. Message Handler សម្រាប់សារផ្សេងៗដែលមិនត្រូវនឹងប៊ូតុង
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_unknown_messages))

    print("Bot កំពុងដំណើរការ...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
