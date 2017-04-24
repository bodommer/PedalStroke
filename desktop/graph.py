import tkinter as tk

'''
Created on 13 Apr 2017
@author: Andrej Jurco
'''

class Graph(tk.Canvas):
    
    def __init__(self, data, master=None):
        super().__init__(master, width=600, height=550, bg='white', borderwidth=0, highlightthickness=0)

        self.data = data
        self.bind('<Motion>', self.motion)
        self.field = self.text = False
        self.yCoords = []
        self.xCoords = []
        
        self.create_rectangle(0, 24, 599, 274, outline='grey')
        self.create_rectangle(0, 299, 599, 549, outline='grey')
        self.create_text(127, 12, text='Training weeks overview', font='Arial 16 bold')
        self.create_text(143, 287, text='Form, condition and fatigue', font='Arial 16 bold')
        column_width = 590//(len(data))
        extra = (590 - (len(data))*column_width)//2
        # kreslenie grafov
        max_hrs = 0
        self.create_line(5, 250, 594, 250)

        for week in data:
            if week['weeklyHours'] > max_hrs:
                max_hrs = week['weeklyHours']
        column_height = 222//max_hrs

        for week in data:
            height = int(round(column_height*week['weeklyHours']))
            self.create_rectangle(6+extra+(week['week']-1)*column_width, 250-height, extra+week['week']*column_width+4, 250, fill='skyblue', activefill='yellow')
            self.xCoords.append((1+extra+(week['week']-1)*column_width, extra+week['week']*column_width-1))
            self.yCoords.append(250-height)
            self.create_text(6+extra+(week['week'])*column_width-column_width//2, 262, text=week['week'])
            self.create_text(6+extra+(week['week'])*column_width-column_width//2, 537, text=week['week'])

        koeficienty = {
        'Preparatory-1': {'C': 1.02,'F': -0.02, 'T': 0.02}, 
        'Base 1-1': {'C': 1.03,'F': -0.03, 'T': 0.04}, 
        'Base 1-2': {'C': 1.04,'F': -0.03, 'T': 0.04}, 
        'Base 1-3': {'C': 1.05,'F': -0.03, 'T': 0.04}, 
        'Base 1-4': {'C': 0.98,'F': 0.11, 'T': -0.06}, 
        'Base 2-1': {'C': 1.04,'F': -0.04, 'T': 0.05}, 
        'Base 2-2': {'C': 1.05,'F': -0.04, 'T': 0.05}, 
        'Base 2-3': {'C': 1.06,'F': -0.04, 'T': 0.05}, 
        'Base 2-4': {'C': 0.98,'F': 0.16, 'T': -0.08}, 
        'Base 3-1': {'C': 1.05,'F': -0.05, 'T': 0.06}, 
        'Base 3-2': {'C': 1.06,'F': -0.05, 'T': 0.06}, 
        'Base 3-3': {'C': 1.07,'F': -0.05, 'T': 0.06}, 
        'Base 3-4': {'C': 0.98,'F': 0.22, 'T': -0.1}, 
        'Build 1-1': {'C': 1.07,'F': -0.06, 'T': 0.08}, 
        'Build 1-2': {'C': 1.07,'F': -0.06, 'T': 0.08}, 
        'Build 1-3': {'C': 1.07,'F': -0.06, 'T': 0.08}, 
        'Build 1-4': {'C': 0.98,'F': 0.28, 'T': -0.12}, 
        'Build 2-1': {'C': 1.06,'F': -0.05, 'T': 0.09}, 
        'Build 2-2': {'C': 1.06,'F': -0.05, 'T': 0.09}, 
        'Build 2-3': {'C': 1.06,'F': -0.05, 'T': 0.09}, 
        'Build 2-4': {'C': 0.98,'F': 0.26, 'T': -0.15}, 
        'Peak 1': {'C': 1.02, 'F': 0.17, 'T': 0.05},
        'Peak 2': {'C': 1.02, 'F': 0.15, 'T': 0.05}, 
        'Racing': {'C': 0.98,'F': -0.25, 'T': 0.2}, 
        'Transitory': {'C': 0.9,'F': 0.05, 'T': -0.35}}

        self.create_line(5, 525, 594, 525)
        self.cPoints = []
        self.fPoints = []
        self.tPoints = []
        cy = 0.3
        fy = 0.5
        ty = 0
        y_max = 220
        cy_old = cy
        fy_old = fy
        ty_old = ty
        
        for week in data:
            w_no = week['week']
            k = koeficienty[week['period']]
            cy *= k['C']
            fy += k['F']
            ty += k['T']
            #column_width//2+(week['week']-1)*column_width, 250-height, column_width//2+week['week']*column_width, 250

            cy = min(1, cy)
            cy = max(0, cy)
            if w_no != 1:
                self.create_line(5+extra+(w_no-1)*column_width-column_width//2, 525-cy_old*y_max, 5+extra+(w_no)*column_width-column_width//2, 525-cy*y_max, fill='skyblue')
            self.cPoints.append(self.create_oval(5+extra+(w_no)*column_width-column_width//2-4, 525-cy*y_max-4, 5+extra+(w_no)*column_width-column_width//2+4, 525-cy*y_max+4, fill='navy', outline='navy'))

            fy = min(1, fy)
            fy = max(0, fy)
            if w_no != 1:
                self.create_line(5+extra+(w_no-1)*column_width-column_width//2, 525-fy_old*y_max, 5+extra+(w_no)*column_width-column_width//2, 525-fy*y_max, fill='pink')
            self.fPoints.append(self.create_oval(5+extra+(w_no)*column_width-column_width//2-4, 525-fy*y_max-4, 5+extra+(w_no)*column_width-column_width//2+4, 525-fy*y_max+4, fill='red', outline='red'))

            ty = min(1, ty)
            ty = max(0, ty)
            if w_no != 1:
                self.create_line(5+extra+(w_no-1)*column_width-column_width//2, 525-ty_old*y_max, 5+extra+(w_no)*column_width-column_width//2, 525-ty*y_max, fill='limegreen')
            self.tPoints.append(self.create_oval(5+extra+(w_no)*column_width-column_width//2-4, 525-ty*y_max-4, 5+extra+(w_no)*column_width-column_width//2+4, 525-ty*y_max+4, fill='green', outline='green'))

            cy_old, fy_old, ty_old = cy, fy, ty
        for item in self.cPoints:
            self.tag_raise(item)
        for item in self.fPoints:
            self.tag_raise(item)
        for item in self.tPoints:
            self.tag_raise(item)

        self.create_rectangle(10, 310, 110, 390)
        for y, farba in ((325, 'skyblue'), (350, 'pink'), (375, 'limegreen')):
            self.create_line(20, y, 40, y, fill=farba, width=3)
        for y, farba, text in ((325, 'navy', 'Condition'), (350, 'red', 'Form'), (375, 'green', 'Tiredness')):
            self.create_oval(26, y-4, 34, y+4, fill=farba, outline=farba)
            self.create_text(75, y, text=text, font='Arial 10 bold')

    def motion(self, event):
        if 24 < event.y < 275:
            for i in range(len(self.xCoords)):
                if self.xCoords[i][0] <= event.x <= self.xCoords[i][1]:
                    if event.y >= self.yCoords[i]:
                        if event.x > 428:
                            x = 429
                        else:
                            x = event.x+1
                        if event.y < 106:
                            y = 105
                        else:
                            y = event.y-1
                        if not self.field:
                            self.field = self.create_rectangle(x, y-80, x+170, y, fill='white')
                        else:
                            self.coords(self.field, (x, y-80, x+170, y))
                        wk = self.data[i]
                        monday = '{}/{}'.format(wk['monday'].day, wk['monday'].month)
                        text='Week: {}\nPeriod: {}\nHours: {}\nMonday: {}\nTraining:'.format(wk['week'], wk['period'][:-2], wk['weeklyHours'], monday)
                        if wk['gym']:
                            text += ' Gym: {}'.format(wk['gym'])                    
                        if wk['endurance'] != ' ':
                            text += ' EN'
                        if wk['force'] != ' ':
                            text += ' FO'
                        if wk['speedSkills'] != ' ':
                            text += ' SpS'
                        if wk['eForce'] != ' ':
                            text += ' EF'
                        if wk['aEndurance'] != ' ':
                            text += ' AE'
                        if wk['maxPower'] != ' ':
                            text += ' MP'
                        if wk['test'] != ' ':
                            text += ' TEST'
                        if not self.text:
                            self.text = self.create_text(x+3, y-77, anchor='nw', text=text)
                        else:
                            self.coords(self.text, (x+3, y-77))
                            self.itemconfig(self.text, text=text)
                        self.update()
                        return
        self.delete(self.field)
        self.delete(self.text)
        self.field = self.text = False
        self.update()
       
        #self.canvas.mainloop()
          

          
#===============================================================================
# class Graph(tk.Toplevel):
#     def __init__(self, data, master=None):
#         tk.Toplevel.__init__(self)
#         self.create_rectangle(0,0,50,50)
#         
#===============================================================================
        
