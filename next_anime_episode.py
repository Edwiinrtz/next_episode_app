from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

#chrome option
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('media.autoplay.default',0)
#chop = webdriver.FirefoxOptions()
#chop.add_argument('--disable-software-rasterizer')
#chop.add_argument("--enable-webgl")
#chop.add_argument('–-disable-gpu')

adBlock = 'C:/Users/edwin/next_episode/firefox/adblocker_ultimate-3.7.18.xpi'
#inicializando driver
#DRIVER_PATH = 'C:/Users/edwin/next_episode/chrome/chromedriver'
#driver = webdriver.Firefox(DRIVER_PATH)
driver = webdriver.Firefox(firefox_profile=firefox_profile)


driver.install_addon(adBlock,True)

driver.maximize_window()

"""sleep(5)
driver.switch_to.window(driver.window_handles[1])
driver.get('about:preferences#privacy')
driver.find_element(By.CSS_SELECTOR, '#autoplaySettingsButton').click()
driver.find_element(By.CSS_SELECTOR, 'menulist').value = 0 """
#driver.close()


#driver.close()

def next_episode(base_url,episode,option):
    
    driver.switch_to.window(driver.window_handles[0])
    driver.get(base_url+'-'+episode)
    video_options = driver.find_elements(By.CSS_SELECTOR, ".CapiTnv.nav.nav-pills li") #document.querySelectorAll('.CapiTnv.nav.nav-pills li')[1].click()
    video_options[int(option)].click() #cambiar opcion de reproduccion
    driver.switch_to.window(driver.window_handles[0])


    if(len(driver.find_elements(By.CSS_SELECTOR, '#video_box button'))>0):
        boton = driver.find_element(By.CSS_SELECTOR, '#video_box button')
        boton.click()

    video_url = driver.find_element(By.CSS_SELECTOR,'iframe').get_attribute("src")
    driver.get(video_url)

    """if(driver.find_element(By.CSS_SELECTOR,'#mainvideo')):
        driver.find_element(By.CSS_SELECTOR,'#mainvideo').click()"""
    sleep(3)
    #video_player = driver.find_element(By.CSS_SELECTOR,'.plyr__controls__item.plyr__control,video')

    print(driver.title)

    if('MEGA' in str(driver.title) or 'OK' in str(driver.title)):
        print('reproducciendo en mega o OK')
        driver.execute_script("document.querySelector('video,.vid-card_img').click();document.querySelector('video,.vid-card_img').requestFullscreen()")

    if('mail.ru' in str(driver.title)):
        sleep(5)
        driver.execute_script("document.querySelector('.b-video-controls__inside-play-button').click();document.querySelector('.b-video-controls__inside-play-button').requestFullscreen()")
        sleep(5)
        driver.execute_script("document.querySelector('b-video-html5__skip').click()")

    if('embedsito' in str(driver.current_url)):
        driver.execute_script("document.querySelector('.loading-container.faplbu').click();document.querySelector('.loading-container.faplbu').requestFullscreen()")

    else:
        driver.execute_script("document.querySelector('video,.plyr-container video,.vid-card_img,.loading-container.faplbu').play();document.querySelector('video,.plyr-container video,.vid-card_img,.loading-container.faplbu').requestFullscreen()")
    #video_player.play()
    #video_player.click()
    """
    
    """






#print(driver.current_url)

#Main process
#next_episode('https://www3.animeflv.net/ver/naruto-shippuden-hd-250')


##driver.execute_script("arguments[0].setAttribute('autoplay','true')", video_player)

#driver.execute_script("document.querySelector('video').load()")
#video_options = driver.execute_script('return document.querySelectorAll(".CapiTnv.nav.nav-pills li")')

#clicking on video options
"""video = video_options[1].click().get_attribute('src')





video_url = driver.execute_script('arguments[0].contentWindow.document.querySelector("video")',video)


driver.get(video_url.src)

video_player = driver.find_element(By.TAG_NAME,'[id="player"] video')

driver.execute_script('arguments[0].setAttribute("autoplay","true")',video_player)
"""