import tkinter as tk
from tkinter.messagebox import showinfo


def add_widget(parent, name):
    def update_widget(child, position, *args, **kwargs):
        def geometry_split(s, char, default=None):
            s = s.split(char)
            if len(s) == 1:
                s = s[0], default
            return s

        position, sticky = geometry_split(position, '/', 'NEWS')
        row, column = position.split(':')
        row, height = geometry_split(row, '+', 0)
        column, width = geometry_split(column, '+', 0)
        row, row_weight = map(int, geometry_split(row, '.', 1))
        column, column_weight = map(int, geometry_split(column, '.', 1))
        children = type(child.__name__ + "_upgraded", tuple([child]), {"__getattr__": add_widget})
        setattr(parent, name, children(parent, *args, **kwargs))
        getattr(parent, name).grid(row=row,
                                   column=column,
                                   sticky=sticky,
                                   rowspan=int(height) + 1,
                                   columnspan=int(width) + 1)
        getattr(parent, name).master.rowconfigure(row, weight=row_weight)
        getattr(parent, name).master.columnconfigure(column, weight=column_weight)

    return update_widget


class Application(tk.Frame):
    def __init__(self, master=None, title=""):
        super().__init__(master)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        if master is None:
            self.master.title(title)
        Application.__getattr__ = add_widget
        self.createWidgets()


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a secret level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))


app = App(title="Simplified")
app.mainloop()
