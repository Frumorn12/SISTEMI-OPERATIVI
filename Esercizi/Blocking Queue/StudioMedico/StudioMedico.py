from threading import Thread
from queue import Queue

from random import random, randrange, randint


from threading import RLock, Condition

# Creaiamo prima di tutto la salaDiAttesa

class SalaDiAttesa:
    codaVisitaMedico = Queue() 
    codaRicetta = Queue()
    codaRicettaPrioritaria = Queue()

    #Blocco aggiunta paziente visita 
    def aggiungiPazienteVisita(self, paziente):
        self.codaVisitaMedico.put(paziente)
        paziente.attendiRicetta()
        return paziente.ricetta
    
    def aggiungiPazienteRicetta(self, paziente):
        self.codaRicetta.put(paziente)
        paziente.attendiRicetta()
        return paziente.ricetta
    
    def aggiungiPazienteRicettaPrioritaria(self, paziente):
        self.codaRicettaPrioritaria.put(paziente)
        paziente.attendiRicetta()
        return paziente.ricetta
    

    # i get dei pazienti
    def getPazienteVisita(self):
        return self.codaVisitaMedico.get()
    # in questo caso prima controlliamo che ricettaprio sia ok
    # se non è vuota ritorniamo il primo paziente prioritario
    def getProssimoPazienteRicetta(self):
        if not self.codaRicettaPrioritaria.empty():
            return self.codaRicettaPrioritaria.get()
        else:
            return self.codaRicetta.get()
        

# Medico

class Medico(Thread):
    def __init__(self, salaDiAttesa):
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):
        while True: 
            p = self.salaDiAttesa.getPazienteVisita()
            p.visitaMedico()

            n = randint(1, 3) 

            if n == 1:
                p.ricetta.medicina = "TUTTO OK"
                p.ricetta.ricettaPronta()
            elif n == 2:
                p.ricetta.medicina = "STAI BENE, PUOI ANDARE VIA SENZA RICETTA"
                p.ricetta.ricettaPronta()

            else:
                self.salaDiAttesa.aggiungiPazienteRicettaPrioritaria(p) 

            
            print("Il paziente " + p.nome + " è uscito con la ricetta " + p.ricetta.medicina)


# Segretaria

class Segretaria(Thread):
    def __init__(self, salaDiAttesa):
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):
        while True:
            p = self.salaDiAttesa.getProssimoPazienteRicetta()
            n = random()
            if n > 0.666666:
                p.ricetta.medicina = "MAALOX"
            elif n > 0.333333:
                p.ricetta.medicina = "OKI"
            else:
                p.ricetta.medicina = "AULIN"
            p.ricetta.ricettaPronta()

# Paziente 

class Paziente:
    nextCodicePaziente = 0
    def __init__(self):
        self.nome = "Paziente" + str(Paziente.nextCodicePaziente)
        Paziente.nextCodicePaziente += 1
        self.ricetta = Ricetta(self)
    
    def visitaMedico(self):
        print("Il paziente " + self.nome + " è stato visitato dal medico")
    
    def attendiRicetta(self):
        self.ricetta.attendiRicetta()


# Ricetta

class Ricetta:
    lockRicetta=RLock()
    conditionRicetta=Condition(lockRicetta)
    medicina=None

    def attendiRicetta(self):
        self.lockRicetta.acquire()
        while(self.medicina==None):
            self.conditionRicetta.wait()
        self.lockRicetta.release()

    def ricettaPronta(self):
        self.lockRicetta.acquire()
        self.conditionRicetta.notifyAll()
        self.lockRicetta.release()

# GeneraPazienti

class PazienteRun(Thread):
    def __init__(self, salaDiAttesa):
        super().__init__()
        self.salaDiAttesa=salaDiAttesa

    def run(self):
        paziente = Paziente()

        n=random()

        if (n>0.5):
            self.salaDiAttesa.aggiungiPazienteVisita(paziente)
        else:
            self.salaDiAttesa.aggiungiPazienteRicetta(paziente)

        print("Il paziente " + paziente.nome + " è uscito con la ricetta " + paziente.ricetta.medicina)



class GeneraPazienti(Thread):
    def __init__(self, salaDiAttesa):
        super().__init__()
        self.salaDiAttesa = salaDiAttesa

    def run(self):
        while(True):
            pazienteRun = PazienteRun(self.salaDiAttesa)
            pazienteRun.start()



def main():
    salaDiAttesa = SalaDiAttesa()

    medico = Medico(salaDiAttesa)
    segretaria = Segretaria(salaDiAttesa)
    generaPazienti = GeneraPazienti(salaDiAttesa)

    medico.start()
    segretaria.start()
    generaPazienti.start()

    print ("Fine") 



main()
