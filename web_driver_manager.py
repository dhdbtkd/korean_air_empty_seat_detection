from selenium import webdriver

class WebDriverManager:
    def __init__(self, url):
        self.url = url
        self.driver = None
    
    def start(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(0.5)
        self.driver.get(self.url)

    def close(self):
        if self.driver:
            self.driver.quit()