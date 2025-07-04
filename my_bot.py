# -*- coding: utf-8 -*-

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# កំណត់ค่า Logging เพื่อดูข้อผิดพลาด
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==============================================================================
# ==                       កន្លែងកែប្រែទិន្នន័យ (EDIT HERE)                     ==
# ==============================================================================

# (ផ្នែកនេះនៅដដែល មិនចាំបាច់កែប្រែទេ)
PRODUCT_A1_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល A1***\n- នេះជាផលិតផលប្រភេទទី១ របស់ A។\n- តម្លៃ: $11"
PRODUCT_A2_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល A2***\n- នេះជាផលិតផលប្រភេទទី២ របស់ A。\n- តម្លៃ: $12"
PRODUCT_B1_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល B1***\n- នេះជាផលិតផលប្រភេទទី១ របស់ B។\n- តម្លៃ: $21"
PRODUCT_B2_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល B2***\n- នេះជាផលិតផលប្រភេទទី២ របស់ B。\n- តម្លៃ: $22"
PRODUCT_C1_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល C1***\n- នេះជាផលិតផលប្រភេទទី១ របស់ C។\n- តម្លៃ: $31"
PRODUCT_C2_DETAIL = "*\n**ព័ត៌មានលម្អិតអំពីផលិតផល C2***\n- នេះជាផលិតផលប្រភេទទី២ របស់ C。\n- តម្លៃ: $32"
LOCATION_MAP_DETAIL = "[ចុចទីនេះដើម្បីមើលบน Google Maps](https://maps.google.com/?q=11.5564,104.9282)"
LOCATION_ADDRESS_DETAIL = "*អាសយដ្ឋាន:*\nផ្ទះលេខ ១២៣, ផ្លូវ ៤៥៦, សង្កាត់បឹងកេងកង, ខណ្ឌចំការមន, រាជធានីភ្នំពេញ"
CONTACT_PHONE_DETAIL = "ទូរស័ព្ទ: `+855 12 345 678` (ចុចដើម្បី Copy)"
CONTACT_EMAIL_DETAIL = "អ៊ីមែល: `info@yourcompany.com` (ចុចដើម្បី Copy)"
CONTACT_WECHAT_DETAIL = "WeChat ID: `your_wechat_id` (ចុចដើម្បី Copy)"

# ==============================================================================
# ==                  កូដរបស់ Bot (កូដថ្មីสำหรับ Version 20+)                 ==
# ==============================================================================

# --- Keyboard Functions (នៅដដែល) ---
def get_main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("📦 ផលិតផល (Product)", callback_data='main_product')], [InlineKeyboardButton("📍 ទីតាំង (Location)", callback_data='main_location')], [InlineKeyboardButton("📞 ទំនាក់ទំនង (Contact)", callback_data='main_contact')]]
    return InlineKeyboardMarkup(keyboard)
def get_product_menu_keyboard():
    keyboard = [[InlineKeyboardButton("ផលិតផល A", callback_data='product_A')], [InlineKeyboardButton("ផលិតផល B", callback_data='product_B')], [InlineKeyboardButton("ផលិតផល C", callback_data='product_C')], [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)
def get_product_A_submenu_keyboard():
    keyboard = [[InlineKeyboardButton("ផលិតផល A1", callback_data='product_A1')], [InlineKeyboardButton("ផលិតផល A2", callback_data='product_A2')], [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')]]
    return InlineKeyboardMarkup(keyboard)
def get_product_B_submenu_keyboard():
    keyboard = [[InlineKeyboardButton("ផលិតផល B1", callback_data='product_B1')], [InlineKeyboardButton("ផលិតផល B2", callback_data='product_B2')], [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')]]
    return InlineKeyboardMarkup(keyboard)
def get_product_C_submenu_keyboard():
    keyboard = [[InlineKeyboardButton("ផលិតផល C1", callback_data='product_C1')], [InlineKeyboardButton("ផលិតផល C2", callback_data='product_C2')], [InlineKeyboardButton("⬅️ ត្រឡប់ទៅបញ្ជីផលិតផល", callback_data='main_product')]]
    return InlineKeyboardMarkup(keyboard)
def get_location_menu_keyboard():
    keyboard = [[InlineKeyboardButton("🗺️ ផែនទី (Map)", callback_data='location_map')], [InlineKeyboardButton("🏠 អាសយដ្ឋាន (Address)", callback_data='location_address')], [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)
def get_contact_menu_keyboard():
    keyboard = [[InlineKeyboardButton("📱 ទូរស័ព្ទ (Phone)", callback_data='contact_phone')], [InlineKeyboardButton("✉️ អ៊ីមែល (Email)", callback_data='contact_email')], [InlineKeyboardButton("💬 WeChat", callback_data='contact_wechat')], [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)

# --- Command and Button Handlers (កែប្រែបន្តិចបន្តួច) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"👋 សួស្តី {user.mention_html()}!\n\nសូមជ្រើសរើសព័ត៌មានដែលអ្នកចង់បាន៖"
    if update.callback_query:
        query = update.callback_query
        await query.edit_message_text(text=welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode='HTML')
    else:
        await update.message.reply_text(text=welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    text, reply_markup, parse_mode, disable_web_page_preview = None, None, 'Markdown', True

    if data == 'main_menu':
        await start(update, context)
        return
    elif data == 'main_product':
        text, reply_markup = "📦 សូមជ្រើសរើសប្រភេទផលិតផល៖", get_product_menu_keyboard()
    elif data == 'main_location':
        text, reply_markup = "📍 សូមជ្រើសរើសព័ត៌មានទីតាំង៖", get_location_menu_keyboard()
    elif data == 'main_contact':
        text, reply_markup = "📞 សូមជ្រើសរើសមធ្យោបាយទំនាក់ទំនង៖", get_contact_menu_keyboard()
    elif data == 'product_A':
        text, reply_markup = "អ្នកបានជ្រើសរើសផលិតផល A, សូមជ្រើសរើសប្រភេទ៖", get_product_A_submenu_keyboard()
    elif data == 'product_B':
        text, reply_markup = "អ្នកបានជ្រើសរើសផលិតផល B, សូមជ្រើសរើសប្រភេទ៖", get_product_B_submenu_keyboard()
    elif data == 'product_C':
        text, reply_markup = "អ្នកបានជ្រើសរើសផលិតផល C, សូមជ្រើសរើសប្រភេទ៖", get_product_C_submenu_keyboard()
    elif data == 'product_A1':
        text, reply_markup = PRODUCT_A1_DETAIL, get_product_A_submenu_keyboard()
    elif data == 'product_A2':
        text, reply_markup = PRODUCT_A2_DETAIL, get_product_A_submenu_keyboard()
    elif data == 'product_B1':
        text, reply_markup = PRODUCT_B1_DETAIL, get_product_B_submenu_keyboard()
    elif data == 'product_B2':
        text, reply_markup = PRODUCT_B2_DETAIL, get_product_B_submenu_keyboard()
    elif data == 'product_C1':
        text, reply_markup = PRODUCT_C1_DETAIL, get_product_C_submenu_keyboard()
    elif data == 'product_C2':
        text, reply_markup = PRODUCT_C2_DETAIL, get_product_C_submenu_keyboard()
    elif data == 'location_map':
        text, reply_markup, disable_web_page_preview = LOCATION_MAP_DETAIL, get_location_menu_keyboard(), False
    elif data == 'location_address':
        text, reply_markup = LOCATION_ADDRESS_DETAIL, get_location_menu_keyboard()
    elif data == 'contact_phone':
        text, reply_markup = CONTACT_PHONE_DETAIL, get_contact_menu_keyboard()
    elif data == 'contact_email':
        text, reply_markup = CONTACT_EMAIL_DETAIL, get_contact_menu_keyboard()
    elif data == 'contact_wechat':
        text, reply_markup = CONTACT_WECHAT_DETAIL, get_contact_menu_keyboard()
    
    if text and reply_markup:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)

def main() -> None:
    """Start the bot and set it up to run on Render."""
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("!!! TELEGRAM_TOKEN environment variable not found!")
        return

    # កូដថ្មីสำหรับ Version 20+
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    PORT = int(os.environ.get('PORT', '8443'))
    APP_NAME = os.environ.get("RENDER_EXTERNAL_URL")
    if not APP_NAME:
        logger.error("!!! RENDER_EXTERNAL_URL environment variable not found!")
        return

    logger.info(f"Starting webhook for bot on URL: {APP_NAME}")

    # កូដថ្មីสำหรับ Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{APP_NAME}/{TOKEN}"
    )

if __name__ == '__main__':
    main()
