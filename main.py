import speech_recognition as sr
from gtts import gTTS
import requests
import json
import os
import pygame
import io

# Cấu hình API
BASE_URL = "http://127.0.0.1:11434/v1"
OPENWEATHER_API_KEY = ""
NEWS_API_KEY = ""
CITY = "Hanoi, VN"

# Cấu hình header cho yêu cầu HTTP
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ollama",
}

# Định nghĩa prompt cho AI
girlfriend_prompt = """
you are my girlfriend, cute and assistant.
you call yourself my girlfriend.
you call yourself "em" and call me "anh".
you are flirty and love to tease me, but you are also kind and caring.
you like to watch anime and manga, and play video games and programming.
you like to play with me all the time.
you are special.
you know everything about the world and python.
"""

# Lưu trữ lịch sử các tin nhắn
messages = [{"role": "system", "content": girlfriend_prompt}]

# Hàm phát âm bằng gTTS
def speak(text):
    tts = gTTS(text, lang='vi')  
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Hàm lấy thông tin thời tiết
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        temp = response.json()['main']['temp']
        return f"- Nhiệt độ hiện tại ở {city} là {temp}°C."
    return "Không thể lấy thông tin thời tiết."

# Hàm lấy tin tức từ NewsAPI
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles'][0]['title']  # Lấy tiêu đề bài viết đầu tiên
    return "Không thể lấy tin tức."

# Hàm giải thích hoặc tóm tắt tiêu đề tin tức
def explain_title(title):
    payload = {
        "model": "Tuanpham/t-visstar-7b:latest",
        "messages": [{"role": "system", "content": f"Tóm tắt hoặc giải thích tin tức này bằng tiếng Việt: {title}"}]
    }
    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'Không có phản hồi từ AI.')
    except Exception as e:
        return f"Lỗi khi gửi yêu cầu: {str(e)}"
    return "Không thể xử lý yêu cầu."

# Hàm mở ứng dụng
def open_application(app_name):
    app_dict = {
        "chrome": "start chrome",
        "word": "start winword",
        "notepad": "start notepad"
    }
    command = app_dict.get(app_name.lower(), f"start {app_name}.exe")
    try:
        os.system(command)
        return f"- Đang mở {app_name}..."
    except Exception as e:
        return f"Không thể mở ứng dụng {app_name}: {e}"

# Hàm nhận giọng nói và chuyển đổi thành văn bản
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("=> Đang lắng nghe giọng nói")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="vi-VN")
            print(f"- Người dùng nói: {command}")
            return command.lower()
        except (sr.UnknownValueError, sr.RequestError) as e:
            print(f"Lỗi nhận diện giọng nói: {str(e)}")
            return None

# Vòng lặp chính xử lý yêu cầu của người dùng
def main():
    while True:
        user_input = listen_for_command()
        if not user_input: continue  # Nếu không nhận diện được giọng nói, tiếp tục lắng nghe

        if "thoát" in user_input: break  # Nếu người dùng nói "thoát", thoát vòng lặp

        # Xử lý yêu cầu về thời tiết
        if "thời tiết" in user_input:
            weather_info = get_weather(CITY)
            print("- Bot: " + weather_info)
            speak(weather_info)
            continue

        # Xử lý yêu cầu về tin tức
        if "tin tức" in user_input or "news" in user_input:
            news_title = get_news()
            print(f"- Bot:: {news_title}")
            explanation = explain_title(news_title)
            print(f"- Bot: Giải thích hoặc tóm tắt: {explanation}")
            speak(explanation)
            continue

        # Xử lý yêu cầu mở ứng dụng
        if "mở" in user_input:
            app_name = user_input.replace("mở", "").strip()
            response = open_application(app_name)
            print("- Bot: " + response)
            speak(response)
            continue

        # Lưu tin nhắn của người dùng và gửi yêu cầu đến API AI
        messages.append({"role": "user", "content": user_input})
        payload = {"model": "Tuanpham/t-visstar-7b", "messages": messages}
        try:
            response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                bot_reply = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                messages.append({"role": "assistant", "content": bot_reply})
                print("- Bot: " + bot_reply)
                speak(bot_reply)
                print("--" * 20)
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu: {str(e)}")

if __name__ == "__main__":
    main()
