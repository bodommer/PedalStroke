import datetime
import pymysql
import pymysql.cursors
from datetime import date

class Plan:
    def __init__(self, id=0):
        self.id = id
        
    def createPlan(self, annualHours, season, typeOfPlan, planStart, planEnd, activeUser, age, seasonID, id=0):
        wrongdata = []
        if not self.setAnnualHours(annualHours):
            wrongdata.append('annual hours')
        if not self.setTypeOfPlan(typeOfPlan):
            wrongdata.append('type of plan')
        if not self.setPlanStart(planStart):
            wrongdata.append('start of plan - must be monday')
        if not self.setPlanEnd(planEnd):
            wrongdata.append('end of plan')
        if wrongdata != []:
            wrongdata = ', '.join(wrongdata)
            self.wrongdata = wrongdata
            return
        weeksCount = (self.planEnd - self.planStart).days // 7 + 1      #spocita ake dlhe je obdobie
        planWeeks = self.createPlanWeeks(weeksCount, season)     #vytvori treningove tyzdne - urci tyzden + pondelok, priradi tyzdnom zoznam pretekov
        peak = self.whenIsPeakRace(planWeeks, weeksCount)        #vrati cisla tyzdnov, kedy su Ackove preteky 
        peakPeriods = self.makePeakPeriods(peak, activeUser, age)        #spravi zavodne obdobia na zaklade Ackovych pretekov
        self.assignRaceWeeks(planWeeks, peakPeriods)
        if peakPeriods == []:
            self.setOtherWeeks(planWeeks, weeksCount-1, typeOfPlan, weeksCount-1, age)   
        else:         
            self.setOtherWeeks(planWeeks, weeksCount-1, typeOfPlan, peakPeriods[0], activeUser)
        self.setSkillTraining(planWeeks, activeUser, annualHours)
        self.planWeeks = planWeeks
        self.setAllRaces(season)
        self.correct = True
        self.wrongdata = wrongdata
        # po dokonceni vytvarania planu zacne ukladat data do databazy (ak vsetko prebehlo v poriadku a spravne)
        if self.wrongdata == []:
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
            for p in self.planWeeks:
                add_planWeek = ("INSERT INTO tp_planweek VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_planWeek = (id, p.getAEndurance(), p.getEForce(), p.getEndurance(), p.getForce(), p.getGym(), p.getMaxPower(), p.getMonday(), p.getPeriod(), p.getSpeedSkills(), p.getTest(), p.getWeek(), p.getWeeklyHours(), p.getRace(), planID)
                a.execute(add_planWeek, data_planWeek)
                conn.commit()
            a.close()
            conn.close()

    def setAnnualHours(self, annualHours):
        if type(annualHours) == int and annualHours%50 == 0:
            self.annualHours = annualHours
            return True
        return False

    def getAnnualHours(self):
        try:
            return self.annualHours
        except:
            return None
        
    def setTypeOfPlan(self, typeOfPlan):
        self.typeOfPlan = typeOfPlan
        return True

    def getTypeOfPlan(self):
        try:
            return self.typeOfPlan
        except:
            return None 
        
    def setPlanStart(self, start):
        now = date.today()
        a = (start - datetime.date(1970, 1, 5))
        if a.days%7 == 0:
            if now <= start:
                self.planStart = start
                return True
        self.planStart = False
        return False

    def getPlanStart(self):
        try:
            return self.planStart
        except:
            return None
        
    def setPlanEnd(self, end):
        if self.planStart:
            if self.planStart < end and end - self.planStart < datetime.timedelta(days=367):
                self.planEnd = end
                return True
        return False

    def getPlanEnd(self):
        try:
            return self.planEnd
        except:
            return None
        
    def createPlanWeeks(self, weeksCount, season):
        planWeeks = [0]*weeksCount
        for i in range(weeksCount):
            weekplan = PlanWeek()
            weekplan.setWeek(i+1)
            weekplan.setMonday(self.planStart + i*datetime.timedelta(days=7))
            weekplan.setPeriod('')
            weekplan.setGym(False)
            weekplan.setEndurance(False)
            weekplan.setForce(False)
            weekplan.setSpeedSkills(False)
            weekplan.setEForce(False)
            weekplan.setAEndurance(False)
            weekplan.setMaxPower(False)
            weekplan.setTest(False)
            planWeeks[i] = weekplan
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_races = ("SELECT date FROM tp_seasonrace WHERE season_id={} AND priority=3".format(season))
        a.execute(get_races)
        for data in a:     #priradzovanie pretekov k tyzdnom
            for week in planWeeks:      #skusa pre kazdy tyzden:
                mon = week.getMonday()
                if mon <= data['date'] < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                    week.setRace(data)
                    break
        a.close()
        conn.close()
        return planWeeks
        
    def whenIsPeakRace(self, planWeeks, weeksCount):
        peaks = []
        for i in range(weeksCount-1, -1, -1):
            for r in planWeeks[i].races:
                if i not in peaks:
                    peaks.append(planWeeks[i].week)
        return peaks
    
    def makePeakPeriods(self, peak, activeUser, age):   
        if peak == []:
            return [] 
        if age > 40: #or gender = woman
            shorterPeriods = 1
        else:
            shorterPeriods = 0
        if len(peak) == 1:
            if peak[0] > 5 - shorterPeriods:
                return list([peak[0]])
                pass
            else:
                return []
        else:
            peakPeriods = []
            ref = 0
            while ref != peak[-1]:
                for i in range(1, 3):
                    if peak[ref] - peak[ref+i] < 3:
                        if peak[ref+i] < 6 - shorterPeriods:
                            peak.pop(ref+i)
                        else:
                            peakPeriods.append([range(ref, ref+i+1)])
                            ref = peak[ref+i]
            return peakPeriods
            
    def assignRaceWeeks(self, planWeeks, racePeriods):
        for week in planWeeks:
            if week.getWeek() in racePeriods:
                week.setPeriod('Racing-1')
    
    def setOtherWeeks(self, planWeeks, weekNumber, typ, peak0, age):
        index = 0
        if age > 39: #or gender = woman
            if typ == 'normal':
                periods = ['Peak 2', 'Peak 1', 
                           'Build 2-4', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-2', 'Build 1-1', 
                           'Base 3-4', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-2', 'Base 1-1',
                           'Preparatory-1']
            elif typ == 'reversed':
                periods = ['Peak 2', 'Peak 1', 
                           'Base 3-4','Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-2', 'Base 1-1', 
                           'Build 2-4', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-2', 'Build 1-1',
                           'Preparatory-1']
        else:
            if typ == 'normal':
                periods = ['Peak 2', 'Peak 1', 
                           'Build 2-4', 'Build 2-3', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-3', 'Build 1-2', 'Build 1-1', 
                           'Base 3-4', 'Base 3-3', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-3', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-3', 'Base 1-2', 'Base 1-1',
                           'Preparatory-1']
            elif typ == 'reversed':
                periods = ['Peak 2', 'Peak 1', 
                           'Base 3-4', 'Base 3-3', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-3', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-3', 'Base 1-2', 'Base 1-1', 
                           'Build 2-4', 'Build 2-3', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-3', 'Build 1-2', 'Build 1-1',
                           'Preparatory-1']
        if weekNumber > len(periods):
            for i in range(weekNumber-len(periods)+1):
                periods.append('Preparatory-1') 
        while weekNumber > -1:
            if weekNumber > 43 and weekNumber > peak0:
                planWeeks[weekNumber].setPeriod('Recovery-1')
            else:
                if planWeeks[weekNumber].getPeriod() == 'Racing-1':
                    index = 0
                else:
                    planWeeks[weekNumber].setPeriod(periods[index])
                    index += 1
            weekNumber -= 1
        for i in range(len(planWeeks)):
            if planWeeks[i].getPeriod() == 'Racing-1':
                if planWeeks[i-1].getPeriod == 'Racing-1':
                    planWeeks[i+2].setPeriod('Recovery-1')
                planWeeks[i+1].setPeriod('Recovery-1')
        
    def setSkillTraining(self, planWeeks, activeUser, annualHours):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_props = ("SELECT weak1, weak2, strong1, strong2 FROM tp_user WHERE id={}".format(activeUser))
        a.execute(get_props)
        data = a.fetchone()
        a.close()
        conn.close() 
        weak = data['weak1']
        weak2 = data['weak2']
        strong = data['strong1']
        strong2 = data['strong2']
        if True:
        #if activeUser.getAge() < 40: #pre 4-tyzdnove cykly
            for week in planWeeks:
                periodName = week.getPeriod()[:4]
                try:
                    periodCount = int(week.getPeriod()[-3])
                    weekCount = int(week.getPeriod()[-1])
                except:
                    periodCount = 1
                    weekCount = 1
                if periodName == 'Prep':
                    week.setEndurance(True)
                    week.setSpeedSkills(True)
                    if 0 < weekCount < 3:
                        week.setGym('MT')
                    elif 2 < weekCount < 6:
                        week.setGym('AA') 
                        
                if weekCount != 4:
                    if periodName == 'Base':
                        week.setEndurance(True)
                        week.setSpeedSkills(True)    
                        if periodCount != 1:
                            week.setForce(True)
                            week.setEForce(True)
                        else:
                            week.setGym('MP')
                        
                    if periodName == 'Buil':
                        week.setEForce(True)
                        week.setEndurance(True)
                        if periodCount == 1:
                            if weak == '':
                                week.setForce(True)
                            else:
                                if weak == 'AEndurance':
                                    week.setAEndurance(True)
                                elif weak == 'Force':
                                    week.setForce(True)
                                elif weak == 'SpeedSkills':
                                    week.setSpeedSkills(True)
                                elif weak == 'MaxPower':
                                    week.setMaxPower(True)
                            if weak not in ('AEndurance', 'MaxPower'):
                                week.setSpeedSkills(True)  
                                
                        else:
                            if weak in ('', 'Force'):
                                week.setForce(True)
                            else:
                                if weak == 'AEndurance':
                                    week.setAEndurance(True)
                                elif weak == 'SpeedSkills':
                                    week.setSpeedSkills(True)
                                elif weak == 'MaxPower':
                                    week.setMaxPower(True)
                            a = False
                            if week.getRace() != []:
                                a = True
                            if a:
                                if weak2 == '':
                                    week.setAEndurance(True)
                                else:
                                    if weak2 == 'AEndurance':
                                        week.setAEndurance(True)
                                    elif weak2 == 'Force':
                                        week.setForce(True)
                                    elif weak2 == 'SpeedSkills':
                                        week.setSpeedSkills(True)
                                    elif weak2 == 'MaxPower':
                                        week.setMaxPower(True)         
            
                    if periodName == 'Peak':
                        week.setEForce(True)
                        if weak == '':
                            week.setAEndurance(True)
                        else:
                            if weak == 'AEndurance':
                                week.setAEndurance(True)
                            elif weak == 'Force':
                                week.setForce(True)
                            elif weak == 'SpeedSkills':
                                week.setSpeedSkills(True)
                            elif weak == 'MaxPower':
                                week.setMaxPower(True)  
                            elif weak == 'Endurance':
                                week.setSpeedSkills(True)
                            elif weak == 'EForce':
                                week.setEForce(True)                      
        
                    if periodName == 'Raci':
                        week.setAEndurance(True)
                        week.setSpeedSkills(True)
                        if strong in ('', 'Endurance', 'EForce'):
                            week.setEForce(True)
                        else:
                            if strong == 'MaxPower':
                                week.setMaxPower(True)  
                            if strong == 'Force':
                                week.setForce(True)
                        
                    if periodName == 'Reco':
                        week.setEndurance(True)
                else:
                    week.setEndurance(True)
                    week.setSpeedSkills(True)
                    week.setTest(True)
                    week.setGym('FM')
            for week in planWeeks:
                if not week.getForce():
                    if week.getPeriod()[:4] in ('Buil', 'Base'):
                        week.setGym('FM')
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            get_hrs = ("SELECT * FROM weeklyhours WHERE annualHours={}".format(annualHours))
            a.execute(get_hrs)
            data = a.fetchone()
            a.close()
            conn.close()
            for week in planWeeks:
                period = data['{}'.format(week.getPeriod())]
                week.setWeeklyHours(period)
 
    def setAllRaces(self, season): 
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_races = ("SELECT * FROM tp_seasonrace WHERE season_id={}".format(season))
        a.execute(get_races)
        if a:
            for data in a:     #priradzovanie pretekov k tyzdnom
                for week in self.planWeeks:      #skusa pre kazdy tyzden:
                    week.races = []
                    mon = week.getMonday()
                    if mon <= data['date'] < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                        week.setRace(data['name'])
                        break
        a.close()
        conn.close()
        
    def getPlanData(self):    
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_plan = ("SELECT * FROM tp_planweek WHERE plan_id={} ORDER BY week ASC".format(self.id))
        a.execute(get_plan)
        data = a.fetchall()
        a.close()
        conn.close()
        return data
        
        
class PlanWeek:
    def __init__(self, id=0):
        self.id = id
        self.races = []

    def setWeek(self, week):
        self.week = week

    def getWeek(self):
        try:
            return self.week
        except:
            return None

    def setMonday(self, monday):
        self.monday = monday

    def getMonday(self):
        try:
            return self.monday
        except:
            return None
        
    def setRace(self, race):
        self.races.append(race)
        
    def getRace(self):
        r = '\n'.join(self.races)
        return r

    def setPeriod(self, period, periodWeek=1):
        self.period = period
        self.periodWeek = periodWeek    
    
    def getPeriod(self):
        try:
            return self.period #, self.periodWeek
        except:
            return None
    
    def setWeeklyHours(self, hours):
        self.weeklyHours = hours

    def getWeeklyHours(self):
        try:
            return self.weeklyHours
        except:
            return None

    def getWeeklyHoursFromDB(self, period, week):
        return 5

    def setGym(self, gym):
        self.gym = gym
        
    def getGym(self):
        try:
            return self.gym
        except:
            return None

    def setEndurance(self, endurance):
        self.endurance = endurance

    def getEndurance(self):
        try:
            return self.endurance
        except:
            return None

    def setForce(self, force):
        self.force = force

    def getForce(self):
        try:
            return self.force
        except:
            return None
        
    def setSpeedSkills(self, speedSkills):
        self.speedSkills = speedSkills

    def getSpeedSkills(self):
        try:
            return self.speedSkills
        except:
            return None
        
    def setEForce(self, eForce):
        self.eForce = eForce

    def getEForce(self):
        try:
            return self.eForce
        except:
            return None
        
    def setAEndurance(self, aEndurance):
        self.aEndurance = aEndurance

    def getAEndurance(self):
        try:
            return self.aEndurance
        except:
            return None
        
    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def getMaxPower(self):
        try:
            return self.maxPower
        except:
            return None
        
    def setTest(self, test):
        self.test = test

    def getTest(self):
        try:
            return self.test
        except:
            return None

    def newPlanWeekDay(self, id=0):
        #pridat do databazy dennych planov daneho tyzdna
        planWeekDay = PlanWeekDay(id)

class PlanWeekDay:
    def __init__(self, id=0):
        self.id = id

    def setDay(self, day):
        self.day = day

    def getDay(self):
        try:
            return self.day
        except:
            return None

    def setWorkoutType(self, workoutType):
        self.workoutType = workoutType

    def getWorkoutType(self):
        try:
            return self.workoutType
        except:
            return None

    def setDailyHours(self, dailyHours):
        self.dailyHours = dailyHours

    def getDailyHours(self):
        try:
            return self.dailyHours
        except:
            return None

    def setIntensity(self, intensity):
        self.intensity = intensity

    def getIntensity(self):
        try:
            return self.intensity
        except:
            return None