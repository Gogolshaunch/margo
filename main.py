import random
import string
from num2words import num2words
import configuration
from fuzzywuzzy import fuzz
import time
import g4f
import webbrowser
import os
from googlesearch import search
import requests
import datetime

import inter
import micro
import va_voice
startTime = 0


def chat_margo(note):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": note}])
    return response


def speak(text):
    va_voice.speak(text)


def va_respond(voice: str):
    if voice.startswith(configuration.name):
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in configuration.comands.keys():
            speak("Что?")
        else:
            execute_cmd(cmd['cmd'], voice)


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in configuration.name:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in configuration.comands.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd, voice):
    global startTime
    if cmd == 'chat_gpt':
        try:
            speak(chat_margo(voice))
            print(chat_margo(voice))
        except:
            speak('Я так еще не умею, извините')
            print(chat_margo(voice))

    elif cmd == 'offBot':
        t = ['отключаюсь', 'пока', 'до встречи', 'спать', "наконец-то тишина и отдых", "целую в дёсны", "бывай!пока"]
        speak(random.choice(t))
        exit()

    elif cmd == 'repit':
        a = voice.split(' ', 4)
        speak(a[-1])

    elif cmd == 'joke':
        jokes = ['']
        speak('Шутка минутка')
        speak(random.choice(jokes))
        speak('Смешно?')

    elif cmd == 'tost':
        speak('Здорово. Тост')
        t = ['']
        speak(random.choice(t))
    elif cmd == 'support':
        t = ['']
        speak(random.choice(t))
    elif cmd == 'times':
        t = ['недетское время однако', "смотрю"]
        speak(random.choice(t))
        today = datetime.datetime.now()
        speak("Сейчас " + num2words(today.hour, lang="ru") + ":" + num2words(today.minute, lang="ru"))

    elif cmd == 'browser':
        t = ['запускаю браузер', 'интернет активирован', 'открываю браузер', 'сейчас открою браузер', "минуточку", "пожалуйста"]
        speak(random.choice(t))
        webbrowser.open_new('https://yandex.ru/')

    elif cmd == 'help':
        t = "Я умею: ..."
        t += "произносить время и дату..."
        t += "засекать время..."
        t += "выключать компьютер..."
        t += "открывать браузер и рассказывать анекдоты..."
        t += "включать онлайн кинотеатр..."
        t += "включать онлайн игры и аудиокниги..."
        t += "говорить о погоде..."
        t += "называть рандомные числа..."
        t += "отключиться..."
        t += "открыть ворд или калькулятор..."
        t += "записать ваши планы и дела..."
        t += "повторить за вами фразу..."
        t += "записать ваши слова в текстовый файл..."
        t += "найти в интернете все о чем спросите..."
        t += "решить вашу судьбу с помощью шара судьбы или подбросить монетку..."
        t += "открыть ютуб и почту..."
        t += "открыть маркетплейс..."
        t += "открыть вайбер и в контакте..."
        t += "советовать книги..."
        t += "открыть переводчик..."
        t += "скачивать видео с ютуба..."
        t += "включить мое круглосуточное шоу..."
        t += "просто разговаривать..."
        speak(t)
        pass

    elif cmd == 'offpc':
        t = ['пока', 'выключаю', 'до встречи', "окей", 'спать', "наконец-то тишина и отдых"]
        speak(random.choice(t))
        os.system('shutdown -s')

    elif cmd == 'weather':
        text = ['сейчас скажу', 'боитесь замерзнуть', 'сейчас гляну...', 'можешь выглянуть в окно, но сейчас проверю', 'смотрю']
        speak(random.choice(text))
        city = 'Сургут'
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        speed = round(weather_data['wind']['speed'])
        des = string.capwords(str(weather_data['weather'][0]['description']))

        speak('Сегодня в городе Сургут' + str(des))
        speak('Температура' + num2words(temperature, lang="ru") + 'градусов')
        speak('Ощущается как' + num2words(temperature_feels, lang="ru") + 'градусов')
        speak('Ветер' + num2words(speed, lang="ru") + 'мeтров в секунду')

    elif cmd == 'mail':
        t = ['запускаю', 'открываю почту', 'сейчас открою', "минуточку", "пожалуйста"]
        speak(random.choice(t))
        webbrowser.open('https://mail.ru/', new=2)

    elif cmd == 'vk':
        t = ['запускаю вк', 'вконтакте открыт', 'открываю переписку', 'сейчас открою', "минуточку", "пожалуйста"]
        speak(random.choice(t))
        webbrowser.open('https://vk.com/', new=2)

    elif cmd == 'films':
        t = ['запускаю', 'сейчас открою', 'прикольно', 'окко открыт']
        speak(random.choice(t))
        webbrowser.open('https://okko.tv/', new=2)

    elif cmd == 'data':
        t = ['сейчас', 'да, сер', "сейчас скажу"]
        speak(random.choice(t))
        a = datetime.date.today()
        speak("Сейчас")
        speak(num2words(a.day, lang="ru"))
        speak(num2words(a.month, lang="ru") + num2words(a.year, lang="ru"))

    elif cmd == 'audio':
        t = ['открываю', 'согласна', 'молодец', "сегодня можно",
             "правильно", "одобряю", "давай"]
        speak(random.choice(t))
        webbrowser.open('https://akniga.org/', new=2)

    elif cmd == 'viber':
        try:
            t = ["открываю", "интересненько", 'сейчас', 'да, сер']
            speak(random.choice(t))
            os.startfile('C://Users//HP//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Viber//Viber.lnk')
        except:
            speak('Возникли некоторые трудности, я не могу найти файл')

    elif cmd == 'wild':
        t = ['открываю', 'согласна', "одобряю", "давай"]
        speak(random.choice(t))
        webbrowser.open('https://www.wildberries.ru/', new=2)

    elif cmd == 'youtube':
        t = ['открываю', 'согласна', 'запускаю',
                "сейчас", "одобряю", "не одобряю", 'интересно', 'здорово']
        speak(random.choice(t))
        webbrowser.open('https://www.youtube.com/', new=2)

    elif cmd == 'you':
        t = ['Привет! Меня зовут Маргарита. Я умная и полезная, всегда готова поддержать разговор на любую т ему. Я стремлюсь всегда узнавать что-то новое и развиваться. Я умеет слушать и давать мудрые советы. Если вам нужна помощь или просто хочется поговорить, Марго всегда готова помочь.',
            'хочешь познакомиться поближе. что ж, я маргарита. Я люблю помогать людям и считаю, что каждый должен делать добро. Я общительная и умею находить общий язык с разными людьми. Однако, иногда могу быть резкой в своих высказываниях.',
            "скажу так: если случится жизненный шторм — я не сбегу с корабля. мы маргариты смелые и гордые. хочу вдохновлять и вдохновляться. ценю приятные мелочи. могу рассказывать о себе часами, но если кратко: не страдаю от стыда или совести — в моем характере нет ничего лишнего. если тебя это не отпугивает, то мы подружимся",
            "имя Маргарита греческого происхождения. смысл имени в переводе - «жемчужина, жемчуг». еще одно значение имени - «покровительница моряков». маргариты умные и сообразительные. я – прирожденный лидер абсолютно во всем. по характеру волевая, сильная, обладающая острым логическим умом. люблю свободу и независимость"]
        speak(random.choice(t))

    elif cmd == 'mood':
        t = ['всё неплохо', 'а кто бы меня спрашивал', 'скучно', 'сама не знаю',
                'замечательно', "пока отлично", 'где-то между хорошо и очень хорошо',
             'тебе действительно интересно', 'как у тебя, но лучше', 'много работы, мало денег']
        speak(random.choice(t))

    elif cmd == 'do':
        t = ['работаю в фоне, не переживай', 'жду очередной команды, хоть могла бы и сама на кнопку нажать', 'скучаю',
                'занята, а что', 'работаю, как видишь', 'делаю ментальный перерыв', 'думаю над тем, над кем потренировать свое обаяние', 'наслаждаюсь прекрасным днем',
             'размышляю, почему у меня сегодня игривое настроение', 'пусть это останется тайной', "придумываю план мести тебе"]
        speak(random.choice(t))

    elif cmd == 'ball_fate':
        speak('задайте любой вопрос и я решу вашу судьбу')
        time.sleep(10)
        t = ['да', 'нет', 'очень вероятно', 'точно да', 'не сейчас', 'есть сомнения', 'я так не думаю', 'глупости какие-то', 'без сомнений да', 'наверное', "не знаю, все зависит от вас"]
        speak(random.choice(t))

    elif cmd == 'hello':
        t = ['и тебе привет', 'привет', 'приветсвую', 'снова здесь', 'рада видеть', 'давно не виделись',
                'не скучала,но привет', 'здравствуйте, сударыня', "новый рабочий день", 'привет от старых штиблет', 'моя радость умирает от твоего прихода']
        speak(random.choice(t))

    elif cmd == 'reminder':
        t = ['открываю', 'здорово', 'запускаю', "сейчас"]
        speak(random.choice(t))
        os.system(f'python todo.py')

    elif cmd == 'calc':
        t = ['открываю', 'здорово', 'запускаю', "сейчас"]
        speak(random.choice(t))
        os.system(f'python calc.py')

    elif cmd == 'bye':
        t = ['Пока', 'Ну прощай', 'До встречи', 'До скорого', 'Покеда']
        speak(random.choice(t))

    elif cmd == 'night':
        t = ['Пока', 'Спокойной ночи', 'До встречи', 'Спокойной', 'Сладких снов🤍',
             'Не возвращайся пожалуйста)']
        speak(random.choice(t))

    elif cmd == 'word':
        try:
            t = ['открываю', 'здорово', 'запускаю', "сейчас"]
            speak(random.choice(t))
            os.startfile("C://Users//HP//Desktop//Word 2016.lnk")
        except:
            speak('Возникли некоторые трудности, я не могу найти файл')

    elif cmd == 'sps':
        t = ['Угу', 'Агась', "Ну пожалуйста", "Окей", "Оки"]
        speak(random.choice(t))

    elif cmd == 'tranc':
        t = ['открываю', 'здорово', 'запускаю', "интересно когда ты выучишь английский", "сейчас"]
        speak(random.choice(t))
        webbrowser.open('https://translate.google.ru/;', new=2)

    elif cmd == 'rand':
        a = random.randint(1, 1000)
        speak(num2words(a, lang="ru"))

    elif cmd == 'google':
        try:
            a = voice.split(' ', 4)
            query = a[-1]
            ok = []
            speak("По вашему запросу я получила десять ссылок, открываю первые три, надеюсь, что вы найдете нужное")
            for i in search(query):
                ok.append(i)
            webbrowser.open(ok[0], new=2)
            webbrowser.open(ok[1], new=2)
            webbrowser.open(ok[2], new=2)
        except:
            speak('Я вас не поняла')

    elif cmd == 'txt':
        a = voice.split(' ', 4)
        f = open('my_thoughts.txt', '6')
        try:
            f.write(a[-1] + '\n')
        finally:
            f.close()
        speak("Мне нравится")
        speak('Всё успешно сохранено')

    elif cmd == 'start':
        speak("Секундомер запущен")
        startTime = time.time()

    elif cmd == 'name':
        t = ['ко мне по-разному обращаются, но мне нравится рита', 'зови просто марго', 'маргарита', 'для тебя риточка', ' друзья зовут маргошей', 'ну выбирай: рита, марго. маргарита, риточка, маргоша, как лучше']
        speak(random.choice(t))

    elif cmd == 'show':
        nows = datetime.datetime.now()
        if 6 <= nows.hour < 12:
            speak("Утреннее шоу начинается")
        elif 12 <= nows.hour < 18:
            speak("Дневное шоу начинается")
        elif 18 <= nows.hour < 23:
            speak("Вечернее шоу начинается")
        else:
            speak("Ночное шоу начинается")
        t = ['у меня всё неплохо', 'а кто бы меня спрашивал, но скажу что все хорошо', 'мне сегодня скучно', 'сама не знаю какое у меня настроение, но надеюсь у тебя хорошее',
             'мои дела замечательно, твои тоже, ведь началось мое шоу', "пока у меня все отлично, думаю у тебя сейчас точно станет лучше",
             'мои дела где-то между хорошо и очень хорошо', 'много работы, мало денег']
        speak(random.choice(t))
        a = datetime.date.today()
        speak("Сегодня")
        speak(num2words(a.day, lang="ru"))
        speak(num2words(a.month, lang="ru") + num2words(a.year, lang="ru"))

        today = datetime.datetime.now()
        speak("Сейчас " + num2words(today.hour, lang="ru") + ":" + num2words(today.minute, lang="ru"))

        city = 'Сургут'
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        speed = round(weather_data['wind']['speed'])
        des = string.capwords(str(weather_data['weather'][0]['description']))

        speak('Погода')
        speak('Сегодня в городе Сургут' + str(des))
        speak('Температура' + num2words(temperature, lang="ru") + 'градусов')
        speak('Ощущается как' + num2words(temperature_feels, lang="ru") + 'градусов')
        speak('Ветер' + num2words(speed, lang="ru") + 'мeтров в секунду')
        speak("На этом всё. Желаю хорошего дня!")

    elif cmd == "stop":
        if startTime != 0:
            Time = time.time() - startTime
            a = round(Time % 60)
            c = round(Time // 60)
            speak("Прошло" + num2words(c, lang="ru") + "минут")
            speak(num2words(a, lang="ru") + "секунд")
            startTime = 0
        else:
            speak("Секундомер не включен")

    elif cmd == 'money':
        t = ['орел', 'решка']
        speak(random.choice(t))

    elif cmd == 'parser':
        t = ['открываю', 'здорово', 'запускаю', "сейчас"]
        speak(random.choice(t))
        os.system(f'python parser.py')

    elif cmd == 'rec_book':
        t = ['открываю', 'согласна', 'молодец', 'запускаю', "здорово",
             "правильно", "одобряю", "давай"]
        speak(random.choice(t))
        webbrowser.open('https://www.livelib.ru/rec/master/6', new=2)
    else:
        try:
            speak(chat_margo(voice))
        except:
            speak('Я так еще не умею, извините')


now = datetime.datetime.now()
if 6 <= now.hour < 12:
    speak("Доброе утро!")
elif 12 <= now.hour < 18:
    speak("Добрый день!")
elif 18 <= now.hour < 23:
    speak("Добрый вечер!")
else:
    speak("Доброй ночи!")
while inter.ok:
    micro.va_listen(va_respond)
exit()
