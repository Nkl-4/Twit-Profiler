from twitter_scraper import *
import requests, shutil, os
from PIL import Image
from fpdf import *
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time, re, io, string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


name = input("Enter name : ")

profile = Profile(name).to_dict()


response = requests.get(profile['profile_photo'], stream=True)
with open('img.jpeg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response    



pdf = FPDF()
pdf.add_page()
pdf.rect(5,5,200,287)
pdf.set_font("Arial", "B", size=15)
pdf.cell(200, 10, txt="Twitter Profiling", ln=1, align="C")


pdf.set_font("Arial", size=12)

pdf.image(name = 'img.jpeg', x=150, y=17, w=35, h=35)



for key, values in profile.items():
    if key not in ['profile_photo', 'banner_photo']:
        pdf.cell(200, 10, txt=f"{key:} : {values}", ln=1, align="L")
    
os.remove('img.jpeg')


fakecount=0
# if ref['biography']==None:
#     fakecount=fakecount+1
# if ref['followers_count']/ref['following_count']<0.4:
#     fakecount=fakecount+1
    
driver = webdriver.Chrome()
url = "https://tineye.com/"
driver.get(url)
time.sleep(2)

link = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/div/div/form[2]/div/input")

link.send_keys(profile['profile_photo'])
time.sleep(1)

driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/div/div/form[2]/input").click()
time.sleep(6)

result = driver.find_element_by_id("result_count")
# print(result.text)

pdf.cell(200, 10, txt=result.text+" for profile picture", ln=1, align="L")

driver.quit()
#print(fakecount)
    

def get_tweerts():
    arr = []
    for tweet in get_tweets(profile['username']):
        arr.append([tweet['text']])
    return arr
text= ""
finalword = []
texttweet=get_tweerts()
#print(texttweet)
l=len(texttweet)
for i in range(0,l):
    text=texttweet[i][0]+" "+text
lowerca = text.lower()
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
for x in lowerca:
    if x in punctuations:
        lowerca = lowerca.replace(x, " ")
tokenwords = word_tokenize(lowerca,"english")
finalword = []
emotionlist=[]
for g in tokenwords:
    if g not in stopwords.words('english'):
        finalword.append(g)
with open('emotion.txt', 'r') as file:
    for line in file:
        lineclear = line.replace('\n', '').replace(',', '').replace("'", '').strip()
        word,emotion=lineclear.split(':')
        if word in finalword:
            emotionlist.append(emotion)
co=Counter(emotionlist)

pdf.set_font("Arial", "B", size=12)

def sentiment_ana(senti_text):
    sc=SentimentIntensityAnalyzer().polarity_scores(senti_text)
    nega=sc['neg']
    post=sc['pos']
    if nega>post:
    	pdf.cell(200, 10, txt="Negative Emotion", ln=1, align="L")
    elif post>nega:
    	pdf.cell(200, 10, txt="Positive Emotion", ln=1, align="L")
    else:
    	pdf.cell(200, 10, txt="Neutral Emotion", ln=1, align="L")
sentiment_ana(lowerca)
fig,axl=plt.subplots()
axl.bar(co.keys(),co.values())
fig.autofmt_xdate()
plt.savefig("graph.png")
# plt.show()

pdf.image(name = 'graph.png', x=75, y=100, w=140, h=100)    

os.remove('graph.png')
# pdf.output(name+".pdf")  


Phone_Regex=r"""^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$"""
Url_Regex= r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
Email_Regex=r""" ([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+) """

final = []

pdf.add_page()
pdf.rect(5,5,200,287)
pdf.set_font("Arial", "B", size=15)
pdf.cell(200, 10, txt="Personally identifiable information", ln=1, align="C")

pdf.set_font("Arial", size=9)

for tweet in get_tweets(name):
    text=tweet['text']
    emails = re.findall(Email_Regex, text)
    url=re.findall(Url_Regex,text)
    ph=re.findall(Phone_Regex,text)
    if emails:
        for e in emails:
            final.append(e)
    elif url:
        for u in url:
            final.append(u)
    elif ph:
        for p in ph:
            final.append(p)
    else:
        pass
    
final_set = []
for f in final:
    if not(re.search('twitter', f) or re.search('youtu', f)):
        final_set.append(f)
        
for f in set(final_set):         
    pdf.cell(200, 10, txt=f, ln=1, align="L")
    
pdf.output(name+".pdf")      

