from random import randint, random
from threading import RLock, Thread
from time import sleep


# Creiamo il ContoBancario
class ContoBancario:
    def __init__(self,id,saldoIniziale):
        self.id = id
        self.saldo = saldoIniziale
        self.listaMovimenti = []
        self.lock = RLock()

    def getSaldo(self):
        return self.saldo
    
    def deposita(self,ammontare):
        self.saldo += ammontare

    def preleva(self,ammontare):
        if self.saldo >= ammontare:
            self.saldo -= ammontare
            return True
        else:
            return False
        
    def addTransazione(self,sorgente,destinazione,ammontare):

        transazione = Transazione(sorgente,destinazione,ammontare)
        self.listaMovimenti.append(transazione)
        if len(self.listaMovimenti) > 50:
            self.listaMovimenti.pop(0)

        

    

class Transazione:
    def __init__(self,sorgente,destinazione,ammontare):
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.ammontare = ammontare

    def __str__(self):
        return f"{self.sorgente.id}=>{self.destinazione.id}:{self.ammontare}"
    
# Creiamo adesso la banca che ci consentira di gestire le nostre transazioni

class Banca:
    def __init__(self):
        self.conti = {}

    def getContoACaso(self):
        codiciConto = list(self.conti.keys())
        return codiciConto[randint(0,len(codiciConto)-1)]


    def aggiungiConto(self,conto):
        if conto.id in self.conti:
            raise Exception("Impossibile aggiungere conto esistente.")
        else:
            self.conti[conto.id]=conto

    def getSaldo(self,idConto):
        with self.conti[idConto].lock:
            return self.conti[idConto].getSaldo()

    def trasferisci(self,idContoSorgente,idContoDestinazione,ammontare):
        
        s = self.conti[idContoSorgente]
        d = self.conti[idContoDestinazione]
        if idContoSorgente < idContoDestinazione:
            s.lock.acquire()
            d.lock.acquire()
        else:
            d.lock.acquire()
            s.lock.acquire()
        #
        # self.conti[min(idContoSorgente,idContoDestinazione)].lock.acquire()
        # self.conti[max(idContoSorgente,idContoDestinazione)].lock.acquire()
        #
        try:
            if s.preleva(ammontare):
                d.deposita(ammontare)
                s.addTransazione(s,d,ammontare)
                d.addTransazione(s,d,ammontare)
                return True
            else:
                return False
        finally:
            s.lock.release()
            d.lock.release()

class Cliente(Thread):
    def __init__(self,conto,banca):
        super().__init__()
        self.banca = banca
        self.mioConto = conto

    def run(self):
        numIterazioni = 1000
        while(numIterazioni > 0):
            numIterazioni -= 1
            destinatario = self.banca.getContoACaso()
            importo = randint(1,1000)
            if destinatario != self.mioConto.id:
                print(f"Sono il thread {self.name} e in questo momento ho {self.banca.getSaldo(self.mioConto.id)} sul mio conto")
                if self.banca.trasferisci(self.mioConto.id,destinatario,importo):
                    print(f"Ho trasferito {importo} da {self.mioConto.id} a {destinatario}")
                else:
                    print(f"Transazione fallita: non ho {importo} su {self.mioConto.id}")
            sleep(random())


siliconValleyBank = Banca()

numConti = 10
for i in range(numConti):
    conto = ContoBancario(i,randint(0,10000))
    siliconValleyBank.aggiungiConto(conto)
    cliente = Cliente(conto,siliconValleyBank)
    cliente.start()



