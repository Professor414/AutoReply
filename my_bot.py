# -*- coding: utf-8 -*-

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# កំណត់ค่า Logging เพื่อดูข้อผิดพลาด
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================================================================
# ==                       កន្លែងកែប្រែទិន្នន័យ (EDIT HERE)                     ==
# ==============================================================================

# --- ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product A ---
PRODUCT_A1_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល A1***
- នេះជាផលិតផលប្រភេទទី១ របស់ A។
- អ្នកអាចបន្ថែមรายละเอียดเพิ่มเติมនៅត្រង់នេះ។
- តម្លៃ: $11
"""
PRODUCT_A2_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល A2***
- នេះជាផលិតផលប្រភេទទី២ របស់ A។
- អ្នកអាចបន្ថែមรายละเอียดเพิ่มเติมនៅត្រង់នេះ។
- តម្លៃ: $12
"""

# --- ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product B ---
PRODUCT_B1_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល B1***
- នេះជាផលិតផលប្រភេទទី១ របស់ B។
- តម្លៃ: $21
"""
PRODUCT_B2_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល B2***
- នេះជាផលិតផលប្រភេទទី២ របស់ B។
- តម្លៃ: $22
"""

# --- ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product C ---
PRODUCT_C1_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល C1***
- នេះជាផលិតផលប្រភេទទី១ របស់ C។
- តម្លៃ: $31
"""
PRODUCT_C2_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល C2***
- នេះជាផលិតផលប្រភេទទី២ របស់ C។
- តម្លៃ: $32
"""

# --- ព័ត៌មានទីតាំង និងទំនាក់ទំនង ---
LOCATION_MAP_DETAIL = "[ចុចទីនេះដើម្បីមើលบน Google Maps](https://maps.google.com/?q=11.5564,104.9282)"
LOCATION_ADDRESS_DETAIL = "*អាសយដ្ឋាន:*\nផ្ទះលេខ ១២៣, ផ្លូវ ៤៥៦, សង្កាត់បឹងកេងកង, ខណ្ឌចំការមន, រាជធានីភ្នំពេញ"
CONTACT_PHONE_DETAIL = "ទូរស័ព្ទ: `+855 12 345 678` (ចុចដើម្បី Copy)"
CONTACT_EMAIL_DETAIL = "អ៊ីមែល: `info@yourcompany.com` (ចុចដើម្បី Copy)"
CONTACT_WECHAT_DETAIL = "WeChat ID: `your_wechat_id` (ចុចដើម្បី Copy)"

# ==============================================================================
# ==                  កូដរបស់ Bot (មិនចាំបាច់កែប្រែខាងក្រោមនេះ)               ==
# ==============================================================================

# --- Functions បង្កើត Keyboard ---
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📦 ផលិតផល (Product)", callback_data='main_product')],
        [InlineKeyboardButton("📍 ទីតាំង (Location)", callback_data='main_location')],
        [InlineKeyboardButton("📞 ទំនាក់ទំនង (Contact)", callback_data='main_contact')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ផលិតផល A", callback_data='product_A')],
        [InlineKeyboardButton("ផលិតផល B", callback_data='product_B')],
        [InlineKeyboardButton("ផលិតផល C", callback_data='product_C')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_A_submenu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ផលិតផល A1", callback_data='product_A1')],
        [InlineKeyboardButton("ផលិតផល A2", callback_data='product_A2')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_B_submenu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ផលិតផល B1", callback_data='product_B1')],
        [InlineKeyboardButton("ផលិតផល B2", callback_data='product_B2')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_C_submenu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ផលិតផល C1", callback_data='product_C1')],
        [InlineKeyboardButton("ផលិតផល C2", callback_data='product_C2')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_location_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🗺️ ផែនទី (Map)", callback_data='location_map')],
        [InlineKeyboardButton("🏠 អាសយដ្ឋាន (Address)", callback_data='location_address')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_contact_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 ទូរស័ព្ទ (Phone)", callback_data='contact_phone')],
        [InlineKeyboardButton("✉️ អ៊ីមែល (Email)", callback_data='contact_email')],
        [InlineKeyboardButton("💬 WeChat", callback_data='contact_wechat')],
        [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Functions សម្រាប់ Command និង Button ---

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_text = f"👋 សួស្តី {user.mention_html()}!\n\nសូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖"
    
    # ពិនិត្យមើលថាជាការចាប់ផ្ដើមថ្មី ឬជាการចុចប៊ូតុងត្រឡប់មកវិញ
    if update.callback_query:
        query = update.callback_query
        query.edit_message_text(text=welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode='HTML')
    else:
        update.message.reply_text(text=welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode='HTML')


def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data

    # Main Menu and Back Buttons
    if data == 'main_menu':
        start(update, context) # ហៅ function start វិញដើម្បីแสดงម៉ឺនុយหลัก
        return
    elif data == 'main_product':
        query.edit_message_text(text="📦 សូមជ្រើសរើសប្រភេទផលិតផល៖", reply_markup=get_product_menu_keyboard())
    elif data == 'main_location':
        query.edit_message_text(text="📍 សូមជ្រើសរើសព័ត៌មានទីតាំង៖", reply_markup=get_location_menu_keyboard())
    elif data == 'main_contact':
        query.edit_message_text(text="📞 សូមជ្រើសរើសមធ្យោបាយទំនាក់ទំនង៖", reply_markup=get_contact_menu_keyboard())

    # Product Menu -> Sub-menu
    elif data == 'product_A':
        query.edit_message_text(text="អ្នកបានជ្រើសរើសផលិតផល A, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_A_submenu_keyboard())
    elif data == 'product_B':
        query.edit_message_text(text="អ្នកបានជ្រើសរើសផលិតផល B, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_B_submenu_keyboard())
    elif data == 'product_C':
        query.edit_message_text(text="អ្នកបានជ្រើសរើសផលិតផល C, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_C_submenu_keyboard())

    # Product Sub-menu Details
    elif data == 'product_A1':
        query.edit_message_text(text=PRODUCT_A1_DETAIL, reply_markup=get_product_A_submenu_keyboard(), parse_mode='Markdown')
    elif data == 'product_A2':
        query.edit_message_text(text=PRODUCT_A2_DETAIL, reply_markup=get_product_A_submenu_keyboard(), parse_mode='Markdown')
    elif data == 'product_B1':
        query.edit_message_text(text=PRODUCT_B1_DETAIL, reply_markup=get_product_B_submenu_keyboard(), parse_mode='Markdown')
    elif data == 'product_B2':
        query.edit_message_text(text=PRODUCT_B2_DETAIL, reply_markup=get_product_B_submenu_keyboard(), parse_mode='Markdown')
    elif data == 'product_C1':
        query.edit_message_text(text=PRODUCT_C1_DETAIL, reply_markup=get_product_C_submenu_keyboard(), parse_mode='Markdown')
    elif data == 'product_C2':
        query.edit_message_text(text=PRODUCT_C2_DETAIL, reply_markup=get_product_C_submenu_keyboard(), parse_mode='Markdown')

    # Location Details
    elif data == 'location_map':
        query.edit_message_text(text=LOCATION_MAP_DETAIL, reply_markup=get_location_menu_keyboard(), parse_mode='Markdown', disable_web_page_preview=False)
    elif data == 'location_address':
        query.edit_message_text(text=LOCATION_ADDRESS_DETAIL, reply_markup=get_location_menu_keyboard(), parse_mode='Markdown')

    # Contact Details
    elif data == 'contact_phone':
        query.edit_message_text(text=CONTACT_PHONE_DETAIL, reply_markup=get_contact_menu_keyboard(), parse_mode='Markdown')
    elif data == 'contact_email':
        query.edit_message_text(text=CONTACT_EMAIL_DETAIL, reply_markup=get_contact_menu_keyboard(), parse_mode='Markdown')
    elif data == 'contact_wechat':
        query.edit_message_text(text=CONTACT_WECHAT_DETAIL, reply_markup=get_contact_menu_keyboard(), parse_mode='Markdown')


def main() -> None:
    """Start the bot and set it up to run on Render."""
    
    # យក Token ពី Environment Variable របស់ Render.com
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("!!! TELEGRAM_TOKEN environment variable not found!")
        raise ValueError("សូមដាក់ TELEGRAM_TOKEN នៅក្នុង Environment Variables លើ Render.com")

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # ចុះឈ្មោះ handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    # យកค่า PORT และ URL ពី Render.com
    PORT = int(os.environ.get('PORT', '8443'))
    APP_NAME = os.environ.get("RENDER_EXTERNAL_URL")
    if not APP_NAME:
        logger.error("!!! RENDER_EXTERNAL_URL environment variable not found!")
        raise ValueError("RENDER_EXTERNAL_URL មិនត្រូវបានកំណត់។ វាควรจะถูกកំណត់ដោយ Render ដោយស្វ័យប្រវត្តិ។")

    logger.info(f"Starting webhook for bot on URL: {APP_NAME}")
    
    # ចាប់ផ្ដើម Bot ដោយใช้ Webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f"{APP_NAME}/{TOKEN}")
    
    updater.idle()


if __name__ == '__main__':
    main()
