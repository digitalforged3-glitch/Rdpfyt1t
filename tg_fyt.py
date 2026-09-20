import asyncio
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 39630731        
API_HASH = "ea47c620b13cf4316bf69956a8e6eba8"

# Aapke 5 naye fresh tokens perfectly aligned hain
BOT_TOKENS = [
    "8919356174:AAGqQj042a11UKyccu69xv3MU1QCFLuiXbw",
    "8942102372:AAGr94WpSfW4obpUYuNpFR3bH0lx00O9O94",
    "8653014765:AAEW26SB4_SESEkex690zIiZtDJCJ41VbDM",
    "8971859921:AAHS6u-t_QGrabanIGsAFCKF1tc_4pT9hE8",
    "8959720350:AAFj3nH2AGmAjh5WUBEkAdCvMGuIAfQMHxw"
]

DELAY = 0.1
# ---------------------

is_fighting = {}
spam_lines = {}
bot_clients = []

async def start_all_bots():
    print(f"⚙️ Total {len(BOT_TOKENS)} Bots ko connect kiya ja rha h...")
    for idx, token in enumerate(BOT_TOKENS):
        try:
            client = TelegramClient(f'bot_army_fresh_{idx}', API_ID, API_HASH)
            await client.start(bot_token=token)
            bot_clients.append(client)
            print(f"✅ Bot {idx + 1} Matrix me online ho gaya h!")
        except Exception as e:
            print(f"❌ Bot connection error: {e}")

    if bot_clients:
        for client in bot_clients:
            @client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?', incoming=True))
            async def start_fyt(event):
                chat_id = event.chat_id
                raw_text = event.pattern_match.group(1)

                if not raw_text:
                    return

                if is_fighting.get(chat_id, False):
                    return

                try:
                    await event.delete()
                except:
                    pass

                messages_list = [line.strip() for line in raw_text.split('|') if line.strip()]
                is_fighting[chat_id] = True
                spam_lines[chat_id] = messages_list
                
                await event.respond(f"🤖 **5-Bot Clean Army Activated! Loaded {len(messages_list)} live lines.**")

                while is_fighting.get(chat_id, False):
                    for msg in spam_lines[chat_id]:
                        if not is_fighting.get(chat_id, False):
                            break
                        
                        tasks = [bot.send_message(chat_id, msg) for bot in bot_clients]
                        try:
                            await asyncio.gather(*tasks)
                            await asyncio.sleep(DELAY)
                        except Exception as e:
                            print(f"⚠️ Limit: {e}")
                            await asyncio.sleep(1)

            @client.on(events.NewMessage(pattern=r'\.stop', incoming=True))
            async def stop_fyt(event):
                chat_id = event.chat_id
                if is_fighting.get(chat_id, False):
                    is_fighting[chat_id] = False
                    try:
                        await event.delete()
                    except:
                        pass

async def main():
    await start_all_bots()
    if bot_clients:
        print("🤖 [FRESH ARMY LIVE] Waiting for '.fyt' command from your ID...")
        await asyncio.gather(*[client.run_until_disconnected() for client in bot_clients])

if __name__ == '__main__':
    asyncio.run(main())
    
