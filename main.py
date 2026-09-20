import os

os.system('pip install pyrogram tgcrypto')

from pyrogram import Client, filters

from pyrogram.types import Message

from pyrogram.enums import ChatMemberStatus

import asyncio

API_ID = 15710310

API_HASH = "41e19b982ee32bbba1ec692497836600"

BOT_TOKEN = '8729228954:AAF0RF-fFQ1FzeUGyHkAX2QxNLjr4Dv2zOg'

app = Client(

    "my_bot",

    api_id=API_ID,

    api_hash=API_HASH,

    bot_token=BOT_TOKEN

)

def is_admin_or_creator(member):

    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

@app.on_message(filters.text & filters.group & filters.regex("^المالك$"))

async def handle_owner(client: Client, message: Message):

    chat = message.chat

    

    async for member in client.get_chat_members(chat.id):

        if member.status == ChatMemberStatus.OWNER:

            creator = member.user

            if creator.username:

                owner_text = f"👑 **مالك المجموعة:** @{creator.username}"

            else:

                owner_text = f"👑 **مالك المجموعة:** {creator.first_name}"

            

            await message.reply_text(owner_text)

            return

    

    await message.reply_text("**لم أتمكن من العثور على المالك**")

@app.on_message(filters.text & filters.group & filters.regex("^المشرفين$"))

async def handle_admins(client: Client, message: Message):

    chat = message.chat

    user = message.from_user

    

    member = await chat.get_member(user.id)

    if not is_admin_or_creator(member):

        await message.reply_text("**هذا الأمر متاح فقط للمشرفين.**")

        return

    

    admins_text = "👥 **قائمة المشرفين:**\n\n"

    

    async for member in client.get_chat_members(chat.id):

        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:

            user = member.user

            role = "👑 المالك" if member.status == ChatMemberStatus.OWNER else "🛡️ مشرف"

            

            if user.username:

                admins_text += f"**{role}:** @{user.username}\n"

            else:

                admins_text += f"**{role}:** {user.first_name}\n"

    

    if len(admins_text) > 10:

        await message.reply_text(admins_text)

    else:

        await message.reply_text("**لا يوجد مشرفين*")

@app.on_message(filters.text & filters.group & filters.regex("^تاك$"))

async def handle_tag(client: Client, message: Message):

    chat = message.chat

    user = message.from_user

    

    member = await chat.get_member(user.id)

    if not is_admin_or_creator(member):

        await message.reply_text("**الامر لايخصك**")

        return

    

    await message.reply_text("**جاري بدء عملية التاكات**")

    

    try:

        members = []

        

        async for member in client.get_chat_members(chat.id):

            members.append(member)

        

        if not members:

            await client.send_message(chat.id, "**لا يوجد أعضاء في المجموعة.**")

            return

        

        chunk_size = 200

        members_chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]

        

        for chunk in members_chunks:

            tag_message = "**تم عمل التاكات**\n\n"

            

            for member in chunk:

                user = member.user

                if user.username:

                    tag_message += f"@{user.username}\n"

                else:

                    tag_message += f"[{user.first_name}](tg://user?id={user.id})\n"

            

            await client.send_message(chat.id, tag_message)

            await asyncio.sleep(2)

        

    except Exception as e:

        await client.send_message(chat.id, f"**حدث خطأ تواصل مع المبرمج @PY_83**")

print("✓ البوت يعمل الآن...")

app.run()
