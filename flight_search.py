import time
import threading
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class FlightSearch:
    def __init__(self, driver, departure, destination, ui, telegram_notifier):
        self.ui = ui
        self.driver = driver
        self.departure = departure
        self.destination = destination
        self.telegram_notifier = telegram_notifier

    def search(self, month, day):
        # 항공권 검색 로직
        self._start_webdriver()
        self._search_start(month, day)
    
    def _start_webdriver(self):
        url = "https://www.koreanair.com/booking/search"
        self.driver.get(url)
        self.driver.implicitly_wait(0.5)  # seconds

    def _search_start(self, month, day):
        # 출발지 및 목적지 입력
        self._select_departure()
        self._select_destination()
        self._select_date(month, day)
        self._select_seat_class()
        self._submit_search()

    def _select_departure(self):
        from_button = self.driver.find_element(By.CSS_SELECTOR, '.-from')
        from_button.click()
        time.sleep(1)
        from_input = self.driver.find_element(By.XPATH, '/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input')
        from_input.send_keys(self.departure)
        from_input.send_keys(Keys.ENTER)

    def _select_destination(self):
        to_button = self.driver.find_element(By.CSS_SELECTOR, '.-to')
        to_button.click()
        time.sleep(0.5)
        from_input = self.driver.find_element(By.XPATH, '/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input')
        from_input.send_keys(self.destination)
        from_input.send_keys(Keys.ENTER)

    def _select_date(self, month, day):
        data_picker_btn = self.driver.find_element(By.XPATH,'/html/body/app-root/div/ke-search/ke-basic-layout/div[1]/div/div[1]/div/div[2]/div/ke-search-ow-rt/div[1]/div[1]/div/div/div[2]/div[1]/button')
        data_picker_btn.click()
        time.sleep(0.5)
        oneway_trip = self.driver.find_element(By.XPATH,'/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div/div[2]/div/label')
        oneway_trip.click()

        month_div = self.driver.find_element(By.CSS_SELECTOR, '#month2025' + month)
        data_picker_table = month_div.find_element(By.CSS_SELECTOR, '.datepicker__table')
        day_span = data_picker_table.find_element(By.XPATH, ".//span[text()='" + day + "']")
        day_span.click()

        data_picker_ok_btn = self.driver.find_element(By.XPATH, '/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[2]/div/div/div[3]/button')
        data_picker_ok_btn.click()

    def _select_seat_class(self):
        seat_class_btn = self.driver.find_element(By.XPATH, '/html/body/app-root/div/ke-search/ke-basic-layout/div[1]/div/div[1]/div/div[2]/div/ke-search-ow-rt/div[1]/div[3]/div[2]/div/button')
        seat_class_btn.click()
        
        all_class_btn = self.driver.find_element(By.XPATH, '/html/body/ke-dynamic-modal/div/ke-upgrade-seat-modal/div/div/div/div[1]/div[1]/div/label')
        all_class_btn.click()
        
        seat_class_submit_btn = self.driver.find_element(By.XPATH, '/html/body/ke-dynamic-modal/div/ke-upgrade-seat-modal/div/div/div/div[2]/button')
        seat_class_submit_btn.click()

    def _submit_search(self):
        submit_btn = self.driver.find_element(By.XPATH, '/html/body/app-root/div/ke-search/ke-basic-layout/div[1]/div/div[1]/div/div[2]/div/ke-search-ow-rt/button')
        submit_btn.click()

    def check_seat_availability(self):
        # 좌석 잔여 여부 확인 로직
        self._query_price("first")
        is_finish = False
        while not is_finish:
            self.ui.master.after(30000, self._query_price("notfirst"))
            # time.sleep(30)  # Wait before the next query
            # self._query_price("notfirst")

    def _query_price(self, query_type):
        if query_type != "first":
            self.driver.refresh()

        try:
            self.ui.query_time.set('조회 시간 :'+ datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초"))
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/ke-select-flight-revenue-cont/ke-select-flight-revenue-pres/ke-basic-layout/div[1]/div/div/ke-revenue-payment-widget/div/div/div/div[2]/button[2]"))
            )
            ul = self.driver.find_element(By.XPATH, "/html/body/app-root/div/ke-select-flight-revenue-cont/ke-select-flight-revenue-pres/ke-basic-layout/div[1]/div/div/ke-select-flight-revenue-domestic-cont/ke-select-flight-revenue-domestic-pres/div/div/div[2]/div/ul")
            lis = ul.find_elements(By.CSS_SELECTOR, ".flight-n__item")
            print(len(lis))
            timeOrder = 0
            for i, li in enumerate(lis):
                data = list()
                flight_time = li.find_element(By.CSS_SELECTOR, ".flight-n__time").get_attribute('innerText')
                data.append(flight_time)
                prices = li.find_elements(By.CSS_SELECTOR, "div.flight-n__cabin-wrap")
                for price in prices:
                    price_name = price.find_element(By.CSS_SELECTOR, ".flight-n__cabin-name").get_attribute('innerText')
                    sold_out = price.find_elements(By.CSS_SELECTOR, ".flight-n__disabled")
                    if sold_out:
                        data.append("매진")
                        print(f"{flight_time}:{price_name} - 매진")
                        continue

                    seat_remaining = price.find_elements(By.CSS_SELECTOR, ".flight-n__remaining-seat")
                    if seat_remaining:
                        seat_count = seat_remaining[0].get_attribute('innerText')
                        data.append(seat_count)
                        print(f"{flight_time}:{price_name} - 잔여 좌석: {seat_count}")

                        #시간 순서 4번쨰 이상일 경우에 알림 보냄
                        # if timeOrder >= 7:
                        #마지막 시간 대일 경우에만 알림을 보냄
                        if i == len(lis) - 1:
                            self.telegram_notifier.send_message(self.departure+"->"+self.destination+ " : " + flight_time +"항공권 잔여 좌석 발견")
                # 결과를 UI에 업데이트
                self.ui.search_result_tv.insert('', 'end', values=data)
                timeOrder += 1
            self.ui.master.update()
        except Exception as error:
            print(error)
