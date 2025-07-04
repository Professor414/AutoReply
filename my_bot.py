import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# បើកដំណើរការ Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ------------------- ទិន្នន័យសម្រាប់ Bot (កែប្រែត្រង់នេះ) -------------------
# ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product A
PRODUCT_A1_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល A1***
- នេះជាផលិតផលប្រភេទទី១ របស់ A
- តម្លៃ: $11
"""
PRODUCT_A2_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល A2***
- នេះជាផលិតផលប្រភេទទី២ របស់ A
- តម្លៃ: $12
"""

# ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product B
PRODUCT_B1_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល B1***
- នេះជាផលិតផលប្រភេទទី១ របស់ B
- តម្លៃ: $21
"""
PRODUCT_B2_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល B2***
- នេះជាផលិតផលប្រភេទទី២ របស់ B
- តម្លៃ: $22
"""

# ព័ត៌មានលម្អិតសម្រាប់ម៉ឺនុយរងរបស់ Product C
PRODUCT_C1_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល C1***
- នេះជាផលិតផលប្រភេទទី១ របស់ C
- តម្លៃ: $31
"""
PRODUCT_C2_DETAIL = """
***ព័ត៌មានលម្អិតអំពីផលិតផល C2***
- នេះជាផលិតផលប្រភេទទី២ របស់ C
- តម្លៃ: $32
"""

# ព័ត៌មានផ្សេងៗ
LOCATION_MAP_DETAIL = "[ចុចទីនេះដើម្បីមើលบน Google Maps](https://maps.google.com/?q=11.5564,104.9282)"
LOCATION_ADDRESS_DETAIL = "*អាសយដ្ឋាន:*\nផ្ទះលេខ ១២៣, ផ្លូវ ៤៥៦, សង្កាត់បឹងកេងកង, ខណ្ឌចំការមន, រាជធានីភ្នំពេញ"
CONTACT_PHONE_DETAIL = "ទូរស័ព្ទ: `+855 12 345 678`"
CONTACT_EMAIL_DETAIL = "អ៊ីមែល: `info@yourcompany.com`"
CONTACT_WECHAT_DETAIL = "WeChat ID: `your_wechat_id`"
# --------------------------------------------------------------------


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

# --- Keyboard សម្រាប់ Sub-Menus ---
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
# --- End Sub-Menu Keyboards ---

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

# --- End Keyboard Functions ---


# Function សម្រាប់ command /start
def start(update: Update, context: CallbackContext) -> None:
    # ពិនិត្យមើលថាសារមកពី Private Chat ឬ Group
    if update.message.chat.type == 'private':
        update.message.reply_text(
            text="👋 សួស្តី! សូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        # បើនៅក្នុង Group ឆ្លើយតបแบบธรรมดา
        update.message.reply_text("សួស្តី! សូម DM ខ្ញុំដើម្បីប្រើប្រាស់ម៉ឺនុយ។")


# Function สำหรับจัดการការចុចប៊ូតុង
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data

    # Main Menu
    if data == 'main_menu':
        query.edit_message_text(text="👋 សូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖", reply_markup=get_main_menu_keyboard())
    elif data == 'main_product':
        query.edit_message_text(text="📦 សូមជ្រើសរើសប្រភេទផលិតផល៖", reply_markup=get_product_menu_keyboard())
    elif data == 'main_location':
        query.edit_message_text(text="📍 សូមជ្រើសរើសព័ត៌មានទីតាំង៖", reply_markup=get_location_menu_keyboard())
    elif data == 'main_contact':
        query.edit_message_text(text="📞 សូមជ្រើសរើសមធ្យោបាយទំនាក់ទំនង៖", reply_markup=get_contact_menu_keyboard())

    # Product Menu (A, B, C) -> បង្ហាញ Sub-menu
    elif data == 'product_A':
        query.edit_message_text(text="ท่านเลือกផលិតផល A, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_A_submenu_keyboard())
    elif data == 'product_B':
        query.edit_message_text(text="ท่านเลือกផលិតផល B, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_B_submenu_keyboard())
    elif data == 'product_C':
        query.edit_message_text(text="ท่านเลือกផលិតផល C, សូមជ្រើសរើសប្រភេទ៖", reply_markup=get_product_C_submenu_keyboard())

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
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("សូមដាក់ TELEGRAM_TOKEN នៅក្នុង Environment Variables")

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    PORT = int(os.environ.get('PORT', '8443'))
    APP_NAME = os.environ.get("RENDER_EXTERNAL_URL")
    if not APP_NAME:
        raise ValueError("RENDER_EXTERNAL_URL is not set")

    logger.info(f"Starting bot on port {PORT}")
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f"{APP_NAME}/{TOKEN}")
    
    updater.idle()

if __name__ == '__main__':
    main()
