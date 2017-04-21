import datetime
from trainingplan.Plan import Plan, PlanWeek, PlanWeekDay

class Season:
    def __init__(self, id=0):
        self.id = id
        self.races = []

    def __str__(self):
        return str(self.id)

    def setYear(self, year):
        dateNow = datetime.date.today()
        seasonYear = dateNow.year - 1
        if year > seasonYear and year < (seasonYear + 25):
            self.year = year
            return True
        else:
            return False
        
    def getYear(self):
        try:
            return self.year
        except:
            return None

    def newPlan(self, id=0):
        #pridat do databzy planov danej sezony
        plan = Plan(id)

    def newRace(self, id=0):
        #pridat do databazy pretekov danej sezony
        race = Race(id)

class Race:
    def __init__(self, id=0):
        self.id = id

    def setName(self, name):
        if type(name) == str and 0 < len(name) < 40:
            self.name = name
            return True
        else:
            return False

    def getName(self):
        try:
            return self.name
        except:
            return None

    def setDate(self, date):
        now = date.today()
        if now < date:
            self.date = date
            return True
        else:
            return False

    def getDate(self):
        try:
            return self.date
        except:
            return None

    def setPriority(self, priority):
        if 0 < priority < 4:
            self.priority = priority
            return True
        else:
            return False

    def getPriority(self):
        try:
            return self.priority
        except:
            return None

    def setTime(self, time):
        if isinstance(time, datetime.time):
            if time.hour < 168:
                self.time = time
            return True
        else:
            return False

    def getTime(self):
        try:
            return self.time
        except:
            return None