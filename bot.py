
# coding: utf-8

# In[ ]:


import telebot 
import requests as re
import math as m
from telebot import types
from bs4 import BeautifulSoup


# In[ ]:


def ChistoEvents():
    from bs4 import BeautifulSoup
    import requests
    html_doc = requests.get("https://www.2do2go.ru/smr/events/today")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    
    events = (soup.find_all("div", class_="media-card_content"))
    data = (soup.find_all("div", class_="media-card_label"))
    ref = (soup.find_all("a", class_="media-card media-card__height__small media-card__width__small media-card__shadowed"))
    
    
    Ndata= (data[0].contents[0].string)
    Name = []
    Refs = []
    for i in range(0,len(events)-1):
        Name.append(events[i].contents[0].string)
        Refs.append("https://www.2do2go.ru"+ref[i].attrs['href'])
        #print(events[i].contents[0].string+" "+"https://www.2do2go.ru"+ref[1].attrs['href'])
    
    BigRefs = []
    BigNews = []
    
    html_doc1 = requests.get("https://bigvill.ru/news/")
    soup = BeautifulSoup(html_doc1.text, 'html.parser')
    a = (soup.find_all("ul", class_="news-list"))
    for i in range(1,len(a[0].contents),2):
        BigNews.append(a[0].contents[i].a.text)
        BigRefs.append(a[0].contents[i].a.attrs["href"])
    
    html_doc2 = requests.get("http://ceny-na.ru/city-samara-315/produkty/vse/")
    soup = BeautifulSoup(html_doc2.text, 'html.parser')
    a = (soup.find_all("tr", class_="cl1"))
    
    food = []
    
    for i in range(0,len(a)):
        food.append(a[i].contents[1].text+" "+a[i].contents[3].text)
    
    return Ndata, Name, Refs, BigNews, BigRefs, food


# In[ ]:


def ChistoRest():
    import requests
    html_doc = requests.get("https://www.tripadvisor.ru/Restaurants-g298521-Samara_Samara_Oblast_Volga_District.html")
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    a = (soup.find_all("a", class_="property_title"))
    
    rest = []
    rew = []
    
    for i in range(0,len(a)-1):
        rest.append(a[i].contents[0][1:-1])
    
    a = (soup.find_all("span", class_="reviewCount"))

    for i in range(0,len(a)-1):
        rew.append(a[i].contents[1].text[1:])
        
    a = (soup.find_all("a", class_="photo_link"))
    refs = []

    for i in range(0,len(a)):
        refs.append("https://www.tripadvisor.ru"+a[i].attrs["href"])
    
    return rest, rew, refs


# In[ ]:


def wth():
    r = re.get("http://api.openweathermap.org/data/2.5/weather?q=Samara,ru&appid=1e3e2028c3d7546072ea676312b338b3")
    j = r.json()
    temp = j["main"]["temp"]
    hum = j["main"]["humidity"]
    wind = j["wind"]["speed"]
    usp_p=(1/((abs(293-abs(temp)))*0.4+1))+(1/((wind)*0.2+1))+(1/(abs(10-hum)*0.2+1))/3
    usp_v=(1/((abs(293-abs(temp)))+1))+(1/((wind)+1))+(1/(abs(10-hum)*0.5+1))/3
    print(round(usp_v,4))
    temp_c=round(temp-273)
    return(temp,wind,hum,usp_p,usp_v)





def walk(message):
    temp,wind,hum,usp_p,usp_v=wth()
    bot.send_message(message.chat.id,("----погода на сегодня----\n температура:" +str(round((temp-273),3))+"\n влажность: "+str(hum)+"% \n ветер: "+str(wind)+" м/c \n вероятность успешной прогулки: " +str(usp_p) ))  
def movie():
    t = re.get("https://www.kinoafisha.info/movies/popular")
    soup = BeautifulSoup(t.text, 'html.parser')
    movie_name = (soup.find_all("a", class_="movie_name"))
    s="---ТОП ФИЛЬМОВ НА СЕГОДНЯ---\n"
    mas = []
    tex = []
    for i in range(1,11):

        tex.append(str(movie_name[i].string))
        mas.append(movie_name[i].get('href'))
    return tex, mas
def mo(message):
    tex,mas=movie()
    keyboard = types.InlineKeyboardMarkup()
    url_button_mas=[]
    for i in range(10):
        keyboard.add(types.InlineKeyboardButton(text=tex[i], url="https:"+mas[i]))
    bot.send_message(message.chat.id, "---------ТОП ФИЛЬМОВ---------", reply_markup=keyboard)
    
def news(message):
    global Ndata, Name, Refs, BigNews, BigRefs
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Большая Деревня')
    itembtn2 = types.KeyboardButton('2DO2GO')
    itembtn3 = types.KeyboardButton('/back')
    markup.add(itembtn1, itembtn2, itembtn3)    
    bot.send_message(message.chat.id, "----------ИЗДАНИЯ----------", reply_markup=markup)
def news_2DO(message):
    global Ndata, Name, Refs, BigNews, BigRefs
    keyboard = types.InlineKeyboardMarkup()
    url_button_mas=[]
    for i in range(len(Name)):
        keyboard.add(types.InlineKeyboardButton(text=Name[i], url=Refs[i]))
    bot.send_message(message.chat.id, "-----БЛИЖАЙШИЕ СОБЫТИЯ-----", reply_markup=keyboard)
def news_BW(message):
    global Ndata, Name, Refs, BigNews, BigRefs
    keyboard = types.InlineKeyboardMarkup()
    url_button_mas=[]
    for i in range(len(BigNews)):
        keyboard.add(types.InlineKeyboardButton(text=BigNews[i], url=BigRefs[i]))
    bot.send_message(message.chat.id, "-----БЛИЖАЙШИЕ СОБЫТИЯ-----", reply_markup=keyboard)
def rest_f(message):
    s = '---------Рестораны---------\n'
    for i in range(10):
        s+=str(i+1)+") "+rest[i]+"\n"
        s+=rew[i]+"\n"
    bot.send_message(message.chat.id, s)
    
        
        
        
        
        
        
        
        


# In[ ]:


bot = telebot.TeleBot("514602615:AAHicDqWnas-36f2p6h3ZQmoqJQUwd8SNzc")
Ndata, Name, Refs, BigNews, BigRefs, food=ChistoEvents()
rest, rew, refs= ChistoRest()
global Ndata, Name, Refs, BigNews, BigRefs
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('кино')
    itembtn2 = types.KeyboardButton('новости')
    itembtn3 = types.KeyboardButton('прогулка')
    itembtn4 = types.KeyboardButton('ужин')
    itembtn5 = types.KeyboardButton('места')
    markup.add(itembtn1, itembtn2, itembtn3,itembtn4, itembtn5)   
    bot.send_message(message.chat.id, "------------------------------------ \n  Вас приветствует SamarainfoBot  \n------------------------------------", reply_markup=markup)
@bot.message_handler(commands=['back'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('кино')
    itembtn2 = types.KeyboardButton('новости')
    itembtn3 = types.KeyboardButton('прогулка')
    itembtn4 = types.KeyboardButton('ужин')
    itembtn5 = types.KeyboardButton('места')
    markup.add(itembtn1, itembtn2, itembtn3,itembtn4, itembtn5)    
    bot.send_message(message.chat.id, "----------МЕНЮ----------", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def obr(message):
    if message.text=="прогулка":
        walk(message)
        bot.send_message(message.chat.id, str((message.chat.id)))
    if message.text=="кино":
        mo(message)
    if message.text=="новости":
        news(message)
    if message.text=="2DO2GO":
        news_2DO(message)
    if message.text=="Большая Деревня":
        news_BW(message)
    if message.text=="ужин":
        rest_f(message)
            
    
    
    
        
    
    
        
bot.polling()

