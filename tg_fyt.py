import asyncio
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 39630731        
API_HASH = "ea47c620b13cf4316bf69956a8e6eba8"

BOT_TOKENS = [
    "8919356174:AAGqQj042a11UKyccu69xv3MU1QCFLuiXbw",
    "8942102372:AAGr94WpSfW4obpUYuNpFR3bH0lx00O9O94",
    "8653014765:AAEW26SB4_SESEkex690zIiZtDJCJ41VbDM",
    "8971859921:AAHS6u-t_QGrabanIGsAFCKF1tc_4pT9hE8",
    "8959720350:AAFj3nH2AGmAjh5WUBEkAdCvMGuIAfQMHxw"
]
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
        master_client = bot_clients[0]

        @master_client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?', incoming=True))
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
            
            await event.respond(f"⚡ **GOD SPEED ACTIVATED! Nonstop firing {len(messages_list)} lines...**")

            # Is loop me hum 'await' nahi kar rahe hain messages bhejne ke liye
            # Isliye bina 1 microsecond ruke saare messages ek sath flood ho jayenge
            while is_fighting.get(chat_id, False):
                for msg in spam_lines[chat_id]:
                    if not is_fighting.get(chat_id, False):
                        break
                    
                    for bot in bot_clients:
                        # asyncio.create_task se background me message chala jata hai, loop rukta nahi hai
                        asyncio.create_task(bot.send_message(chat_id, msg))
                
                # Ek round poora hone ke baad micro-delay taaki script crash na ho aur processor free rahe
                await asyncio.sleep(0.01)

        @master_client.on(events.NewMessage(pattern=r'\.stop', incoming=True))
        async def stop_fyt(event):
            chat_id = event.chat_id
            if is_fighting.get(chat_id, False):
                is_fighting[chat_id] = False
                try:
                    await event.delete()
                except:
                    pass
                await event.respond("🛑 **God Speed Stopped!**")

async def main():
    await start_all_bots()
    if bot_clients:
        print("🤖 [GOD SPEED LIVE] Waiting for '.fyt' command...")
        await asyncio.gather(*[client.run_until_disconnected() for client in bot_clients])

if __name__ == '__main__':
    asyncio.run(main())
    
