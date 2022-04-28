import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesnocancel
from pathlib import Path

def func(*args):
    # print(*args)
    return False

class Application:
    def __init__(self, master, function):
        self.master = master
        self.master.geometry('400x400')
        self.master.minsize(430, 430)
        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=0)

        self.function = function

        self.step = tk.StringVar(value='1000')
        self.speed = tk.StringVar(value='1000')
        self.accel = tk.StringVar(value='1000')

        self.is_recording = False
        self.filename = 'Untitled.txt'

        self.update_title(is_file_saved=False)

        self.frame_left = tk.Frame(self.master)
        self.frame_right = tk.Frame(self.master)

        self.frame_left.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
        self.frame_right.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)

        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.columnconfigure(0, weight=1)
        self.frame_right.rowconfigure(0, weight=2)
        self.frame_right.columnconfigure(0, weight=1)

        self.layer_1()
        self.layer_2()
        self.layer_3()
        self.layer_4()
        self.layer_5()
        self.layer_6()
        self.layer_7()

        self.layer_8()
        self.layer_9()

        self.create_menu()
        self.bindings()

        self.update_rec_label()

    def layer_1(self):
        self.frame_1 = tk.Frame(self.frame_left)
        self.frame_1.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)

        self.forward_b = tk.Button(self.frame_1, text='^', command=lambda event=None, dir='forward', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.left_b = tk.Button(self.frame_1, text='<', command=lambda event=None, dir='left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.back_b = tk.Button(self.frame_1, text='v', command=lambda event=None, dir='back', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.right_b = tk.Button(self.frame_1, text='>', command=lambda event=None, dir='right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))

        self.turn_left_b = tk.Button(self.frame_1, text='<<', command=lambda event=None, dir='turn_left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))
        self.turn_right_b = tk.Button(self.frame_1, text='>>', command=lambda event=None, dir='turn_right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step))

        self.discard_b = tk.Button(self.frame_1, text='Discard', command=self.discard_move)

        self.forward_b.grid(row=0, column=1, sticky='nsew')
        self.left_b.grid(row=1, column=0, sticky='nsew')
        self.back_b.grid(row=1, column=1, sticky='nsew')
        self.right_b.grid(row=1, column=2, sticky='nsew')

        self.turn_left_b.grid(row=0, column=0, sticky='nsew')
        self.turn_right_b.grid(row=0, column=2, sticky='nsew')

        self.discard_b.grid(row=2, column=0, columnspan=3, sticky='nsew')

        self.frame_1.columnconfigure(0, weight=1)
        self.frame_1.columnconfigure(1, weight=1)
        self.frame_1.columnconfigure(2, weight=1)
        
        self.frame_1.rowconfigure(0, weight=1)
        self.frame_1.rowconfigure(1, weight=1)
        self.frame_1.rowconfigure(2, weight=0)

    def layer_2(self):
        self.frame_2 = tk.Frame(self.frame_left)
        self.frame_2.grid(row=1, column=0, padx=0, pady=(10, 0))

        self.enter_step = tk.Entry(self.frame_2)
        self.enter_step.grid(row=0, column=0)

        self.send_step = tk.Button(self.frame_2, text='Set steps', command=lambda var=self.enter_step: self.change_step(var))
        self.send_step.grid(row=0, column=1)

        self.frame_2.columnconfigure(0, weight=1)
        self.frame_2.columnconfigure(1, weight=1)
        
        self.frame_2.rowconfigure(0, weight=1)

    def layer_3(self):
        self.frame_3 = tk.Frame(self.frame_left)
        self.frame_3.grid(row=2, column=0, sticky='nsew', padx=0, pady=(0, 5))
        self.display_step = tk.Label(self.frame_3, text=f'Default steps: {self.step.get()}')
        self.display_step.pack()

    def layer_4(self):
        self.frame_4 = tk.Frame(self.frame_left)
        self.frame_4.grid(row=3, column=0, padx=0, pady=0)

        tk.Label(self.frame_4, text='\nSpeed:').grid(row=0, column=0)

        self.speed_slider = tk.Scale(self.frame_4, variable=self.speed, from_=100, to=2000, resolution=50, length=500, orient=tk.HORIZONTAL, command=self.change_speed)
        self.speed_slider.grid(row=0, column=1)
        self.frame_4.columnconfigure(0, weight=0)
        self.frame_4.columnconfigure(1, weight=1)

    def layer_5(self):
        self.frame_5 = tk.Frame(self.frame_left)
        self.frame_5.grid(row=4, column=0, padx=0, pady=0)

        tk.Label(self.frame_5, text='\nAccel. :').grid(row=0, column=0)

        self.accel_slider = tk.Scale(self.frame_5, variable=self.accel, from_=100, to=2000, resolution=50, length=500, orient=tk.HORIZONTAL, command=self.change_accel)
        self.accel_slider.grid(row=0, column=1)

        self.frame_5.columnconfigure(0, weight=0)
        self.frame_5.columnconfigure(1, weight=1)

    def layer_6(self):
        self.frame_6 = tk.Frame(self.frame_left)
        self.frame_6.grid(row=5, column=0, padx=0, pady=(10, 5))

        self.rec_b = tk.Button(self.frame_6, text='Record', command=lambda: self.change_rec_status())
        self.rec_b.grid(row=0, column=0)

        self.frame_6.columnconfigure(0, weight=1)
        self.frame_6.columnconfigure(1, weight=1)

    def layer_7(self):
        self.frame_7 = tk.Frame(self.frame_left)
        self.frame_7.grid(row=6, column=0, sticky='nsew', padx=0, pady=0)

        self.status_label = tk.Label(self.frame_7, text='')
        self.status_label.pack(side='left')

        self.rec_label = tk.Label(self.frame_7, text='⚫', fg='red')
        self.rec_label.pack(side='right')

    def layer_8(self):
        self.frame_8 = tk.Frame(self.frame_right)
        self.frame_8.grid(row=0, column=0, sticky='nsew', padx=0, pady=(0, 5))

        self.steps_list = tk.Listbox(self.frame_8, width=25)

        self.steps_list.grid(row=0, column=0, sticky='nsew')

        self.frame_8.columnconfigure(0, weight=1)
        self.frame_8.rowconfigure(0, weight=1)

    def layer_9(self):
        self.frame_9 = tk.Frame(self.frame_right)
        self.frame_9.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

        self.step_up = tk.Button(self.frame_9, text='^', command=lambda: self.switch_step_position(dir='up'))
        self.step_up.grid(row=0, column=0, sticky='nsew')

        self.step_down = tk.Button(self.frame_9, text='v', command=lambda: self.switch_step_position(dir='down'))
        self.step_down.grid(row=0, column=1, sticky='nsew')

        self.step_settings = tk.Button(self.frame_9, text='Properties', command=lambda: self.master.focus_get())
        self.step_settings.grid(row=0, column=2, sticky='nsew', columnspan=3)

        self.frame_9.columnconfigure(0, weight=0)
        self.frame_9.columnconfigure(1, weight=0)
        self.frame_9.columnconfigure(2, weight=1)
        self.frame_9.columnconfigure(3, weight=1)

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.configure(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label='Open', command=self.file_open, accelerator='Ctrl+O')
        self.file_menu.add_command(label='Save', command=self.file_save, accelerator='Ctrl+S')
        self.file_menu.add_command(label='Save as...', command=lambda: self.file_save(saveas=True), accelerator='Ctrl+Shift+S')
        self.menu.add_cascade(label='File', menu=self.file_menu)

    def bindings(self):
        self.master.bind('<Up>', lambda event, dir='forward', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) == '.' else 0)
        self.master.bind('<Left>', lambda event, dir='left', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) == '.' else 0)
        self.master.bind('<Down>', lambda event, dir='back', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) == '.' else 0)
        self.master.bind('<Right>', lambda event, dir='right', step = self.step, speed=self.speed, accel=self.accel: self.move(event, dir, speed, accel, step) if str(self.master.focus_get()) == '.' else 0)

        self.master.bind('<Control_L><o>', self.file_open)
        self.master.bind('<Control_L><s>', self.file_save)
        self.master.bind('<Control_L><S>', lambda event: self.file_save(saveas=True))

        self.master.bind('<Return>', lambda event, var=self.enter_step: self.change_step(var) if str(self.master.focus_get()) != '.' else self.enter_step.focus_set())
        self.master.bind('<Escape>', lambda event: self.escape_event(event))

        self.master.bind('<Button-1>', lambda event: self.focus_on_master(event))

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
            self.update_title(is_file_saved=False)
            
            self.steps_list.insert('end', self.to_str([dir, speed, accel, step]))

        reply = self.function(dir, speed, accel, step)
        self.change_status(reply)

    def discard_move(self):
        try:
            step = self.steps_list.get('end')
            self.steps_list.delete('end')
            step = self.to_list(step)
            try:
                reply = self.function(step[0], -step[1], step[2], step[3])
                self.change_status(reply)
                self.update_title(is_file_saved=False)
            except TypeError:
                pass
        except IndexError:
            pass

    def change_status(self, reply):
        if reply:
            self.status_label.configure(text='⚫ Last command successful', fg='green')
        else:
            self.status_label.configure(text='⨯ Couldn\'t transmit', fg='red')

    def escape_event(self, event=None):
        if str(self.master.focus_get()) == '.':
            if self.is_recording == True:
                self.change_rec_status()
        else:
            self.master.focus_set()

    def focus_on_master(self, event=None):
        x,y = self.master.winfo_pointerxy()                   # get the mouse position on screen
        widget = self.master.winfo_containing(x,y)
        if str(widget) not in ('.!frame.!frame2.!entry', '.!frame2.!frame.!listbox'):
            self.master.focus_set()

    def switch_step_position(self, dir):
        
        try:
            current_pos = self.steps_list.curselection()[0]
        except IndexError:
            return

        if dir == 'up':
            needed_pos = current_pos - 1
        elif dir == 'down':
            needed_pos = current_pos + 1

        current_val = self.steps_list.get(current_pos)
        needed_val = self.steps_list.get(needed_pos)

        length = len(self.steps_list.get(0, 'end'))

        if current_pos == needed_pos or needed_pos >= length or needed_pos < 0:
            return
        elif current_pos > needed_pos:
            self.steps_list.delete(current_pos)
            self.steps_list.delete(needed_pos)

            self.steps_list.insert(needed_pos, current_val)
            self.steps_list.insert(current_pos, needed_val)
        elif current_pos < needed_pos:
            self.steps_list.delete(needed_pos)
            self.steps_list.delete(current_pos)

            self.steps_list.insert(current_pos, needed_val)
            self.steps_list.insert(needed_pos, current_val)

        self.steps_select(needed_pos)

        self.update_title(is_file_saved=False)

    def steps_select(self, index):
        self.steps_list.select_clear(0, 'end')
        self.steps_list.selection_set(index)
        self.steps_list.see(index)
        self.steps_list.activate(index)
        self.steps_list.selection_anchor(index)

    def file_open(self, event=None):
        if self.is_recording:
                self.change_rec_status()

        filename = askopenfilename(defaultextension='.txt',filetypes=[('All Files','*.*'), ('Text Documents','*.txt')])
        if filename == '':
            return
        if not self.is_initial_file() and not self.is_file_saved:
            answer = askyesnocancel('Quit', 'Opened file contains unsaved changes. Would you like to save them?')
            if answer == True:
                self.file_save()
            elif answer == False:
                pass
            elif answer == None:
                return

        try:
            with open(filename, 'r') as file:
                self.steps_list.delete(0, 'end')
                for line in file.readlines():
                    if self.to_list(line):
                        self.steps_list.insert('end', line.strip('\n'))

            self.filename = filename
            self.update_title(is_file_saved=True)
        except TypeError:
            pass
        except FileNotFoundError:
            pass

    def file_save(self, event=None, saveas=False):
        if self.is_recording:
                self.change_rec_status()

        if saveas or self.filename == 'Untitled.txt':
            self.filename = asksaveasfilename(initialfile=Path(self.filename).name, defaultextension='.txt',filetypes=[('All Files','*.*'), ('Text Documents','*.txt')])

        if not self.filename:
            self.filename = 'Untitled.txt'
            return

        with open(self.filename, 'w') as file:
            for step in self.steps_list.get(0, 'end'):
                file.write(step + '\n')

        if self.is_recording:
                self.change_rec_status()
        self.update_title(is_file_saved=True)

    def update_title(self, is_file_saved):
        self.is_file_saved = is_file_saved
        if is_file_saved:
            self.master.title(Path(self.filename).name + ' — trackmaster')
        else:
            self.master.title(Path(self.filename).name + '*' + ' — trackmaster')

    def on_closing(self):
        if self.is_initial_file() or self.is_file_saved:
            self.master.destroy()
        else:
            answer = askyesnocancel('Quit', 'Opened file contains unsaved changes. Would you like to save them?')
            
            if answer == True:
                self.file_save()
                self.master.destroy()
            elif answer == False:
                self.master.destroy()

    def is_initial_file(self):
        return not self.is_file_saved and Path(self.filename).name == 'Untitled.txt' and len(self.steps_list.get(0, 'end')) == 0

    def to_str(self, l):
        return ' '.join(map(str, l))

    def to_list(self, s):
        l = s.split(' ')

        if len(l) == 4 and l[0] in ('forward', 'back', 'left', 'right', 'turn_left', 'turn_right'):
            try:
                l[1:4] = list(map(int, l[1:4]))
            except ValueError:
                return False
        else:
            return False

        return l

def main():
    root = tk.Tk()
    app = Application(master=root, function=func)
    root.mainloop()

if __name__ == '__main__':
    main()