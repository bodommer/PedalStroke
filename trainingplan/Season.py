import pymysql
import pymysql.cursors
import datetime
from trainingplan.Plan import Plan, PlanWeek, PlanWeekDay

class Season:
    def __init__(self, id=0):
        self.id = id
        self.races = []

    def __str__(self):
        return str(self.id)

    def setYear(self, year, userID):
        dateNow = datetime.date.today()
        seasonYear = dateNow.year - 1
        if year > seasonYear and year < (seasonYear + 25):
            self.year = year
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            get_years = ("SELECT year FROM tp_season WHERE user_id={}".format(userID))
            a.execute(get_years)
            years = a.fetchall()
            for y in years:
                if y['year'] == year:
                    a.close()
                    conn.close()
                    return ['already exists']
            return []
        else:
            return ['wrong year']
        
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

    def createSeason(self, year, userID=0):
        self.errordata = self.setYear(year, userID)
        if self.errordata != []:
            return
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        add_season = ("INSERT INTO tp_season VALUES (%s, %s, %s)")
        data_season = (id, year, userID)
        a.execute(add_season, data_season)
        conn.commit()
        get_season_id = ("SELECT id FROM tp_season WHERE year={} AND user_id={}".format(year, userID))
        a.execute(get_season_id)
        self.id = a.fetchone()
        a.close()
        conn.close()

    def loadSeason(self):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_season = ("SELECT * FROM tp_season WHERE user_id={} ORDER BY year ASC".format(self.id))
        a.execute(get_season)
        data = a.fetchall()
        a.close()
        conn.close()
        self.errordata = self.setYear(year, userID)
        
        

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
        