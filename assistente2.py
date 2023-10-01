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
def ascolta():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Regolazione automatica del microfono
            audio = r.listen(source)
            text = r.recognize_google(audio, language='it-IT')
            print(text)
            return text
        
def controlloOra(a,b):
    try:
        if a < 0 or a > 24 or b<0 or b>60:
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
        print(z)
        parla(z,engine)
        try:
            if modo=="scrivo":
                attività = input("attività: ")
            elif modo=="vocale":
                parla("dimmi l'attività che devi svolgere",engine)
                print("attività: ")
                attività = ascolta()

            sdfg="hai detto"+str(attività)+"?"
            print(sdfg)
            parla(sdfg,engine)
        except:
            print("attività non valido")
            parla("attività non valido",engine)
        a=input("sì/no")


    while True:
        b="Inserisci l' ora di inizio dell' attività"
        print(b)
        parla(b,engine)
        if modo=="scrivo":
            inizio = input("ora: (HH:MM)")
            ora=inizio[0]+inizio[1]
            minuti=inizio[3]+inizio[4]
            ora = int(ora)
            minuti = int(minuti)
            f=controlloOra(ora,minuti)
            if f==-1:
                sos="l'orario che hai inserito non è valido"
                print(sos)
                parla(sos,engine)
                True
            else:
                break
        elif modo=="vocale":
            parla("dimmi l'ora di di inizio",engine)
            print("ora: ")
            inizio = int(ascolta())
            ora, minuti = inizio.split(":")
            ora = int(ora)
            minuti = int(minuti)
            f=controlloOra(ora)
            if f==-1:
                sos="l'orario che hai inserito non è valido"
                print(sos)
                parla(sos,engine)
                True
            else:
                break
            
        
    while True:
        print("quanti minuti dura?")
        parla("quanti minuti dura?",engine)
        try:
            if modo=="scrivo":
                durata = int(input("minuti: "))
            elif modo=="vocale":
                parla("dimmi quanti minuti dura l'attività",engine)
                print("minuti: ")
                durata = int(ascolta())
        except:
            print("minuti non validi")
            parla("minuti non validi",engine)
        if durata<0:
            sos="la durata che hai inserito non è valido"
            print(sos)
            parla(sos,engine)
            True
        else:
            break
    cc="ok ho aggiunto nella tua lista delle cose da fare"+attività
    print(cc)
    parla(cc,engine)

    inizio_str= f"{ora:02d}:{minuti:02d}"
    diz={'Attività': attività, 'Inizio': inizio_str, 'durata': int(durata)}
    return diz

# Funzione per la creazione di un nuovo programma settimanale
def attivitàSettimanale(d):
    for giorno in GIORNI_SETTIMANA:
        vfi='Creazione del programma per il'+ giorno
        print(vfi)
        parla(vfi,engine)
        attivitàGiorno(giorno, d,modo)
    return d

def cercaGiornoAttivitàSettimanale(arch, modo):
    # Cerca un'attività settimanale nell'archivio e la restituisce con giorno e ora
    giorno_attività, ora_inizio, durata = None, None, None

    if modo == "scrivo":
        a = input("Attività: ")
    elif modo == "vocale":
        parla("Dimmi l'attività da cercare", engine)
        print("Attività: ")
        a = ascolta()

    for giorno in arch:
        for attività in arch.values():
            for elemento in attività:
                if "Attività" in elemento and elemento["Attività"] == a:
                    giorno_attività = list(giorno.keys())[0]
                    ora_inizio = elemento["Inizio"]
                    durata = elemento["durata"]
                    return giorno_attività, ora_inizio, durata

    # Se l'attività non è stata trovata, restituisci i valori predefiniti
    return giorno_attività, ora_inizio, durata



def eliminaProgrammaSettimanale(di):
    di.clear()



def modifica_attivita(programma_settimanale, modo):
    if modo == "scrivo":
        parla("Inserisci il giorno da modificare", engine)
        giorno_da_modificare = input("Inserisci il giorno da modificare: ")
        parla("inserisci l'attività da modificare: ", engine)
        attivita_da_modificare = input("Inserisci l'attività da modificare: ")
    elif modo == "vocale":
        parla("dimmi il giorno dell'attività", engine)
        print("Giorno da Modificare: ")
        giorno_da_modificare = ascolta()
        parla("Inserisci l'attività da modificare: ", engine)
        print("Attività da modificare: ")
        attivita_da_modificare = ascolta()

    attivita_modificata = creaAttività(modo)

    if giorno_da_modificare in programma_settimanale:
        for attivita in programma_settimanale[giorno_da_modificare]:
            if "Attività" in attivita and attivita["Attività"] == attivita_da_modificare:
                attivita["Attività"] = attivita_modificata["Attività"]
                attivita["Inizio"] = attivita_modificata["Inizio"]
                attivita["durata"] = attivita_modificata["durata"]
                break

                        


    

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

def cerca_prossimi_eventi(programma_settimanale):
    oggi = date.today()
    domani = oggi + timedelta(days=1)
    numero_giorno = domani.weekday()
    giorno_settimana = converti_numero_a_giorno(numero_giorno)

    if giorno_settimana in programma_settimanale:
        attivita = programma_settimanale[giorno_settimana]
        risultato = f"Attività pianificate per {giorno_settimana.capitalize()}:\n"
        for att in attivita:
            desc = att["Attività"]
            inizio = att["Inizio"]
            durata = att["durata"]
            risultato += f"- Attività: {desc}, Inizio: {inizio}, Durata: {durata} minuti\n"
    else:
        risultato = f"Nessuna attività pianificata per {giorno_settimana.capitalize()}."

    return risultato

#per ora il promemoria non funziona
def propremoriain(modo, dizpromemoria):
    if modo == "scrivo":
        data_input = input("Inserisci la data (gg/mm/aaaa): ")
    elif modo == "vocale":
        parla("dimmi la data in formato giorno mese anno",engine)
        print("giorno mese anno: ")
        data_input = ascolta()
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
                bg=f"Promemoria per oggi ({oggi}): {attività}"
                print(bg)
                parla(bg,engine)
            elif data.date() > oggi:
                giorni_rimanenti = (data.date() - oggi).days
                bg=f"Promemoria tra {giorni_rimanenti} giorni ({data.date()}): {attività}"
                print(bg)
                parla(bg,engine)
            else:
                bg=f"La data inserita ({data.date()}) è già trascorsa."
                print(bg)
                parla(bg,engine)
    except ValueError:
        print("assicurati che tutti i campi siano completati")
        parla("assicurati che tutti i campi siano completati",engine)


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
            p=input("inserisci il nome: ")
        elif modo=="vocale":
            parla("inserisci il tuo nome",engine)
            print("Nome: ")
            p=ascolta()
        if len(p)==0:
            print("non hai inserito nessun nome")
            parla("non hai inserito nessun nome",engine)
            errore=True
        elif controllo_formato(p)==False:
            print('formato non valido')
            parla('formato non valido',engine)
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
            print(a)
            parla(a,engine)
            if modo=="scrivo":
                risposta = input("si/no: ")
            elif modo=="vocale":
                print("si/no: ")
                risposta = ascolta()
    return l
def attivitàGiorno(giorno, d,modo):
    risposta = "sì"
    while risposta == "sì" or risposta == "va bene" or risposta == "ok" or risposta == "certo":
        attività = creaAttività(modo)
        if giorno in d:
            d[giorno].append(attività)
        else:
            d[giorno] = [attività]
        a = "Vuoi inserire un'altra attività?"
        print(a)
        parla(a,engine)
        if modo=="scrivo":
            risposta = input("sì/no")
        else:
            print("si/no: ")
            risposta = ascolta()

# Funzioni per la visualizzazione del programma settimanale o lista delle cose da fare
def print_programma_settimana(programma_settimanale):
    for giorno, attivita in programma_settimanale.items():
        print(f"Programma per {giorno}:")
        for attivita_item in attivita:
            desc = attivita_item["Attività"]
            inizio = attivita_item["Inizio"]
            durata = attivita_item["durata"]
            a=f"- Attività: {desc}, Inizio: {inizio}, Durata: {durata} minuti"
            aa=f"per {giorno} hai {desc} alle{inizio} fino alle{inizio}e{durata}"
            print(a)
            parla(aa,engine)


def mostrami_la_lista_delle_cose_da_fare(l):
    for i in range(len(l)):
        attività_descrizione = l[i]["Attività"]
        inizio = datetime.strptime(l[i]['Inizio'], TIME_FORMAT).strftime('%I:%M %p')
        fine = (datetime.strptime(l[i]['Inizio'], TIME_FORMAT) + timedelta(minutes=l[i]['durata'])).strftime('%I:%M %p')
        sdire="hai da fare"+attività_descrizione+"dalle ore"+inizio+"fino alle"+fine
        print(sdire)
        parla(sdire,engine)
        
def menuPrincipale():
    print("-------------------------------")
    print(" || FUNZIONALITà e COMANDI ||")
    print("-------------------------------")
    print("------------------------------------------------------------------------------------------------------------------")
    print("1- aggiungere un'attività alla lista delle cose da fare| comando: aggiungi nella mia lista delle cose da fare    |")
    print("2- creare un nuovo programma settimanale| comando: crea un nuovo programma settimanale                           |")
    print("3- vedere a che ora hai un programma| comando: voglio vedere a che ora ho un programma                           |")
    print("4- vedere la lista delle cose da fare| comando: fammi vedere la lista delle cose da fare                         |")
    print("5- vedere il programma settimanale| comando: fammi vedere il programma settimanale                               |")
    print("6- vedere i prossimi eventi del programma settimanale| comando: fammi vedere i prossimi eventi del programma     |")
    print("7- chiedere che ore sono| comando: che ore sono?                                                                 |")
    print("8- vedere a che ora hai un programma| comando: voglio sapere a che ora ho un programma                           |")
    print("9- sapere che tempo farà oggi?| comando: che tempo fa oggi?                                                      |")
    print("10- eliminare un programma settimanale| comando: elimina programma settimanale?                                  |")
    print("11- modificare un programma settimanale| comando: modifica programma settimanale?                                |")  
    print("12- chiudere il programma| comando: arrivederci                                                                  |")
    print("-----------------------------------------------------------------------------------------------------------------")
# questa funzione è il guscio del programma la parte in cui l'utente interagisce con l'assistente
def main(a,b,modo,dipromemoria):
    text="dfdf"
    while text!="arrivederci":
        try:
            if modo=="scrivo":
                text = input("comando: ")
            else:
                print("comando: ")
                text = ascolta()
            print('Comando vocale: ',text)
            risposta = riconoscimento_comando(text, dati_risposte)
            print(risposta)
            parla(risposta,engine)
            if risposta=="ora guardo":
                Traduttore=Translator(from_lang="en",to_lang="it")
                città = "Spirano" # è da migliorare mettendo che rileva da solo la poszione ma queta è un versione base.
                tempo_di_oggi = condizione_tempo(città)
                tempo_di_oggi = Traduttore.translate(tempo_di_oggi)
                te="Oggi a "+ str(città)+" c'è" + ":", tempo_di_oggi
                print(te)
                parla(te,engine)
            if risposta=="va bene ora creiamo il tuo programma settimanale":
                ssss=attivitàSettimanale(b)
                datijson=json.dumps(ssss)
                f=open("dizsettimana.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            if risposta=="ecco cosa poi chiedermi":
                menuPrincipale()  
            if risposta=="ok va bene":
                attivitàGiornaliere(a,modo)
                datijson=json.dumps(a)
                f=open("listagiorno.txt","w",encoding="utf-8")
                f.write(datijson)
                f.close()
            if risposta=="ecco a te il programma":
                print_programma_settimana(b)
            if risposta=="ecco a te la lista":
                mostrami_la_lista_delle_cose_da_fare(a)
            if risposta=="":
                evento=cerca_prossimi_eventi(b)
                print(evento)
                parla(evento,engine)
            if risposta=="sono le":
                ora=ore()
                print(ora)
                parla(ora,engine)
            if risposta=="va bene elimino il tuo programma":
                eliminaProgrammaSettimanale(b)
            if risposta=="va bene ora modifichiamo il tuo programma settimanale":
                modifica_attivita(b,modo)
            if risposta=="va bene":
                giorno_attività, ora_inizio, durata=cercaGiornoAttivitàSettimanale(b,modo)
                ss=f"ce l'hai il{giorno_attività} alle {ora_inizio} fino alle{durata}"
                print(ss)
                parla(ss)
                
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
        except sr.UnknownValueError:
            print('mi dispiace sono ancora in fase di sviluppo non posso rispondere a questa domanda')
            parla('mi dispiace sono ancora in fase di sviluppo non posso rispondere a questa domanda',engine)
        except sr.RequestError as e:
            dd='Errore nella richiesta di riconoscimento vocale: ',e
            print(dd)
            parla(dd,engine)

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
try:
    with open("listagiorno.txt", "r", encoding="utf-8") as f:
        datijso = f.read()
    listaGiorno = json.loads(datijso)

    with open("dizsettimana.txt", "r", encoding="utf-8") as f:
        datijso = f.read()
    dizSettimana = json.loads(datijso)

    with open("dizpromemoria.txt", "r", encoding="utf-8") as f:
        datijso = f.read()
    dizpromemoria = json.loads(datijso)

except FileNotFoundError:
    print("I file JSON non sono presenti.")
except json.JSONDecodeError as e:
    print(f"Errore nella decodifica JSON: {str(e)}")
except Exception as e:
    print(f"Errore sconosciuto: {str(e)}")
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
            sd=inserisci_nome(modo)
            conoscenza(sd)
            dati=json.dump(sd,c)
            c.write(dati)
    except:
        pass         
with open("nome_cognome.txt","r",encoding="utf-8") as f:
    srt=f.read()
if scd==0:
    ffff="bentornato"+srt
    print(ffff)
    parla(ffff,engine)
#print(dizpromemoria)
main(listaGiorno,dizSettimana,modo,dizpromemoria)