import os 
import logging 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.WARNING)


tgraph = Client(
   "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH
)


@tgraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\n Image to Telegrph Media Bot by [TUBOTS](https://t.me/tubots)",
        disable_web_page_preview=True
    )


@tgraph.on_message(filters.photo)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading to database...", True)
    img_path = await message.download()
    await dwn.edit_text("Uploading as telegra.ph media link...")
    try:
        url_path = upload_file(img_path)[0]
    except Exception as error:
        await dwn.edit_text(f"error something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}"
                    ),
                    InlineKeyboardButton(
                        text="Share",
                        url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}",
                    )
                ]
            ]
        )
    )
    os.remove(img_path)


tgraph.run()
