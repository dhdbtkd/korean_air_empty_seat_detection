import tkinter as tk
from tkinter import ttk

class FlightSearchUI:
    def __init__(self, master, search_callback, web_driver_manager):
        self.master = master
        self.search_callback = search_callback
        self.web_driver_manager = web_driver_manager
        self.master.title("Korean Air Price Chasing Tool")
        self.master.geometry("640x480")
        self.create_widgets()

    def create_widgets(self):
        # 월 목록
        month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        # 일 목록
        day_list = [i+1 for i in range(31)]
        
        # 상단 프레임
        frame_top = tk.Frame(self.master)
        frame_top.pack(side="top", pady=20)

        # 하단 프레임
        frame_bottom = tk.Frame(self.master)
        frame_bottom.pack(side="bottom", pady=20)

        # 월 선택 ComboBox
        self.month_combo = ttk.Combobox(frame_top, values=month_list)
        self.month_combo.set(month_list[0])

        # 일 선택 ComboBox
        self.day_combo = ttk.Combobox(frame_top, values=day_list)
        self.day_combo.set(day_list[0])

        # 레이블
        select_month_label = tk.Label(frame_top, text="월")
        select_day_label = tk.Label(frame_top, text="일")

        # 위젯 배치
        self.month_combo.pack(padx=10, side="left")
        select_month_label.pack(padx=10, side="left")
        self.day_combo.pack(padx=10, side="left")
        select_day_label.pack(padx=10, side="left")

        # "항공권 감시 시작" 버튼
        find_btn = tk.Button(self.master, text="항공권 감시 시작", command=self.on_search_start)
        find_btn.pack()

        # 조회 시간 레이블
        self.query_time = tk.StringVar()
        self.query_time.set("조회 시간")
        query_time_label = tk.Label(self.master, textvariable=self.query_time)
        query_time_label.pack(pady=20)

        # 결과 표시 Treeview
        self.search_result_tv = ttk.Treeview(frame_bottom, columns=(1, 2, 3, 4, 5), show="headings", height="12")
        self.search_result_tv.pack(expand=True, fill='y')

        # Treeview 열 설정
        self.search_result_tv.column(1, anchor=tk.CENTER, stretch=tk.NO, width=90)
        self.search_result_tv.column(2, anchor=tk.CENTER, stretch=tk.NO, width=90)
        self.search_result_tv.column(3, anchor=tk.CENTER, stretch=tk.NO, width=90)
        self.search_result_tv.column(4, anchor=tk.CENTER, stretch=tk.NO, width=90)
        self.search_result_tv.column(5, anchor=tk.CENTER, stretch=tk.NO, width=90)

        # Treeview 헤딩 설정
        self.search_result_tv.heading(1, text="시간")
        self.search_result_tv.heading(2, text="특가")
        self.search_result_tv.heading(3, text="할인")
        self.search_result_tv.heading(4, text="정상")
        self.search_result_tv.heading(5, text="프레스티지")

    def on_search_start(self):
        month = self.month_combo.get()
        day = self.day_combo.get()
        self.search_callback(month, day, self.web_driver_manager, self)
