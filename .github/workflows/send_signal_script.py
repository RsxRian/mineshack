# send_signal_script.py
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import time
import os
import logging

# --- লগিং কনফিগারেশন ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- এনভায়রনমেন্ট ভেরিয়েবল থেকে কনফিগারেশন নিন ---
BOT_TOKEN = os.getenv("7649120098:AAGU1nDW280cMTGphthcSXKjGbtWFzLC0DU")
CHANNEL_ID = os.getenv("-1002212000149") # যেমন: "@yourchannelname" বা -100xxxxxxxxxx

HOW_TO_PLAY_VIDEO_URL = os.getenv("HOW_TO_PLAY_VIDEO_URL", "https://www.youtube.com/watch?v=examplevideo")
PROMO_CODE = os.getenv("PROMO_CODE", "RS6T9")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "@rsx_rian") # শুরুতে @ সহ
GAME_PLAY_URL = os.getenv("GAME_PLAY_URL", "https://example.com/playgame")
GRID_SIZE = 5

# --- ইমোজি ---
BOMB_EMOJI = "💣"; ATTEMPT_EMOJI = "🔄"; STAR_EMOJI = "⭐"; EMPTY_CELL_EMOJI = "🟦"
CONTROLLER_EMOJI = "🎮"; POINTER_EMOJI = "👇"; DIAMOND_EMOJI = "💎"; THINKING_EMOJI = "😳"
RIGHT_POINTER_EMOJI = "👉"; SMILEY_EMOJI = "😊"; KEY_EMOJI = "🔑"; CHECK_EMOJI = "✅"
WARNING_EMOJI = "⚠️"; MEGAPHONE_EMOJI = "📢"; HAND_WAVE_EMOJI = "👋"; PLAY_BUTTON_EMOJI = "▶️"

def generate_mines_grid_string_html(stars_to_place):
    grid = [[EMPTY_CELL_EMOJI for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    all_cells = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            all_cells.append((r, c))
    random.shuffle(all_cells)
    for i in range(min(stars_to_place, len(all_cells))):
        r, c = all_cells[i]
        grid[r][c] = STAR_EMOJI
    grid_str_lines = ["".join(row) for row in grid]
    return "\n".join(grid_str_lines)

def send_signal():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN এনভায়রনমেন্ট ভেরিয়েবল সেট করা নেই।")
        return
    if not CHANNEL_ID:
        logger.error("TELEGRAM_CHANNEL_ID এনভায়রনমেন্ট ভেরিয়েবল সেট করা নেই।")
        return

    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        logger.info(f"বট ইনিশিয়ালাইজ হয়েছে। '{CHANNEL_ID}' চ্যানেলে সিগন্যাল পাঠানো হচ্ছে...")

        num_bombs = 5
        num_attempts = 5
        num_stars_in_grid = random.randint(7, 12)
        grid_representation = generate_mines_grid_string_html(num_stars_in_grid)
        
        clean_support_username = SUPPORT_USERNAME.lstrip('@')
        support_link = f"https://t.me/{clean_support_username}"

        message_text = f"""
{CHECK_EMOJI} <b>CONFIRMED ENTRY!</b>

{BOMB_EMOJI} Bombs: {num_bombs}  {ATTEMPT_EMOJI} Attempts: {num_attempts}
{CONTROLLER_EMOJI} <b>Play Now</b> {POINTER_EMOJI}

<pre>{grid_representation}</pre>

{DIAMOND_EMOJI} <b>VIP MINES SIGNAL</b> {DIAMOND_EMOJI}

{THINKING_EMOJI} যেভাবে খেলবেন ? {RIGHT_POINTER_EMOJI} <a href="{HOW_TO_PLAY_VIDEO_URL}">ভিডিও দেখতে ক্লিক করুন</a> {SMILEY_EMOJI}

{KEY_EMOJI} Promo Code: <code>{PROMO_CODE}</code> {CHECK_EMOJI}

{WARNING_EMOJI} একাউন্ট খোলার সময় আমার প্রোমো কোড (<code>{PROMO_CODE}</code>) ব্যবহার করুন। না হলে সিগন্যাল মিলে না {WARNING_EMOJI}

{MEGAPHONE_EMOJI} Support Id <a href="{support_link}">{SUPPORT_USERNAME}</a>
"""
        keyboard = [[InlineKeyboardButton(f"{HAND_WAVE_EMOJI} Click Here To Play {PLAY_BUTTON_EMOJI}", url=GAME_PLAY_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(
            chat_id=CHANNEL_ID,
            text=message_text,
            parse_mode='HTML',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.info(f"HTML সিগন্যাল সফলভাবে '{CHANNEL_ID}' চ্যানেলে পাঠানো হয়েছে।")

    except telegram.error.BadRequest as e:
        logger.error(f"টেলিগ্রাম মেসেজ পাঠাতে সমস্যা (BadRequest): {e}")
    except telegram.error.Unauthorized as e:
        logger.error(f"টেলিগ্রাম মেসেজ পাঠাতে সমস্যা (Unauthorized): {e}. বট টোকেন বা চ্যানেলের অনুমতি পরীক্ষা করুন।")
    except Exception as e:
        logger.error(f"সিগন্যাল পাঠানোর সময় একটি অপ্রত্যাশিত সমস্যা হয়েছে: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("সিগন্যাল পাঠানোর স্ক্রিপ্ট শুরু হচ্ছে...")
    send_signal()
    logger.info("সিগন্যাল পাঠানোর স্ক্রিপ্ট সম্পন্ন।")