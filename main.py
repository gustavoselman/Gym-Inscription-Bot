from threading import Thread
import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import get_chrome_options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


class GymInscriptionBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        options = get_chrome_options(show_interface=True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.login()

    def login(self):
        """ Login in UPV Intranet """
        self.driver.get('https://intranet.upv.es/pls/soalu/est_intranet.NI_Portal_n?p_idioma=c')

        username_input = self.get_element_by_xpath("//form//table/tbody/tr[1]/td/input")
        username_input.send_keys(self.username)
        
        password_input = self.get_element_by_xpath("//form//table/tbody/tr[2]/td/input")
        password_input.send_keys(self.password + "\n")
        
        self.driver.implicitly_wait(10)
        self.driver.get('https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_tipoact=6690&p_codacti=21229&p_vista=intranet&p_idioma=c&p_solo_matricula_sn=&p_anc=filtro_actividad')
        self.driver.implicitly_wait(5)

    def get_element_by_xpath(self, xpath):
        """ Get the element by xpath, waiting 10 seconds to load """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, xpath)))
            return element
        except Exception as e:
            print(
                f"{e}: Doesn't exist the element with the xpath: {xpath}")
            return
        
    def click_on_class_by_day_and_schedule(self, day, schedule):
        """ Click the class by day and hour """
        try:
            # find the table containing the schedules
            table = self.get_element_by_xpath("(//table[@class='upv_listacolumnas'])[2]")

            # find the column corresponding to the day 
            day_row = table.find_element(By.XPATH, f".//tr[1]/th[contains(text(), '{day}')]")
            day_row_index = day_row.get_attribute("cellIndex")
            day_row_index = int(day_row_index) + 1

            # find the row corresponding to the schedule
            schedule_column = table.find_element(By.XPATH, f".//td[contains(text(), '{schedule}')]")
            schedule_column_index = schedule_column.find_element(By.XPATH, "..").get_attribute("rowIndex")

            print(f"Day row index (x): {day_row_index}")
            print(f"Schedule column index (y): {schedule_column_index}")

            # find the intersection cell
            cell = table.find_element(By.XPATH, f".//tr[{schedule_column_index}]/td[{day_row_index}]")
            print(f"Texto en celda ({day} | {schedule}))")
            if "Ya inscrito" in cell.text:
                print("Ya estás inscrito en esa clase \n")
                return
            else:
                print("No estás inscrito")
                print("Inscribiendo... \n")
                cell.click()
        except Exception as e:
            print(f"Error: {e}")
            return

def run_bot(username, password, day, schedule):
    bot = GymInscriptionBot(username, password)
    while True:
        bot.click_on_class_by_day_and_schedule(day, schedule)
        # bot.driver.refresh()
        bot.driver.get('https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_tipoact=6690&p_codacti=21229&p_vista=intranet&p_idioma=c&p_solo_matricula_sn=&p_anc=filtro_actividad')
        sleep(1)

if __name__ == "__main__":
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    classes = [
        ("Lunes", "16:30-17:30"),
        ("Martes", "14:30-15:30"),
        ("Miércoles", "15:30-16:30"),
        ("Jueves", "16:30-17:30"),
        ("Viernes", "13:30-14:30"),
    ]

    threads = []
    for day, schedule in classes:
        thread = Thread(target=run_bot, args=(username, password, day, schedule))
        threads.append(thread)
        thread.start()
