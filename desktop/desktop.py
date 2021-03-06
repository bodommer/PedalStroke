import tkinter as tk
from tkinter.constants import DISABLED
import datetime
import pymysql
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
from desktop.graph import Graph
from email.generator import _width

class Desktop(tk.Frame):
    def __init__(self, prog, master=None):
        super().__init__(master, width=1000)
        master.title('PedalStroke v1.0')
        self.master = master
        self.pack()
        self.widgets = {}
        self.program = prog
        
    def chooseUser(self, data):
        self.deleteWindow()
        self.widgets = {}
        self.config()
        
        def chosenUser(event):
            selected = userName.get()
            self.program.chosenUser(selected)

        self.widgets['title'] = tk.Label(self, text='Please, choose user:')
        self.widgets['title'].grid(row=0, columnspan=4)
        
        userName = tk.StringVar(self)
        userName.set('Create user')
        li = []
        li.append('Create user')
        for i in data:
            li.append(i['name'])
        
        self.widgets['dropdown'] =tk.OptionMenu(self, userName, *tuple(li))
        self.widgets['dropdown'].grid(row=1)
        
#===============================================================================
#         self.widgets['scrollbar'] = tk.Scrollbar(self)
#         self.widgets['scrollbar'].grid(column=2, row=1)
# 
#         self.widgets['listbox'] = tk.Listbox(self, height=5, width=30)
#         self.widgets['listbox'].insert(0, "New user")
#         for user in data:
#             self.widgets['listbox'].insert(tk.END, user['name'])
#         self.widgets['listbox'].grid(row=1)
#         self.widgets['listbox'].config(yscrollcommand=self.widgets['scrollbar'].set)
#         self.widgets['scrollbar'].config(command=self.widgets['listbox'].yview)
#===============================================================================
            
        self.widgets['confirm'] = tk.Button(self, text='     Ok     ')
        self.widgets['confirm'].grid(row=4, sticky='W', padx=5, pady=5)
        self.widgets['confirm'].bind('<Button-1>', chosenUser)        
        
        self.widgets['Exit'] = tk.Button(self, text=' Exit ')
        self.widgets['Exit'].grid(row=4, sticky='E', padx=5, pady=5)
        self.widgets['Exit'].bind('<Button-1>', self.exitApp)


    def newUserWindow(self, wrongdata=''):
        self.deleteWindow()
        self.widgets = {}
        
        def createUser(event):
            self.program.createUser(self.widgets['name'].get(), int(self.widgets['age'].get()), int(self.widgets['cp60'].get()), int(self.widgets['maxHR'].get()), int(self.widgets['yearsOfExperience'].get()), self.strong1.get(), self.strong2.get(), self.weak1.get(), self.weak2.get())

        self.widgets['title'] = tk.Label(self, text='Fill in the data according to pre-set values.', anchor='e', font='Arial 12')
        self.widgets['title'].grid(row=0, columnspan=6, padx=10, pady=10)        
        
        if wrongdata != '':
            wrongdata = 'Invalid data in fields: ' + wrongdata
        self.widgets['wrongdata'] = tk.Label(self, text=wrongdata)
        self.widgets['wrongdata'].grid(row=1)   
        
        self.widgets['frame1'] = tk.Frame(self)
        self.widgets['frame1'].grid(row=2, rowspan=10, columnspan=3, padx=5, pady=5)
        
        self.widgets['nameLabel'] = tk.Label(self.widgets['frame1'], text='Username: ')
        self.widgets['nameLabel'].grid(row=0, padx=5, pady=5)
        self.widgets['name'] = tk.Entry(self.widgets['frame1'], justify='center', relief='flat')
        self.widgets['name'].grid(row=0, column=1, padx=5, pady=5)        
        
        self.widgets['ageLabel'] = tk.Label(self.widgets['frame1'], text='Age: ')
        self.widgets['ageLabel'].grid(row=3, padx=5, pady=5)
        self.widgets['age'] = tk.Spinbox(self.widgets['frame1'], from_=15, to=99, justify='center', relief='flat')
        self.widgets['age'].grid(row=3, column=1, padx=5, pady=5)    

        self.widgets['cp60label'] = tk.Label(self.widgets['frame1'], text='CP 60: ')
        self.widgets['cp60label'].grid(row=4, padx=5, pady=5)
        self.widgets['cp60'] = tk.Spinbox(self.widgets['frame1'], from_=80, to=500, increment=5, justify='center', relief='flat')
        self.widgets['cp60'].grid(row=4, column=1, padx=5, pady=5)  
        
        self.widgets['maxHRlabel'] = tk.Label(self.widgets['frame1'], text='Maximum heart rate: ')
        self.widgets['maxHRlabel'].grid(row=5, padx=5, pady=5)
        self.widgets['maxHR'] = tk.Spinbox(self.widgets['frame1'], from_=130, to=230, increment=3, justify='center', relief='flat')
        self.widgets['maxHR'].grid(row=5, column=1, padx=5, pady=5)  
        
        self.widgets['yearsOfExperienceLabel'] = tk.Label(self.widgets['frame1'], text='Years of experience: ')
        self.widgets['yearsOfExperienceLabel'].grid(row=6, padx=5, pady=5)
        self.widgets['yearsOfExperience'] = tk.Spinbox(self.widgets['frame1'], from_=0, to=90, justify='center', relief='flat')
        self.widgets['yearsOfExperience'].grid(row=6, column=1, padx=5, pady=5)  
        
        self.widgets['frame2'] = tk.Frame(self, height=500)
        self.widgets['frame2'].grid(row=12, rowspan=2, columnspan=4, padx=5, pady=5)
        
        properties = ('', 'Endurance', 'Force', 'Speed skills', 'Anaerobic endurance', 'Endurance force', 'Maximum power')
        
        self.strong1 = tk.StringVar(self)
        self.strong1.set('')
        self.widgets['strong1Label'] = tk.Label(self.widgets['frame2'], text='Strongest skill: ')
        self.widgets['strong1Label'].grid(row=0, padx=5, pady=5)
        self.widgets['strong1'] =tk.OptionMenu(self.widgets['frame2'], self.strong1, *properties)
        self.widgets['strong1'].grid(column=1, row=0, padx=5, pady=5)
        
        self.strong2 = tk.StringVar(self)
        self.strong2.set('')
        self.widgets['strong2Label'] = tk.Label(self.widgets['frame2'], text='Second strongest skill: ')
        self.widgets['strong2Label'].grid(row=0, column=2, padx=5, pady=5)
        self.widgets['strong2'] =tk.OptionMenu(self.widgets['frame2'], self.strong2, *properties)
        self.widgets['strong2'].grid(row=0, column=3, padx=5, pady=5)
        
        self.weak1 = tk.StringVar(self)
        self.weak1.set('')
        self.widgets['weak1Label'] = tk.Label(self.widgets['frame2'], text='Weakest skill: ')
        self.widgets['weak1Label'].grid(row=1, padx=5, pady=5)
        self.widgets['weak1'] =tk.OptionMenu(self.widgets['frame2'], self.weak1, *properties)
        self.widgets['weak1'].grid(row=1, column=1, padx=5, pady=5)
        
        self.weak2 = tk.StringVar(self)
        self.weak2.set('')
        self.widgets['weak2Label'] = tk.Label(self.widgets['frame2'], text='Second weakest skill: ')
        self.widgets['weak2Label'].grid(row=1, column=2, padx=5, pady=5)
        self.widgets['weak2'] =tk.OptionMenu(self.widgets['frame2'], self.weak2, *properties)
        self.widgets['weak2'].grid(row=1, column=3, padx=5, pady=5)
        
        self.widgets['confirm'] = tk.Button(self, text='Create', height=2, width=7)
        self.widgets['confirm'].grid(row=15, sticky='W', padx=5, pady=5)
        self.widgets['confirm'].bind('<Button-1>', createUser)        
        
        self.widgets['Exit'] = tk.Button(self, text='Exit', height=2, width=7)
        self.widgets['Exit'].grid(row=15, column=4, sticky='E', padx=5, pady=5)
        self.widgets['Exit'].bind('<Button-1>', self.exitApp)
        
    def displayUserData(self, data, seasonData, startData):
        self.deleteWindow()
        self.widgets = {}
        
        def changeUser(event):
            self.run = False
            self.program.chooseUser()
        
        def deleteUser(event):
            self.run = False
            self.program.deleteUser()
        
        def deleteRace(event):
            selectedItem = self.widgets['tree'].focus()
            if self.widgets['tree'].item(selectedItem)['values'] != '':
                self.program.deleteRace(self.widgets['tree'].item(selectedItem)['text'])
    
        def newSeasonWindow(event):
            self.run = False
            self.deleteWindow()
            self.widgets = {}
            
            def createSeason(event):
                self.run = False
                self.program.createSeason(self.widgets['year'].get())
            
            self.widgets['frame1'] = tk.Frame(self)
            self.widgets['frame1'].grid(row=0, rowspan=2, columnspan=2, padx=5, pady=5)
        
            self.widgets['yearLabel'] = tk.Label(self.widgets['frame1'], text='Select the year of season: ')
            self.widgets['yearLabel'].grid(row=0, padx=5, pady=5)
            self.widgets['year'] = tk.Spinbox(self.widgets['frame1'], from_=startData[2]+2000, to=startData[2]+2070, increment=1, justify='center', relief='flat')
            self.widgets['year'].grid(row=0, column=1, padx=5, pady=5)  
            
            self.widgets['createSeason'] = tk.Button(self.widgets['frame1'], text='Create\nnew season', height=2, width=11)
            self.widgets['createSeason'].grid(row=1, column=0, sticky='E', padx=5, pady=5)
            self.widgets['createSeason'].bind('<Button-1>', createSeason)
            
            self.widgets['cancel'] = tk.Button(self.widgets['frame1'], text='Cancel', height=2, width=11)
            self.widgets['cancel'].grid(row=1, column=1, sticky='E', padx=5, pady=5)
            self.widgets['cancel'].bind('<Button-1>', self.backToUserDataView)
        
        def displayPlans(back=True):
            if back:
                if self.widgets['listbox'].curselection():
                    self.program.getSeasonPlans(seasonData[self.widgets['listbox'].curselection()[0]]['id'])
            else:
                self.program.getSeasonPlans() 
             
        def deleteSeason(event):
            self.run = False
            if self.widgets['listbox'].curselection():
                season_year = seasonData[self.widgets['listbox'].curselection()[0]]['year']  
                self.program.deleteSeason(season_year)
    
        def newRaceWindow(event, season_id=0, errordata=''):   
            def createRace(event):
                self.run = False
                self.program.createRace(self.widgets['name'].get(), self.widgets['year'].get(), 
                                        self.widgets['month'].get(), self.widgets['day'].get(), 
                                        self.widgets['priority'].get(), self.widgets['hour'].get(),
                                        self.widgets['minute'].get(), selectedID)
                
            if season_id or self.widgets['listbox'].curselection(): 
                #===============================================================
                # if season_id == 0:
                #     self.season = seasonData[self.widgets['listbox'].curselection()[0]]['id']
                #===============================================================
                selectedID = seasonData[self.widgets['listbox'].curselection()[0]]['id']
                self.run = False
                self.deleteWindow()
                self.widgets = {}  
                
                self.widgets['title'] = tk.Label(self, text='Fill in the data.', anchor='e', font='Arial 12')
                self.widgets['title'].grid(row=0, columnspan=6, padx=10, pady=10)  
                
                if errordata != '': 
                    self.widgets['errordata'] = tk.Label(self, text='Wrongly entered fields: {}'.format(errordata), anchor='e', font='Arial 9')
                    self.widgets['errordata'].grid(row=1, columnspan=6, padx=10, pady=10) 
      
                self.widgets['frame1'] = tk.Frame(self)
                self.widgets['frame1'].grid(row=2, rowspan=5, columnspan=6, padx=5, pady=5)  
                
                self.widgets['nameLabel'] = tk.Label(self.widgets['frame1'], text='Name of the race: ', width = 45)
                self.widgets['nameLabel'].grid(padx=5, pady=5)     
                self.widgets['name'] = tk.Entry(self.widgets['frame1'], justify='center', relief='flat')
                self.widgets['name'].grid(row=0, column=1, padx=5, pady=5, columnspan=5)  
                
                self.widgets['datelabel'] = tk.Label(self.widgets['frame1'], text='Race date (dd.mm.yy): ')
                self.widgets['datelabel'].grid(row=1, pady=5)
                
                self.startDay = tk.StringVar(self)
                self.startDay.set(startData[0])

                self.widgets['day'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=31, increment=1, justify='center', relief='flat', width=2, textvariable=self.startDay)
                self.widgets['day'].grid(row=1, column=1) 
                self.widgets['dotLabel'] = tk.Label(self.widgets['frame1'], text='.', width=1)
                self.widgets['dotLabel'].grid(row=1, column=2)
                  
                self.startMonth = tk.StringVar(self)
                self.startMonth.set(startData[1])
                
                self.widgets['month'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=12, increment=1, justify='center', relief='flat', width=2, textvariable=self.startMonth)
                self.widgets['month'].grid(row=1, column=3) 
                self.widgets['dot2Label'] = tk.Label(self.widgets['frame1'], text='.', width=1)
                self.widgets['dot2Label'].grid(row=1, column=4)     
                
                self.startYear = tk.StringVar(self)
                self.startYear.set(startData[2])
                
                self.widgets['year'] = tk.Spinbox(self.widgets['frame1'], from_=startData[2], to=startData[2]+70, increment=1, justify='center', relief='flat', width=2, textvariable=self.startYear)
                self.widgets['year'].grid(row=1, column=5)         
            
                self.widgets['prioritylabel'] = tk.Label(self.widgets['frame1'], text='Race priority: ')
                self.widgets['prioritylabel'].grid(row=2, pady=5)
                self.widgets['priority'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=3, increment=1, justify='center', relief='flat', width=2)
                self.widgets['priority'].grid(row=2, column=1)     
    
                self.widgets['timelabel'] = tk.Label(self.widgets['frame1'], text='Race duration(hh:mm): ')
                self.widgets['timelabel'].grid(row=3, pady=5)
                self.widgets['hour'] = tk.Spinbox(self.widgets['frame1'], from_=0, to=167, increment=1, justify='center', relief='flat', width=3)
                self.widgets['hour'].grid(row=3, column=1) 
                self.widgets['colonLabel'] = tk.Label(self.widgets['frame1'], text=':', width=1)
                self.widgets['colonLabel'].grid(row=3, column=2)  
                self.widgets['minute'] = tk.Spinbox(self.widgets['frame1'], from_=0, to=59, increment=5, justify='center', relief='flat', width=2)
                self.widgets['minute'].grid(row=3, column=3)    
    
                self.widgets['frame2'] = tk.Frame(self)
                self.widgets['frame2'].grid(row=7, rowspan=1, columnspan=6, padx=5, pady=5) 
                
                self.widgets['createRace'] = tk.Button(self.widgets['frame2'], text='Create\nnew race', height=2, width=11)
                self.widgets['createRace'].grid(row=1, column=0, sticky='E', padx=5, pady=5)
                self.widgets['createRace'].bind('<Button-1>', createRace)
                
                self.widgets['cancel'] = tk.Button(self.widgets['frame2'], text='Cancel', height=2, width=11)
                self.widgets['cancel'].grid(row=1, column=1, sticky='E', padx=5, pady=5)
                self.widgets['cancel'].bind('<Button-1>', self.backToUserDataView)  
        
        self.widgets['frame1'] = tk.Frame(self)
        self.widgets['frame1'].grid(rowspan=6, columnspan=2, padx=5, pady=5)
        
        self.widgets['nameLabel'] = tk.Label(self.widgets['frame1'], text='Username: {}'.format(data['name']))
        self.widgets['nameLabel'].grid(padx=5, pady=5)
        
        self.widgets['ageLabel'] = tk.Label(self.widgets['frame1'], text='Age: {}'.format(data['age']))
        self.widgets['ageLabel'].grid(row=1, padx=5, pady=5)
        
        self.widgets['cp60Label'] = tk.Label(self.widgets['frame1'], text='CP60: {}'.format(data['cp60']))
        self.widgets['cp60Label'].grid(row=2, padx=5, pady=5)
        
        self.widgets['maxHRLabel'] = tk.Label(self.widgets['frame1'], text='Maximum heart rate: {}'.format(data['maxHR']))
        self.widgets['maxHRLabel'].grid(row=3, padx=5, pady=5)
        
        self.widgets['yearsOfExperienceLabel'] = tk.Label(self.widgets['frame1'], text='Years of experience: {}'.format(data['yearsOfExperience']))
        self.widgets['yearsOfExperienceLabel'].grid(row=4, padx=5, pady=5)
        
        self.widgets['strong1'] = tk.Label(self.widgets['frame1'], text='Strongest skill: {}'.format(data['strong1']))
        self.widgets['strong1'].grid(row=4, padx=5, pady=5)
        
        self.widgets['strong2'] = tk.Label(self.widgets['frame1'], text='2nd strongest skill: {}'.format(data['strong2']))
        self.widgets['strong2'].grid(row=4, column=1, padx=5, pady=5)
        
        self.widgets['weak1'] = tk.Label(self.widgets['frame1'], text='Weakest skill: {}'.format(data['weak1']))
        self.widgets['weak1'].grid(row=5, padx=5, pady=5)
        
        self.widgets['weak2'] = tk.Label(self.widgets['frame1'], text='2nd weakest skill: {}'.format(data['weak2']))
        self.widgets['weak2'].grid(row=5, column=1, padx=5, pady=5)
        
        self.widgets['listbox'] = tk.Listbox(self.widgets['frame1'], height=7, width=25)
        if seasonData is not None:
            for season in seasonData:
                self.widgets['listbox'].insert(tk.END, season['year'])
        self.widgets['listbox'].grid(row=0, column=1, rowspan=4)
        
        self.widgets['frame2'] = tk.Frame(self)
        self.widgets['frame2'].grid(rowspan=9, columnspan=1, padx=5, pady=5)        

        self.widgets['tree'] = ttk.Treeview(self.widgets['frame2'])
        self.widgets['tree'].column("#0", width=0)
        self.widgets['tree']["columns"]=("raceName","raceDate", 'racePriority', 'raceTime')
        self.widgets['tree'].column("raceName", width=150)
        self.widgets['tree'].column("raceDate", width=100)
        self.widgets['tree'].column("racePriority", width=100)
        self.widgets['tree'].column("raceTime", width=100)
        self.widgets['tree'].heading("raceName", text="Race name")
        self.widgets['tree'].heading("raceDate", text="Race date")
        self.widgets['tree'].heading("racePriority", text="Race priority")
        self.widgets['tree'].heading("raceTime", text="Race time")
        
        self.run = True
        
        def displayRaces():
            if self.run:
                try:
                    if self.widgets['listbox'].curselection(): 
                        if self.selectedSeason != self.widgets['listbox'].curselection():
                            self.selectedSeason = self.widgets['listbox'].curselection()
                            if self.selectedSeason != ():
                                #print('a')
                                season = self.widgets['listbox'].curselection()[0]
                                season_id = seasonData[season]['id']
                                data = self.program.getSeasonRaces(season_id)
                                self.delTree()
                                if data is not None:
                                    for race in data:
                                        self.widgets['tree'].insert("", 'end', text=race['id'], values=(race['name'], race['date'], race['priority'], race['time']))
                except:
                    pass
                self.widgets['tree'].pack()
                self.after(250, displayRaces)
            
        self.widgets['frame3'] = tk.Frame(self)
        self.widgets['frame3'].grid(row=15, rowspan=3, columnspan=4, padx=5, pady=5)
        
        self.widgets['changeUser'] = tk.Button(self.widgets['frame3'], text='Change user', height=2, width=10)
        self.widgets['changeUser'].grid(row=0, column=0, sticky='E', padx=5, pady=5)
        self.widgets['changeUser'].bind('<Button-1>', changeUser)

        self.widgets['deleteUser'] = tk.Button(self.widgets['frame3'], text='Delete\ncurrent user', height=2, width=9)
        self.widgets['deleteUser'].grid(row=0, column=1, sticky='E', padx=5, pady=5)
        self.widgets['deleteUser'].bind('<Button-1>', deleteUser)
        
        self.widgets['addSeason'] = tk.Button(self.widgets['frame3'], text='Add season', height=2, width=9)
        self.widgets['addSeason'].grid(row=0, column=2, sticky='E', padx=5, pady=5)
        self.widgets['addSeason'].bind('<Button-1>', newSeasonWindow)
        
        self.widgets['showPlans'] = tk.Button(self.widgets['frame3'], text="Show season's\nplans", height=2, width=11)
        self.widgets['showPlans'].grid(row=0, column=3, sticky='E', padx=5, pady=5)
        self.widgets['showPlans'].bind('<Button-1>', displayPlans)
        
        self.widgets['deleteSeason'] = tk.Button(self.widgets['frame3'], text='Delete\nseason', height=2, width=10)
        self.widgets['deleteSeason'].grid(row=1, column=0, sticky='E', padx=5, pady=5)
        self.widgets['deleteSeason'].bind('<Button-1>', deleteSeason)
        
        self.widgets['addRace'] = tk.Button(self.widgets['frame3'], text='Add race', height=2, width=9)
        self.widgets['addRace'].grid(row=1, column=1, sticky='E', padx=5, pady=5)
        self.widgets['addRace'].bind('<Button-1>', newRaceWindow)
        
        self.widgets['deleteRace'] = tk.Button(self.widgets['frame3'], text='Delete race', height=2, width=9)
        self.widgets['deleteRace'].grid(row=1, column=2, sticky='E', padx=5, pady=5)
        self.widgets['deleteRace'].bind('<Button-1>', deleteRace)
        
        self.widgets['Exit'] = tk.Button(self.widgets['frame3'], text='Exit', height=2, width=11)
        self.widgets['Exit'].grid(row=1, column=3, sticky='E', padx=5, pady=5)
        self.widgets['Exit'].bind('<Button-1>', self.exitApp)

        self.selectedSeason = ()
        displayRaces()
    
    def displaySeasonPlans(self, seasonPlans, seasonYear):
        self.run = False
        self.deleteWindow()
        self.widgets = {}
  
        def showPlan(event):
            selectedItem = self.widgets['tree'].focus()
            if self.widgets['tree'].item(selectedItem)['values'] != '':
                self.program.showPlan(self.widgets['tree'].item(selectedItem)['text'],
                                      self.widgets['tree'].item(selectedItem)['values'])   
                  
        def newPlanWindow(event):
            self.program.newPlanWindow()
                  
        def deletePlan(event):
            selectedItem = self.widgets['tree'].focus()
            if self.widgets['tree'].item(selectedItem)['values'] != '':
                self.program.deletePlan(self.widgets['tree'].item(selectedItem)['text'])
       
        self.widgets['frame1'] = tk.Frame(self)
        self.widgets['frame1'].grid(rowspan=1, columnspan=2, padx=5, pady=5)
        
        self.widgets['seasonYearLabel'] = tk.Label(self.widgets['frame1'], text='Season: {}'.format(seasonYear))
        self.widgets['seasonYearLabel'].grid(columnspan=2, padx=5, pady=5)
        
        self.widgets['frame2'] = tk.Frame(self)
        self.widgets['frame2'].grid(rowspan=9, columnspan=2, padx=5, pady=5)        

        self.widgets['tree'] = ttk.Treeview(self.widgets['frame2'])
        self.widgets['tree'].column("#0", width=0)
        self.widgets['tree']["columns"]=("annualHours","typeOfPlan", 'planStart', 'planEnd')
        self.widgets['tree'].column("annualHours", width=100)
        self.widgets['tree'].column("typeOfPlan", width=100)
        self.widgets['tree'].column("planStart", width=100)
        self.widgets['tree'].column("planEnd", width=100)
        self.widgets['tree'].heading("annualHours", text="Annual hours")
        self.widgets['tree'].heading("typeOfPlan", text="Type of plan")
        self.widgets['tree'].heading("planStart", text="Start of plan")
        self.widgets['tree'].heading("planEnd", text="End of plan")
        
        if seasonPlans is not None:
            for plan in seasonPlans:
                self.widgets['tree'].insert("", 'end', text=plan['id'], values=(plan['annualHours'], plan['typeOfPlan'], plan['planStart'], plan['planEnd']))
            self.widgets['tree'].pack()
        
        self.widgets['frame3'] = tk.Frame(self)
        self.widgets['frame3'].grid(row=13, rowspan=1, columnspan=5, padx=5, pady=5)
        
        self.widgets['newPlan'] = tk.Button(self.widgets['frame3'], text='New plan', height=2, width=10)
        self.widgets['newPlan'].grid(row=0, column=0, sticky='E', padx=5, pady=5)
        self.widgets['newPlan'].bind('<Button-1>', newPlanWindow)
        
        self.widgets['openPlan'] = tk.Button(self.widgets['frame3'], text='Open plan', height=2, width=10)
        self.widgets['openPlan'].grid(row=0, column=1, sticky='E', padx=5, pady=5)
        self.widgets['openPlan'].bind('<Button-1>', showPlan)
        
        self.widgets['deletePlan'] = tk.Button(self.widgets['frame3'], text='Delete plan', height=2, width=10)
        self.widgets['deletePlan'].grid(row=0, column=2, sticky='E', padx=5, pady=5)
        self.widgets['deletePlan'].bind('<Button-1>', deletePlan)
        
        self.widgets['back'] = tk.Button(self.widgets['frame3'], text='Back', height=2, width=10)
        self.widgets['back'].grid(row=0, column=3, sticky='E', padx=5, pady=5)
        self.widgets['back'].bind('<Button-1>', self.backToUserDataView)

        self.widgets['Exit'] = tk.Button(self.widgets['frame3'], text='Exit', height=2, width=11)
        self.widgets['Exit'].grid(row=0, column=4, sticky='E', padx=5, pady=5)
        self.widgets['Exit'].bind('<Button-1>', self.exitApp)

    def newPlanWindow(self, startData, errordata=''):
        
        def createPlan(event):
            self.program.createPlan(self.widgets['annualHours'].get(), self.typeOfPlan.get(), 
                                    self.widgets['startYear'].get(), self.widgets['startMonth'].get(), self.widgets['startDay'].get(),
                                    self.widgets['endYear'].get(), self.widgets['endMonth'].get(), self.widgets['endDay'].get())
        
        self.run = False
        self.deleteWindow()
        self.widgets = {}  
        
        self.widgets['title'] = tk.Label(self, text='Fill in the data.', anchor='e', font='Arial 12')
        self.widgets['title'].grid(row=0, columnspan=6, padx=10, pady=10)  
         
        if errordata != '': 
            self.widgets['errordata'] = tk.Label(self, text='Wrongly entered fields: {}'.format(errordata), anchor='e', font='Arial 9')
            self.widgets['errordata'].grid(row=1, columnspan=6, padx=10, pady=10) 
            
        self.widgets['frame1'] = tk.Frame(self)
        self.widgets['frame1'].grid(row=2, rowspan=4, columnspan=6, padx=5, pady=5)  
          
        self.widgets['annualHoursLabel'] = tk.Label(self.widgets['frame1'], text='Annual hours (divisible by 50): ')
        self.widgets['annualHoursLabel'].grid(padx=5, pady=5)     
        self.widgets['annualHours'] = tk.Spinbox(self.widgets['frame1'], from_=200, to=1200, increment=50, justify='center', relief='flat', width=4)
        self.widgets['annualHours'].grid(row=0, column=1, padx=5, pady=5, columnspan=5)  
        
        self.typeOfPlan = tk.IntVar()
        self.typeOfPlan.set(1)
        
        self.widgets['typeOfPlanLabel'] = tk.Label(self.widgets['frame1'], text='Type of plan: ')
        self.widgets['typeOfPlanLabel'].grid(row=1, column=0, padx=5, pady=5)  
        self.widgets['radio1'] = tk.Radiobutton(self.widgets['frame1'], text='Classic', variable=self.typeOfPlan, value=1)
        self.widgets['radio1'].grid(row=1, column=1, columnspan=2,pady=5)
        self.widgets['radio2'] = tk.Radiobutton(self.widgets['frame1'], text='Reversed', variable=self.typeOfPlan, value=2)
        self.widgets['radio2'].grid(row=1, column=3, columnspan=2, pady=5)
        
        self.widgets['startlabel'] = tk.Label(self.widgets['frame1'], text='Start of plan (dd.mm.yy, must be Monday): ')
        self.widgets['startlabel'].grid(row=2, pady=5)
        
        self.startDay = tk.StringVar(self)
        self.startDay.set(startData[0])
        
        self.widgets['startDay'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=31, increment=1, justify='center', relief='flat', width=2, textvariable=self.startDay)
        self.widgets['startDay'].grid(row=2, column=1) 
        self.widgets['dotLabel'] = tk.Label(self.widgets['frame1'], text='.', width=1)
        self.widgets['dotLabel'].grid(row=2, column=2)
        
        self.startMonth = tk.StringVar(self)
        self.startMonth.set(startData[1])
          
        self.widgets['startMonth'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=12, increment=1, justify='center', relief='flat', width=2, textvariable=self.startMonth)
        self.widgets['startMonth'].grid(row=2, column=3) 
        self.widgets['dot2Label'] = tk.Label(self.widgets['frame1'], text='.', width=1)
        self.widgets['dot2Label'].grid(row=2, column=4)       
        
        self.startYear = tk.StringVar(self)
        self.startYear.set(startData[2])
        
        self.widgets['startYear'] = tk.Spinbox(self.widgets['frame1'], from_=startData[2], to=startData[2]+70, increment=1, justify='center', relief='flat', width=2, textvariable=self.startYear)
        self.widgets['startYear'].grid(row=2, column=5)   
        
        self.endDay = tk.StringVar(self)
        self.endDay.set(31)
        self.endMonth = tk.StringVar(self)
        self.endMonth.set(12)        
        self.endYear = tk.StringVar(self)
        self.endYear.set(startData[2])        
        
        self.widgets['endlabel'] = tk.Label(self.widgets['frame1'], text='End of plan (dd.mm.yy): ')
        self.widgets['endlabel'].grid(row=3, pady=5)
        self.widgets['endDay'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=31, increment=1, justify='center', relief='flat', width=2, textvariable=self.endDay)
        self.widgets['endDay'].grid(row=3, column=1) 
        self.widgets['dotLabel'] = tk.Label(self.widgets['frame1'], text='.', width=1)
        self.widgets['dotLabel'].grid(row=3, column=2)  
        self.widgets['endMonth'] = tk.Spinbox(self.widgets['frame1'], from_=1, to=12, increment=1, justify='center', relief='flat', width=2, textvariable=self.endMonth)
        self.widgets['endMonth'].grid(row=3, column=3) 
        self.widgets['dot2Label'] = tk.Label(self.widgets['frame1'], text='.', width=1)
        self.widgets['dot2Label'].grid(row=3, column=4)     
        self.widgets['endYear'] = tk.Spinbox(self.widgets['frame1'], from_=startData[2], to=startData[2]+70, increment=1, justify='center', relief='flat', width=2, textvariable=self.endYear)
        self.widgets['endYear'].grid(row=3, column=5)         
     
        self.widgets['frame2'] = tk.Frame(self)
        self.widgets['frame2'].grid(row=7, rowspan=1, columnspan=6, padx=5, pady=5) 
          
        self.widgets['createPlan'] = tk.Button(self.widgets['frame2'], text='Create\nnew plan', height=2, width=11)
        self.widgets['createPlan'].grid(row=1, column=0, sticky='E', padx=5, pady=5)
        self.widgets['createPlan'].bind('<Button-1>', createPlan)
          
        self.widgets['cancel'] = tk.Button(self.widgets['frame2'], text='Cancel', height=2, width=11)
        self.widgets['cancel'].grid(row=1, column=1, sticky='E', padx=5, pady=5)
        self.widgets['cancel'].bind('<Button-1>', self.backToDisplayPlans) 

    def showPlanWindow(self, data, planInfo):
        self.run = False
        self.deleteWindow()
        self.widgets = {}
        
        self.widgets['frame1'] = tk.Frame(self)
        self.widgets['frame1'].grid(rowspan=2, columnspan=2, padx=5, pady=5)
        
        self.widgets['annualHoursLabel'] = tk.Label(self.widgets['frame1'], text='Annual hours: {}'.format(planInfo[0]))
        self.widgets['annualHoursLabel'].grid(padx=5, pady=5)
        
        self.widgets['planStartLabel'] = tk.Label(self.widgets['frame1'], text='Start of Plan: {}'.format(planInfo[2]))
        self.widgets['planStartLabel'].grid(row=0, column=1, padx=5, pady=5)
        
        self.widgets['typeOfPlanLabel'] = tk.Label(self.widgets['frame1'], text='Type of plan: {}'.format(planInfo[1]))
        self.widgets['typeOfPlanLabel'].grid(row=1, padx=5, pady=5)
        
        self.widgets['planEndLabel'] = tk.Label(self.widgets['frame1'], text='End of plan: {}'.format(planInfo[3]))
        self.widgets['planEndLabel'].grid(row=1, column=1, padx=5, pady=5)
        
        self.widgets['frame2'] = tk.Frame(self)
        self.widgets['frame2'].grid(rowspan=25, columnspan=3, padx=5, pady=5)        

        self.widgets['tree'] = ttk.Treeview(self.widgets['frame2'], height=25)
        self.widgets['tree'].column("#0", width=0)
        self.widgets['tree']["columns"]=('week', 'monday', 'period', 'weeklyHours', 'race', 'gym', 'endurance', 'force', 'speedSkills', 'eForce', 'aEndurance', 'maxPower', 'test')
        self.widgets['tree'].column('week', width=45)
        self.widgets['tree'].column('monday', width=75)
        self.widgets['tree'].column('period', width=60)
        self.widgets['tree'].column('weeklyHours', width=75)
        self.widgets['tree'].column('race', width=100)
        self.widgets['tree'].column('gym', width=35)
        self.widgets['tree'].column('endurance', width=30)
        self.widgets['tree'].column('force', width=30)
        self.widgets['tree'].column('speedSkills', width=30)
        self.widgets['tree'].column('eForce', width=30)
        self.widgets['tree'].column('aEndurance', width=30)
        self.widgets['tree'].column('maxPower', width=30)
        self.widgets['tree'].column('test', width=50)
        
        self.widgets['tree'].heading('week', text="Week")
        self.widgets['tree'].heading('monday', text="Monday")
        self.widgets['tree'].heading('period', text="Period")
        self.widgets['tree'].heading('weeklyHours', text="Weekly hrs")
        self.widgets['tree'].heading('race', text="Race")
        self.widgets['tree'].heading('gym', text="Gym")
        self.widgets['tree'].heading('endurance', text="E")
        self.widgets['tree'].heading('force', text="F")
        self.widgets['tree'].heading('speedSkills', text="SpS")
        self.widgets['tree'].heading('eForce', text="EF")
        self.widgets['tree'].heading('aEndurance', text="AE")
        self.widgets['tree'].heading('maxPower', text="MP")
        self.widgets['tree'].heading("test", text="Test")

        
        if data is not None:
            for week in data:
                self.widgets['tree'].insert("", 'end', text=week['id'], values=(week['week'], week['monday'], 
                                            week['period'][:-2], week['weeklyHours'], week['races'], week['gym'], 
                                            week['endurance'], week['force'], week['speedSkills'], 
                                            week['eForce'], week['aEndurance'], week['maxPower'], 
                                            week['test']))
        self.widgets['tree'].pack()

        self.widgets['frame3'] = tk.Frame(self)
        self.widgets['frame3'].grid(row=27, rowspan=2, columnspan=4, padx=5, pady=5)
        self.widgets['frame4'] = tk.Frame(self)
        self.widgets['frame4'].grid(row=2, column=4, rowspan=25, padx=10)
        
        self.widgets['back'] = tk.Button(self.widgets['frame3'], text='Back', height=2, width=11)
        self.widgets['back'].grid(row=0, column=1, sticky='E', padx=5, pady=5)
        self.widgets['back'].bind('<Button-1>', self.backToDisplayPlans)

        self.widgets['Exit'] = tk.Button(self.widgets['frame3'], text='Exit', height=2, width=11)
        self.widgets['Exit'].grid(row=0, column=2, sticky='E', padx=5, pady=5)
        self.widgets['Exit'].bind('<Button-1>', self.exitApp)

        self.widgets['graph'] = Graph(data, self.widgets['frame4'])
        self.widgets['graph'].grid()
                
    def backToDisplayPlans(self, event):
        self.program.getSeasonPlans()

            
    def delTree(self):
        for row in self.widgets['tree'].get_children():
            self.widgets['tree'].delete(row)
        
    def deleteWindow(self):
        for wid in self.widgets.keys():
            try:
                self.widgets[wid].destroy()
            except:
                pass
        self.widgets = {}
        
    def backToUserDataView(self, event):
        self.program.loadUser()
        
    def messageBox(self, title, body):
        self.widgets['failMesage'] = messagebox.showinfo(title, body)

    def exitApp(self, event):
        self.quit()

if __name__ == '__main__':
    myapp = Desktop()