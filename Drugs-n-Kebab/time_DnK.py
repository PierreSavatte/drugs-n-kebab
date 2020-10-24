import time

class Time:
    
    def __init__(self):
        self.temps_depart = time.time()
        self.temps_horloge_depart = '10:00'
        self.temps_depart_pause = None
        self.decalage = 0
        self.pause = False
        return
    
    def set_pause(self):
        self.temps_depart_pause = self.get_time()
        self.pause = True
        return
    
    def set_continuer(self):
        self.pause = False
        temps_fin_pause = self.get_time()
        self.decalage += temps_fin_pause - self.temps_depart_pause
        return
    
    def get_time(self):
        if not(self.pause):
            return time.time() - self.decalage
        else:
            return self.temps_depart_pause
    
    def est_en_pause(self):
        return self.pause
    
    def inverser(self):
        if self.pause:
            self.set_continuer()
        else:
            self.set_pause()
        return
    
    def get_temps_horloge(self):
        temps_actuel = self.get_time()
        diff_temps = int(temps_actuel - self.temps_depart)
        heure = int(self.temps_horloge_depart[:2])
        minute = int(self.temps_horloge_depart[3:])
        while diff_temps != 0:
            if diff_temps >= 60:
                heure +=1
                diff_temps -=60
            else:
                minute += 1
                diff_temps -=1
                if minute == 60:
                    minute = 0
                    heure +=1
            if heure == 24:
                heure = 0
        if minute < 10:
            temps_horloge_actuel = str(heure)+":"+'0'+str(minute)
        else:
            temps_horloge_actuel = str(heure)+":"+str(minute)
        return temps_horloge_actuel