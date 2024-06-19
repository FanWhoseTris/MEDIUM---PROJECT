from tkinter import *
from tkinter import messagebox
from chat import get_response, bot_name
import subprocess
import os

BG_GRAY = "#ABB2B9"
BG_COLOR = "#141414"
TEXT_COLOR = "#149414"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self.window.iconbitmap('data/icon.ico')
        self.running = True
        self.runv = False
        self.voice_process = None
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat With Sin")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg="yellow",
                           text="Welcome To Chat With Sin", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # mic
        # mic_image = PhotoImage(file="path/to/mic_icon.png")  # Thay "path/to/mic_icon.png" bằng đường dẫn tới hình ảnh biểu tượng mic
        mic_button = Button(head_label, text="V", font=FONT_BOLD, bg=BG_GRAY, fg="black", bd=0, width=4, height=4,
                            command=lambda: self._on_mic_button_pressed())
        # mic_button.image = mic_image  # Lưu tham chiếu tới hình ảnh, tránh bị thu hồi bởi garbage collector
        mic_button.place(relx=0.955, rely=0.5, anchor="center")

        # Guide
        # mic_image = PhotoImage(file="path/to/mic_icon.png")  # Thay "path/to/mic_icon.png" bằng đường dẫn tới hình ảnh biểu tượng mic
        ask_button = Button(head_label, text="?", font=FONT_BOLD, bg=BG_GRAY, fg="black", bd=0, width=4, height=4,
                            command=lambda: self.show_guide())
        # mic_button.image = mic_image  # Lưu tham chiếu tới hình ảnh, tránh bị thu hồi bởi garbage collector
        ask_button.place(relx=0.04, rely=0.5, anchor="center")

        # update
        # mic_image = PhotoImage(file="path/to/mic_icon.png")  # Thay "path/to/mic_icon.png" bằng đường dẫn tới hình ảnh biểu tượng mic
        u_button = Button(head_label, text="U", font=FONT_BOLD, bg=BG_GRAY, fg="black", bd=0, width=4, height=4,
                          command=lambda: self._on_update_button_pressed())
        # mic_button.image = mic_image  # Lưu tham chiếu tới hình ảnh, tránh bị thu hồi bởi garbage collector
        u_button.place(relx=0.15, rely=0.5, anchor="center")

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#353740", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Gửi", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_update_button_pressed(self):
        try:
            train_py_path = os.path.join(os.path.dirname(__file__), "train.py")
            subprocess.Popen(["python", train_py_path])
        except Exception as e:
            print(e)

    def _on_mic_button_pressed(self):
        self.runv = not self.runv
        # print(self.runv)
        if self.runv:
            try:
                v_py_path = os.path.join("voice.py")
                self.voice_process = subprocess.Popen(["python", v_py_path])
            except Exception as e:
                print(e)
        else:
            try:
                if self.voice_process:
                    self.voice_process.terminate()
                    self.voice_process = None
            except Exception as e:
                print(e)

    def show_guide(self):
        guide_text = """
        Hướng dẫn sử dụng chương trình:
        - Bước 1: Nhập nội dung chat vào ô phía dưới và nhấn Enter hoặc nút "Gửi".
        - Bước 2: Xem phản hồi của chatbot trong khung phía trên.
        - Bước 3: Bật/Tắt chế độ giọng nói bằng nút "V".
        - Bước 4: Nhấn nút "?" để xem lại hướng dẫn sử dụng chương trình này.
        """

        # Hiển thị hộp thoại thông báo chứa text label
        messagebox.showinfo("Hướng dẫn sử dụng", guide_text)

    def note(self):
        try:
            note_exe_path = os.path.join("note", "note.exe")
            subprocess.Popen([note_exe_path])
        except Exception as e:
            print(e)
        self.msg_entry.delete(0, END)

    def _open_todolist(self):
        try:
            todolist_exe_path = os.path.join("WorkWise", "todolist.exe")
            subprocess.Popen([todolist_exe_path])
        except Exception as e:
            print(e)
        self.msg_entry.delete(0, END)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if msg.lower() == "quit":
            self.window.destroy()
            if self.voice_process:
                self.voice_process.terminate()
                self.voice_process = None
            self.running = False
        self._insert_message(msg, "Bạn")

    def _insert_message(self, msg, sender):
        if not msg:
            return
        if not self.running:
            return
        if msg.lower() == "sin.note":
            self.msg_entry.delete(0, END)
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, "//////////////////////Opening Note////////////////////////\n\n")
            self.text_widget.configure(state=DISABLED)
            self.note()
            return

        elif msg.lower() == "sin.todo":
            self.msg_entry.delete(0, END)
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, "////////////////////Opening To-Do-List///////////////////\n\n")
            self.text_widget.configure(state=DISABLED)
            self._open_todolist()
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    runv = False
    app = ChatApplication()
    app.run()