from queue import Queue
from random import randint
from threading import Condition, RLock, Thread, current_thread
import time

# Iniziamo vedendo come impostare il codice

# Abbiamo i clienti che ordinano la pizza
# i pizzaglioli che depositano la pizza fatta
# e poi i clienti che ritirano la pizza
# quindi iniziamo a creare prima di tutto la pizzeria

pizze = { "margherita" : "(.)", 
          "capricciosa" : "(*)", 
          "diavola" : "(@)",
          "ananas" : "(,)"}

class BlockingSet(set):

    def __init__(self, size = 10):
        super().__init__()
        self.size = size
        self.lock = RLock()
        self.condition = Condition(self.lock)

    def add(self,T):
        with self.lock:
            while len(self) == self.size:
                self.condition.wait()
            self.condition.notify_all()
            return super().add(T)

    def remove(self,T):
        with self.lock:
            while not T in self:
                self.condition.wait()
            super().remove(T)
            self.condition.notify_all()
            return True
        

class Pizzeria:
    def __init__(self):
        # Dobbiamo creare una coda per gli ordini
        # e un Buffer per le pizze 

        # Creiamo la coda per gli ordini di al massimo 10 elementi
        self.ordini = Queue(10) 


        # Creiamo il buffer per le pizze di al massimo 10 elementi
        self.pizze = BlockingSet() 

    def getOrdine(self):
        return self.ordini.get() 
    
    def putOrdine(self, ordine):
        self.ordini.put(ordine)

    def getPizza(self, pizza):
        return self.pizze.remove(pizza) 
    
    def putPizza(self, pizza):
        self.pizze.add(pizza)

# Ora creiamo la classe ordine 

class Ordine:
    nextCodiceOrdine = 0
    def __init__(self,tipoPizza,quantita):
        self.tipoPizza = tipoPizza
        self.quantita = quantita
        self.codiceOrdine = Ordine.nextCodiceOrdine
        self.pizzePronte = ""
        Ordine.nextCodiceOrdine += 1

    def prepara(self):
        for i in range(self.quantita):
            self.pizzePronte += pizze[self.tipoPizza]



# Ora creiamo la classe Cliente

class Cliente(Thread):
    def __init__(self,pizzeria,tipoPizza,quantita):
        super().__init__()
        self.pizzeria = pizzeria
        self.tipoPizza = tipoPizza
        self.quantita = quantita

    def run(self):
        while True: 
            print(f"{current_thread().getName()} ha ordinato {self.quantita} {self.tipoPizza}")
            self.pizzeria.putOrdine(Ordine(self.tipoPizza,self.quantita))
            print(f"{current_thread().getName()} ha ordinato {self.quantita} {self.tipoPizza}")

            time.sleep(randint(1,5))
            pizze = self.pizzeria.getPizza(self.tipoPizza)

            print(f"{current_thread().getName()} ha ritirato {self.quantita} {self.tipoPizza}")

            time.sleep(randint(1,5))  

# Ora creiamo la classe Pizzaiolo

class Pizzaiolo(Thread):
    def __init__(self,pizzeria):
        super().__init__()
        self.pizzeria = pizzeria

    def run(self):
        while True:
            ordine = self.pizzeria.getOrdine()
            ordine.prepara()
            print(f"Il pizzaiolo ha preparato {ordine.quantita} {ordine.tipoPizza}")
            self.pizzeria.putPizza(ordine.pizzePronte)
            print(f"Il pizzaiolo ha preparato {ordine.quantita} {ordine.tipoPizza}")

            time.sleep(randint(1,5)) 


def main(): 
    pizzeria = Pizzeria()

    for i in range(10):
        Cliente(pizzeria,"margherita",1).start()
        Cliente(pizzeria,"capricciosa",1).start()
        Cliente(pizzeria,"diavola",1).start()
        Cliente(pizzeria,"ananas",1).start()

    for i in range(2):
        Pizzaiolo(pizzeria).start() 


if __name__ == "__main__": 
    main() 