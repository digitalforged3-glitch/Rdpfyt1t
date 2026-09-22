import asyncio
import multiprocessing
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

# Multiprocessing me status share karne ke liye global dictionaries kaam nahi karti, Isliye Value use ki hai
is_fighting_shared = multiprocessing.Value('b', False)

def run_bot_process(bot_idx, token, is_fighting_shared):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = TelegramClient(f'bot_army_proc_{bot_idx}', API_ID, API_HASH)
    
    async def bot_main():
        try:
            await client.start(bot_token=token)
            print(f"🚀 [ENGINE {bot_idx + 1}] Fully Loaded & Running Dedicated Core!")
        except Exception as e:
            print(f"❌ [ENGINE {bot_idx + 1}] Connection Error: {e}")
            return

        @client.on(events.NewMessage(pattern=r'\.fyt(?:\s+(.+))?', incoming=True))
        async def start_fyt(event):
            raw_text = event.pattern_match.group(1)
            if not raw_text:
                return

            if is_fighting_shared.value:
                return

            try:
                await event.delete()
            except:
                pass

            messages_list = [line.strip() for line in raw_text.split('|') if line.strip()]
            is_fighting_shared.value = True
            
            await event.respond(f"⚡ **ALL CORES UNLOCKED! Machine-Gun Mode Active.**")

            # Har ek bot apne alag core par bina ruke loop chalayega
            while is_fighting_shared.value:
                for msg in messages_list:
                    if not is_fighting_shared.value:
                        break
                    try:
                        # Direct fire bina kisi await lag ke
                        asyncio.create_task(client.send_message(event.chat_id, msg))
                    except:
                        pass
                # Sirf microsecond ka break taaki computer freeze na ho, speed slow nahi hogi
                await asyncio.sleep(0.001)

        @client.on(events.NewMessage(pattern=r'\.stop', incoming=True))
        async def stop_fyt(event):
            if is_fighting_shared.value:
                is_fighting_shared.value = False
                try:
                    await event.delete()
                except:
                    pass
                await event.respond("🛑 **All Engines Stopped!**")

        await client.run_until_disconnected()

    loop.run_until_complete(bot_main())

if __name__ == '__main__':
    # Windows/Android compatibility ke liye freeze_support uri hai
    multiprocessing.freeze_support()
    
    print(f"🔥 Core Engines ko boot kiya ja rha hai...")
    processes = []
    
    for idx, token in enumerate(BOT_TOKENS):
        p = multiprocessing.Process(target=run_bot_process, args=(idx, token, is_fighting_shared))
        p.start()
        processes.append(p)
        
    for p in processes:
        p.join()
        
