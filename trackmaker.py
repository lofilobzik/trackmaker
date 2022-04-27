import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import time

def func(*args):
    print(*args)
    return False

class Application:
    def __init__(self, master, function):
        self.master = master
        self.master.geometry('300x400')
        self.master.minsize(300, 480)
        self.master.maxsize(600, 700)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.function = function

        self.step = tk.StringVar(value='1000')
        self.speed = tk.StringVar(value='1000')
        self.accel = tk.StringVar(value='1000')

        self.is_recording = False

        self.route = []

        self.layer_1()
        self.layer_2()
        self.layer_3()
        self.layer_4()
        self.layer_5()
        self.layer_6()
        self.layer_7()
        self.bindings()

        self.update_rec_label()

    def layer_1(self):
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.forward_b = tk.Button(self.frame, text='^', command=lambda event=None, dir='forward', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.left_b = tk.Button(self.frame, text='<', command=lambda event=None, dir='left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.back_b = tk.Button(self.frame, text='v', command=lambda event=None, dir='back', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.right_b = tk.Button(self.frame, text='>', command=lambda event=None, dir='right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))

        self.turn_left_b = tk.Button(self.frame, text='<<', command=lambda event=None, dir='turn_left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.turn_right_b = tk.Button(self.frame, text='>>', command=lambda event=None, dir='turn_right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))

        self.discard_b = tk.Button(self.frame, text='Discard', command=self.discard_move)

        self.forward_b.grid(row=0, column=1, sticky='nsew')
        self.left_b.grid(row=1, column=0, sticky='nsew')
        self.back_b.grid(row=1, column=1, sticky='nsew')
        self.right_b.grid(row=1, column=2, sticky='nsew')

        self.turn_left_b.grid(row=0, column=0, sticky='nsew')
        self.turn_right_b.grid(row=0, column=2, sticky='nsew')

        self.discard_b.grid(row=2, column=0, columnspan=3, sticky='nsew')

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=0)

    def layer_2(self):
        self.frame_2 = tk.Frame(self.master)
        self.frame_2.grid(row=1, column=0, padx=10, pady=5)

        self.enter_step = tk.Entry(self.frame_2)
        self.enter_step.grid(row=0, column=0)

        self.send_step = tk.Button(self.frame_2, text='Set steps', command=lambda var=self.enter_step: self.change_step(var))
        self.send_step.grid(row=0, column=1)

        self.frame_2.columnconfigure(0, weight=1)
        self.frame_2.columnconfigure(1, weight=1)
        
        self.frame_2.rowconfigure(0, weight=1)

    def layer_3(self):
        self.frame_3 = tk.Frame(self.master)
        self.frame_3.grid(row=2, column=0, sticky='nsew', padx=20, pady=0)
        self.display_step = tk.Label(self.frame_3, text=f'Default steps: {self.step.get()}')
        self.display_step.pack()

    def layer_4(self):
        self.frame_4 = tk.Frame(self.master)
        self.frame_4.grid(row=3, column=0, padx=10, pady=5)

        tk.Label(self.frame_4, text='\nSpeed:').grid(row=0, column=0)

        self.speed_slider = tk.Scale(self.frame_4, variable=self.speed, from_=100, to=2000, resolution=50, length=500, orient=tk.HORIZONTAL, command=self.change_speed)
        self.speed_slider.grid(row=0, column=1)
        self.frame_4.columnconfigure(0, weight=0)
        self.frame_4.columnconfigure(1, weight=1)

    def layer_5(self):
        self.frame_5 = tk.Frame(self.master)
        self.frame_5.grid(row=4, column=0, padx=10, pady=5)

        tk.Label(self.frame_5, text='\nAccel. :').grid(row=0, column=0)

        self.accel_slider = tk.Scale(self.frame_5, variable=self.accel, from_=100, to=2000, resolution=50, length=500, orient=tk.HORIZONTAL, command=self.change_accel)
        self.accel_slider.grid(row=0, column=1)

        self.frame_5.columnconfigure(0, weight=0)
        self.frame_5.columnconfigure(1, weight=1)

    def layer_6(self):
        self.frame_6 = tk.Frame(self.master)
        self.frame_6.grid(row=5, column=0, sticky = '', padx=10, pady=5)

        self.rec_b = tk.Button(self.frame_6, text='Record', command=lambda: self.change_rec_status())
        self.rec_b.grid(row=0, column=0)

        self.frame_6.columnconfigure(0, weight=1)
        self.frame_6.columnconfigure(1, weight=1)


    def layer_7(self):
        self.frame_7 = tk.Frame(self.master)
        self.frame_7.grid(row=6, column=0, sticky='nsew', padx=20, pady=10)

        self.status_label = tk.Label(self.frame_7, text='')
        self.status_label.pack(side='left')

        self.rec_label = tk.Label(self.frame_7, text='⚫', fg='red')
        self.rec_label.pack(side='right')


    def bindings(self):
        # Disable keys if tk.Entry is focused
        self.master.bind('<Up>', lambda event, dir='forward', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) != '.!frame2.!entry' else 0)
        self.master.bind('<Left>', lambda event, dir='left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) != '.!frame2.!entry' else 0)
        self.master.bind('<Down>', lambda event, dir='back', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) != '.!frame2.!entry' else 0)
        self.master.bind('<Right>', lambda event, dir='right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) != '.!frame2.!entry' else 0)

        # <Escape> to unfocus tk.Entry; <Return> to focus if unfocused and run self.change_step if focused
        self.master.bind('<Return>', lambda event, var=self.enter_step: self.change_step(var) if str(self.master.focus_get()) != '.' else self.enter_step.focus_set())
        self.master.bind('<Escape>', lambda event: self.master.focus_set())

    def change_step(self, var, event=None):
        try:
            var = var.get()
            self.display_step.configure(text=f'Default steps: {int(var)}') # filters non-integers
            self.step.set(var)
            self.enter_step.configure(textvariable=tk.StringVar(value=''))
        except ValueError:
            pass

    def change_speed(self, event):
        self.speed.set(event)

    def change_accel(self, event):
        self.accel.set(event)

    def change_rec_status(self):
        self.is_recording = not self.is_recording

        if self.is_recording:
            self.rec_b.configure(text='Stop recording')
        else:
            filename = asksaveasfilename(initialfile = time.strftime('%Y%m%d-%H%M%S') + '.txt', defaultextension='.txt',filetypes=[('All Files','*.*'), ('Text Documents','*.txt')])
            
            try:
                with open(filename, 'w') as file:
                    for step in self.route:
                        file.write(' '.join(map(str, step)) + '\n')
            except TypeError:
                pass

            self.rec_b.configure(text='Record')

    def update_rec_label(self):
        if self.rec_label.cget('text') == '' and self.is_recording:
            self.rec_label.configure(text='⚫')
        else:
            self.rec_label.configure(text='')
        self.master.after(1000, self.update_rec_label)

    def move(self, event, dir, speed, accel, step):
        speed = int(speed.get())
        accel = int(accel.get())
        step = int(step.get())

        try:
            step = int(self.enter_step.get())
            self.enter_step.configure(textvariable=tk.StringVar(value=''))
        except ValueError:
            pass

        if self.is_recording:
            self.route.append([dir, speed, accel, step])

        reply = self.function(dir, speed, accel, step)
        self.change_status(reply)

    def discard_move(self):
        try:
            step = self.route.pop()
            reply = self.function(step[0], -step[1], step[2], step[3])
            self.change_status(reply)
        except IndexError:
            pass

    def change_status(self, reply):
        if reply:
            self.status_label.configure(text='⚫ Last command successful', fg='green')
        else:
            self.status_label.configure(text='⨯ Couldn\'t transmit', fg='red')

def main():
    root = tk.Tk()
    app = Application(master=root, function=func)
    root.mainloop()

if __name__ == '__main__':
    main()