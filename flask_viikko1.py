#!/wwwhome/home/oma_tunnus/public_html/cgi-bin/ties4080//venv/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import io
import random
import urllib.request
import simplejson as json
app = Flask(__name__)

#Testi ryhma
kolmeRraa = {
      "nimi": "Hello123",
      "jasenet": ["Riku" 
        "Repo",
        "Roisto"
      ],
      "id": 609609609609609,
      "leimaustapa": [0,1],
      "rastit": [{"aika":"2077-03-18", "rasti":"609"}, {"aika":"2077-03-20", "rasti":"608"}, {"aika":"2077-03-22", "rasti":"607"}]
}

muoto = "nimi, jasenet, id, leimaustapa, rastit"


def jarjestaJoukkueet():
    nimet = []
    # Kerätään ryhmien nimet uuteen listaan
    for sarjaNimi in JSON_OBJECT["sarjat"]:
        for joukkueet in sarjaNimi["joukkueet"]:
            nimet.append(joukkueet["nimi"])

    # Järjestetään ryhmät aakkosittain
    nimetPlain = ""
    nimet.sort(key=str.lower)
    for nimi in nimet:
        nimetPlain += nimi + "\n"
    return nimetPlain


#Generoi ID:n
def generateiID():
    #Luodaan uusi 16 numeroinen ID
    id = random.randint(10**15,(10**16)-1)
    #Tarkistetaan, etta ID ei ole jo olemassa
    for jsonSarja in JSON_OBJECT["sarjat"]:
        for jsonJoukkue in jsonSarja["joukkueet"]:
            #Jos sama ID loytyy ajetaan aliohjelma uusiksi
            if jsonJoukkue["id"] == id:
                generateiID()
    #Palautetaan uusi ID
    return id


#Lisataan joukkue, annetaan sarja str ja joukkue arr
def lisaaJoukkue(sarja, joukkue):

    #Tarkistetaan joukkueen muoto
    for tar in joukkue:
        #Tarkistetaan joukkuuen muoto ja avainten oikea maara
        if(muoto.__contains__(tar) and len(joukkue) == 5):
            continue
        else: 
            print("Joukkueen muoto on vaarin")
            return

    #Tarkistetaan, että joukkue ei ole olemassa samalla nimella
    for jsonSarja in JSON_OBJECT["sarjat"]:
        # Tarkistetaan etta joukkue ei ole olemassa samalla nimella
        for jsonJoukkue in jsonSarja["joukkueet"]:
            #Poistetaan if lauseessa turhat tyhjät välit edestä ja lopusta
            #Muutetaan molemmat nimet pieniksi kirjaimiksi ja verrataan ovatko nimet samat
            #Jos nimet samat palautetaan funktio
            if " ".lower().join(str(joukkue["nimi"]).split()) == " ".lower().join(str(jsonJoukkue["nimi"]).split()):
                return

    #Annetaan uusi ID joukkueelle
    joukkue["id"] = generateiID()

    #Lisataan joukkue
    for jsonSarja in JSON_OBJECT["sarjat"]:
        if(jsonSarja["nimi"] == sarja):
            jsonSarja["joukkueet"].append(joukkue)
            #Tallenetaan uusi versio data.json
            generateData()
            return
    
    return

#Kerataan kaikki rasti koodit
def palautaKoodit():
    rastiKoodit = ""
    for koodit in JSON_OBJECT["rastit"]:
        #Tarkistetaan etta koodin ensimmainen merkki on numero (int)
        if koodit["koodi"][0].isdigit():
            #Lisataan koodi merkkijonoon ja peraan ";"
            rastiKoodit += koodit["koodi"] + ";"
    #Palautetaan koodit, mutta poistetaan viimeinen merkki, joka on ";"
    return rastiKoodit[:-1]

def generateData():
    with open("data.json", "w") as f:
        json.dump(JSON_OBJECT,f)





###################TASO3#######################
def poistaJoukkue(sarja, joukkueNimi):
    # Luodaan index sarja for-looppeja varten
    index = 0
    #Kaydaan ensiksi kaikki sarjat lapi
    for jsonSarja in JSON_OBJECT["sarjat"]:
        #Tarkistetaan onko oikea sarja
        if JSON_OBJECT["sarjat"][index]["nimi"] == sarja:
            #Indexi sarjassa olevaa joukkuetta varten
            itemIndex = 0
            #Kaydaan kaikki sarjan joukkueet lapi
            for jsonJoukkue in jsonSarja["joukkueet"]:
                # Poistetaan if lauseessa turhat tyhjät välit edestä ja lopusta
                # Muutetaan molemmat nimet pieniksi kirjaimiksi ja verrataan ovatko nimet samat
                # Jatketaan jos nimi joukkueessa on sama kuin joukkueNimi
                #Jos ei toteudu kasvatetaan itemIdexia yhdella
                if " ".lower().join(str(joukkueNimi).split()) == " ".lower().join(str(jsonJoukkue["nimi"]).split()):
                    # poistetaan joukkue JSON_OBJECT:sta
                    del JSON_OBJECT["sarjat"][index]["joukkueet"][itemIndex]
                    generateData()
                    return
                itemIndex += 1
        index += 1
    generateData()
    return

#Ladataan olemassa oleva data.json tiedosto
def loadJson():
    #Tehdaan JSON_OBJECT:sta globaali muuttuja
    global JSON_OBJECT
    tiedosto = io.open("data.json", encoding="UTF-8")
    #Sijoitetaan data.json tiedot JSON_OBJECT:iin
    JSON_OBJECT = json.load(tiedosto)

#Ladataan nettisivulta oleva data.json tiedosto
def loadUrl():
    #Tehdaan JSON_OBJECT:sta globaali muuttuja
    global JSON_OBJECT
    #Haetaan json tiedosto
    req = urllib.request.urlopen("http://hazor.eu.pythonanywhere.com/2021/data2021.json")
    data = req.read()

    encoding = req.info().get_content_charset("UTF-8")
    JSON_OBJECT = json.loads(data.decode(encoding))

#Aliohjelma etsii id:n perusteella vastaavan rastin id:n ja silla id:lla olevan rastin koodin
def idPisteet(id):
    #Kaydaan kaikki rastit lapi
    for koodit in JSON_OBJECT["rastit"]:
        #Jos JSON_OBJECT:ssa oleva id vastaa annettua id:a jatketaan
        if str(koodit["id"]) == str(id):
            #Tarkistetaan, etta id:lla loydetyn rastin koodin ensimmainen merkki on numero
            #ja etta koodi on ylipaataan olemassa
            if koodit["koodi"][0].isdigit() and koodit["koodi"] != None:
                #Palautetaan koodin ensimmainen merkki
                return int(koodit["koodi"][0])
            else:
            #Muuten palautetaan 0
                return 0
    return 0


def tulostaPisteet():
    #Alustetaan palutus teksti
    returnTxt = ""
    #Tehdaan lista joukkueet johon tallennetaan kaikki joukkueet
    joukkueet = []
    #Kaydaan jokainen sarjalapi ja etsitaan sarjojen joukkueet
    for jsonSarja in JSON_OBJECT["sarjat"]:
        for jsonJoukkue in jsonSarja["joukkueet"]:
            #Tehdaan pisteet dict johon tallennetaan joukkueen nimi, pisteet ja jasenet
            pisteet = {
                "nimi": "",
                "pisteet": 0,
                "jasenet": []
            }
            #Sijoitetaan ensiksi joukkueen nimi pisteet dict
            pisteet["nimi"] = jsonJoukkue["nimi"]
            #Luodaan tyhjajoukko rastit johon tallennetaan kaikki joukkuueen rastit
            rastit = []
            #Kaydaan joukkuuen merkkaamat rastit
            for jsonPisteet in jsonJoukkue["rastit"]:
                #Jos joukkuueen merkkaama rasti ei loydy rastit joukosta jatketaan pisteen laskemiseen
               if rastit.__contains__(str(jsonPisteet["rasti"])) == False:
                #Sijoitetaan pisteet kutsumalla aliohjelmaa idPisteet jolla on parametrina joukkueen merkkaaman rastin id
                pisteet["pisteet"] += idPisteet(jsonPisteet["rasti"])
                #Tarkistetaan, etta onko joukkueen rasti LAHTO jos on joukkueen pisteet nollataan
                if str(jsonPisteet["rasti"]) == "6580427":
                    pisteet["pisteet"] = 0
                #Tarkistetaan onko joukkueen rasti MAALI, jos on lopetetaan pisteiden laskeminen joukkueelle
                if str(jsonPisteet["rasti"]) == "9101016":
                    break
                #Lisataan kayty rasti rastit joukkoon
                rastit.append(str(jsonPisteet["rasti"]))
            #Lisataan joukkueen jasenet pisteet dict:n
            pisteet["jasenet"].append(jsonJoukkue["jasenet"])
            #Tehdaan kopio pisteet dict
            pisteetCopy = pisteet.copy()
            #Lisataan pisteet joukkueet listaan
            joukkueet.append(pisteetCopy)
    #Jarjestetaan joukkueet pisteiden mukaan
    sortedList = sorted(joukkueet, key=lambda k: k['pisteet'], reverse=True)
    #Jarjestetaan lopuksi jasenet aakkosjerjestyskeen ja listaan joukkuuen nimi, pisteet ja jasenet returnTxt:n
    for palautus in sortedList:
        jasenet = palautus["jasenet"]
        #Jarejestetaan jasenet
        jasenet[0].sort()
        jasenet = ', '.join(jasenet[0])
        returnTxt += palautus["nimi"] + " " + "(" + str(palautus["pisteet"]) + " p)" + "\n" + " " + jasenet.replace(",", "\n") + "\n"
    return returnTxt


# @app.route määrää mille osoitteille tämä funktio suoritetaan
@app.route('/')
def default():
    return Response(jarjestaJoukkueet() + "\n" + palautaKoodit() , mimetype="text/plain;charset=UTF-8")

@app.route('/data.json')
def generate():
   generateData()
   return JSON_OBJECT

@app.route('/vt1')
def queryString():
    
    #Kerataan nimi, jasen ja sarja
    nimi = request.args.get("nimi")
    jasen = request.args.getlist("jasen")
    sarja = request.args.get("sarja")
    reset = request.args.get("reset")
    tila = request.args.get("tila")
    leimaus = request.args.getlist("leimaustapa")


    if reset == None:
        print("Reset: " + str(reset))
        reset = 0
    
    if int(reset) == 0:
        loadJson()
    else:
        loadUrl()
        
    #print("Nimi: "+ str(nimi))
    #Tyhja joukkue
    joukkue = {
        "nimi": "",
        "jasenet": [ 
        ],
        "id": 0,
        "leimaustapa": [],
        "rastit": []
      }
    #Laitetaan joukkueelle nimi ja jasenet
    joukkue["nimi"] = nimi
    joukkue["jasenet"] = jasen
    joukkue["leimaustapa"] = leimaus

    
    print(joukkue)

    #Jos tila == insert lisataan joukkue listaan
    if tila == "insert" or tila == None:
        if sarja != None and nimi != None:
            #Listaan joukkue oikeaan sarjaan
            lisaaJoukkue(sarja, joukkue)
    
    #Jos tila == delete poistetaan joukkue listasta
    if tila =="delete":
        if sarja != None and nimi != None:
            poistaJoukkue(sarja, nimi)

    return Response(jarjestaJoukkueet() + "\n" + palautaKoodit() + "\n" + "\n" + tulostaPisteet(), mimetype="text/plain;charset=UTF-8")
    
    