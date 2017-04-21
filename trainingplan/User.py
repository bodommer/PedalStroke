from trainingplan.Season import Season

class User:
    def __init__(self, id=0):
        self.id = id

    def setName(self, name):
        if type(name) == str and 0 < len(name) < 21:
            self.name = name
            return True
        else:
            return False
        
    def getName(self):
        try:
            return self.name
        except:
            return None
        
    def setAge(self, age):
        if type(age) == int and 99 > age > 14:
            self.age = age
            return True
        else:
            return False

    def getAge(self):
        try:
            return self.age
        except:
            return None

    def setcp60(self, cp60):
        if type(cp60) == int and 500 > cp60 > 1:
            self.cp60 = cp60
            return True
        else:
            return False

    def getcp60(self):
        try:
            return self.cp60
        except:
            return None

    def setmaxHR(self, maxHR):
        if type(maxHR) == int and 100 < maxHR < 240:
            self.maxHR = maxHR
            return True
        else:
            return False

    def getmaxHR(self):
        try:
            return self.maxHR
        except:
            return None

    def setYearsOfExperience(self, yearsOfExperience):
        if type(yearsOfExperience) == int and -1 < yearsOfExperience < 99:
            self.yearsOfExperience = yearsOfExperience
            return True
        else:
            return False

    def getYearsOfExperience(self):
        try:
            return self.yearsOfExperience
        except:
            return None
        
    def setStrong1(self, strong1):
        if strong1 == '':
            self.strong1 = 'Endurance'
        else:
            self.strong1 = strong1

    def getStrong1(self):
        try:
            return self.strong1
        except:
            return None

    def setStrong2(self, strong2):
        self.strong2 = strong2

    def getStrong2(self):
        try:
            return self.strong2
        except:
            return None

    def setWeak1(self, weak1):
        self.weak1 = weak1

    def getWeak1(self):
        try:
            return self.weak1
        except:
            return None

    def setWeak2(self, weak2):
        self.weak2 = weak2

    def getWeak2(self):
        try:
            return self.weak2
        except:
            return None
        
    def loadSeasons(self, userID):
        #nacitanie sezon z databazy
        #return list_of_seasons ako list
        pass 

    def newSeason(self, id=0):
        season = Season(id)
        # pridat do databazy pretekov pre usera/sezonu
