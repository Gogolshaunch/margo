from tkinter import *
window = Tk()
window.configure(bg="black")
window.geometry("500x550")
window.title("Калькулятор")
window.resizable(False, False)


def cal(operation):
    global formula

    if operation == 'C':
        formula = ''
    elif operation == 'del':
        formula = formula[0: -1]
    elif operation == '+/-':
        formula = str((eval(formula)) * -1)
    elif operation == '%':
        formula = str((eval(formula)) * 100)
    elif operation == 'X^2':
        formula = str((eval(formula)) ** 2)
    elif operation == '=':
        formula = str(eval(formula))
    else:
        if formula == '0':
            formula = ''
        formula += operation
    label_text.configure(text=formula)


formula = '0'
label_text = Label(text=formula, font=('Roboto', 40, 'bold'), bg='black', fg='white')
label_text.place(x=25, y=60)

button = ['C', 'del', '*', '=', '1', '2', '3', '/', '4', '5', '6', '+', '7', '8', '9', '-', '+/-', '0', '%', 'X^2']
x = 15
y = 140
for i in button:
    get_lbl = lambda x = i: cal(x)
    a = Button(text=i, bg='orange', font=('Roboto', 20), command=get_lbl).place(x=x, y=y, width=115, height=79)
    x += 117
    if x > 400:
        x = 15
        y += 81

window.mainloop()
