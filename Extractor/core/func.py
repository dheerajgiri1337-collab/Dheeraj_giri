import asyncio
from datetime import datetime
from pyrogram.errors import UserNotParticipant
from pyrogram.types import *
from config import CHANNEL_ID2
from Extractor.core import script
from Extractor.core.mongo.plans_db import premium_users

# --- YAHAN APNA BACKUP CHANNEL USERNAME DALO (Bina @ ke) ---
CHECK_CH = "BR0DG" 

async def chk_user(query, user_id):
    user = await premium_users()
    if user_id in user:
        await query.answer("Premium User!!")
        return 0
    else:
        await query.answer("Sir, you don't have premium access!!", show_alert=True)
        return 1

async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string.lower())
    if unit == 's': return value
    elif unit == 'min': return value * 60
    elif unit == 'hour': return value * 3600
    elif unit == 'day': return value * 86400
    elif unit == 'month': return value * 86400 * 30
    elif unit == 'year': return value * 86400 * 365
    else: return 0

async def subscribe(app, message):
    try:
        # Bot ab @BR0DG mein check karega ki user ne join kiya ya nahi
        update_channel = CHECK_CH 
        if not update_channel:
            return 0

        try:
            user = await app.get_chat_member(update_channel, message.from_user.id)
            if user.status == "kicked":
                await message.reply_text("🚫 Sorry Sir, You are Banned.")
                return 1
        except UserNotParticipant:
            try:
                # User ko join karne ke liye naya link dikhayega
                join_url = f"https://t.me/{CHECK_CH}"
                sent = await message.reply_photo(
                    photo="https://telegra.ph/file/b7a933f423c153f866699.jpg",
                    caption=script.FORCE_MSG.format(message.from_user.mention),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🤖 JOIN BACKUP CHANNEL 🤖", url=join_url)
                    ]])
                )
                await asyncio.sleep(15)
                await sent.delete()
            except Exception as e:
                print(f"Link error: {e}")
                await message.reply_text(
                    "❗ Please join our backup channel to use the bot.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🤖 JOIN BACKUP 🤖", url=f"https://t.me/{CHECK_CH}")
                    ]])
                )
            return 1
        except Exception as e:
            print(f"Subscribe error inner: {e}")
            return 0
        return 0
    except Exception as e:
        print(f"Subscribe error outer: {e}")
        return 0
