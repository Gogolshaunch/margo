import vosk
import sys
import sounddevice as sd
import queue
import psutil
import random
import string
from num2words import num2words
from fuzzywuzzy import fuzz
import time
import webbrowser
import os
from googlesearch import search
import requests
import datetime
import va_voice
import win32api
import win32gui
import ctypes
import json
from gigachat import GigaChat
import screen_brightness_control as sbc
startTime = 0

name = ('рита', 'марго', 'маргарита', 'риточка', 'маргош', 'маруся', 'рит')
with open('data_file.json', "r") as file:
    configuration = json.load(file)


def get_layout():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        return 'ru'
    if hex(pf(0)) == '0x4090409':
        return 'en'


def setCyrillicLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04190419)
    return(result)


def setEngLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return(result)


def chat_margo(note):
    with GigaChat(
            credentials='OGViMjExZWItOWJlZS00N2ZjLWI4ZDUtM2MyZTlkN2UwZjI0OjA3NjM3MzNjLTk2M2UtNGFlZS1iZTNkLTBhMjllZGZlNjZkNw==',
            verify_ssl_certs=False) as giga:
        response = giga.chat(note)
        return response.choices[0].message.content


def com(name_def):
    if name_def in configuration.keys():
        if configuration[name_def][-1] == 'открытие файла':
            try:
                t = ["открываю", "интересненько", 'сейчас', 'да, сер']
                assistant.speak(random.choice(t))
                os.startfile(f'{configuration[name_def][-2]}')
            except:
                assistant.speak('Возникли некоторые трудности, я не могу найти файл')
        elif configuration[name_def][-1] == 'открытие сайта':
            try:
                t = ['запускаю браузер', 'интернет активирован', 'открываю браузер', 'сейчас открою браузер', "минуточку",
                     "пожалуйста"]
                assistant.speak(random.choice(t))
                webbrowser.open_new(f'{configuration[name_def][-2]}')
            except:
                assistant.speak('Возникли некоторые трудности, скорее всего неверная ссылка')
        elif configuration[name_def][-1] == 'ответ на вопрос':
            t = []
            call_def = configuration[name_def][-2].split(',')
            for i in call_def:
                t.append(i)
            assistant.speak(random.choice(t))


model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, tim, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


class Assistant:
    def __init__(self, commands: dict[str: tuple]):
        self.__make_commands(commands)

    def speak(self, message: str):
        va_voice.speak(message)

    def filter_cmd(self, raw_voice: str):
        cmd = raw_voice

        for x in name:
            cmd = cmd.replace(x, "").strip()

        return cmd

    def recognize_cmd(self, cmd: str):
        rc = {'cmd': '', 'percent': 75}
        for c, v in configuration.items():

            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > rc['percent']:
                    rc['cmd'] = c
                    rc['percent'] = vrt

        return rc

    def listen(self, callback):
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                               channels=1, callback=q_callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            time.sleep(1)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    callback(json.loads(rec.Result())["text"])

    def va_respond(self, voice: str):
        if voice.startswith(name):
            cmd = self.recognize_cmd(self.filter_cmd(voice))

            if cmd['cmd'] not in configuration.keys():
                self.speak(random.choice(["я тебя не понимаю", "говори четче", "не расслышала"]))
            else:
                self.execute_cmd(cmd['cmd'], voice)

    def execute_cmd(self, cmd, voice: str):
        global startTime
        if cmd == 'chat_gpt':
            try:
                self.speak(chat_margo(voice))
            except:
                self.speak('Я так еще не умею, извините')

        elif cmd == 'offBot':
            t = ['отключаюсь', 'пока', 'до встречи', 'спать', "наконец-то тишина и отдых", "целую в дёсны",
                 "бывай!пока"]
            self.speak(random.choice(t))
            exit()

        elif cmd == 'repit':
            a = voice.split(' ', 4)
            self.speak(a[-1])

        elif cmd == 'brightness':
            voice = voice.split(' ')
            a = sbc.get_brightness()
            self.speak("Сейчас яркость" + num2words(a, lang="ru"))
            sbc.set_brightness(voice[-1], display=0)
            self.speak("Яркость изменена")

        elif cmd == 'battery':
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            percent = battery.percent
            if plugged:
                self.speak("Зарядка подключена, заряд батареи: " + num2words(percent, lang="ru") + "процентов")
            else:
                self.speak("Зарядка отключена, заряд батареи: " + num2words(percent, lang="ru") + "процентов")

        elif cmd == 'joke':
            jokes = []
            self.speak('Шутка минутка')
            self.speak(random.choice(jokes))
            self.speak('Смешно?')

        elif cmd == 'times':
            t = ['недетское время однако', "смотрю"]
            self.speak(random.choice(t))
            today = datetime.datetime.now()
            self.speak("Сейчас " + num2words(today.hour, lang="ru") + ":" + num2words(today.minute, lang="ru"))

        elif cmd == 'browser':
            t = ['запускаю браузер', 'интернет активирован', 'открываю браузер', 'сейчас открою браузер', "минуточку",
                 "пожалуйста"]
            self.speak(random.choice(t))
            webbrowser.open_new('https://yandex.ru/')

        elif cmd == 'key_layout':
            if get_layout() == 'en':
                setCyrillicLayout()
            elif get_layout() == 'ru':
                setEngLayout()
            self.speak('Готово')

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
            t += "записать ваши слова в текстовый файл и прочитать его..."
            t += "найти в интернете все о чем спросите..."
            t += "решить вашу судьбу с помощью шара судьбы или подбросить монетку..."
            t += "открыть ютуб и почту..."
            t += "открыть маркетплейс..."
            t += "открыть вайбер и в контакте..."
            t += "советовать книги..."
            t += "открыть переводчик..."
            t += "скачивать видео с ютуба..."
            t += "включить мое круглосуточное шоу..."
            t += "поменять настройки компьютера(изменить звук, раскладку, яркость и так далее)..."
            t += "кроме этого я могу выполнять функции, которые вы добавили..."
            t += "и просто разговаривать..."
            self.speak(t)
            pass

        elif cmd == 'offpc':
            t = ['пока', 'выключаю', 'до встречи', "окей", 'спать', "наконец-то тишина и отдых"]
            self.speak(random.choice(t))
            os.system('shutdown -s')

        elif cmd == 'weather':
            text = ['сейчас скажу', 'боитесь замерзнуть', 'сейчас гляну...',
                    'можешь выглянуть в окно, но сейчас проверю', 'смотрю']
            self.speak(random.choice(text))
            city = 'Сургут'
            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])
            speed = round(weather_data['wind']['speed'])
            des = string.capwords(str(weather_data['weather'][0]['description']))

            self.speak('Сегодня в городе Сургут' + str(des))
            self.speak('Температура' + num2words(temperature, lang="ru") + 'градусов')
            self.speak('Ощущается как' + num2words(temperature_feels, lang="ru") + 'градусов')
            self.speak('Ветер' + num2words(speed, lang="ru") + 'мeтров в секунду')

        elif cmd == 'mail':
            t = ['запускаю', 'открываю почту', 'сейчас открою', "минуточку", "пожалуйста"]
            self.speak(random.choice(t))
            webbrowser.open('https://mail.ru/', new=2)

        elif cmd == 'vk':
            t = ['запускаю вк', 'в контакте открыт', 'открываю', 'сейчас открою', "минуточку", "пожалуйста"]
            self.speak(random.choice(t))
            webbrowser.open('https://vk.com/', new=2)

        elif cmd == 'films':
            t = ['запускаю', 'сейчас открою', 'прикольно', 'кинотеатр открыт']
            self.speak(random.choice(t))
            webbrowser.open('https://okko.tv/', new=2)

        elif cmd == 'data':
            t = ['сейчас', "сейчас скажу"]
            self.speak(random.choice(t))
            a = datetime.date.today()
            self.speak("Сейчас")
            self.speak(num2words(a.day, lang="ru"))
            self.speak(num2words(a.month, lang="ru") + num2words(a.year, lang="ru"))

        elif cmd == 'audio':
            t = ['открываю', 'согласна', "сегодня можно",
                 "правильно", "одобряю", "давай"]
            self.speak(random.choice(t))
            webbrowser.open('https://akniga.org/', new=2)

        elif cmd == 'viber':
            try:
                t = ["открываю", "интересненько", 'сейчас']
                self.speak(random.choice(t))
                os.startfile(
                    'C://Users//HP//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Viber//Viber.lnk')
            except:
                self.speak('Возникли некоторые трудности, я не могу найти файл')

        elif cmd == 'wild':
            t = ['открываю', 'согласна', "одобряю", "давай"]
            self.speak(random.choice(t))
            webbrowser.open('https://www.wildberries.ru/', new=2)

        elif cmd == 'youtube':
            t = ['открываю', 'согласна', 'запускаю',
                 "сейчас", "одобряю", "не одобряю", 'интересно', 'здорово']
            self.speak(random.choice(t))
            webbrowser.open('https://www.youtube.com/', new=2)

        elif cmd == 'you':
            t = ['Привет! Меня зовут Маргарита. Я умная и полезная, всегда готова поддержать разговор на любую тему. Я стремлюсь всегда узнавать что-то новое и развиваться. Я умею слушать, если вам нужна помощь или просто хочется поговорить, Марго всегда готова помочь.',
                'хочешь познакомиться поближе. что ж, я маргарита. Я люблю помогать людям. Я общительная и умею находить общий язык с разными людьми. Однако, иногда могу быть резкой в своих высказываниях.',
                "скажу так: мы маргариты смелые и гордые. хочу вдохновлять и вдохновляться. ценю приятные мелочи. если кратко: не страдаю от стыда или совести — в моем характере нет ничего лишнего. если тебя это не отпугивает, то мы подружимся",
                "имя Маргарита греческого происхождения. смысл имени в переводе - «жемчужина, жемчуг». маргариты умные и сообразительные. по характеру сильная. люблю свободу и независимость"]
            self.speak(random.choice(t))

        elif cmd == 'mood':
            t = ['всё неплохо', 'а кто бы меня спрашивал', 'скучно', 'сама не знаю',
                 'замечательно', "пока отлично", 'где-то между хорошо и очень хорошо',
                 'тебе действительно интересно', 'как у тебя, но лучше', 'много работы']
            self.speak(random.choice(t))

        elif cmd == 'do':
            t = ['работаю в фоне, не переживай',
                 'скучаю', 'занята, а что', 'работаю, как видишь', 'делаю ментальный перерыв',
                 'думаю над тем, над кем потренировать свое обаяние', 'наслаждаюсь прекрасным днем',
                 'размышляю, почему у меня сегодня игривое настроение', 'пусть это останется тайной']
            self.speak(random.choice(t))

        elif cmd == 'ball_fate':
            self.speak('задайте любой вопрос и я решу вашу судьбу')
            time.sleep(15)
            t = ['да', 'нет', 'очень вероятно', 'точно да', 'не сейчас', 'есть сомнения', 'я так не думаю',
                 'глупости какие-то', 'без сомнений да', 'наверное', "не знаю, все зависит от вас"]
            self.speak(random.choice(t))

        elif cmd == 'hello':
            t = ['и тебе привет', 'привет', 'приветсвую', 'снова здесь', 'рада видеть', 'давно не виделись',
                 'не скучала,но привет', 'здравствуйте', "новый рабочий день", 'привет от старых штиблет']
            self.speak(random.choice(t))

        elif cmd == 'reminder':
            t = ['открываю', 'здорово', 'запускаю', "сейчас"]
            self.speak(random.choice(t))
            os.system(f'python todo.py')

        elif cmd == 'calc':
            t = ['открываю', 'здорово', 'запускаю', "сейчас"]
            self.speak(random.choice(t))
            os.system(f'python calc.py')

        elif cmd == 'bye':
            t = ['Пока', 'Ну прощай', 'До встречи', 'До скорого', 'Покеда']
            self.speak(random.choice(t))

        elif cmd == 'night':
            t = ['Пока', 'Спокойной ночи', 'До встречи', 'Спокойной', 'Сладких снов🤍',
                 'Не возвращайся пожалуйста']
            self.speak(random.choice(t))

        elif cmd == 'word':
            try:
                t = ['открываю', 'здорово', 'запускаю', "сейчас"]
                self.speak(random.choice(t))
                os.startfile("C://Users//HP//Desktop//Word 2016.lnk")
            except:
                self.speak('Возникли некоторые трудности, я не могу найти файл')

        elif cmd == 'sps':
            t = ['Угу', 'Агась', "Ну пожалуйста", "Окей", "Оки"]
            self.speak(random.choice(t))

        elif cmd == 'tranc':
            t = ['открываю', 'здорово', 'запускаю', "сейчас"]
            self.speak(random.choice(t))
            webbrowser.open('https://translate.google.ru/;', new=2)

        elif cmd == 'rand':
            a = random.randint(1, 500)
            self.speak(num2words(a, lang="ru"))

        elif cmd == 'google':
            try:
                a = voice.split(' ', 4)
                query = a[-1]
                ok = []
                self.speak("По вашему запросу я получила десять ссылок, открываю первые три, надеюсь, что вы найдете нужное")
                for i in search(query):
                    ok.append(i)
                webbrowser.open(ok[0], new=2)
                webbrowser.open(ok[1], new=2)
                webbrowser.open(ok[2], new=2)
            except:
                self.speak('Я вас не поняла')

        elif cmd == 'txt':
            a = voice.split(' ', 4)
            with open('my_thoughts.txt', 'a') as f:
                f.write(a[-1] + '\n')
            self.speak("Мне нравится")
            self.speak('Всё успешно сохранено')

        elif cmd == 'read_txt':
            with open('my_thoughts.txt', 'r') as f:
                for line in f:
                    try:
                        self.speak(line)
                    except:
                        self.speak('Я не умею читать такие символы')

        elif cmd == 'del_txt':
            open('file.txt', 'w').close()

        elif cmd == 'start':
            self.speak("Секундомер запущен")
            startTime = time.time()

        elif cmd == 'name':
            t = ['ко мне по-разному обращаются, но мне нравится рита', 'зови просто марго', 'маргарита',
                 'для тебя риточка', 'друзья зовут маргошей',
                 'ну выбирай: рита, марго. маргарита, риточка, маргоша, как лучше']
            self.speak(random.choice(t))

        elif cmd == 'show':
            nows = datetime.datetime.now()
            if 6 <= nows.hour < 12:
                self.speak("Утреннее шоу начинается")
            elif 12 <= nows.hour < 18:
                self.speak("Дневное шоу начинается")
            elif 18 <= nows.hour < 23:
                self.speak("Вечернее шоу начинается")
            else:
                self.speak("Ночное шоу начинается")
            t = ['у меня всё неплохо', 'а кто бы меня спрашивал, но скажу что все хорошо', 'мне сегодня скучно',
                 'сама не знаю какое у меня настроение, но надеюсь у тебя хорошее',
                 'мои дела замечательно, твои тоже, ведь началось мое шоу',
                 "пока у меня все отлично, думаю у тебя сейчас точно станет лучше",
                 'мои дела где-то между хорошо и очень хорошо']
            self.speak(random.choice(t))
            a = datetime.date.today()
            self.speak("Сегодня")
            self.speak(num2words(a.day, lang="ru"))
            self.speak(num2words(a.month, lang="ru") + num2words(a.year, lang="ru"))

            today = datetime.datetime.now()
            self.speak("Сейчас " + num2words(today.hour, lang="ru") + ":" + num2words(today.minute, lang="ru"))

            city = 'Сургут'
            url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])
            speed = round(weather_data['wind']['speed'])
            des = string.capwords(str(weather_data['weather'][0]['description']))

            self.speak('Погода')
            self.speak('Сегодня в городе Сургут' + str(des))
            self.speak('Температура' + num2words(temperature, lang="ru") + 'градусов')
            self.speak('Ощущается как' + num2words(temperature_feels, lang="ru") + 'градусов')
            self.speak('Ветер' + num2words(speed, lang="ru") + 'мeтров в секунду')
            self.speak("На этом всё. Желаю хорошего дня!")

        elif cmd == "stop":
            if startTime != 0:
                Time = time.time() - startTime
                a = round(Time % 60)
                c = round(Time // 60)
                self.speak("Прошло" + num2words(c, lang="ru") + "минут")
                self.speak(num2words(a, lang="ru") + "секунд")
                startTime = 0
            else:
                self.speak("Секундомер не включен")

        elif cmd == 'money':
            t = ['орел', 'решка']
            self.speak(random.choice(t))

        elif cmd == 'parser':
            t = ['открываю', 'здорово', 'запускаю', "сейчас"]
            self.speak(random.choice(t))
            os.system(f'python parser.py')

        elif cmd == 'rec_book':
            t = ['открываю', 'согласна', 'молодец', 'запускаю', "здорово",
                 "правильно", "одобряю", "давай"]
            self.speak(random.choice(t))
            webbrowser.open('https://www.livelib.ru/rec/master/6', new=2)
        else:
            try:
                com(configuration[cmd])
            except:
                try:
                    self.speak(chat_margo(voice))
                except:
                    self.speak('Я так еще не умею, извините')

    def __make_commands(self, _commands: dict[str: tuple]):
        self.commands = {}
        for k, v_arr in _commands.items():
            k = k.lower()
            for v in v_arr:
                self.commands[v.lower()] = k

    def make_com(self, name_def, call_def, work_def, val):
        try:
            call_def = call_def.split(',')
            a = []
            for i in call_def:
                a.append(i)
            a.append(work_def, val)
            configuration[name_def] = a
            with open('data_file.json', "w") as file:
                json.dump(configuration, file, indent=2)
        except:
            self.speak('Не удалось добавить функцию, видимо какие-то данные введены неверно')

    def run(self):
        self.listen(self.va_respond)


if __name__ == "__main__":
    assistant = Assistant(configuration)
    assistant.run()
