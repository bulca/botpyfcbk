from bs4 import BeautifulSoup
import requests
from flask import Flask, request, redirect, render_template, request, session, abort
from pymessenger.bot import Bot
from pymessenger import Element, Button
from random import randint
import os, sys
import json
import urllib.parse
import csv

app = Flask(__name__)
bot = Bot (os.environ['ACCESS_TOKEN'])

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == os.environ['VERIFY_TOKEN']:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
    if request.method == 'POST':
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for x in messaging:
            recipient_id = x['sender']['id']

            if x.get('message'):
                if x['message'].get('text'):
                    from bs4 import BeautifulSoup
                    import requests
                    import json
                    import pyperclip

                    print('Sahibinden İlan Detay Botu : \n')

                    HEADERS     = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                    }
                    url         = "https://www.sahibinden.com/ilan/" + x['message'].get('text') + "/detay"
                    response    = requests.get(url, timeout=5, headers=HEADERS)

                    html        = response.text

                    soup = BeautifulSoup(html, 'html.parser')
                    detailsJson = soup.find("div", {"id": "gaPageViewTrackingJson"})['data-json']
                    phoneNumber = soup.find_all("span", {"class": "pretty-phone-part"})[0].string
                    details     = json.loads(detailsJson)
                    data        = details['customVars']

                    i = 0
                    #for item in details['customVars']:
                    #    print("[" + str(i) + "] = " +item['name'] + " : " + item['value'] + " \n")
                    #    i += 1

                    for item in details['customVars']:
                        if(item['name'] == 'Marka'):
                            marka = item['value']
                        if(item['name'] == 'Seri'):
                            model = item['value']
                        if(item['name'] == 'loc3'):
                            loc3 = item['value']
                        if(item['name'] == 'loc4'):
                            loc4 = item['value']
                        if(item['name'] == 'loc5'):
                            loc5 = item['value']
                        if(item['name'] == 'ilan_fiyat'):
                            fiyat = item['value']
                        if(item['name'] == 'Yıl'):
                            yil = item['value']
                        if(item['name'] == 'KM'):
                            km = item['value']
                        if(item['name'] == 'Vites'):
                            vites = item['value']
                        if(item['name'] == 'Yakıt'):
                            yakit = item['value']
                        if(item['name'] == 'Takas'):
                            takas = item['value']
                        if(item['name'] == 'Kimden'):
                            kimden = item['value']
                        i += 1

                    stri        = "{} Model {} {} {} {} {} {} KM'de \n🕹 Vites: {} \n⛽️ Yakıt: {} \n🚗 Takas: {} \n👤 Kimden: {} \n💵 Fiyat: {}\n📞 Telefon: {}\n#istanbulikincielaraç #istanbulikincielaraba #araba #ikincielaraba #istanbularaba #{} #{} #{}{}".format(yil,marka,model,loc3,loc4,loc5,km,vites,yakit,takas,kimden,fiyat,phoneNumber,marka,model,marka,model)
                    a = bot.send_text_message(recipient_id, stri)


                if x['message'].get('attachments'):
                    with open('./magic_csv/blackgirlmagicCSV.csv', 'r') as csvfile:
                        magiccsv = list(csv.reader(csvfile))
                    lengthofcsv = len(magiccsv)
                    position = randint(0, lengthofcsv)
                    response = magiccsv[position][0]
                    try:
                        a = bot.send_image_url(recipient_id, response)
                        if "error" in a:
                            b = bot.send_text_message(recipient_id, response)
                    except:
                        c = bot.send_text_message(recipient_id, response)
                    return "success"
            else:
                pass
    return "success"

@app.route("/privacypolicy", methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')

if __name__ == "__main__":
    app.run(port=6550)
