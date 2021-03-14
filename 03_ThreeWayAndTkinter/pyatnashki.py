from tkinter import *
import random

Numbers = [i for i in range(1, 16)]


class game(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Пятнашки')
        random.shuffle(Numbers)
        self.check_Numbers()
        self.grid(sticky=N + S + E + W)
        self.spot = {"row": 4, "column": 3}
        self.init_widgets()

    def check_Numbers(self):
        count = 0
        for i in range(0, len(Numbers)):
            for j in range(i, len(Numbers)):
                if Numbers[i] > Numbers[j]:
                    count += 1
        if count % 2 == 1:
            Numbers[0], Numbers[1] = Numbers[1], Numbers[0]

    def new_game(self):
        random.shuffle(Numbers)
        self.check_Numbers()
        self.spot = {"row": 4, "column": 3}
        for bt in self.Buttons:
            bt.destroy()
        self.init_widgets()

    def init_widgets(self):
        self.winfo_toplevel().columnconfigure(0, weight=1)
        self.winfo_toplevel().rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.rowconfigure(i, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

        self.new_B = Button(self, text="New", command=self.new_game)
        self.exit_B = Button(self, text='Exit', command=self.quit)
        self.new_B.grid(row=0, column=0, sticky="NEWS", columnspan=2)
        self.exit_B.grid(row=0, column=2, sticky="NEWS", columnspan=2)
        self.Buttons = [Button(self, text=str(n), command=self.make_move(i)) for i, n in enumerate(Numbers)]
        for i, bt in enumerate(self.Buttons):
            bt.grid(row=i // 4 + 1, column=i % 4, sticky="NEWS")

    def make_move(self, number):
        def move():
            grid_info = self.Buttons[number].grid_info()
            column = grid_info['column']
            row = grid_info['row']
            if (row == self.spot['row'] and (column == self.spot['column'] - 1
                                             or column == self.spot['column'] + 1)):
                self.Buttons[number].grid(row=self.spot['row'], column=self.spot['column'])
                self.spot['column'] = column
                if self.win_flag():
                    messagebox.showinfo('Пятнашки', 'Победа')
                    self.new_game()
            elif (column == self.spot['column'] and (row == self.spot['row'] - 1 or row == self.spot['row'] + 1)):
                self.Buttons[number].grid(row=self.spot['row'], column=self.spot['column'])
                self.spot['row'] = row
                if self.win_flag():
                    messagebox.showinfo('Пятнашки', 'Победа')
                    self.new_game()

        return move

    def win_flag(self):
        for i, bt in enumerate(self.Buttons):
            info = bt.grid_info()
            col = info['column']
            row = info['row']
            if col != (Numbers[i] - 1) % 4 or row != (Numbers[i] - 1) // 4 + 1:
                return False
        return True


g = game()
g.mainloop()
