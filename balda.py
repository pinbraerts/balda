import re
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL, SUNKEN, RAISED
from random import choice


selected_field = None
selected_letter = None
repeat = None
override = None
score_1 = None
score_2 = None


def write_letter(cell, letter):
    cell.config(
        text=letter['text'],
        relief=RAISED,
        state=NORMAL if override.get() else DISABLED,
    )
    letter.config(
        relief=RAISED,
        state=NORMAL if repeat.get() else DISABLED,
    )


def field_click(e):
    if e.widget['state'] == DISABLED and not override.get():
        return
    global selected_field, selected_letter
    if selected_letter is not None:
        write_letter(e.widget, selected_letter)
        selected_letter = None
        return
    if selected_field is not None:
        selected_field.config(relief=RAISED, text=' ', state=NORMAL)
    if selected_field is e.widget:
        selected_field = None
        return
    selected_field = e.widget
    selected_field.config(relief=SUNKEN, state=NORMAL)


def letter_click(e):
    if e.widget['state'] == DISABLED and not repeat.get():
        return
    global selected_field, selected_letter
    if selected_field is not None:
        write_letter(selected_field, e.widget)
        selected_field = None
        return
    if selected_letter is not None:
        selected_letter.config(relief=RAISED, state=NORMAL)
    if selected_letter is e.widget:
        selected_letter = None
        return
    selected_letter = e.widget
    selected_letter.config(relief=SUNKEN, state=NORMAL)


words = open('word5.txt', encoding='utf-8').read().splitlines()
w = tk.Tk()
font = ('FiraCode Nerd Font Mono', 32)
small = ('FiraCode Nerd Font Mono', 16)
w.title('Балда')
repeat = tk.BooleanVar(value=False)
override = tk.BooleanVar(value=False)

field_size = 5
w.columnconfigure(field_size, weight=6)

panel_size = 2


definition = tk.Label(
    text='',
    width=50,
    font=small,
    wraplength=600,
    anchor='nw',
    justify='left',
)
definition.grid(
    column=field_size,
    row=2,
    rowspan=field_size,
    columnspan=panel_size,
    sticky='nw',
)


def clear():
    for i in range((len(alphabet) + field_size - 1) // field_size):
        for j in range(field_size * 2 + panel_size):
            a = w.grid_slaves(row=i, column=j)
            if not a:
                continue
            a = a[0]
            if i < field_size and j >= field_size + panel_size:
                a.config(text=' ', relief=RAISED, state=NORMAL)
            if j < field_size:
                a.config(relief=RAISED, state=NORMAL)

    score_1.config(text='0')
    score_2.config(text='0')
    definition.config(text='')


def generate_word():
    clear()
    word, defi = choice(words).split(':', maxsplit=1)
    defi = re.sub(r' ((\d|\w\)|\.))', '\n\\1', defi)[:-1]
    definition.config(text=defi)
    for i, c in enumerate(word):
        cell = w.grid_slaves(row=2, column=field_size + panel_size + i)[0]
        j = alphabet.index(c)
        letter = w.grid_slaves(column=j % field_size, row=j // field_size)[0]
        write_letter(cell, letter)


width = 4
height = width // 2

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
for i, letter in enumerate(alphabet):
    b = tk.Label(
        text=letter,
        width=width,
        height=height,
        font=font,
        relief=RAISED,
        disabledforeground='red',
    )
    b.grid(column=i % field_size, row=i // field_size)
    b.bind('<1>', letter_click)

field = list()
for i in range(5):
    row = list()
    for j in range(5):
        b = tk.Label(
            text=' ',
            width=width,
            height=height,
            font=font,
            relief=RAISED,
            disabledforeground='blue',
        )
        b.grid(column=field_size + panel_size + j, row=i)
        b.bind('<1>', field_click)
        row.append(b)
    field.append(row)

tk.Checkbutton(
    text='Повторение',
    variable=repeat,
    onvalue=True,
    offvalue=False,
    font=font,
).grid(column=field_size, row=0)

tk.Checkbutton(
    text='Перезапись',
    variable=override,
    onvalue=True,
    offvalue=False,
    font=font,
).grid(column=field_size + 1, row=0)

tk.Button(
    text='Очистить',
    font=font,
    command=clear,
).grid(column=field_size, row=1)

tk.Button(
    text='Слово',
    font=font,
    command=generate_word,
).grid(column=field_size + 1, row=1)


def counter():
    counter = tk.Label(text='0', font=font)
    counter.bind(
        '<1>',
        lambda e: e.widget.config(text=str(int(e.widget['text']) + 1)),
    )
    counter.bind(
        '<3>',
        lambda e: e.widget.config(text=str(int(e.widget['text']) - 1)),
    )
    return counter


tk.Label(text='Илья', font=font).grid(column=field_size + panel_size, row=5)
score_1 = counter()
score_1.grid(column=field_size + panel_size + 1, row=5)

tk.Label(text='Дима', font=font).grid(column=field_size + panel_size, row=6)
score_2 = counter()
score_2.grid(column=field_size + panel_size + 1, row=6)

w.mainloop()
