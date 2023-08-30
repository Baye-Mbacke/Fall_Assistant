from datetime import*
import json
import speech_recognition as sr
import pyttsx3
import requests
import difflib
from translate import*
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
modo="scrivo"

# Funzione per la lettura del testo in voce
def parla(text,engine):
    engine.say(text)
    engine.runAndWait()

def riconoscimento_comando(text, dizionario):
    closest_match = difflib.get_close_matches(text, dizionario.keys(), n=1, cutoff=0.5)
    if closest_match:
        matched_command = closest_match[0]
        response = dizionario[matched_command]
        return response
    else:
        return "Non ho capito la tua richiesta."

#funzione per ascoltare l'utente ascolta
def ascolta(niente):
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Regolazione automatica del microfono
            audio = r.listen(source)
            text = r.recognize_google(audio, language='it-IT')
            print(text)
            return text
        
def controlloOra(a):
    try:
        ora = int(a)
        if ora < 0 or ora >= 24:
            return -1
        return 1
    except:
        return -1


def ore():
    ora = datetime.now()
    ore = ora.strftime("%H:%M")
    return ore

def condizione_tempo(città):
    api_key="1dffac1e57e042979d7aaf9fe91f578f"
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
città = "Spirano"
tempo_di_oggi = condizione_tempo(città)
tempo_di_oggi = Traduttore.translate(tempo_di_oggi)
print("Oggi a", città,"c'è" + ":", tempo_di_oggi)
'''



# Funzione per la creazione di una nuova attività
def creaAttività(modo):
    a="no"
    while a!="sì":
        z="che attività aggiungo?"
        print(parla(z,engine))
        try:
            if modo=="scrivo":
                attività = input("attività: ")
            elif modo=="vocale":
                attività = ascolta("attività: ")

            sdfg="hai detto"+str(attività)+"?"
            print(parla(sdfg,engine))
        except:
            print(parla("attività non valido",engine))
        a=input("sì/no")
    while True:
        b="Inserisci l' ora di inizio dell' attività"
        print(parla(b,engine))
        try:
            if modo=="scrivo":
                inizio = input("ora: ")
            elif modo=="vocale":
                inizio = int(ascolta("ora: "))
            ora, minuti = inizio.split(":")
            ora = int(ora)
            minuti = int(minuti)
            f=controlloOra(ora)
        except:
            print(parla("orario non valido",engine))
        if f==-1:
            sos="l'orario che hai inserito non è valido"
            (parla(sos,engine))
            True
        else:
            break
    while True:
        c="quanti minuti dura?"
        print(parla(c,engine))
        try:
            if modo=="scrivo":
                durata = int(input("minuti: "))
            elif modo=="vocale":
                durata = int(ascolta("minuti: "))
        except:
            print(parla("minuti non validi",engine))
        if durata<0:
            sos="la durata che hai inserito non è valido"
            print(parla(sos,engine))
            True
        else:
            break
    cc="ok ho aggiunto nella tua lista delle cose da fare"+attività
    parla(cc,engine)
    inizio_str= f"{ora:02d}:{minuti:02d}"
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

def converti_numero_a_giorno(numero):
    giorni_settimana = {
        0: "lunedì",
        1: "martedì",
        2: "mercoledì",
        3: "giovedì",
        4: "venerdì",
        5: "sabato",
        6: "domenica"
    }
    return giorni_settimana.get(numero)

def cerca_prossimi_eventi(archivio):
    oggi = date.today()
    domani = oggi + timedelta(days=1)
    numero_giorno = domani.weekday()
    giorno_settimana = converti_numero_a_giorno(numero_giorno)

    if giorno_settimana in archivio[0]:
        attivita = archivio[0][giorno_settimana]
        risultato = f"Attività pianificate per {giorno_settimana.capitalize()}:\n"
        for att in attivita:
            risultato += f"- {att['Attività']}, Inizio: {att['Inizio']}, Durata: {att['durata']} minuti\n"
    else:
        risultato = f"Nessuna attività pianificata per {giorno_settimana.capitalize()}."

    return risultato

#per ora il promemoria non funziona
def propremoriain(modo, dizpromemoria):
    if modo == "scrivo":
        data_input = input("Inserisci la data (gg/mm/aaaa): ")
    elif modo == "vocale":
        data_input = ascolta("Inserisci la data (giorno mese anno): ")
        data_input = data_input.replace(" ", "/")
    attività = creaAttività(modo)
    try:
        data = datetime.strptime(data_input, "%d/%m/%Y")
        dizpromemoria[data_input] = attività
        print("Attività aggiunta correttamente.")
    except ValueError:
        print("La data inserita non è nel formato corretto (gg/mm/aaaa). Riprova.")

    return dizpromemoria

#da un errore in cui dice che strptime non ce un errore strano
def promemoriaout(di):
    try:    
        for dataaa, attività in di.items():
            oggi = datetime.now().date()
            data = datetime.strptime(dataaa, "%d/%m/%Y")
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
    

def inserisci_nome(modo):
    errore=True
    while True:
        if modo=="scrivo":
            p=input("inserisci il nome")
        elif modo=="vocale":
            p=ascolta("inserisci il nome")
        if len(p)==0:
            print(parla("non hai inserito nessun nome",engine))
            errore=True
        elif controllo_formato(p)==False:
            print(parla('formato non valido',engine))
            errore=True
        else:
            return p

# Funzione per la creazione di una nuova giornata di attività
def attivitàGiornaliere(l,modo):
    risposta="sì"
    while risposta=="sì" or risposta=="va bene" or risposta=="ok" or risposta=="certo": 
            parla("ok")
            l.append(creaAttività(modo))
            a="Vuoi inserire un'altra attività"
            parla(a,engine)
            if modo=="scrivo":
                risposta = input("si/no: ")
            elif modo=="vocale":
                risposta = ascolta("si/no: ")
    return l
'''
questa funzione è diversa da quella precedente 
perchè è per la settimana mentre l'altra è gnerale
'''
def attivitàGiorno(giorno, d,modo):
    risposta = "sì"
    while risposta == "sì" or risposta == "va bene" or risposta == "ok" or risposta == "certo":
        attività = creaAttività(modo)
        if giorno in d:
            d[giorno].append(attività)
        else:
            d[giorno] = [attività]
        a = "Vuoi inserire un'altra attività?"
        parla(a,engine)
        if modo=="scrivo":
            risposta = input("sì/no")
        else:
            risposta = ascolta("sì/no")

# Funzione per la creazione di un nuovo programma settimanale
def attivitàSettimanale(d):
    for giorno in GIORNI_SETTIMANA:
        print('Creazione del programma per il', giorno)
        attivitàGiorno(giorno, d,modo)
    return d


# Funzioni per la visualizzazione del programma settimanale o lista delle cose da fare
def print_programma_settimana(programmaSettimanale):
    for giorno_attività in programmaSettimanale:
        for giorno, attività in giorno_attività.items():
            print('Programma per:', giorno)
            for i in range(len(attività)):
                attività_corrente = attività[i]
                attività_descrizione = attività_corrente["Attività"]
                inizio = datetime.strptime(attività_corrente['Inizio'], TIME_FORMAT).strftime('%I:%M %p')
                fine = (datetime.strptime(attività_corrente['Inizio'], TIME_FORMAT) + timedelta(minutes=attività_corrente['durata'])).strftime('%I:%M %p')
                cc = "Per il giorno " + giorno + " hai da fare " + attività_descrizione + " dalle ore " + inizio + " alle " + fine
                print(parla(cc,engine))


def mostrami_la_lista_delle_cose_da_fare(l):
    for i in range(len(l)):
        attività_descrizione = l[i]["Attività"]
        inizio = datetime.strptime(l[i]['Inizio'], TIME_FORMAT).strftime('%I:%M %p')
        fine = (datetime.strptime(l[i]['Inizio'], TIME_FORMAT) + timedelta(minutes=l[i]['durata'])).strftime('%I:%M %p')
        sdire="hai da fare"+attività_descrizione+"dalle ore"+inizio+"fino alle"+fine
        print(parla(sdire,engine))

        
def menuPrincipale():
    print("------------------")
    print("FUNZIONALITà e COMANDI")
    print("------------------")
    print("--------------------------------------------")
    print("1- aggiungere un'attività alla lista delle cose da fare| comando: aggiungi nella mia lista delle cose da fare")
    print("2- creare un nuovo programma settimanale| comando: crea un nuovo programma settimanale")
    print("3- vedere a che ora hai un programma| comando: voglio vedere a che ora ho un programma")
    print("4- vedere la lista delle cose da fare| comando: fammi vedere la lista delle cose da fare")
    print("5- vedere il programma settimanale| comando: fammi vedere il programma settimanale ")
    print("6- vedere i prossimi eventi del programma settimanale| comando: fammi vedere i prossimi eventi del programma")
    print("7- chiedere che ore sono| comando: che ore sono?")
    print("8- vedere a che ora hai un programma| comando: voglio sapere a che ora ho un programma")
    print("9- sapere che tempo farà oggi?| comando: che tempo fa oggi?")
    print("10- chiudere il programma| comando: arrivederci")
    print("--------------------------------------------")
    
# questa funzione è il guscio del programma la parte in cui l'utente interagisce con l'assistente
def main(a,b,d,modo,dipromemoria):
    text="dfdf"
    while text!="arrivederci":
        try:
            if modo=="scrivo":
                text = input("comando: ")
            else:
                text = ascolta("comando: ")
            print('Comando vocale: ',text)
            risposta = riconoscimento_comando(text, dati_risposte)
            print(parla(risposta,engine))
            if risposta=="ora guardo":
                Traduttore=Translator(from_lang="en",to_lang="it")
                città = "Spirano" # è da migliorare mettendo che rileva da solo la poszione ma queta è un versione base.
                tempo_di_oggi = condizione_tempo(città)
                tempo_di_oggi = Traduttore.translate(tempo_di_oggi)
                te="Oggi a"+ str(città)+"c'è" + ":", tempo_di_oggi
                print(parla(te,engine))
            if risposta=="va bene ora creiamo il tuo programma settimanale":
                ssss=attivitàSettimanale(b)
                d.append(ssss)
                datijson=json.dumps(d)
                f=open("dizsettimana.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            if risposta=="ecco cosa poi chiedermi":
                print(menuPrincipale)    
            if risposta=="ok va bene":
                attivitàGiornaliere(a,modo)
                datijson=json.dumps(a)
                f=open("listagiorno.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            if risposta=="ecco a te il programma":
                print_programma_settimana(d)
            if risposta=="ecco a te la lista":
                mostrami_la_lista_delle_cose_da_fare(a)
            if risposta=="":
                evento=cerca_prossimi_eventi(d)
                print(parla(evento,engine))
            if risposta=="sono le":
                ora=ore()
                print(parla(ora,engine))
            '''
            PER ORA NON DISPONIBILE
            if risposta=="ok creiamo il tuo promemoria":
                datattività=propremoriain(modo,dipromemoria)
                datijson=json.dumps(datattività)
                f=open("dizpromemoria.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            if risposta==".":
                promemoriaout(dipromemoria)
            '''
            if risposta=="ora guardo":
                condizione_tempo("Spirano")
            if risposta=="va bene":
                a=input("attività da cercare:")
                gior,orve,data=cercaAttivitàSettimanale(d,a)
                sdenc="giorno: "+gior+"ore: "+orve+"data: "+data
        except sr.UnknownValueError:
            print(parla('mi dispiace sono ancora in fase di sviluppo non posso rispondere a questa domanda',engine))
        except sr.RequestError as e:
            print('Errore nella richiesta di riconoscimento vocale: ',e)

# prima volta              
def conoscenza(a):
    b="ciao"+a+"Benvenuto in Fall Assistant io sarò il tuo assistente personale."
    parla(b,engine)

#---------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------MAIN-----------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
listaGiorno=[]
lista2=[]
dizSettimana={}
dizpromemoria={}
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

    f=open("dizpromemoria.txt","r",encoding="utf-8")
    datijso=f.read()
    f.close()
    dizpromemoria=json.loads(datijso)

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
            parla(cc,engine)
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
    parla(ffff,engine)
main(listaGiorno,dizSettimana,lista3,modo,dizpromemoria)