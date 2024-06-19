from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from chat import get_response, bot_name
from kivy.core.window import Window

BG_GRAY = (171 / 255, 178 / 255, 185 / 255, 1)
BG_COLOR = (77,77,123,.2)
TEXT_COLOR = (234 / 255, 236 / 255, 238 / 255, 1)
namec = (1, 1, 0, 1)

class ChatApp(App):

    def build(self):
        self.window = BoxLayout(orientation='vertical')

        # Set app icon
        icon = "data/icon.png"
        Window.set_icon(icon)

        #Set title
        self.title = "Chat With Sin"

        # Create a RelativeLayout to hold head_label and icon
        head_layout = RelativeLayout(size_hint_y=0.1)

        # head label
        head_label = Label(text="SIN", font_size=34,color = namec)
        head_layout.add_widget(head_label)

        # Set app icon
        iconr = Image(source='data/sinr.png', size_hint=(None, None), size=(52, 52),
                     pos_hint={'right': 1, 'y': 0.3}, pos=(0, 0))  # Đường dẫn đến tập tin hình ảnh icon
        iconl = Image(source='data/sinl.png', size_hint=(None, None), size=(52, 52),
                      pos_hint={'left': 1, 'y': 0.3}, pos=(0, 0))  # Đường dẫn đến tập tin hình ảnh icon
        head_layout.add_widget(iconr)
        head_layout.add_widget(iconl)

        self.window.add_widget(head_layout)

        # Scroll View
        self.text_scroll_view = ScrollView()

        # layout for containing messages
        self.text_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)  # Đặt giá trị spacing tại đây
        self.text_layout.bind(minimum_height=self.text_layout.setter('height'))

        self.text_scroll_view.add_widget(self.text_layout)
        self.window.add_widget(self.text_scroll_view)

        # bottom layout
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)

        # message entry box
        self.msg_entry = TextInput(background_color=BG_COLOR, foreground_color=TEXT_COLOR,
                                   font_size=25, size_hint_x=0.74, multiline=False, cursor_blink=True)
        self.msg_entry.bind(on_text_validate=self._on_enter_pressed)
        bottom_layout.add_widget(self.msg_entry)

        # send button
        send_button = Button(text="Gửi", font_size=25, background_color=BG_GRAY, size_hint_x=0.22)
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

        # Create and add a label for user's message
        user_msg_label = Label(text=f"{sender}: {msg}", color=TEXT_COLOR, font_size=25, size_hint_y=None,
                               halign='left', markup=True, text_size=(self.text_layout.width, None))
        user_msg_label.bind(texture_size=user_msg_label.setter('size'))
        self.text_layout.add_widget(user_msg_label)

        # Create and add a label for bot's response
        botmsg = get_response(msg)
        bot_msg_label = Label(text=f"{bot_name}: {botmsg}", color=TEXT_COLOR, font_size=25, size_hint_y=None,
                              halign='left', markup=True, text_size=(self.text_layout.width, None))
        bot_msg_label.bind(texture_size=bot_msg_label.setter('size'))
        self.text_layout.add_widget(bot_msg_label)

        # Scroll to the end of the text_layout (the bottom of the ScrollView)
        self.text_scroll_view.scroll_y = 0


if __name__ == "__main__":
    ChatApp().run()
