from pyrogram import Client, types
import functions

# Вставить свои значения
api_id = 123456789
api_hash = 'avfksngdsjfgn23456480958082yrhe'

app = Client("my_account")

# Принимаем из стандартного ввода ссылку, извлекаем логин канала и передаем в функцию проверки
async def main():
    link = input("Введите ссылку на телеграм канал: ")
    chanel = link[13:]
    async with app:
        await functions.checks(app, chanel, link)

app.run(main())
