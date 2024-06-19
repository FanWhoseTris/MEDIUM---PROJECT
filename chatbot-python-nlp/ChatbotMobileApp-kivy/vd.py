from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from chat import get_response, bot_name

BG_GRAY = (171 / 255, 178 / 255, 185 / 255, 1)
BG_COLOR = (23 / 255, 32 / 255, 42 / 255, 1)
TEXT_COLOR = (234 / 255, 236 / 255, 238 / 255, 1)


class ChatApp(App):
    def build(self):
        self.window = BoxLayout(orientation='vertical')

        # head label
        head_label = Label(text="Welcome", color=TEXT_COLOR, font_size=18, size_hint_y=0.07)
        self.window.add_widget(head_label)

        # text widget
        self.text_widget = TextInput(background_color=BG_COLOR, foreground_color=TEXT_COLOR,
                                     font_size=14, readonly=True, cursor_blink=False)
        self.window.add_widget(self.text_widget)

        # bottom layout
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)

        # message entry box
        self.msg_entry = TextInput(background_color=(44 / 255, 62 / 255, 80 / 255, 1), foreground_color=TEXT_COLOR,
                                   font_size=14, size_hint_x=0.74, multiline=False, cursor_blink=True)
        self.msg_entry.bind(on_text_validate=self._on_enter_pressed)
        bottom_layout.add_widget(self.msg_entry)

        # send button
        send_button = Button(text="Gửi", font_size=14, background_color=BG_GRAY, size_hint_x=0.22)
        send_button.bind(on_release=self._on_send_button_press)
        bottom_layout.add_widget(send_button)

        self.window.add_widget(bottom_layout)

        return self.window

    def _on_send_button_press(self, instance):
        msg = self.msg_entry.text
        self._insert_message(msg, "Bạn")

    def _on_enter_pressed(self, instance):
        msg = self.msg_entry.text
        self._insert_message(msg, "Bạn")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.text = ""
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.text += msg1

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.text += msg2

        # Scroll to the end of the text
        self.text_widget.scroll_y = 0


if __name__ == "__main__":
    ChatApp().run()
