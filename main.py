import discord
from discord.ext import tasks
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import threading
import random
import os


client = discord.Client()
url = "empty"
text = []
code = ""
index = 0
#month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#account = 'testingtestinglin@gmail.com'
account = 'porterwp.tw@gmail.com'
password = 'portertest'

@client.event
async def on_ready():
    print('Bot is now online and ready to roll')

    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name="ATCC FB粉專")
    await client.change_presence(status= status_w, activity=activity_w)

@tasks.loop(seconds= 10)
async def auto_send():
    global index
    if index == 1:
        channel = await client.fetch_channel('944300842910093392') #ATCC
        #channel = await client.fetch_channel('944904236012023860') #DC Bot
        temp = ""
        print('-------------------------------')
        print(text)
        for i in range(len(text)):
            if i == 0:
                continue

            temp += text[i]
            if i == len(text) - 1:
                break
            temp += '\n'
            
        embed = discord.Embed(title=text[0], url=url, description=temp, color=0xffed24)
        file = discord.File("test.jpg", filename="image.png")
        embed.set_image(url="attachment://image.png")
        str = '標題: ' + text[0]
        await channel.send(str)
        str = '連結: <' + url + '>'
        await channel.send(str)
        await channel.send(file=file,embed=embed)
        index = 0

def cal(llist): #llist=['天', '時', '分', '秒']
    temp = int(llist[0]) * 24 * 60 * 60 + int(llist[1]) * 60 * 60 + int(llist[2]) * 60 + int(llist[3])
    return str(temp)

def job():
    global account
    global password
    while True:
        #開啟瀏覽器視窗(Chrome)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        #driver = webdriver.Chrome('D:\chromedriver', chrome_options=chrome_options) #windows

        driver.get('https://www.facebook.com/')

        #帳號
        element = driver.find_element_by_id('email')
        element.send_keys(account)
        time.sleep(1)

        #密碼
        element = driver.find_element_by_id('pass')
        element.send_keys(password)
        time.sleep(1)

        element.submit()

        # button = driver.find_element_by_class_name('_42ft._4jy0._6lth._4jy6._4jy1.selected._51sy')
        # button.click()
        time.sleep(7)

        driver.get('https://www.facebook.com/myatcc')

        time.sleep(5)

        for i in range(3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
        
        Soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(7)
        timess = Soup.find_all('a', class_ = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw') #找出所有連結
        print(timess)

        #global month#
        times = []
        for i in range(len(timess)):
            times.append(timess[i].get('aria-label'))

        for i in range(len(times)): #轉換成秒
            if '月' in times[i] or 'at' in times[i]:
                continue

            ll = ['0', '0', '0', '0']
            if '分鐘' in times[i]:
                p = times[i].index('分')
                part = times[i][:p]
                ll[2] = part
                times[i] = cal(ll)
            elif 'm' in times[i]:
                p = times[i].index('m')
                part = times[i][:p-1]
                ll[2] = part
                times[i] = cal(ll)
            elif '小時' in times[i]:
                p = times[i].index('小')
                part = times[i][:p]
                ll[1] = part
                times[i] = cal(ll)
            elif 'h' in times[i]:
                p = times[i].index('h')
                part = times[i][:p-1]
                ll[1] = part
                times[i] = cal(ll)
            elif '天' in times[i]:
                p = times[i].index('天')
                part = times[i][:p]
                ll[0] = part
                times[i] = cal(ll)
            elif 'd' in times[i]:
                p = times[i].index('d')
                part = times[i][:p-1]
                ll[0] = part
                times[i] = cal(ll)
        
        print(times)

        mini = 1000000
        for i in range(len(times)): #找出最近的發文時間
            if '月' in times[i] or 'at' in times[i]:
                continue
            
            if i == 0:
                if int(times[i]) < mini:
                    mini = i
            else:
                if mini == 1000000:
                    mini = i
                if int(times[i]) < int(times[mini]):
                    mini = i
        
        print(mini)

        global url
        global code
        url = timess[mini].get('href')
        jj = url.index('?')
        codecp = url[:jj]
        url = codecp

        print(codecp)

        if codecp != code:
            code = codecp
            driver.get(codecp)
            time.sleep(5)
    
            driver.get_screenshot_as_file("test.jpg")
            
            for i in range(3):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(5)

            Soup = BeautifulSoup(driver.page_source, 'html.parser')
        
            global text
            text = []
            #buft = Soup.find_all('div', class_ = 'ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a') #找出所有貼文的文章存成list # kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql
            buft = Soup.findAll('div', {'class':['ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a', 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']})
            print(len(buft))
            buf = buft[0].find_all('div')
            
            buf1 = []
            for i in range(len(buf)):
                buf1.append(buf[i].text)
            print(buf1)

            str1 = ''
            str1 = ''.join(buf1)
            
            right1 = str1.index('】')
            text.append(str1[0:right1+1]) #分離出標題

            tt = str1[right1+1:]

            num = 0
            while True:
                num+=20
                if num >= 120 or num >= len(str1):
                    text.append('...')
                    break

                text.append(tt[:num])
                tt = tt[num:]

            global index
            index = 1
            num = 0
        driver.quit()
        delay_choices = [300, 350, 500, 320, 415, 390]  #延遲的秒數
        delay = random.choice(delay_choices)  #隨機選取秒數
        time.sleep(delay)

t = threading.Thread(target = job)
t.start()
auto_send.start()
client.run('OTQ0MzIzODA4NDAyMjE0OTYz.Yg_8FA.H5TDRqYseu2_pxZr2AOl352xkMw') #ATCC
#client.run('OTQ0OTA0NTE1OTMxNDg4MzA3.YhIY6A.77R8o7R8qRvmiQDMcHPtyAyUseE') #DC Bot