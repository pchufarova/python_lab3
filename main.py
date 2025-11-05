import tkinter as tk
from random import randint, choice
from playsound import playsound
from threading import Thread
from PIL import Image
import time

HEIGHT = 500 # размеры окна
WIDTH = 600

LBL_HEIGHT = 40 # размеры лейбла где будет ключ
LBL_WIDTH = 200
LBL_PAD_Y = 90 # отступ для лейбла сверху

GIF_HEIGHT = 135 # размеры гиф
GIF_WIDTH = 185
GIF_PAD_X = 2 # отступы для нее
gif_pad_y = HEIGHT - GIF_HEIGHT - GIF_PAD_X

BTN_HEIGHT = 50 # размеры кнопки
BTN_WIDTH = 150
btn_pad_y = gif_pad_y # отступ для кнопки сверху

TEXT_PAD_X = 120
TEXT_PAD_Y = 10 # отступы для текста 

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GIF_FILE = "punchyandbob.gif" 
ICON_FILE = "acnh_bells.png"
MUSIC_FILE = "bubblegum k.k..mp3"
BG_FILE = "acnh_bg.png"
EFFECT_SOUND_FILE = "effect.mp3"


def generate_key():
    first_num = 0
    scnd_num = 0
    while scnd_num - first_num < 2: # проверяем, чтобы буквы не равнялись 
        first_num = randint(0, 25) # друг другу, а так же чтобы между ними
        scnd_num = randint(0, 25) # была хотя бы одна буква, чтобы можно
        # было заполнить среднюю часть ключа
    # индексы всех букв в промежутке, не берем первую букву и последнюю
    possible_nums = list(range(first_num + 1, scnd_num)) 
    # выбираем 7 рандомных
    middle_nums = [choice(possible_nums) for _ in range(7)] 
    # если числа типа 1 2 и тд добавляем 0 перед ними
    first_num += 1
    scnd_num += 1
    frst_prt = str(first_num) if len(str(first_num)) == 2 else f'0{first_num}'
    last_prt = str(scnd_num) if len(str(scnd_num)) == 2 else f'0{scnd_num}'
    middle_part = [ALPHABET[i] for i in middle_nums] # буквы по индексам
    key = f'{frst_prt} {"".join(middle_part)} {last_prt}'

    return key


def init_frames(root):

    generated_key = tk.StringVar() # класс позволяет реализовать
    # динамическое управление переменными
    generated_key.value = "" # стартовое значение

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    bg = tk.PhotoImage(file=BG_FILE) # задний фон
    bg_canvas = tk.Canvas(main_frame, width=WIDTH, height=HEIGHT)
    bg_canvas.pack(fill=tk.BOTH, expand=True)
    bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    bg_canvas.image = bg # чтобы картинка после выхода из функции оставалась 

    def click():
        playsound(EFFECT_SOUND_FILE, False)
        time.sleep(0.5)
        generated_key.set(generate_key()) # задаем в переменную новое
        # сгенерированное значение

    key_label = tk.Label(main_frame, # делаем лейбл для вывода ключа
                         textvariable=generated_key, 
                         font="IMPACT 15",
                         borderwidth=1,
                         relief=tk.GROOVE,
                         background="#FFF8DC")
    bg_canvas.create_window((WIDTH - LBL_WIDTH)//2, # добавляем в окно на фон
                            LBL_PAD_Y, 
                            anchor=tk.NW, 
                            window=key_label, 
                            width=LBL_WIDTH, 
                            height=LBL_HEIGHT)
    start_button = tk.Button(main_frame, # делаем кнопку
                             text="Сгенерировать",
                             font="Impact 15",
                             background="#008000",
                             foreground="#FFF8DC",
                             command=click,
                             cursor="heart")
    bg_canvas.create_window((WIDTH - BTN_WIDTH)//2, # добавляем кнопку 
                            btn_pad_y,
                            anchor=tk.NW,
                            window=start_button,
                            width=BTN_WIDTH,
                            height=BTN_HEIGHT)
    bg_canvas.create_text(TEXT_PAD_X, 
                          TEXT_PAD_Y, # добавляем текст
                          text="Бесплатные ключи Animal Crossing",
                          font="Impact 18",
                          anchor=tk.NW)
    
    gif = Image.open(GIF_FILE) # делаем гифку
    gif_label = tk.Label(main_frame, # лейбл для гифки
                         image="",
                         background="#008000")
    gif_frames = gif.n_frames # берем количество кадров в гифке
    gif_obj = [] 
    for i in range(gif_frames): # каждый кадр добавляем в список
         obj = tk.PhotoImage(file=GIF_FILE, format=f"gif -index {i}")
         gif_obj.append(obj)
    
    def animation(current_frame=0): # функция с рекурсией
        image = gif_obj[current_frame] # каждый раз мы загружаем новый кадр
        gif_label.config(image=image) # и отображаем его в лейбле
        current_frame += 1 # переходим на след. кадр
        if current_frame == gif_frames: # здесь 'сбрасываем' кадры, чтобы
             current_frame = 0 # гифка продолжалась
        main_frame.after(50, lambda: animation(current_frame))
        # after - отложенный вызов функции, мы снова вызываем функцию, чтобы
        # гифка продолжала воспроизводиться. первое число влияет на скорость

    animation()

    bg_canvas.create_window(GIF_PAD_X, # добавляем гифку
                            gif_pad_y,
                            window=gif_label,
                            anchor=tk.NW,
                            width=GIF_WIDTH,
                            height=GIF_HEIGHT,)
    return main_frame


def init_gui():
    root = tk.Tk()
    root.title("Tom Nook's keygen") # название окна и иконка
    icon = tk.PhotoImage(file=ICON_FILE)
    root.iconphoto(False, icon)

    screen_height = root.winfo_screenheight() # размеры экрана
    screen_width = root.winfo_screenwidth()
    x_offset = (screen_width-WIDTH)//2
    y_offset = (screen_height-HEIGHT)//2 # размещаем окно посередине экрана
    root.geometry(f"{WIDTH}x{HEIGHT}+{x_offset}+{y_offset}")
    root.resizable(False, False) # нельзя менять размеры окна

    init_frames(root)
    return root


def play_music(): # функция для воспроизведения музыки
        playsound(MUSIC_FILE)


if __name__ == "__main__":
    root = init_gui()
    # отдельный поток для проигрыша музыки
    Thread(target=play_music, daemon=True).start()
    root.mainloop()