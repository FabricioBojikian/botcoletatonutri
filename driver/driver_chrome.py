import sys
import os
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
sys.path.insert(0, os.path.abspath(os.curdir))
from config.system import *
from driver.driver_abstract import DriverAbstract

class DriverChrome(DriverAbstract):

    def __init__(self, visible: bool) -> None:
        super().__init__(visible)
    
    def __str__(self) -> str:
        return f'Visible: {self._visible}'
    
    def initialize(self):
        self._service = Service(ChromeDriverManager().install())
        self._options = webdriver.ChromeOptions()
        return 

    def agents(self, options):
        agent = super().DRIVER_AGENTS[random.randint(0, len(super().DRIVER_AGENTS)-1)]
        options.add_argument('--user-agent=' + agent)
        options.add_argument("start-maximized")
        # options.add_argument("--start-fullscreen")

    def visible(self, options):
        if not self._visible:
            options.add_argument('--headless')
            options.add_argument('--disable-notifications')
            options.add_argument('--no-sandbox')
            options.add_argument('--mute-audio')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")  # Apenas necessário para algumas versões do Chrome
            options.add_argument("--window-size=1920x1080")
            # Configurando para desativar os logs de console
            options.add_argument("--log-level=3")  # Desativa logs de erro, aviso e informação
            options.add_argument("--silent")  # Modo silencioso
            
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.default_content_setting_values.popups": 2,
                "profile.default_content_setting_values.automatic_downloads": 1
            }
            
            options.add_experimental_option("prefs", prefs)
    
    def config(self):
        self.initialize()
        self.agents(self._options)
        self.visible(self._options)
    
    def start(self):
        self.config()
        return webdriver.Chrome(service=self._service, options=self._options)