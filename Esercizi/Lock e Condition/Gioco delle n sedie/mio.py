from threading import Thread,Lock
from time import sleep
from random import random,randrange




# L'Obiettivo è quello di riuscire a creare un codice che mi consenta di
# simulare una situazione dove si possano occupare nel gioco delle n sedie
# le sedie senza incorrere in nessuna race condition.


class PostoSafe: 
    
        def __init__(self):
            self.occupato = False
            self.lock = Lock()

        #Ora dobbiamo creare un metodo che ci permetta di capire se il posto è libero
        #e se libero dobbiamo occuparlo 
        
        #In questo caso conviene unire i due metodi in uno solo per evitare 
        #race condition 

        def testaEoccupa(self):
            with self.lock:
                if (self.occupato):
                    return False
                else:
                    self.occupato = True
                    return True 
                

class PartecipanteSafe(Thread):

    def __init__(self,posti):
        super().__init__()
        self.posti = posti

    def run(self):
        sleep(randrange(5))
        for i in range(0,len(self.posti)):
            if self.posti[i].testaEoccupa():
                print( "Sono il Thread %s. Occupo il posto %d" % ( self.getName(), i ) )
                return                
        
        print( "Sono il Thread %s. HO PERSO" % self.getName() )


class Display(Thread):

    def __init__(self,posti):
        super().__init__()
        self.posti = posti

    def run(self):
        while(True):
            sleep(1)
            for i in range(0,len(self.posti)):
                if self.posti[i].libero():
                    print("-", end='', flush=True)
                else:
                    print("o", end='', flush=True)
            print('')



NSEDIE = 10


posti = [PostoSafe()      for i in range(0,NSEDIE)]

lg = Display(posti)
lg.start()



for t in range(0,NSEDIE+1):
    
    t = PartecipanteSafe(posti)
    t.start()



                

        