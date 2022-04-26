import tkinter
from tkinter import messagebox
import serial

ser = serial.Serial('COM3', 9600)

class Application:
    def __init__(self):
        self.main_root = tkinter.Tk()
        self.main_root.title('MainWindow')
        self.main_root.geometry('600x400')
        self.light = Light()
        self.light_btn = tkinter.Button(text='LEDウィンドウ', command=self.light.light_win)
        self.light_btn.pack()
        self.create_widgets()
        self.main_root.mainloop()

    def create_widgets(self):
        # 閉じるボタン
        quit_btn = tkinter.Button(self.main_root, height=2, width=10, text='閉じる', command=self.main_root.destroy)
        quit_btn.pack(side='bottom')

class Light:
    def __init__(self):
        self.light_root = None

    def light_win(self):
        if self.light_root == None or not self.light_root.winfo_exists():
            self.light_root = tkinter.Toplevel()
            self.create_subwidget()
        self.light_root.title('LED点灯ウィンドウ')
        self.light_root.geometry('600x400')
        
    def create_subwidget(self):
        quit_btn = tkinter.Button(self.light_root, text='close', command=self.root_close)
        quit_btn.pack()

        # arduinoとのシリアル通信を切断するボタン
        close_btn = tkinter.Button(self.light_root, text='シリアル通信切断', command=self.ser_close)
        close_btn.pack(pady=10, side='bottom')

        # arduinoとシリアル通信を開始するボタン
        open_btn = tkinter.Button(self.light_root, text='シリアル通信開始', command=self.ser_open)
        open_btn.pack(pady=5, side='bottom')

        # 光らせるボタン
        flash_btn = tkinter.Button(self.light_root, height=2, width=10, text='ON', command=self.on_light)
        flash_btn.pack(fill='x', padx=150, side='left')

        # 光を消すボタン
        off_btn = tkinter.Button(self.light_root, height=2, width=10, text='OFF', command=self.off_light)
        off_btn.pack(fill='x', padx=0, side='left')

    def on_light(self):
        try:
            ser.write('H'.encode('utf-8'))
        except serial.serialutil.PortNotOpenError:
            messagebox.showwarning('エラー', 'シリアル通信が切断されています。')

    def off_light(self):
        try:
            ser.write('L'.encode('utf-8'))
        except serial.serialutil.PortNotOpenError:
            messagebox.showwarning('エラー', 'シリアル通信が切断されています。')
            
    def ser_open(self):
        try:
            ser.open()
        except serial.serialutil.SerialException:
            messagebox.showwarning('エラー', '既にシリアル通信が開始されています。')

    def ser_close(self):
        try:
            ser.write('L'.encode('utf-8'))
            ser.close()
        except serial.serialutil.PortNotOpenError:
            messagebox.showwarning('エラー', '既にシリアル通信が切断されています。')

    def root_close(self):
        try:
            ser.write('L'.encode('utf-8'))
            self.light_root.destroy()
        except serial.serialutil.PortNotOpenError:
            ser.open()
            ser.write('L'.encode('utf-8'))
            self.light_root.destroy()


def main():
    Application()

if __name__ == '__main__':
    main()