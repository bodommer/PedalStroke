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
        self.activeUser = self.activeSeason = self.activePlan = None
        root = tk.Tk()
        self.gui = Desktop(self, root)
        self.gui.chooseUser(self.getListOfUsers())
        self.gui.mainloop()
        
    def createUser(self, name, age, cp60, maxHR, yearsOfExperience, strong1, strong2, weak1, weak2, id=0):
        self.activeUser = User(id)
        self.activeUser = self.activeUser.createUser(name, age, cp60, maxHR, yearsOfExperience, strong1, strong2, weak1, weak2, id)
        if type(self.activeUser.errordata) == str:
            self.gui.newUserWindow(self.activeUser.errordata)
            self.gui.messageBox('Wrong data', 'Some of the data you entered were in a wrong format!')
        else:
            self.gui.displayUserData({'name': name, 'age':age, 'cp60':cp60, 'maxHR':maxHR, 'yearsOfExperience':yearsOfExperience, 'strong1':strong1, 'strong2':strong2, 'weak1':weak1, 'weak2':weak2})
            
    def chosenUser(self, selected):
        if selected == 'Create user':
            self.gui.newUserWindow()
        else:
            for user in self.getListOfUsers():
                if user['name'] == selected:
                    activeUser = user['id']
                    break
            self.loadUser(activeUser)

        
    def loadUser(self, user_id=0):
        if self.activeUser is None:
            self.activeUser = User(user_id)
            self.activeUser.loadUser(user_id)
        self.gui.displayUserData({'name': self.activeUser.getName(), 'age':self.activeUser.getAge(), 'cp60':self.activeUser.getcp60(), 'maxHR':self.activeUser.getmaxHR(), 
                                  'yearsOfExperience':self.activeUser.getYearsOfExperience(), 'strong1':self.activeUser.getStrong1(), 'strong2':self.activeUser.getStrong2(), 
                                  'weak1':self.activeUser.getWeak1(), 'weak2':self.activeUser.getWeak2()}, self.getUserSeasons())
        ### chyba??? - DOROBIT
        
    def getListOfUsers(self):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_users = ("SELECT name, id FROM tp_user")
        a.execute(get_users)
        data = a.fetchall()
        a.close()
        conn.close()
        return data
        
        
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

    def getUserSeasons(self):
        self.seasonData = self.activeUser.getUserSeasons()      
        return self.seasonData

    def deleteUser(self):
        if self.activeUser.deleteUser():
            self.gui.chooseUser()
        else:
            self.gui.messageBox("Delete user error", "User was not deleted")
    
    def createSeason(self, year, id=0):
        self.activeSeason = Season(id)
        self.activeSeason.createSeason(year, self.activeUser.id)
        if self.activeSeason.errordata == []:
            self.getSeasonPlans()
        else:
            self.gui.displayUserData({'name': self.activeUser.getName(), 'age':self.activeUser.getAge(), 'cp60':self.activeUser.getcp60(), 'maxHR':self.activeUser.getmaxHR(), 
                                      'yearsOfExperience':self.activeUser.getYearsOfExperience(), 'strong1':self.activeUser.getStrong1(), 'strong2':self.activeUser.getStrong2(), 
                                      'weak1':self.activeUser.getWeak1(), 'weak2':self.activeUser.getWeak2()}, self.getUserSeasons())
            self.gui.messageBox("Season creation error", "This season already exists!")
    
    def getSeasonRaces(self, season_id):
        if season_id != self.activeSeason.id:
            season = Season(season_id)
            data = season.getSeasonRaces()
        else:
            data = self.activeSeason.getSeasonRaces()
        #zavola funnkciu na zobrazovanie 
        
    def getSeasonPlans(self, season_id=0):
        if self.activeSeason is None and not season_id:
            self.activeSeason = Season(season_id)
            self.activeSeason.loadSeason()
        if self.activeSeason.errordata == []:
            self.gui.displaySeasonPlans(self.activeSeason.getPlans(), self.activeSeason.getYear())
        else:
            self.gui.displayUserData({'name': self.activeUser.getName(), 'age':self.activeUser.getAge(), 'cp60':self.activeUser.getcp60(), 'maxHR':self.activeUser.getmaxHR(), 
                                      'yearsOfExperience':self.activeUser.getYearsOfExperience(), 'strong1':self.activeUser.getStrong1(), 'strong2':self.activeUser.getStrong2(), 
                                      'weak1':self.activeUser.getWeak1(), 'weak2':self.activeUser.getWeak2()}, self.getUserSeasons())
            self.gui.messageBox("Season loading error", "Something went wrong!")
        
    def deleteSeason(self, season_id):
        self.activeUser.deleteSeason(season_id)
        self.activeSeason = None
        #znovu nacitat user hub

    def createRace(self, name, year, month, day, priority, hour, minute, id=0):
        name = self.widgets['name'].get()
        date = datetime.date(int(year)+2000, int(month), int(day))
        priority = int(priority)
        time = datetime.time(int(hour), int(minute))
        season_id = self.activeSeason.id
        race = Race(id)
        race.createRace(name, date, priority, time, season_id)
        
        if race.errordata == []:
            self.gui.displayUserData({'name': self.activeUser.getName(), 'age':self.activeUser.getAge(), 'cp60':self.activeUser.getcp60(), 'maxHR':self.activeUser.getmaxHR(), 
                                      'yearsOfExperience':self.activeUser.getYearsOfExperience(), 'strong1':self.activeUser.getStrong1(), 'strong2':self.activeUser.getStrong2(), 
                                      'weak1':self.activeUser.getWeak1(), 'weak2':self.activeUser.getWeak2()}, self.getUserSeasons())
        else:
            self.gui.messageBox("Race creation error", "Race was not added:\nInput data were probably wrong")
            self.gui.newRaceWindow(1, self.season, race.errordata)

    def deleteRace(self, race_id):
        if self.activeSeason is not None:
            self.activeSeason.deleteRace(race_id)
        else:
            season = Season(1)
            season.deleteRace(race_id)
        self.gui.displayUserData({'name': self.activeUser.getName(), 'age':self.activeUser.getAge(), 'cp60':self.activeUser.getcp60(), 'maxHR':self.activeUser.getmaxHR(), 
                                  'yearsOfExperience':self.activeUser.getYearsOfExperience(), 'strong1':self.activeUser.getStrong1(), 'strong2':self.activeUser.getStrong2(), 
                                  'weak1':self.activeUser.getWeak1(), 'weak2':self.activeUser.getWeak2()}, self.getUserSeasons())
    
    def createPlan(self, annualHours, typeOfPlan, startYear, startMonth, startDay, endYear, endMonth, endDay, id=0):
        annualHours = int(annualHours)
        planStart = datetime.date(int(startYear)+2000, int(startMonth), int(startDay))        
        planEnd = datetime.date(int(endYear)+2000, int(endMonth), int(endDay))
        if typeOfPlan == 1:
            typeOfPlan = 'normal'
        else:
            typeOfPlan = 'reversed' 
        self.activePlan = Plan(id)
        self.activePlan.createPlan(annualHours, self.activeSeason.id, typeOfPlan, planStart, planEnd, self.activeUser.id, self.activeUser.getAge())
        if self.activePlan.errordata == []:
            self.gui.displaySeasonPlans(self.activeSeason.getPlans(), self.activeSeason.getYear())
        else:
            self.newPlanWindow(self.activePlan.errordata) 
                               
    def showPlan(self, plan_id, planInfo):   
        def convert(value):
            if value == 1:
                return 'X'
            else:
                return ' '
            
        self.activePlan = Plan(plan_id)
        data = self.activePlan.getPlanData()
        if data is not None:
            for week in data:
                if week['races'] is None:
                    week['races'] = ''
                for prop in ('gym', 'endurance', 'force', 'speedSkills', 'eForce',
                                 'aEndurance', 'maxPower', 'test'):
                    week[prop] = convert(week[prop])
                    
        self.gui.showPlanWindow(data, planInfo) #zavola metodu na zobrazenie plan hubu

    def deletePlan(self, plan_id):
        self.activeSeason.deletePlan(plan_id)
        self.activePlan = None
        self.getSeasonPlans()
            
    #===========================================================================
    # def getSeasonPlans(self, season_id):
    #
    #     DUPLIKAT
    #
    #     conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    #     a=conn.cursor()
    #     get_plans = ("SELECT * FROM tp_plan WHERE season_id={} ORDER BY planStart ASC".format(season_id))
    #     a.execute(get_plans)
    #     data = a.fetchall()
    #     a.close()
    #     conn.close()
    #     return data
    #===========================================================================

    def showPlanWeek(self, plan_id):
        pass #zobrazia sa vsetky dni daneho tyzdna
    
#===============================================================================
# TEST COMMANDS
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