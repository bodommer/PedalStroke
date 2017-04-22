import pymysql
import pymysql.cursors
from trainingplan.Season import Season

class User:
    def __init__(self, id=0):
        self.id = id

    def setName(self, name):
        if type(name) == str and 0 < len(name) < 21:
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            get_names = ("SELECT name FROM tp_user")
            a.execute(get_names)
            names = a.fetchall()
            names = [di['name'] for di in names]
            if name in names:
                    a.close()
                    conn.close()
                    return False
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
        
    def createUser(self, name, age, cp60, maxHR, yearsOfExperience, strong1, strong2, weak1, weak2, id=0):
        errordata = []
        if not self.setName(name):
            errordata.append('username')
        if not self.setAge(age):
            errordata.append('age')
        if not self.setcp60(cp60):
            errordata.append('cp60')
        if not self.setmaxHR(maxHR):
            errordata.append('maximum heart rate')
        if not self.setYearsOfExperience(yearsOfExperience):
            errordata.append('years of experience')
        self.setStrong1(strong1)
        self.setStrong2(strong2)
        self.setWeak1(weak1)
        self.setWeak2(weak2)
        if errordata == []:
            conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            add_user = ("INSERT INTO tp_user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_user = (id, cp60, maxHR, name, strong1, strong2, weak1, weak2, yearsOfExperience, age)
            a.execute(add_user, data_user)
            conn.commit()
            get_user_id = ("SELECT id FROM tp_season WHERE name={}".format(name))
            a.execute(get_user_id)
            self.id = a.fetchone()['id']
            conn.close()
            self.errordata = []
        else:
            string = ', '.join(errordata)
            self.errordata = string 
            
    def loadUser(self, user_id=0):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_user = ("SELECT * FROM tp_user WHERE id={}".format(user_id))
        a.execute(get_user)
        data = a.fetchone()
        a.close()
        conn.close()
        self.setName(data['name'])
        self.setcp60(data['cp60'])
        self.setmaxHR(data['maxHR'])
        self.setStrong1(data['storng1'])
        self.setStrong2(data['strong2'])
        self.setWeak1(data['weak1'])
        self.setWeak2(data['weak2'])
        self.setYearsOfExperience(data['yearsOfExperience'])
        self.setAge(data['age'])
        
    def getUserSeasons(self):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_seasons = ("SELECT id, year FROM tp_season WHERE user_id={}".format(self.id))
        a.execute(get_seasons)
        data = a.fetchall()
        a.close()
        conn.close() 
        return data
    
    def deleteSeason(self, season_id):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_season = ("DELETE FROM tp_season WHERE id={} AND user_ID={}".format(season_id, self.id))
        a.execute(delete_season)
        conn.commit()
        a.close()
        conn.close()     
              
    def deleteUser(self):
        conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        delete_user = ("DELETE FROM tp_user WHERE id={}".format(self.id))
        a.execute(delete_user)
        conn.commit()
        a.close()
        conn.close()
        return True
            
            
            
            
            
            
            
            
            