import json
diz={
  "Come ti chiami?": "Il mio nome è Fall Assistant.",
  "Come stai?": "Sto bene grazie!",
  "Che tempo fa oggi?": "ora guardo",
  "Cosa puoi fare?": "Posso aiutarti ad organizzare a meglio la tua giornata",
  "Grazie!": "Di niente! Sono qui per aiutarti in qualsiasi momento.",
  "chi ti ha creato": "sono stato creato da Mbacke Gueye, nato il 31 ottobre 2005 in Senegal e attualmente frequenta l'Istituto Tecnico Marconi di Dalmine.",
  "crea un nuovo programma settimanale": "va bene ora creiamo il tuo programma settimanale",
  "aggiungere nella mia lista delle cose da fare ": "ok va bene",
  "mostrami il calendario": "ok",
  "mostrami la la lista delle attività":"ecco a te la lista",
  "mostrami il programma settimanale":"ecco a te il programma",
  "voglio vedere a che ora ho un programma": "va bene",
  "ciao":"ciao sono felice di averti assistito anche oggi",
  "arrivederci":"ciao sono felice di averti assistito anche oggi",
  "prossimi eventi":"",
  "che ore sono":"sono le",
  "nuovo promemoria":"ok creiamo il tuo promemoria",
  "voglio vedere i miei promemoria":".",
}
datijson=json.dumps(diz)
f=open("conv.txt","w",encoding="utf-8")
f.write(datijson)
f.close()
#leggere
f=open("conv.txt","r",encoding="utf-8")
datijso=f.read()
f.close()
dati=json.loads(datijso)
print(dati)