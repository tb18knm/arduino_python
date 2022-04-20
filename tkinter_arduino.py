import tkinter
from tkinter import messagebox
import serial

ser = serial.Serial('COM3', 9600)

class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=500, height=400, borderwidth=1, relief="groove")
        self.root = root
        self.pack() #位置を指定して配置
        self.pack_propagate(0) #サイズ調整
        self.create_widgets()

    def create_widgets(self):

        # 閉じるボタン
        quit_btn = tkinter.Button(self, height=2, width=10)
        quit_btn['text'] = '閉じる'
        quit_btn['command'] = self.root_close
        # quit_btn['command'] = self.root.destroy
        quit_btn.pack(side='bottom')

        # arduinoとのシリアル通信を切断するボタン
        close_btn = tkinter.Button(self)
        close_btn['text'] = 'シリアル通信切断'
        close_btn['command'] = self.ser_close
        close_btn.pack(pady=10, side='bottom')

        # arduinoとシリアル通信を開始するボタン
        open_btn = tkinter.Button(self)
        open_btn['text'] = 'シリアル通信開始'
        open_btn['command'] = self.ser_open
        open_btn.pack(pady=5, side='bottom')

        # 光らせるボタン
        flash_btn = tkinter.Button(self, height=2, width=10)
        flash_btn['text'] = 'ON'
        flash_btn['command'] = self.on_light
        flash_btn.pack(fill='x', padx=110, side='left')

        # 光を消すボタン
        off_btn = tkinter.Button(self, height=2, width=10)
        off_btn['text'] = 'OFF'
        off_btn['command'] = self.off_light
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
        ser.open()

    def ser_close(self):
        ser.write('L'.encode('utf-8'))
        ser.close()

    def root_close(self):
        try:
            ser.write('L'.encode('utf-8'))
            self.root.destroy()
        except serial.serialutil.PortNotOpenError:
            ser.open()
            ser.write('L'.encode('utf-8'))
            self.root.destroy()


root = tkinter.Tk()
root.title('LED SWITCH')
root.geometry('500x400')
app = Application(root=root)
app.mainloop()