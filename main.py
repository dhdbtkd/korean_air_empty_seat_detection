import os
from web_driver_manager import WebDriverManager
from flight_search import FlightSearch
from telegram_notify import TelegramNotifier
from ui import FlightSearchUI
from dotenv import load_dotenv
import tkinter as tk
# .env 파일 로드
load_dotenv()

def start_search(month, day, web_driver_manager, ui):
    telegram_notifier = TelegramNotifier(os.getenv('TELEGRAM_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))
    telegram_notifier.send_message("탐색 시작")

    flight_search = FlightSearch(web_driver_manager.driver, "제주", "부산", ui, telegram_notifier)
    flight_search.search(month, day)
    flight_search.check_seat_availability()


    # UI 업데이트 작업 추가 등

def main():
    web_driver_manager = WebDriverManager(os.getenv('URL'))
    web_driver_manager.start()
    window = tk.Tk()
    ui = FlightSearchUI(window, start_search, web_driver_manager)
    window.mainloop()

if __name__ == "__main__":
    main()
