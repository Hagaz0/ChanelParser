import pymorphy2

# Вставляем ссылку в глагол с использованием библиотеки pymorphy2. Если флаг поднят, ссылка уже была вставлена
# Собираем конечную строчку по словам и возвращаем ее
def input_link(chanel, message_id, text):
    result = ""
    flag = 0
    link = f"https://t.me/{chanel}/{message_id}"
    words = text.split()
    morph = pymorphy2.MorphAnalyzer()
    for word in words:
        p = morph.parse(word)[0]
        if 'VERB' in p.tag and flag == 0:
            flag = 1
            result += f"[{word}]({link}) "
        else:
            result += word + " "
    if flag:
        return result
    else:
        return 0

# Функция возвращает первое предложение. Первым предложением считается весь текст до первого \n
def text_cutter(text):
    result = ""
    for i in text:
        if i != '\n':
            result += i
        else:
            break
    return result

# Находим эмодзи с наибольшим количеством реакций
def get_emoji(message):
    max = 0
    emoji = 0
    if message.reactions is not None:
        if message.reactions.reactions is not None:
            max = 0
            emoji = 0
            for i in message.reactions.reactions:
                if i.count > max:
                    max = i.count
                    emoji = i.emoji
    return emoji

# Проверка на существование чата
async def is_valid_chat(app, chanel):
    try:
        chat = await app.get_chat(chanel)
    except:
        chat = 0
    return chat

# Парсим последние 30 постов (если конечное сообщение будет слишком длинным, может быть ошибка об отправке)
# Постом считаются те записи, которые содержать хотя-бы одну реакцию и глагол в первом предложении
async def parse_chanel(app, chanel):
    result = ""
    # Начинаем проходиться по сообщениям
    async for message in app.get_chat_history(chanel, limit=30):
        # Парсим эмодзи с наибольшим количеством реакций. Если таких нет, не считаем за пост
        emoji = get_emoji(message)
        if emoji == 0:
            continue
        # В зависимости от поста, текст может храниться либо в text, либо в caption. Вставляем ссылку в глагол,
        # если он есть, и возвращаем первое предложение с ссылкой на пост
        if message.text is not None:
            with_link = input_link(chanel, message.id, text_cutter(message.text))
        elif message.caption is not None:
            with_link = input_link(chanel, message.id, text_cutter(message.caption))
        else:
            continue
        # Добавляем к конечному результату информацию о посте
        if with_link != 0:
            result += emoji + " " + with_link + "\n\n"
    return result

# Проверяем существование канала, является ли чат каналом, есть ли в нем посты
async def checks(app, chanel, link):
    chat = await is_valid_chat(app, chanel)
    if chat == 0:
        print("Такого канала не существует")
        return 0
    result = f"[{chat.title}]({link})\n\n"
    if result is None:
        print("Чат не является каналом")
        return 0

    # Если вернется пустая строка, то канал не содержит нужных нам постов
    text = await parse_chanel(app, chanel)
    if text == "":
        print("Канал не содержит постов")
        return 0

    # Конечный формат отправляется в личные сообщения самому себе
    await app.send_message("me", result + text)
