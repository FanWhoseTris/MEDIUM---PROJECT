import speech_recognition as sr
import pyttsx3
from chat import get_response
import subprocess
import os

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Mời sếp nói, em đang lắng nghe...")
        recognizer.adjust_for_ambient_noise(source)  # Cân chỉnh âm thanh nền
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

    return ""


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Tốc độ nói
    engine.setProperty('volume', 0.9)  # Âm lượng
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Xin chào sếp,chúc sếp có một ngày tuyệt vời.")
    while True:
        input_text = recognize_speech()
        speak(input_text)
        if "dừng lại" in input_text.lower():
            speak("Dừng lại.Chào Tạm Biệt Sếp!")
            break
        elif "danh sách công việc" in input_text.lower():
            speak("Đang mở tu đu lít")
            todolist_exe_path = os.path.join("WorkWise", "todolist.exe")
            subprocess.Popen([todolist_exe_path])
        elif input_text.lower() == "":
            speak("Sếp nói gì em nghe không rõ.Sếp nói lại đi.")
            pass
        else:
            response_text = f"{get_response(input_text)}\n\n"
            speak(response_text)
