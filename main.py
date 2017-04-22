import datetime
import pymysql
import pymysql.cursors
import tkinter as tk
from trainingplan.User import User
from trainingplan.Plan import Plan
from trainingplan.Season import Race, Season
from desktop.desktop import Desktop
from desktop.graph import Graph
from pip._vendor.requests.api import delete

class Program:
    def __init__(self):
        root = tk.Tk()
        self.gui = Desktop(self, root)
        #self.gui.title('pedalstroke')
        self.gui.mainloop()
        
    def createUser(self, name, age, cp60, maxHR, yearsOfExperience, strong1, strong2, weak1, weak2, id=0):
        self.activeUser = User(id)
        self.activeUser = self.activeUser.createUser(name, age, cp60, maxHR, yearsOfExperience, strong1, strong2, weak1, weak2, id)
        if type(self.activeUser.errordata) == str:
            pass
            # vypisat chybove hlasenie
        else:
            #len nacitat user hub
            pass
        
    def loadUser(self, user_id=0):
        self.activeUser = User(user_id)
        self.activeUser.loadUser(user_id)
        #vypisat user hub
        ### chyba??? - DOROBIT
    
    #===========================================================================
    # def showUserData(self, user_id):
    #     conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    #     a=conn.cursor()
    #     get_user = ("SELECT * FROM tp_user WHERE id={} ORDER BY name ASC".format(user_id))
    #     a.execute(get_user)
    #     data = a.fetchone()
    #     a.close()
    #     conn.close()
    #     return data
    #===========================================================================
    
    def createSeason(self, year, id=0):
        self.activeSeason = Season(id)
        self.activeSeason.createSeason(year, self.activeUser.id)
        if self.activeSeason.errordata == []:
            pass
            #zobrazit season hub
        else:
            #chybova prava, navrat na user hub
            pass

    def getUserSeasons(self):
        seasons = self.activeUser.getUserSeasons()      
        # poslat dalej

    def getSeasonPlans(self, season_id):
        self.activeSeason = Season(season_id)
        self.activeSeason.loadSeason()
        if self.activeSeason.errordata == []:
            seasonPlans = self.activeSeason.getPlans()
            
            #zobrazit season hub
        else:
            #something went wrong message
            pass

    
    def deleteSeason(self, season_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_season = ("DELETE FROM tp_season WHERE id={}".format(season_id))
        #print(delete_season)
        a.execute(delete_season)
        conn.commit()
        a.close()
        conn.close()    
        return True
    
    def deleteUser(self):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_user = ("DELETE FROM tp_user WHERE id={}".format(self.activeUser))
        a.execute(delete_user)
        conn.commit()
        a.close()
        conn.close()
        return True

        
    def createRace(self, name, date, priority, time, seasonID, id=0):
        errordata = []
        race = Race(id)
        if not race.setName(name):
            errordata.append('name')
        if not race.setDate(date):
            errordata.append('date')
        if not race.setPriority(priority):
            errordata.append('priority')
        if not race.setTime(time):
            errordata.append('time')
        if errordata == []:
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            add_race = ("INSERT INTO tp_seasonrace VALUES (%s, %s, %s, %s, %s, %s)")
            data_race = (id, race.getDate(), race.getName(), race.getPriority(), race.getTime(), seasonID)
            a.execute(add_race, data_race)
            conn.commit()
            a.close()
            conn.close()    
        if errordata != []:
            errordata = ', '.join(errordata)
        return errordata
    
    def showRaceData(self, season_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_race = ("SELECT * FROM tp_seasonrace WHERE season_id={} ORDER BY date ASC".format(season_id))
        a.execute(get_race)
        data = a.fetchall()
        a.close()
        conn.close()
        return data
    
    def deleteRace(self, race_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_race = ("DELETE FROM tp_seasonrace WHERE id={}".format(race_id))
        a.execute(delete_race)
        conn.commit()
        a.close()
        conn.close()
    
    def createPlan(self, annualHours, seasonID, typeOfPlan, planStart, planEnd, activeUserID, id=0):
        age = self.loadUser(activeUserID)['age']
        plan = Plan(annualHours, seasonID, typeOfPlan, planStart, planEnd, activeUserID, age, id=0)
        if plan.wrongdata == []:
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            add_plan = ("INSERT INTO tp_plan VALUES (%s, %s, %s, %s, %s, %s)")
            data_plan = (id, annualHours, typeOfPlan, planStart, planEnd, seasonID)
            a.execute(add_plan, data_plan)
            conn.commit()
            get_id = ("SELECT id FROM tp_plan WHERE annualHours={} AND season_id={}".format(annualHours, seasonID))
            a.execute(get_id)
            planID = a.fetchone()
            planID = planID['id']
            for p in plan.planWeeks:
                add_planWeek = ("INSERT INTO tp_planweek VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_planWeek = (id, p.getAEndurance(), p.getEForce(), p.getEndurance(), p.getForce(), p.getGym(), p.getMaxPower(), p.getMonday(), p.getPeriod(), p.getSpeedSkills(), p.getTest(), p.getWeek(), p.getWeeklyHours(), p.getRace(), planID)
                a.execute(add_planWeek, data_planWeek)
                conn.commit()
            a.close()
            conn.close()
        return plan.wrongdata
        
    def showSeasonPlan(self, season_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_plans = ("SELECT * FROM tp_plan WHERE season_id={} ORDER BY planStart ASC".format(season_id))
        a.execute(get_plans)
        data = a.fetchall()
        a.close()
        conn.close()
        return data
                               
    def showPlan(self, plan_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_plan = ("SELECT * FROM tp_planweek WHERE plan_id={} ORDER BY week ASC".format(plan_id))
        a.execute(get_plan)
        data = a.fetchall()
        a.close()
        conn.close()
        return data
    
    def showPlanWeek(self, plan_id):
        #zobrazia sa vsetky dni daneho tyzdna
        pass
    
    def deletePlan(self, plan_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_plan = ("DELETE FROM tp_plan WHERE id={}".format(plan_id))
        a.execute(delete_plan)
        conn.commit()
        a.close()
        conn.close()

#===============================================================================
# activeUser = createUser('Andrej', 20, 200, 180, 2, 'endurance', 'speed skills', 'anaerobic endurance', 'max power')
# print('hotovo')
#  season = createSeason(2017, id=1)
#  season.races.append(createRace('Preteky Mieru', datetime.date(2017, 8, 1), 3, datetime.time(2, 34),id=2))
#  print(season.races[0].getName())
#  createPlan(600, season, 'reversed', datetime.date(2017, 4, 1), datetime.date(2018, 4, 1), activeUser, id=3)
#  print('Tyz Pon          Obdobie           End   For   SpSk  EFor  AEnd  MxPw Gym')
#  for tyzd in season.plans[0].planWeeks:
#      print('{:02}  {}   {:<13} {:5} {:5} {:5} {:5} {:5} {:5}    {}'.format(tyzd.getWeek(), tyzd.getMonday(), tyzd.getPeriod(), tyzd.getEndurance(),
#                                                            tyzd.getForce(), tyzd.getSpeedSkills(), tyzd.getEForce(), tyzd.getAEndurance(),
#                                                           tyzd.getMaxPower(), tyzd.getGym()))
# activeUser = loadUser(30)
# season = createSeason(2017, activeUser)
# season = 1
# print(createRace('Preteky mieru', datetime.date(2017, 5, 4), 3, datetime.time(2, 3, 1), season))
# createPlan(300, season, 'reversed', datetime.date(2017, 4, 1), datetime.date(2018, 4, 1), activeUser)
# print('hotovo')
# print(activeUser.id)
#===============================================================================
if __name__ == '__main__':
    prog = Program()