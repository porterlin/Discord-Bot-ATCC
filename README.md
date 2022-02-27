# Discord-Bot-ATCC

此專案利用 discord.py, Selenium, BeautifulSoup4, Heroku 來實現爬取 ATCC 粉絲專頁最新貼文，並透過 Discord 機器人自動傳送通知

由於 Facebook 爬蟲限制許多，所以先使用 Selenium 模擬人類登入，到達指定頁面後再透過 BeautifulSoup4 將 Html 提取出來分析，取出我們要的資訊後再由 Discord Bot 將收集的資訊傳送至特定頻道，Heroku 則讓我們可以 24 小時運作程式碼

## 使用前設定

``` python=16
account = '你的FB帳號'
password = '你的FB密碼'
```

填入你的 FB 帳號密碼，建議新創一個帳號，避免被鎖帳

```python=31
channel = await client.fetch_channel('要傳送到的頻道id(channel ID)')
```

填入 Channel ID，在 Discord 的頻道上按滑鼠右鍵可複製 ID

```python=209
client.run('你的Bot Token')
```

填入機器人的 Token，需前往 Discord Developer 頁面查詢



請先至 https://chromedriver.chromium.org/ 下載對應版本的 chromedriver

```python=61
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless") #無頭模式
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

driver = webdriver.Chrome('D:\chromedriver') #windows
```

61 至 68 行是為了放在 Heroku 的 Linux 環境運行需要的，Windows 端只要將下載好的chromedriver 指定過去就可以了

在 Heroku 運行 chromedriver 可以參考此影片 https://youtu.be/Ven-pqwk3ec

## 介紹

由於程式分為 Discord bot 部分以及網頁爬蟲，我們使用多執行緒的方法讓子執行緒去處理爬蟲，父執行緒去跑 Discord Bot

爬蟲的部分不多做贅述，將我們需要的資訊分離出來就好。下一次爬蟲的間隔時間隨機選擇，減少被偵測到的機會



這邊我根據 ATCC 粉絲專頁的發文架構，擷取出標題、內文、連結以及螢幕截圖當作預覽畫面，發送的結果如下圖

![1](https://user-images.githubusercontent.com/65625447/155887923-b435660c-ceb4-4011-abda-f43b66c999a8.jpg)

## 其他

`.fonts` 資料夾存放中文字型，如果沒放的話，在 Heroku 上的螢幕截圖中文字會變亂碼

`requirements.txt` 放需要安裝的檔案給 Heroku 知道，可以透過終端機輸入`pip freeze > requirements.txt` 自動產生
