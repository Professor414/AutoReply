import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# បើកដំណើរការ Logging ដើម្បីឲ្យយើងដឹងពីបញ្ហា
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ផ្នែករៀបចំ Menu ---
button_products = KeyboardButton(text="♾ ផលិតផល")
button_location = KeyboardButton(text="📍 ទីតាំង & ទំនាក់ទំនង")
button_about_us = KeyboardButton(text="ℹ️ អំពីយើង")

main_menu_layout = [
    [button_products, button_location],
    [button_about_us]
]
main_menu_keyboard = ReplyKeyboardMarkup(main_menu_layout, resize_keyboard=True)

# --- ផ្នែក Handlers (មុខងារឆ្លើយតប) ---
# Function ថ្មីៗត្រូវតែជា async
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ផ្ញើសារស្វាគមន៍ និងបង្ហាញ Menu នៅពេលអ្នកប្រើប្រាស់វាយ /start"""
    user = update.effective_user
    await update.message.reply_html(
        f"♾ សួស្តីបាទ {user.mention_html()}! សូមស្វាគមន៍\n\nតើបងមានអ្វីខ្ញុំអាចជួយអ្វីបានទេ? សូមជ្រើសរើសពី Menu ខាងក្រោម៖",
        reply_markup=main_menu_keyboard
    )

async def handle_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'ផលិតផល'"""
    reply_text = "នេះគឺជាបញ្ជីផលិតផលរបស់យើង៖\n- ផលិតផល A: តម្លៃ $10\n- ផលិតផល B: តម្លៃ $20\n- ផលិតផល C: តម្លៃ $30"
    await update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'ទីតាំង & ទំនាក់ទំនង'"""
    reply_text = "📍 ហាងយើងខ្ញុំមានទីតាំងនៅផ្ទះលេខ 25, ផ្លូវ 123, សង្កាត់បឹងកេងកង, រាជធានីភ្នំពេញ។\n\n📞 លេខទូរសព្ទទំនាក់ទំនង៖ 012 345 678"
    await update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

async def handle_about_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ឆ្លើយតបនៅពេលគេចុចប៊ូតុង 'អំពីយើង'"""
    reply_text = "ℹ️ យើងខ្ញុំគឺជាហាងដែលផ្តល់ជូនផលិតផលដែលមានគុណភាពខ្ពស់ និងសេវាកម្មល្អបំផុតជូនអតិថិជន។"
    await update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

async def handle_unknown_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ឆ្លើយតបទៅសារដែលមិនស្គាល់"""
    reply_text = "ขออภัยครับ ខ្ញុំមិនយល់ពីអ្វីដែលអ្នកចង់បានទេ។ សូមសាកល្បងជ្រើសរើសពី Menu ដែលមានស្រាប់។"
    await update.message.reply_text(reply_text, reply_markup=main_menu_keyboard)

def main() -> None:
    """ចាប់ផ្តើមដំណើរការ Bot"""
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        logger.error("!!! សូមកំណត់ TELEGRAM_TOKEN ជា Environment Variable ជាមុនសិន។")
        return

    # ប្រើ Application.builder() ជំនួស Updater
    application = Application.builder().token(TOKEN).build()

    # ចុះឈ្មោះ Handlers
    application.add_handler(CommandHandler("start", start))

    # ប្រើ filters (អក្សរតូច) ជំនួស Filters (អក្សរធំ)
    application.add_handler(MessageHandler(filters.Regex('^🛍️ ផលិតផល$'), handle_products))
    application.add_handler(MessageHandler(filters.Regex('^📍 ទីតាំង & ទំនាក់ទំនង$'), handle_location))
    application.add_handler(MessageHandler(filters.Regex('^ℹ️ អំពីយើង$'), handle_about_us))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_messages))

    # ចាប់ផ្តើម Bot
    logger.info("Bot កំពុងដំណើរការ...")
    application.run_polling()

if __name__ == "__main__":
    main()
