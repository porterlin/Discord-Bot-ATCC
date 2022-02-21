from turtle import right
import discord
from discord.ext import tasks
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import threading
import random
import os


client = discord.Client()
url = "empty"
text = []
code = ""
index = 0
num = 0
str1 = ""
tt = ""

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

def job():
    while True:
        print("in")
        account = 'testingtesting@gamil.com'
        password = 'portertest'

        #開啟瀏覽器視窗(Chrome)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        #driver = webdriver.Chrome('\chromedriver') #windows

        driver.get('https://www.facebook.com/')

        #帳號
        element = driver.find_element_by_id('email')
        element.send_keys(account)
        time.sleep(1)

        #密碼
        element = driver.find_element_by_id('pass')
        element.send_keys(password)
        time.sleep(1)

        button = driver.find_element_by_class_name('_42ft._4jy0._6lth._4jy6._4jy1.selected._51sy')
        button.click()
        time.sleep(7)

        driver.get('https://www.facebook.com/myatcc')

        time.sleep(5)
        element = driver.find_element_by_class_name('nqmvxvec.j83agx80.jnigpg78.cxgpxx05.dflh9lhu.sj5x9vvc.scb9dxdr.odw8uiq3')
        element.click()
        time.sleep(5)
        element = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.p7hjln8o.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.abiwlrkh.p8dawk7l.lzcic4wl.dwo3fsh8.rq0escxv.nhd2j8a9.j83agx80.btwxx1t3.pfnyh3mw.opuu4ng7.kj2yoqh6.kvgmc6g5.oygrvhab.l9j0dhe7.i1ao9s8h.du4w35lb.bp9cbjyn.cxgpxx05.dflh9lhu.sj5x9vvc.scb9dxdr')[2]
        element.click()
        time.sleep(5)
        element = driver.find_element_by_class_name('oajrlxb2.f1sip0of.hidtqoto.e70eycc3.lzcic4wl.b3i9ofy5.l6v480f0.maa8sdkg.s1tcr66n.aypy0576.beltcj47.p86d2i9g.aot14ch1.kzx2olss.rq0escxv.oo9gr5id.l94mrbxd.ekzkrbhg.cxgpxx05.d1544ag0.sj5x9vvc.tw6a2znq.k4urcfbm.o8yuz56k.duhwxc4d.bs68lrl8.f56r29tw.e16z4an2.ei4baabg.b4hei51z.ehryuci6.hzawbc8m.tv7at329')
        global url
        global code
        url = element.get_attribute('value')
        codecp = url[110:126]

        if codecp != code:
            code = codecp
            f = open('text.txt', 'w')
            f.write(code)
            f.close()
            url = 'https://www.facebook.com/165317680181335/posts/' + code
            driver.get(url)
            time.sleep(1)

            Soup = BeautifulSoup(driver.page_source, 'html.parser')
        
            global text
            #buf = Soup.find(class_ = 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q').find_all('div')
            buf = Soup.find(class_ = 'ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a').find_all('div')
            buf1 = []
            for i in range(len(buf)):
                buf1.append(buf[i].text)
            print(buf1)

            global str1
            str1 = ''
            str1 = ''.join(buf1)
            
            right = str1.index('】')
            text.append(str1[0:right+1]) #分離出標題
            str1 = str1[right+1:]

            global tt
            tt = str1

            global num
            num = 0
            while True:
                num+=20
                if num >= 120 or num >= len(str1):
                    text.append('...')
                    break

                text.append(tt[:num])
                tt = tt[num:]

            driver.get_screenshot_as_file("test.jpg")

            global index
            index = 1
            num = 0
        driver.close()
        delay_choices = [300, 350, 500, 320, 415, 390]  #延遲的秒數
        delay = random.choice(delay_choices)  #隨機選取秒數
        time.sleep(delay)


f = open('text.txt', 'r')
code = f.read()
f.close()
print(code)
t = threading.Thread(target = job)
t.start()
auto_send.start()
client.run('OTQ0MzIzODA4NDAyMjE0OTYz.Yg_8FA.H5TDRqYseu2_pxZr2AOl352xkMw') #ATCC
#client.run('OTQ0OTA0NTE1OTMxNDg4MzA3.YhIY6A.77R8o7R8qRvmiQDMcHPtyAyUseE') #DC Bot