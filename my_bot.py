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
# ព័ត៌មានលម្អិតសម្រាប់ផលិតផលនីមួយៗ
PRODUCT_A_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល A***
- លក្ខណៈពិសេសទី១: ...
- លក្ខណៈពិសេសទី២: ...
- តម្លៃ: $10
"""
PRODUCT_B_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល B***
- លក្ខណៈពិសេស: ...
- តម្លៃ: $20
"""
PRODUCT_C_DETAIL = """
*
**ព័ត៌មានលម្អិតអំពីផលិតផល C***
- លក្ខណៈពិសេស: ...
- តម្លៃ: $30
"""

# ព័ត៌មានលម្អិតសម្រាប់ទីតាំង
LOCATION_MAP_DETAIL = "[ចុចទីនេះដើម្បីមើល trên Google Maps](https://maps.google.com/?q=11.5564,104.9282)"
LOCATION_ADDRESS_DETAIL = """
*អាសយដ្ឋាន:*
ផ្ទះលេខ ១២៣, ផ្លូវ ៤៥៦, សង្កាត់បឹងកេងកង, ខណ្ឌចំការមន, រាជធានីភ្នំពេញ
"""

# ព័ត៌មានលម្អិតសម្រាប់ទំនាក់ទំនង
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

def get_back_to_product_keyboard():
    keyboard = [[InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')]]
    return InlineKeyboardMarkup(keyboard)
# --- End Keyboard Functions ---


# Function សម្រាប់ command /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="👋 សួស្តី! សូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖",
        reply_markup=get_main_menu_keyboard()
    )

# Function សម្រាប់គ្រប់គ្រងការចុចប៊ូតុងទាំងអស់
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # ឆ្លើយតបទៅ Telegram ថាបានទទួលការចុចហើយ

    # Main Menu selections
    if query.data == 'main_menu':
        query.edit_message_text(
            text="👋 សូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖",
            reply_markup=get_main_menu_keyboard()
        )
    elif query.data == 'main_product':
        query.edit_message_text(
            text="📦 សូមជ្រើសរើសផលិតផលដើម្បីមើលព័ត៌មានលម្អិត៖",
            reply_markup=get_product_menu_keyboard()
        )
    elif query.data == 'main_location':
        query.edit_message_text(
            text="📍 សូមជ្រើសរើសព័ត៌មានទីតាំង៖",
            reply_markup=get_location_menu_keyboard()
        )
    elif query.data == 'main_contact':
        query.edit_message_text(
            text="📞 សូមជ្រើសរើសមធ្យោបាយទំនាក់ទំនង៖",
            reply_markup=get_contact_menu_keyboard()
        )

    # Product sub-menu selections
    elif query.data == 'product_A':
        query.edit_message_text(
            text=PRODUCT_A_DETAIL,
            reply_markup=get_back_to_product_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == 'product_B':
        query.edit_message_text(
            text=PRODUCT_B_DETAIL,
            reply_markup=get_back_to_product_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == 'product_C':
        query.edit_message_text(
            text=PRODUCT_C_DETAIL,
            reply_markup=get_back_to_product_keyboard(),
            parse_mode='Markdown'
        )
        
    # Location sub-menu selections
    elif query.data == 'location_map':
        query.edit_message_text(
            text=LOCATION_MAP_DETAIL,
            reply_markup=get_location_menu_keyboard(),
            parse_mode='Markdown',
            disable_web_page_preview=False
        )
    elif query.data == 'location_address':
        query.edit_message_text(
            text=LOCATION_ADDRESS_DETAIL,
            reply_markup=get_location_menu_keyboard(),
            parse_mode='Markdown'
        )

    # Contact sub-menu selections
    elif query.data == 'contact_phone':
        query.edit_message_text(
            text=CONTACT_PHONE_DETAIL,
            reply_markup=get_contact_menu_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == 'contact_email':
        query.edit_message_text(
            text=CONTACT_EMAIL_DETAIL,
            reply_markup=get_contact_menu_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == 'contact_wechat':
        query.edit_message_text(
            text=CONTACT_WECHAT_DETAIL,
            reply_markup=get_contact_menu_keyboard(),
            parse_mode='Markdown'
        )


def main() -> None:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("សូមដាក់ TELEGRAM_TOKEN នៅក្នុង Environment Variables")

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # ចុះឈ្មោះ Command Handler
    dispatcher.add_handler(CommandHandler("start", start))

    # ចុះឈ្មោះ Callback Query Handler (สำหรับจัดการប៊ូតុង)
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    # សម្រាប់ Render.com
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
