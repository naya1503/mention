import os, logging, asyncio
from telethon import Button
from telethon import nan as nan
from telethon import TelegramClient as ky
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantErro
from config import *

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = API_ID
api_hash = API_HASH
bot_token = TOKEN
pler = TelegramClient('kynan', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@ky.on(nan.NewMessage(pattern="start$"))
async def start(event):
  await event.reply(
    "Ngapa njeng ? Ni Repo tag all req si RW Buaya Darat",
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/kontenfilm'),
        Button.url('📦 Source', 'https://kynansupport')
      ]
    )
  )

@ky.on(nan.NewMessage(pattern="help$"))
async def help(event):
  helptext = "**Yaelah biji tinggal ketik all doang bego pake ketik help**"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/kontenfilm'),
        Button.url('📦 Source', 'https://kynansupport')
      ]
    )
  )
  
@ky.on(nan.NewMessage(pattern="(all|utag|mention) ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("**Jangan prive bego**")
  
  is_admin = False
  try:
    partici_ = await ky(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("**Lu bukan admin anjeng**")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("**Minimal kasih pesan anjeng!!**")
  elif event.pattern_match.group(1):
    mode = "teks"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "balas"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("**Si anjeng dibilang kasih pesan !!**")
  else:
    return await event.respond("**Si anjeng dibilang kasih pesan !!**")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in ky.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id})\n "
    if usrnum == 5:
      if mode == "teks":
        txt = f"{usrtxt}\n\n{msg}"
        await ky.send_message(chat_id, txt)
      elif mode == "balas":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@ky.on(nan.NewMessage(pattern="(cancel|stop|batal)$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('**Bego orang gak ada tag all**')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('**Iya Anjeng Nih Gua Stop.**')

print("GOBLOK GA JELAS")
ky.run_until_disconnected()