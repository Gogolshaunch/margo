from tkinter import *
import tkinter.messagebox
import pickle

window = Tk()
window.configure(bg="white")
window.title("TO DO LIST")


def add_task():
    task = entry_task.get()
    if task != "":
        task = f'●{task}'
        listbox_tasks.insert(END, task)
        entry_task.delete(0, END)

    else:
        tkinter.messagebox.showwarning(title="Warning!", message="Вы должны ввести задачу.")


def delete_task():
    try:
        task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(task_index)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Вы должны выбрать задачу.")


def load_tasks():
    try:
        tasks = pickle.load(open("../tasks.dat", "rb"))
        listbox_tasks.delete(0, tkinter.END)
        for task in tasks:
            listbox_tasks.insert(tkinter.END, task)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Cannot find tasks.dat.")


def save_tasks():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    pickle.dump(tasks, open("../tasks.dat", "wb"))


frame_tasks = Frame(window)
frame_tasks.pack()

listbox_tasks = Listbox(frame_tasks, height=10, width=50)
listbox_tasks.pack(side=tkinter.LEFT)

scrollbar_tasks = Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

lab = Label(window, text="Введите новые заметки: ", font=20, bg='white')
lab.pack()

entry_task = Entry(window, width=50)
entry_task.pack()

button_add_task = Button(window, text="Добавить задачу", width=48, command=add_task)
button_add_task.pack()

button_delete_task = Button(window, text="Удалить задачу", width=48, command=delete_task)
button_delete_task.pack()

button_load_tasks = tkinter.Button(window, text="Вывести сохраненные задачи", width=48, command=load_tasks)
button_load_tasks.pack()

button_save_tasks = Button(window, text="Сохранить задачу", width=48, command=save_tasks)
button_save_tasks.pack()

window.mainloop()
