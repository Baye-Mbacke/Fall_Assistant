import datetime
import json
import speech_recognition as sr
import pyttsx3
import requests
#from guizero import App, Text, TextBox, PushButton
# Definizione delle costanti
GIORNI_SETTIMANA = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
TIME_FORMAT = '%H:%M'
f=open("conv.txt","r",encoding="utf-8")
datijso=f.read()
f.close()
dati_risposte=json.loads(datijso)
# Configurazione del motore di sintesi vocale
engine = pyttsx3.init()
engine.setProperty('rate', 140)  # Velocità di lettura del testo

# Funzione per la lettura del testo in voce
def parla(text):
    engine.say(text)
    engine.runAndWait()

#funzione per ascoltare l'utente ascolta
def ascolta():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Regolazione automatica del microfono
            audio = r.listen(source)
            text = r.recognize_google(audio, language='it-IT')
            print(text)
            return text
def controlloOra(a):
    if a>24 or a<0 or a==24:
        return -1
    return 1

def ore():
    ora = datetime.datetime.now()
    ore = ora.strftime("%H:%M")
    return ore

def condizione_tempo(api_key, città):
    url = f"http://api.weatherbit.io/v2.0/current?key={api_key}&city={città}"
    response = requests.get(url)
    data = response.json()
    try:
        weather = data["data"][0]["weather"]["description"]
        return weather
    except:
        return "Impossibile ottenere le condizioni meteo"
        
'''
#esempio di utilizzo
Traduttore=Translator(from_lang="en",to_lang="it")
api_key = "1dffac1e57e042979d7aaf9fe91f578f"
città = "Spirano"
tempo_di_oggi = condizione_tempo(api_key, città)
tempo_di_oggi = Traduttore.translate(tempo_di_oggi)
print("Oggi a", città,"c'è" + ":", tempo_di_oggi)
'''



# Funzione per la creazione di una nuova attività
def creaAttività():
    a="no"
    while a!="sì":
        z="che attività devi fare?"
        print(parla(z))
        try:
            attività = input("attività: ")

            sdfg="hai detto"+str(attività)+"?"
            print(parla(sdfg))
        except:
            print(parla("attività non valido"))
        a=input("sì/no")
    while True:
        b="Inserisci l' ora di inizio dell' attività"
        print(parla(b))
        try:
            inizio = int(input("ora: "))
            f=controlloOra(inizio)
        except:
            print(parla("orario non valido"))
        if f==-1:
            sos="l'orario che hai inserito non è valido"
            (parla(sos))
            True
        else:
            break
    while True:
        c="quanti minuti dura?"
        print(parla(c))
        try:
            durata = int(input("minuti: "))
        except:
            print(parla("minuti non validi"))
        if durata<0:
            sos="la durata che hai inserito non è valido"
            print(parla(sos))
            True
        else:
            break
    cc="ok ho aggiunto nella tua lista delle cose da fare"+attività
    parla(cc)
    inizio_str = f'{inizio:02d}:00'
    diz={'Attività': attività, 'Inizio': inizio_str, 'durata': int(durata)}
    return diz



def cercaAttivitàSettimanale(arch,a):
    #cerca un'attività settimanale nell'archivio e la restituisce con giorno e ora
    for giorno in arch:
        for attività in giorno.values():
            for elemento in attività:
                if "Attività" in elemento and elemento["Attività"] == a:
                    giorno_attività = list(giorno.keys())[0]
                    ora_inizio = elemento["Inizio"]
                    durata = elemento["durata"]
                    return giorno_attività, ora_inizio, durata
                else:
                    return -1


def cerca_prossimi_eventi(arch):
    oggi = datetime.today().weekday()  # Ottieni il giorno della settimana (0 = lunedì, 6 = domenica)
    giorno_successivo = (oggi + 1) % 7  # Calcola il giorno successivo (ritorna a lunedì se è domenica)
    giorno_successivo_nome = None

    for giorno in arch:
        nome_giorno = list(giorno.keys())[0]

        if giorno_successivo_nome is None:
            giorno_successivo_nome = nome_giorno

        if nome_giorno == giorno_successivo_nome:
            attività_giorno = giorno[giorno_successivo_nome]
            for attività in attività_giorno:
                if "Attività" in attività:
                    attività_nome = attività["Attività"]
                    ora_inizio = attività["Inizio"]
                    durata = attività["durata"]
                    return attività_nome,ora_inizio,durata
                    #print(f"{giorno_successivo_nome}: {attività_nome} - Inizio: {ora_inizio}, Durata: {durata} minuti")

    if giorno_successivo_nome is None:
        print("Nessuna attività trovata per il giorno successivo.")

    

def propremoria():
    attività=input("attività: ")
    gg=input("giorno: ")
    gg+="/"
    mese=input("mese: ")
    mese+="/"
    anno=input("anno: ")
    anno+="/"
    try:
        data = datetime.strptime(gg+mese+anno, "%d/%m/%Y")
        oggi = datetime.now().date()

        if data.date() == oggi:
            print(f"Promemoria per oggi ({oggi}): {attività}")
        elif data.date() > oggi:
            giorni_rimanenti = (data.date() - oggi).days
            print(f"Promemoria tra {giorni_rimanenti} giorni ({data.date()}): {attività}")
        else:
            print(f"La data inserita ({data.date()}) è già trascorsa.")
    except ValueError:
        print("assicurati che tutti i campi siano completati")


def controllo_formato(a):
    v='abcdefghijklmnopqrstuvzywxABCDEFGHILMNOPQRSTVUYWZX'
    for i in a:
        if i not in v:
            return False
        return True
def inserisci_nome():
    errore=True
    while True:
        p=input("inserisci il nome")
        if len(p)==0:
            print("nome non valido")
            errore=True
        elif controllo_formato(p)==False:
            print('formato non valido')
            errore=True
        else:
            return p

# Funzione per la creazione di una nuova giornata di attività
def attivitàGiornaliere(l):
    risposta="sì"
    while risposta=="sì" or risposta=="va bene" or risposta=="ok" or risposta=="certo": 
            parla("ok")
            l.append(creaAttività())
            a="Vuoi inserire un'altra attività"
            parla(a)
            risposta = input("si/no: ")
    return l
'''
questa funzione è diversa da quella precedente 
perchè è per la settimana mentre l'altra è gnerale
'''
def attivitàGiorno(giorno, d):
    risposta = "sì"
    while risposta == "sì" or risposta == "va bene" or risposta == "ok" or risposta == "certo":
        attività = creaAttività()
        if giorno in d:
            d[giorno].append(attività)
        else:
            d[giorno] = [attività]
        a = "Vuoi inserire un'altra attività?"
        parla(a)
        risposta = input("sì/no")

# Funzione per la creazione di un nuovo programma settimanale
def attivitàSettimanale(d):
    d={}
    for giorno in GIORNI_SETTIMANA:
        print('Creazione del programma per il', giorno)
        attivitàGiorno(giorno, d)
    return d

# Funzioni per la visualizzazione del programma settimanale o lista delle cose da fare
def print_programma_settimana(programmaSettimanale):
    for giorno_attività in programmaSettimanale:
        for giorno, attività in giorno_attività.items():
            print('Programma per:', giorno)
            for i in range(len(attività)):
                attività_corrente = attività[i]
                attività_descrizione = attività_corrente["Attività"]
                inizio = datetime.datetime.strptime(attività_corrente['Inizio'], TIME_FORMAT).strftime('%I:%M %p')
                fine = (datetime.datetime.strptime(attività_corrente['Inizio'], TIME_FORMAT) + datetime.timedelta(minutes=attività_corrente['durata'])).strftime('%I:%M %p')
                cc = "Per il giorno " + giorno + " hai da fare " + attività_descrizione + " dalle ore " + inizio + " alle " + fine
                print(parla(cc))
def mostrami_la_lista_delle_cose_da_fare(l):
    for i in range(len(l)):
        attività_descrizione = l[i]["Attività"]
        inizio = datetime.datetime.strptime(l[i]['Inizio'], TIME_FORMAT).strftime('%I:%M %p')
        fine = (datetime.datetime.strptime(l[i]['Inizio'], TIME_FORMAT) + datetime.timedelta(minutes=l[i]['durata'])).strftime('%I:%M %p')
        sdire="hai da fare"+attività_descrizione+"dalle ore"+inizio+"fino alle"+fine
        print(parla(sdire))
def menuPrincipale():
    print("------------------")
    print("MENU PRINCIPALE")
    print("------------------")
    print("--------------------------------------------")
    print("1- aggiungi un'attività ")
    print("2- nuova attività settimanale ")
    print("3- mostrami la lista delle cose da fare")
    print("4- mostrami il programma settimanale ")
    print("--------------------------------------------")


# questa funzione è il guscio del programma la parte in cui l'utente interagisce con l'assistente
def main(a,b,d):
    text="dfdf"
    while text!="ciao":
        try:
            menuPrincipale()
            text = input("comando: ")
            print('Comando vocale: ',text)
            if text in dati_risposte:
                risposta = dati_risposte[text]
                print(parla(risposta))
            elif text=="aggiungi un'attività":
                attivitàGiornaliere(a)
                datijson=json.dumps(a)
                f=open("listagiorno.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            elif text=="nuova attività settimanale":
                ssss=attivitàSettimanale(b)
                d.append(ssss)
                datijson=json.dumps(d)
                f=open("dizsettimana.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            elif text=="mostrami il programma settimanale" :
                print_programma_settimana(d)
            elif text=="mostrami la lista delle cose da fare":
                mostrami_la_lista_delle_cose_da_fare(a)
            elif text=="arrivederci" or text=="ciao ci vediamo alla prossima" or text=="ciao":
                fin="ciao sono felice di averti assistito anche oggi"
                parla(fin)
        except sr.UnknownValueError:
            print(parla('mi dispiace sono ancora in fase di sviluppo non posso rispondere a questa domanda'))
        except sr.RequestError as e:
            print('Errore nella richiesta di riconoscimento vocale: ',e)

#prima volta              
def conoscenza(a):
    b="ciao"+a+"Benvenuto in Spazio Tempo io sarò il tuo assistente"
    parla(b)
#MAIN
listaGiorno=[]
lista2=[]
dizSettimana={}
lista3=[]
lista3.append(dizSettimana)
try:
    f=open("listagiorno.txt","r",encoding="utf-8")
    datijso=f.read()
    f.close()
    listaGiorno=json.loads(datijso)
    f=open("dizsettimana.txt","r",encoding="utf-8")
    datijso=f.read()
    f.close()
    lista3=json.loads(datijso)
except:
    pass
scd=0
try:
    with open("nome_cognome.txt","r",encoding="utf-8") as f:
        aa=f.read()
        if len(aa)==0:
            scd=-1
        else:
            scd=0
except:
    pass
if scd==-1:
    try:
        with open("nome_cognome.txt","w",encoding="utf-8") as c:
            cc="ciao inserisci il tuo nome e cognome:"
            parla(cc)
            sd=inserisci_nome()
            conoscenza(sd)
            dati=json.dump(sd,c)
            c.write(dati) 
    except:
        pass         
with open("nome_cognome.txt","r",encoding="utf-8") as f:
    srt=f.read()
if scd==0:
    ffff="bentornato"+srt
    parla(ffff)
main(listaGiorno,dizSettimana,lista3)