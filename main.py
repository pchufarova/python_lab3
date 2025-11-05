import tkinter as tk
from random import randint, choice
from playsound import playsound
from threading import Thread
from PIL import Image
import time


def generate_key():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
    middle_part = [alphabet[i] for i in middle_nums] # буквы по индексам
    key = f'{frst_prt} {"".join(middle_part)} {last_prt}'

    return key


def init_frames(root):
    height = 500 # размеры окна
    width = 600

    lbl_height = 40 # размеры лейбла где будет ключ
    lbl_width = 200
    lbl_pad_y = 90 # отступ для лейбла сверху

    gif_height = 135 # размеры гиф
    gif_width = 185
    gif_pad_x = 2 # отступы для нее
    gif_pad_y = height - gif_height - gif_pad_x

    btn_height = 50 # размеры кнопки
    btn_width = 150
    btn_pad_y = gif_pad_y # отступ для кнопки сверху

    text_pad_x = 120
    text_pad_y = 10 # отступы для текста 

    generated_key = tk.StringVar() # класс позволяет реализовать
    # динамическое управление переменными
    generated_key.value = "" # стартовое значение

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    bg = tk.PhotoImage(file="acnh_bg.png") # задний фон
    bg_canvas = tk.Canvas(main_frame, width=width, height=height)
    bg_canvas.pack(fill=tk.BOTH, expand=True)
    bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    bg_canvas.image = bg # чтобы картинка после выхода из функции оставалась 

    def click():
        playsound("effect.mp3", False)
        time.sleep(0.5)
        generated_key.set(generate_key()) # задаем в переменную новое
        # сгенерированное значение

    key_label = tk.Label(main_frame, # делаем лейбл для вывода ключа
                         textvariable=generated_key, 
                         font="IMPACT 15",
                         borderwidth=1,
                         relief=tk.GROOVE,
                         background="#FFF8DC")
    bg_canvas.create_window((width - lbl_width)//2, # добавляем в окно на фон
                            lbl_pad_y, 
                            anchor=tk.NW, 
                            window=key_label, 
                            width=lbl_width, 
                            height=lbl_height)
    start_button = tk.Button(main_frame, # делаем кнопку
                             text="Сгенерировать",
                             font="Impact 15",
                             background="#008000",
                             foreground="#FFF8DC",
                             command=click,
                             cursor="heart")
    bg_canvas.create_window((width - btn_width)//2, # добавляем кнопку 
                            btn_pad_y,
                            anchor=tk.NW,
                            window=start_button,
                            width=btn_width,
                            height=btn_height)
    bg_canvas.create_text(text_pad_x, 
                          text_pad_y, # добавляем текст
                          text="Бесплатные ключи Animal Crossing",
                          font="Impact 18",
                          anchor=tk.NW)
    
    gif_file = "punchyandbob.gif" # делаем гифку
    gif = Image.open(gif_file)
    gif_label = tk.Label(main_frame, # лейбл для гифки
                         image="",
                         background="#008000")
    gif_frames = gif.n_frames # берем количество кадров в гифке
    gif_obj = [] 
    for i in range(gif_frames): # каждый кадр добавляем в список
         obj = tk.PhotoImage(file=gif_file, format=f"gif -index {i}")
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

    bg_canvas.create_window(gif_pad_x, # добавляем гифку
                            gif_pad_y,
                            window=gif_label,
                            anchor=tk.NW,
                            width=gif_width,
                            height=gif_height,)
    return main_frame


def init_gui():
    root = tk.Tk()
    root.title("Tom Nook's keygen") # название окна и иконка
    icon = tk.PhotoImage(file="acnh_bells.png")
    root.iconphoto(False, icon)

    height = 500 # размеры окна
    width = 600
    screen_height = root.winfo_screenheight() # размеры экрана
    screen_width = root.winfo_screenwidth()
    x_offset = (screen_width-width)//2
    y_offset = (screen_height-height)//2 # размещаем окно посередине экрана
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
    root.resizable(False, False) # нельзя менять размеры окна

    init_frames(root)
    return root


def play_music(): # функция для воспроизведения музыки
        playsound("bubblegum k.k..mp3")


if __name__ == "__main__":
    root = init_gui()
    # отдельный поток для проигрыша музыки
    Thread(target=play_music, daemon=True).start()
    root.mainloop()