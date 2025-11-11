
import asyncio
from core.waifu import Waifu


async def main():
    waifu = Waifu()
    await waifu.init()

    while True:
        #user_input = input("Você: ")
        response = await waifu.handle_recognition()
        waifu.handle_output(response)
        # waifu.handle_speak(spoken_text)


if __name__ == "__main__":
    asyncio.run(main())