
import asyncio
from core.waifu import Waifu


async def main():
    waifu = Waifu()
    await waifu.init()

    while True:
        user_input = input("Você: ")
        response = waifu.handle_input(user_input)

        #waifu.handle_speak(response)
        print(f"Kiana: {response}")

if __name__ == "__main__":
    asyncio.run(main())