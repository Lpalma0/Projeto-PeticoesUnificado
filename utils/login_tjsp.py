import os
from typing import Dict
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests





class ChromeDriver:
    def __init__(self, prefs: Dict[str, str]) -> None:
        
        user = os.getenv('USERNAME')
        self.options = Options()
        caminho_extensao = f'C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Extensions/bbafmabaelnnkondpfpjmdklbmfnbmol'
        #self.options.add_argument(f"--load-extension={caminho_extensao}")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--enable-automation')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--kiosk-printing')
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument(f"user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
        self.options.add_experimental_option('prefs', {
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        })
        self.service = ChromeService(
            executable_path=ChromeDriverManager().install()
        )

    @property
    def path_folder_temp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while not current_dir.endswith('src'):
            current_dir = os.path.dirname(current_dir)

        self.path_temp = os.path.join(current_dir, 'temp')
        if not os.path.exists(self.path_temp):
            os.makedirs(self.path_temp)
        return self.path_temp

    def start_driver(self) -> tuple[WebDriver, WebDriverWait[WebDriver]]:
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 15)
        return driver, wait


class LoginTJ:
    def __init__(self) -> None:
        prefs = {
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'profile.default_content_settings.popups': 0,
            'profile.content_settings.pattern_pairs.*.multiple-automatic-downloads': 1,  # noqa: E501
            'profile.default_content_setting_values.automatic_downloads': 1,
            'profile.content_settings.exceptions.automatic_downloads.*.setting': 1,  # noqa: E501
            'download.extensions_to_open': '',
            'safebrowsing.enabled': True,
        }

        self._driver, self._wait = ChromeDriver(prefs).start_driver()

    def login(self) :
     
        self._driver.maximize_window()
        self._driver.get("https://esaj.tjsp.jus.br/sajcas/login?service=https%3A%2F%2Fesaj.tjsp.jus.br%2Fesaj%2Fj_spring_cas_security_check")
        sleep(2)
        try:
            
            cont = 0
            while cont <3:
                try:
                    aba_certificado = self._wait.until(EC.presence_of_element_located((By.ID, 'linkAbaCertificado')))
                    aba_certificado.click()
                    sleep(2)
                    submit = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitCertificado"]')))
                    sleep(20)
                    submit.click()
                    
                    break
                except:
                    sleep(4)
                finally:
                    cont +=1                
        except:
            pass
        sleep(30)
        self._driver.get("https://esaj.tjsp.jus.br/cpopg/open.do")
        

        cookies = self._driver.get_cookies()
        
        # Converter os cookies para um formato compatível com requests
        session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        session = requests.Session()
        session.cookies.update(session_cookies)
    
        # Usar a sessão requests para fazer uma requisição com os cookies
        response = session.get("https://esaj.tjsp.jus.br/cpopg/open.do")
    
        return session
