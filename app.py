from vkbottle.bot import Bot, Message
from config import token
from vkbottle import BaseStateGroup
from vkbottle import Keyboard, Text, CtxStorage
import psycopg2 as ps
import smtplib
import datetime

bot = Bot(token=token)
ctx = CtxStorage()


async def send_mail(mail, text):
    sender = 'iMediatorChatBot@yandex.ru'
    password = '!QZ2wxas'
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
        sender, mail, 'Заявка')
    msg += text
    mail_lib.sendmail(sender, mail, msg.encode('utf8'))
    mail_lib.quit()


class UserState(BaseStateGroup):
    name = 1
    city = 2
    phone_number = 3
    email = 4
    comment = 5


@bot.on.message(text='start')
async def start_msg(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Кто вы?'))
    keyboard.row()
    keyboard.add(Text('Зачем мне это?'))
    keyboard.row()
    keyboard.add(Text('Описать проблему и оставить данные'))
    await message.answer("Добрый день!\n"
                         "Я — Евгений, виртуальный ассистент проекта i-Mediator.\n"
                         "Чем могу быть полезен?", keyboard=keyboard)


@bot.on.message(text='Кто вы?')
async def cmd_1_1(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Кто такой медиатор?'))
    # keyboard.row()   #после создание сайта добавить эти кнопки
    # keyboard.add(Text('Перейти на сайт i-mediator.ru'))
    await message.answer("Мы — сообщество профессиональных медиаторов.\n"
                         "Помогаем решать юридические, семейные и административные споры во внесудебном порядке.",
                         keyboard=keyboard)


@bot.on.message(text='Зачем мне это?')
async def cmd_1_2(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Кто такой медиатор?'))
    keyboard.row()
    keyboard.add(Text('Перейти на сайт i-mediator.ru'))
    await message.answer('К нам обращаются, если:\n'
                         '- необходимо решить спор в кратчайшие сроки\n'
                         '- при этом сохранить полную конфиденциальность\n'
                         '- а также отношения с участником спора в будущем', keyboard=keyboard)


@bot.on.message(text=['Описать проблему и оставить данные', 'Свяжитесь со мной, хочу задать вопрос консультанту'])
async def cmd_1_3(message: Message):
    await bot.state_dispenser.set(message.peer_id, UserState.name)
    return 'Введите пожалуйста ФИО:'


@bot.on.message(state=UserState.name)
async def cmd_name(message: Message):
    ctx.set('name', message.text)
    await bot.state_dispenser.set(message.peer_id, UserState.city)
    return 'Город:'


@bot.on.message(state=UserState.city)
async def cmd_city(message: Message):
    ctx.set('city', message.text)
    await bot.state_dispenser.set(message.peer_id, UserState.phone_number)
    return 'Номер телефона:'


@bot.on.message(state=UserState.phone_number)
async def cmd_phone_number(message: Message):
    ctx.set('phone_number', message.text)
    await bot.state_dispenser.set(message.peer_id, UserState.email)
    return 'Почта:'


@bot.on.message(state=UserState.email)
async def cmd_email(message: Message):
    ctx.set('email', message.text)
    await bot.state_dispenser.set(message.peer_id, UserState.comment)
    return 'Комментарии по желанию'


@bot.on.message(state=UserState.comment)
async def cmd_comment(message: Message):
    global connect
    name = ctx.get('name').split()
    city = ctx.get('city')
    phone_number = ctx.get('phone_number')
    email = ctx.get('email')
    comment = message.text
    time = datetime.datetime.now()
    all_info = f"ФИО: {name}\n" \
               f"Город: {city}\n" \
               f"Телефон номер: {phone_number}\n" \
               f"Почта:  {email}\n" \
               f"Комментарии: {comment}\n" \
               f"Время и дата заявки: {time}"
    try:
        connect = ps.connect(host='92.255.76.86',
                             port=5432,
                             database='imediators',
                             user='mekan99',
                             password='Mm6347455627.')
        if len(name) == 2:
            with connect.cursor() as cursor:
                cursor.execute("""INSERT INTO users (firstname, lastname, patronymic, city, phone_number, email, 
                comment_users, where_user, date_request, user_request, search_mediators, work_mediators, payments, 
                refusal, expectation, comment_admin) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (name[0], name[1], None, city, phone_number, email,
                                comment, 'VK', time, None, None, None, None, None, None, None))
                connect.commit()
        else:
            with connect.cursor() as cursor:
                cursor.execute("""INSERT INTO users (firstname, lastname, patronymic, city, phone_number, email, 
                comment_users, where_user, date_request, user_request, search_mediators, work_mediators, payments, 
                refusal, expectation, comment_admin) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (name[0], name[1], name[2], city, phone_number,
                                email,
                                comment, 'VK', time, None, None, None, None, None, None, None))
                connect.commit()

    except Exception as ex:
        print(f"[Error] {ex}")
    finally:
        if connect:
            connect.close()
    await send_mail('info.i.mediator@yandex.ru', all_info)
    await message.answer("Спасибо!\n"
                         "Мы свяжемся с вами в ближайшее время.")


@bot.on.message(text='Кто такой медиатор?')
async def cmd_2_1(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Сколько стоят услуги?'))
    keyboard.row()
    keyboard.add(Text('Как долго длится медиация?'))
    keyboard.row()
    keyboard.add(Text('Описать проблему и оставить данные'))
    await message.answer('Медиатор — это нейтральное лицо, которое помогает достичь соглашения в споре.\n'
                         'Его главные задачи:\n'
                         '- перевести переговоры из эмоционального русла в конструктивное.\n'
                         '- помочь сторонам понять свои интересы и договориться о взаимовыгодном решении конфликта.\n'
                         '95% соглашений, достигнутых на процедуре медиации, исполняется сторонами добровольно!',
                         keyboard=keyboard)


@bot.on.message(text='Сколько стоят услуги?')
async def cmd_3_1(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Как долго длится медиация?'))
    keyboard.row()
    keyboard.add(Text('Описать проблему и оставить данные'))
    await message.answer('Это зависит от сложности и вида проблемы. Но зачастую услуги медиатора обходятся '
                         'значительно дешевле услуг адвоката, а оплата взимается с обеих сторон в равных частях и '
                         'только в случае положительного завершения спора', keyboard=keyboard)


@bot.on.message(text='Как долго длится медиация?')
async def cmd_3_2(message: Message):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text('Интересно, но у меня остались вопросы'))
    keyboard.row()
    keyboard.add(Text('Описать проблему и оставить данные'))
    await message.answer('В среднем, требуется 2-4 медиации для достижения соглашения. Как правило, это занимает '
                         '2-3 недели.\n'
                         'Но все случаи индивидуальны, поэтому для уточнения сроков вы можете оставить контакты. '
                         'Мы свяжемся с вами для уточнения деталей и сможем сказать более точные сроки.',
                         keyboard=keyboard)


@bot.on.message(text='Интересно, но у меня остались вопросы')
async def cmd_4_1(message: Message):
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text('Все понятно, готов оставить заявку'))
    keyboard.row()
    keyboard.add(Text('Этапы работы'))
    keyboard.row()
    keyboard.add(Text('Где проходят переговоры?'))
    keyboard.row()
    keyboard.add(Text('Поможет ли медиатор в моем случае?'))
    keyboard.row()
    keyboard.add(Text('А если мне не понравится мой медиатор?'))
    keyboard.row()
    keyboard.add(Text('Свяжитесь со мной, хочу задать вопрос консультанту'))
    keyboard.row()
    keyboard.add(Text('Преимущества работы с медиаторами'))
    keyboard.row()
    keyboard.add(Text('Как быстро я получу результат?'))
    keyboard.row()
    keyboard.add(Text('Сколько стоят услуги?'))
    # keyboard.row()
    # keyboard.add(Text('Сайт  i-Mediator'))
    keyboard.row()
    await message.answer('Я подобрал для вас ответы на часто задаваемые вопросы', keyboard=keyboard)


@bot.on.message(text='Этапы работы')
async def cmd_5_1(message: Message):
    await message.answer('<b>1</b>. Проводим консультацию, где знакомим со сроками и стоимостью\n'
                         '<b>2</b>. Заключаем договор, согласуем план и количество встреч\n'
                         '<b>3</b>. Проводим медиации и подписываем соглашение\n'
                         '<b>4</b>. Принимаем оплату услуги с обеих сторон в соотношении 50/50')


@bot.on.message(text='Где проходят переговоры?')
async def cmd_5_2(message: Message):
    await message.answer('Процедура медиации предварительно согласуется с обеими сторонами. Ведь для разрешения '
                         'конфликта важно обсуждение в спокойной и комфортной обстановке. '
                         'Если по каким-то причинам очное проведение медиации невозможно, обсудим возможность '
                         'проведения процедуры онлайн.')


@bot.on.message(text='Поможет ли медиатор в моем случае?')
async def cmd_5_3(message: Message):
    await message.answer('Медиаторы работают со всеми конфликтными ситуациями от бракоразводных процессов и раздела'
                         ' имущества до бизнес-споров.Скорее всего, ваш случай подходит под кейс для медиации. '
                         'Но все равно, можете оставить контакты и мы с вами свяжемся и ответим на все вопросы.')


@bot.on.message(text='А если мне не понравится мой медиатор?')
async def cmd_5_4(message: Message):
    await message.answer('Это не проблема!\n'
                         '<b>I-mediator</b> - это сообщество профессиональных медиаторов. Если вам по каким-либо'
                         ' причинам не '
                         'подойдет специалист, мы поможем подобрать другого.')


@bot.on.message(text='Преимущества работы с медиаторами')
async def cmd_5_5(message: Message):
    await message.answer('Наши преимущества:\n'
                         '<b>- Экономим ваши деньги.</b>\n'
                         'Услуги медиатора стоят дешевле услуг адвоката и, оплата производится обеими сторонами спора '
                         'и только после его урегулирования. '
                         '- Предоставляем <b>бесплатные консультации.</b>\n'
                         'Мы ответим на вопросы о необходимости и процедуре медиации в вашем случае.\n'
                         '<b>- Экономим ваше время.</b>\n'
                         'Как известно, суды могут длиться годами. Медиации позволяют достичь соглашения всего за '
                         '<b>2-4</b> '
                         'недели. \n'
                         '- Гарантируем <b>конфиденциальность.</b>\n'
                         'Плюс, Более <b>85%</b> соглашений по результатам медиации исполняются сторонами '
                         'добровольно и без задержек.')


@bot.on.message(text='Как быстро я получу результат?')
async def cmd_5_6(message: Message):
    await message.answer('В среднем, требуется <b>2-4</b> медиации для достижения соглашения. Как правило, это занимает'
                         '<b>2-3</b> недели.\n'
                         '\n'
                         'Но все случаи индивидуальны, поэтому для уточнения сроков вы можете оставить '
                         'контакты. Мы свяжемся с вами для уточнения деталей и сможем сказать более точные сроки.')


@bot.on.message(text='Сколько стоят услуги?')
async def cmd_5_7(message: Message):
    await message.answer('Это зависит от сложности и вида проблемы. Но зачастую услуги медиатора обходятся '
                         'значительно дешевле услуг адвоката, а оплата взимается с обеих сторон в равных частях '
                         'и только в случае положительного завершения спора')


if __name__ == "__main__":
    bot.run_forever()
