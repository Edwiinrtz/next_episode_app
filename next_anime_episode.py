from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver import ActionChains
from dotenv import load_dotenv
load_dotenv()
import os

client = MongoClient(os.getenv('MONGO_URI_NE'))
db = client['mae']

#chrome option
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('media.autoplay.default',0)


adBlock = 'firefox/adblocker_ultimate-3.7.18.xpi'
driver = webdriver.Firefox()


driver.install_addon(adBlock,True)

driver.maximize_window()

driver.fullscreen_window()

player = ''
paused = False

selected_script = ""

def omitirOpening():
    driver.execute_script("document.querySelector('video,.vid_play').currentTime = document.querySelector('video,.vid_play').currentTime + 75")


def forward():
    driver.execute_script("document.querySelector('video,.vid_play').currentTime = document.querySelector('video,.vid_play').currentTime + 15")

def backward():
    driver.execute_script("document.querySelector('video,.vid_play').currentTime = document.querySelector('video,.vid_play').currentTime - 15")


def volumen(action):
    try:
        driver.execute_script("document.querySelector('video,.vid_play').volume =  document.querySelector('video,.vid_play').volume"+action+".1")
    except:
        print('valores no permitidos')

def pause():
    play()
    

def getting_image(anime):
    driver.get(f"https://www3.animeflv.net/anime/{anime}")
    sleep(2)
    try:
        url_img = driver.find_element(By.CSS_SELECTOR,'.SidebarA img').get_attribute('src')
    except:
        url_img = 'https://i.pinimg.com/564x/1a/84/35/1a8435b262f70dc441a52bf15a9c620d.jpg'
    print(url_img)

    return url_img


def play():
    global player, paused
    ActionChains(driver).click(player).perform()
    # selected_script = scripts_collection.find_one({"player":player_name})
    # print(f'selected script {selected_script}')
    # driver.execute_script(selected_script['script'])


def next_episode(base_url,episode,option):
    global player, selected_script
    
    driver.switch_to.window(driver.window_handles[0])
    driver.get(base_url+'-'+episode)
    video_options = driver.find_elements(By.CSS_SELECTOR, ".CapiTnv.nav.nav-pills li") #document.querySelectorAll('.CapiTnv.nav.nav-pills li')[1].click()
    video_options[int(option)].click() #cambiar opcion de reproduccion

    player_name = video_options[int(option)].get_attribute('data-original-title')
    print(f'player: {player_name}')

    driver.switch_to.window(driver.window_handles[0])




    if(len(driver.find_elements(By.CSS_SELECTOR, '#video_box button'))>0):
        boton = driver.find_element(By.CSS_SELECTOR, '#video_box button')
        boton.click()

    video_url = driver.find_element(By.CSS_SELECTOR,'iframe').get_attribute("src")
    driver.get(video_url)

    sleep(3)
    player = driver.find_element(By.CSS_SELECTOR, "video, .vid_play")    
    
    play()