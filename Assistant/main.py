import asyncio
from talk import Talk
from listen import Listen
from helpers import load_data, save_user
from app import AssistCore


async def main():
    init_talk = Talk()
    init_listen = Listen()

    async def assistant_set_up(talk, listen):
        await init_talk.speak_text(audioname="aud001", text="You need to set up this personal assistant before using it. Firstly, What is your name? say only the name you want the assistant to call you.")
        user_name = init_listen.record_text()
        await init_talk.speak_text(audioname="aud002", text=f"Nice to meet you, {user_name}. What would you like to call me?")
        ai_name = init_listen.record_text()
        return user_name, ai_name
    
    async def creator(status):
        data = load_data()

        Assistant = AssistCore(data)  
        if status == "new":
            await Assistant.new_greet()
        else:
            await Assistant.greet()
    
        await Assistant.activate()

    data = load_data()
    if data:
        await creator(status = "old")
    else:
        user_name, ai_name = await assistant_set_up(init_talk, init_listen)
        save_user(user_name, ai_name)
        await creator(status= "new")
    

if __name__ == "__main__":
    asyncio.run(main())