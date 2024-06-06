from random import randrange
from threading import Lock, Thread
from time import sleep

# Abbiamo 5 filosofi, ognuno con un proprio piatto di spaghetti
# e 5 forchette, una per ogni piatto
# I filosofi devono prendere due forchette per mangiare
# e devono attendere che le forchette siano disponibili
# per poter mangiare

# Bisogna evitare il deadlock, quindi bisogna evitare che un filosofo
# prenda una forchetta se non può prendere anche l'altra


## Inanzitutto creiamo la classe Forchetta 

class Forchetta:
    def __init__(self):
        self.lock = Lock()

    def prendi(self):
        self.lock.acquire()

    def rilascia(self):
        self.lock.release()

    

# poi la classe Tavolo

class Tavolo:
    def __init__(self):
        self.forchette = [Forchetta() for i in range(5)] # Creiamo 5 forchette


# e infine la classe Filosofo

class Filosofo(Thread):
    def __init__(self, tavolo, pos, nome):
        super().__init__()
        self.tavolo = tavolo
        self.pos = pos
        self.nome = nome    

    def attendiACaso(self,msec):
         sleep(randrange(msec)/1000.0)

    def pensa(self):
        print(f"{self.nome} sta pensando")
        self.attendiACaso(1000) 

    def mangia(self):
        # Qui è importante, dobbiamo evitare deadlock

        if self.pos < (self.pos + 1) % 5 : 
            self.tavolo.forchette[self.pos].prendi()
            print (f"{self.nome} ha preso la forchetta {self.pos}") 
            self.tavolo.forchette[(self.pos + 1) % 5].prendi() 
            print (f"{self.nome} ha preso la forchetta {(self.pos + 1) % 5}")

        else:
            self.tavolo.forchette[(self.pos + 1) % 5].prendi()
            print (f"{self.nome} ha preso la forchetta {(self.pos + 1) % 5}")
            self.tavolo.forchette[self.pos].prendi()
            print (f"{self.nome} ha preso la forchetta {self.pos}")

        
        print(f"{self.nome} sta mangiando")
        self.attendiACaso(1000)
        print(f"{self.nome} ha finito di mangiare")
        self.tavolo.forchette[self.pos].rilascia()
        self.tavolo.forchette[(self.pos + 1) % 5].rilascia()

    def run(self):
        while True:
            self.pensa()
            self.mangia()



nomi = ["Aristotele", "Socrate", "Platone", "Eraclito", "Parmenide"] 

tavolo = Tavolo()

filosofi = [Filosofo(tavolo, i, nomi[i]) for i in range(5)] 

for f in filosofi:
    f.start() 


