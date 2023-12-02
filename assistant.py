import vosk
import sys
import sounddevice as sd
import queue
import json
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
import va_voice
startTime = 0


def chat_margo(note):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": note}])
    return response


def com(name_def):
    if name_def in configuration.commands.keys():
        if configuration.commands[name_def][-1] == 'открытие файла':
            try:
                t = ["открываю", "интересненько", 'сейчас', 'да, сер']
                assistant.speak(random.choice(t))
                os.startfile(f'{configuration.commands[name_def][-2]}')
            except:
                assistant.speak('Возникли некоторые трудности, я не могу найти файл')
        elif configuration.commands[name_def][-1] == 'открытие сайта':
            try:
                t = ['запускаю браузер', 'интернет активирован', 'открываю браузер', 'сейчас открою браузер', "минуточку",
                     "пожалуйста"]
                assistant.speak(random.choice(t))
                webbrowser.open_new(f'{configuration.commands[name_def][-2]}')
            except:
                assistant.speak('Возникли некоторые трудности, скорее всего неверная ссылка')
        elif configuration.commands[name_def][-1] == 'ответ на вопрос':
            t = []
            call_def = configuration.commands[name_def][-2].split(',')
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

        for x in configuration.name:
            cmd = cmd.replace(x, "").strip()

        return cmd

    def recognize_cmd(self, cmd: str):
        rc = {'cmd': '', 'percent': 75}
        for c, v in configuration.commands.items():

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
        if voice.startswith(configuration.name):
            cmd = self.recognize_cmd(self.filter_cmd(voice))

            if cmd['cmd'] not in configuration.commands.keys():
                self.speak(random.choice([
                    "я тебя не понимаю", "говори четче", "не расслышала"]))
            else:
                self.execute_cmd(cmd['cmd'], voice)

    def execute_cmd(self, cmd, voice: str):
        global startTime
        if cmd == 'chat_gpt':
            try:
                self.speak(chat_margo(voice))
                print(chat_margo(voice))
            except:
                self.speak('Я так еще не умею, извините')
                print(chat_margo(voice))

        elif cmd == 'offBot':
            t = ['отключаюсь', 'пока', 'до встречи', 'спать', "наконец-то тишина и отдых", "целую в дёсны",
                 "бывай!пока"]
            self.speak(random.choice(t))
            exit()

        elif cmd == 'repit':
            a = voice.split(' ', 4)
            self.speak(a[-1])

        elif cmd == 'joke':
            jokes = []
            self.speak('Шутка минутка')
            self.speak(random.choice(jokes))
            self.speak('Смешно?')

        elif cmd == 'tost':
            self.speak('Здорово. Тост')
            t = ['Дорогой друг, желаю, чтобы у тебя всегда было легкое сердце и тяжелые карманы!',
                 'Выпьем за тех, кто, отсутствуя, незримо присутствует здесь!',
                 'Как говорил мой пра-прадед, а что он говорил я уже не помню. Вот выпьем за то, чтобы мы меньше всего помнили и наслаждались настоящим моментом',
                 'Выпьем за нашу удачу, хоть иногда пусть бьется в наших силках птица счастья!',
                 'Счастья! Добра и зеленого бабла!',
                 'Дорогие друзья, давайте выпьем за страсть! Страсть как хочется выпить!',
                 'Давайте выпьем за дружбу, ведь именно она умножает радости и разделяет печаль!',
                 'Чтобы ваши желания офигевали от ваших возможностей!',
                 'Философ Диоген сказал: «Быть богатым и иметь много денег — не одно и то же. По-настоящему богат тот, кто удовлетворен своей жизнью». Выпьем за богатство!',
                 'Мы все умрем, людей бессмертных нет. И это все известно и не ново. Но мы живем, чтобы оставить след — Дом или тропинку, дерево иль слово. Им не исчезнуть начисто, до тла. Так выпьем же за добрые дела!',
                 'Чем больше мы ищем смысл жизни, тем меньше его в нашей жизни. И наоборот. Отвергая смысл жизни, мы наполняем свою жизнь большим смыслом. Так не будем же искать приключений на свою голову!',
                 'Армянское радио спрашивают: — Что будет, если армянин станет судиться с евреем? — Прокурор получит десять лет. Так выпьем за то, чтоб не судить и не судимыми быть.']
            self.speak(random.choice(t))
        elif cmd == 'support':
            t = ['Безвыходных ситуаций не бывает. Мы сможем все решить и когда-то будет вспоминать эти времена с улыбкой',
                "Если проблема решается деньгами, то это не проблема, а расходы",
                "Тебе тяжело, то ты очень сильный. Купи себе большую биту, чтобы у твоих проблем были проблемы с тобой. Жизнь продолжается",
                "Если опоздал на один поезд, то всегда появится другой. Так и в жизни. Всегда будут новые возможности, даже тогда, когда казалось все упущено",
                "Беспокойство не освобождает от будущих неприятностей. Оно только лишает тебя сил",
                "Цель каждого человека стать счастливым. У тебя обязательно получится со временем, когда горести немного позабудутся",
                "Драгоценный камень не может стать таким без трения, а человек без испытаний. Держись",
                "Есть много примеров, кто сталкивался с подобным. В конце концов они все находили себя и выбирались из этой тяжелой ситуации",
                "Я уже давно не переживаю из-за ситуаций, которые лежат вне моего контроля. Просто отпусти ситуацию и двигайся дальше",
                "Для счастья человеку многое не нужно. Требуется только яркое солнце, свежий воздух и немного отдыха. Просто возьми паузу и немногого отдохни. У тебя все наладится.",
                "Если проблемы нельзя решить, то о ней не стоит беспокоиться. Расслабься и плыви по течению",
                "Все, что не делается – то к лучшему. А что не произошло, то на пользу",
                "Не смей сдаваться и отчаиваться. Каждый день появляются новые возможности и технологии двигаются вперед. Что еще сегодня кажется невозможным, завтра станет реальностью",
                "Пока мы крутим педали к цели, порой цепь соскальзывает и колеса пробиваются. Но ты не должен забывать о прекрасном, что открывается каждый день за новым поворотом дороги",
                "Помни о том, что любой минус можно превратить в плюс",
                "Направь свою печаль и грев на что-то позитивное", "Если радость на всех одна, на всех и беда одна",
                "Не стоит себя винить в том, что произошло. Чувство вины мешает исправлять проблемы, а значит не стоит впадать в депрессию",
                "Держи нос выше. Не погружайся в уныние, ведь оптимистам всегда приходит удача на помощь" "Черные полосы всегда сменяют белые, а в будущем ты будешь вспоминать все это как плохой сон",
                'Нельзя найти место, где тебе будет хорошо. Нужно создавать хорошо самому в любом месте',
                'Сила воли, положительные мысли и оптимизм способны на многое',
                "Вспомни о своих прошлых проблемах. Тогда тебе казалось, что жизнь кончена, но сейчас это воспринимается как мелкая неприятность. Так будет и с сегодняшними бедами",
                "Если ты не можешь изменить ситуацию, то просто переступи через нее и иди дальше",
                "С твоим опытом, умом и способностями ты найдешь себе место под солнцем. Я не удивлюсь, если через год ты будешь счастлив, что все так случилось",
                "Самая большая ошибка в жизни – это боязнь ошибаться. Ты был смелый, что хотя бы попробовал",
                "Завтра опять взойдет солнце, несмотря ни на что",
                'Если ты грустишь, то можешь упустить чудо, которое постучится тебе в дверь',
                'Молись не о легкой жизни, а о силе вынести тяжелую',
                'Как поддержать приятеля, если у него грустное настроение? Давай я куплю пива или чего покрепче, а затем будет болтать по душам? Быть свободным и независимым. Что это значит и как найти себя?',
                "Беспокойство – это защитный организм, который помогает нам в сложные времена. Не зацикливайся и двигайся дальше",
                'Данная трудная ситуация – это только глава твоей жизни, а не вся ее книга',
                'Все эти трудности временные, а ты это прекрасно знаешь. Когда-то и на нашей улице перевернется самосвал с пряниками',
                "Тебе нечего грустить и бояться. Проблемы – это не остановки, а только рекомендации",
                "Сколько возможностей и прекрасного упустишь, если будешь загоняться по этому поводу?",
                "У тебя не должно быть времени на печаль, раздумья и беспокойство, когда нужно действовать!",
                "Сложно даже представить, что испытываешь и чувствуешь ты. Если понадобится моя поддержка, только скажи",
                "Твоя неудача – это только трамплин к успеху",
                "Все лучшее приходит через изменения и борьбу", 'За любой зимой всегда придет теплое и солнечное лето',
                "Мечтай, как будто будешь жить вечно. А живи и действуй так, словно ты умрешь уже сегодня вечером"]
            self.speak(random.choice(t))
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
            self.speak(t)
            pass # todo перечитать

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
            t = ['запускаю вк', 'вконтакте открыт', 'открываю переписку', 'сейчас открою', "минуточку", "пожалуйста"]
            self.speak(random.choice(t))
            webbrowser.open('https://vk.com/', new=2)

        elif cmd == 'films':
            t = ['запускаю', 'сейчас открою', 'прикольно', 'окко открыт']
            self.speak(random.choice(t))
            webbrowser.open('https://okko.tv/', new=2)

        elif cmd == 'data':
            t = ['сейчас', 'да, сер', "сейчас скажу"]
            self.speak(random.choice(t))
            a = datetime.date.today()
            self.speak("Сейчас")
            self.speak(num2words(a.day, lang="ru"))
            self.speak(num2words(a.month, lang="ru") + num2words(a.year, lang="ru"))

        elif cmd == 'audio':
            t = ['открываю', 'согласна', 'молодец', "сегодня можно",
                 "правильно", "одобряю", "давай"]
            self.speak(random.choice(t))
            webbrowser.open('https://akniga.org/', new=2)

        elif cmd == 'viber':
            try:
                t = ["открываю", "интересненько", 'сейчас', 'да, сер']
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
            t = ['Привет! Меня зовут Маргарита. Я умная и полезная, всегда готова поддержать разговор на любую т ему. Я стремлюсь всегда узнавать что-то новое и развиваться. Я умеет слушать и давать мудрые советы. Если вам нужна помощь или просто хочется поговорить, Марго всегда готова помочь.',
                'хочешь познакомиться поближе. что ж, я маргарита. Я люблю помогать людям и считаю, что каждый должен делать добро. Я общительная и умею находить общий язык с разными людьми. Однако, иногда могу быть резкой в своих высказываниях.',
                "скажу так: если случится жизненный шторм — я не сбегу с корабля. мы маргариты смелые и гордые. хочу вдохновлять и вдохновляться. ценю приятные мелочи. могу рассказывать о себе часами, но если кратко: не страдаю от стыда или совести — в моем характере нет ничего лишнего. если тебя это не отпугивает, то мы подружимся",
                "имя Маргарита греческого происхождения. смысл имени в переводе - «жемчужина, жемчуг». еще одно значение имени - «покровительница моряков». маргариты умные и сообразительные. я – прирожденный лидер абсолютно во всем. по характеру волевая, сильная, обладающая острым логическим умом. люблю свободу и независимость"]
            self.speak(random.choice(t))

        elif cmd == 'mood':
            t = ['всё неплохо', 'а кто бы меня спрашивал', 'скучно', 'сама не знаю',
                 'замечательно', "пока отлично", 'где-то между хорошо и очень хорошо',
                 'тебе действительно интересно', 'как у тебя, но лучше', 'много работы, мало денег']
            self.speak(random.choice(t))

        elif cmd == 'do':
            t = ['работаю в фоне, не переживай', 'жду очередной команды, хоть могла бы и сама на кнопку нажать',
                 'скучаю',
                 'занята, а что', 'работаю, как видишь', 'делаю ментальный перерыв',
                 'думаю над тем, над кем потренировать свое обаяние', 'наслаждаюсь прекрасным днем',
                 'размышляю, почему у меня сегодня игривое настроение', 'пусть это останется тайной',
                 "придумываю план мести тебе"]
            self.speak(random.choice(t))

        elif cmd == 'ball_fate':
            self.speak('задайте любой вопрос и я решу вашу судьбу')
            time.sleep(10)
            t = ['да', 'нет', 'очень вероятно', 'точно да', 'не сейчас', 'есть сомнения', 'я так не думаю',
                 'глупости какие-то', 'без сомнений да', 'наверное', "не знаю, все зависит от вас"]
            self.speak(random.choice(t))

        elif cmd == 'hello':
            t = ['и тебе привет', 'привет', 'приветсвую', 'снова здесь', 'рада видеть', 'давно не виделись',
                 'не скучала,но привет', 'здравствуйте, сударыня', "новый рабочий день", 'привет от старых штиблет',
                 'моя радость умирает от твоего прихода']
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
                 'Не возвращайся пожалуйста)']
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
            t = ['открываю', 'здорово', 'запускаю', "интересно когда ты выучишь английский", "сейчас"]
            self.speak(random.choice(t))
            webbrowser.open('https://translate.google.ru/;', new=2)

        elif cmd == 'rand':
            a = random.randint(1, 1000)
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
            f = open('my_thoughts.txt', '6')
            try:
                f.write(a[-1] + '\n')
            finally:
                f.close()
            self.speak("Мне нравится")
            self.speak('Всё успешно сохранено')

        elif cmd == 'start':
            self.speak("Секундомер запущен")
            startTime = time.time()

        elif cmd == 'name':
            t = ['ко мне по-разному обращаются, но мне нравится рита', 'зови просто марго', 'маргарита',
                 'для тебя риточка', ' друзья зовут маргошей',
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
                 'мои дела где-то между хорошо и очень хорошо', 'много работы, мало денег']
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
                com(configuration.commands[cmd])
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
            a = ()
            for i in call_def:
                a = a + (i,)
            a = a + (work_def, val)
            configuration.commands[name_def] = a
        except:
            self.speak('Не удалось добавить функцию, видимо какие-то данные введены неверно')


    def run(self):
        self.listen(self.va_respond)


if __name__ == "__main__":
    assistant = Assistant(configuration.commands)
    assistant.run()
