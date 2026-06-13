import aiohttp
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from utils import modules_help, prefix

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Tumhari Nayi Free API Key yahan set ho gayi hai
FREE_GROQ_KEY = "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"

async def fetch_free_ai_response(query: str, message: Message, reply=False):
    if reply:
        response_msg = await message.reply("<code>Thinking (Free Fast Server)... please wait.</code>")
    else:
        response_msg = await message.edit("<code>Thinking (Free Fast Server)... please wait.</code>")

    headers = {
        "Authorization": f"Bearer {FREE_GROQ_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": query}
        ],
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_API_URL, headers=headers, json=payload) as resp:
                if resp.status == 401:
                    await response_msg.edit_text("❌ Invalid Groq API Key! Please check your key.")
                    return
                resp.raise_for_status()
                data = await resp.json()

        response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "I'm sorry, I couldn't find an answer.")
        response_content = f"Question:\n{query}\nAnswer:\n{response_text}"
        await response_msg.edit_text(response_content, parse_mode=enums.ParseMode.MARKDOWN)

    except Exception as e:
        await response_msg.edit_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("grok", prefix))
async def grok(_, message: Message):
    if len(message.command) < 2:
        if message.from_user and message.from_user.is_self:
            await message.edit(f"Usage: {prefix}grok <query>")
        else:
            await message.reply(f"Usage: {prefix}grok <query>")
        return

    query = " ".join(message.command[1:]).strip()
    is_reply = False
    if message.from_user and message.from_user.is_self:
        is_reply = False

    await fetch_free_ai_response(query, message, reply=is_reply)

modules_help["grokai"] = {
    "grok [query]*": "Ask anything to Free Fast AI (No billing required!)."
}
