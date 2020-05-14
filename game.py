from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import time
import q_n_a

root=Tk()

def login_register():
   clean()
   Label(root,text='Login or \nRegister',justify='center',font=('Arial',20,'bold')).pack()
   loginBtn=Button(root,
                   width=10,
                   height=2,
                   text='Login',
                   command=LoginScreen
                   )
   loginBtn.place(x=110,y=160)
   registerBtn=Button(root,
                      width=10,
                      height=2,
                      text='Register',
                      command=RegisterScreen)
   registerBtn.place(x=110,y=220)
   Label(root,text=(time.asctime( time.localtime(time.time()))),justify='center').place(x=90,y=360)
   
def RegisterScreen():
   global name,password
   clean()
   Label(root,text='Registration',font=('Arial',20,'bold')).place(x=70,y=20)
   name=StringVar()
   password=StringVar()
   namelabel=Label(root,text='Name: ').place(x=50,y=100)
   passwordLabel=Label(root,text='Key: ').place(x=50,y=150)
   nameEntry=Entry(root,textvariable=name).place(x=110,y=100)
   passwordEntry=Entry(root,textvariable=password).place(x=110,y=150)
   Button(root,text='Register',width=10,height=1,command=register).place(x=120,y=210)
   Button(root,text='Back',command=backToRegisterLogin).place(x=140,y=360)
   
def LoginScreen():
   global name,password
   clean()
   Label(root,text='User Login',font=('Arial',20,'bold')).place(x=70,y=20)
   name=StringVar()
   password=StringVar()
   namelabel=Label(root,text='Name: ').place(x=50,y=100)
   passwordLabel=Label(root,text='Key: ').place(x=50,y=150)
   nameEntry=Entry(root,textvariable=name).place(x=110,y=100)
   passwordEntry=Entry(root,textvariable=password).place(x=110,y=150)
   Button(root,text='Login',width=10,height=1,command=login).place(x=120,y=210)
   Button(root,text='Back',command=backToRegisterLogin).place(x=140,y=360)
   
def login():
   global show,cx,conn
   conn = sqlite3.connect('sqldb.db')
   cx = conn.cursor()
   usersList=[]
   cx.execute('SELECT usrname FROM users')
   check=cx.fetchall()
   for i in range(len(check)):
       usersList.append(check[i][0])
   if name.get() not in usersList:
       messagebox.showinfo('Error','You are not registered!\n\nRedirecting to Registration Screen...')
       RegisterScreen()
   elif name.get() in usersList:
          cx.execute('SELECT pass FROM users WHERE usrname=(?)',(name.get(),))
          user_pass=cx.fetchall()[0][0]
          if password.get()==user_pass:
              main()
          else:
              messagebox.showinfo('Error','Password Incorrect!')
              
def backToRegisterLogin():
   clean()
   login_register()
   
def register():
   conn = sqlite3.connect('sqldb.db')
   cursor = conn.cursor()
   usersList=[]
   cx.execute('SELECT usrname FROM users')
   check=cx.fetchall()
   for i in range(len(check)):
       usersList.append(check[i][0])
   if name.get() not in usersList:
       cursor.execute('CREATE TABLE IF NOT EXISTS users(usrname CHAR(10),pass CHAR(10))')
       cursor.execute('INSERT INTO users(usrname,pass) VALUES (?,?)',(name.get(),password.get()))
       conn.commit()
       conn.close()
       messagebox.showinfo('Success','Registration Successful')
       main()
   elif name.get() in usersList:
          messagebox.showinfo('Information','You are already registered!\n\nRedirecting to Login Screen...')
          LoginScreen()
          
def settings():
    clean()
    Label(root,text=('Logged in as '+name.get().title()),font=('Arial',17,'bold'),justify='center').pack()
    Button(root,text='Log Out',command=login_register).place(x=120,y=360)
    
def clean():
   for widget in root.winfo_children():
      widget.destroy()
      
def main():
   clean()
   messagebox.showinfo('Logged In','Welcome '+(name.get().title()+'!'))
   head=Label(root,
         font=('Arial',30,'bold'),
         text='Python Quiz',
        )
   head.pack(pady=(30,70))
   startBtn=Button(root,
          width=10,
          height=2,
          relief=FLAT,
          border=0,
          text='Start',
          justify='center',
          command=start,
        )
   startBtn.pack()
   rulesBtn=Button(root,
          width=10,
          height=2,
          relief=FLAT,
          border=0,
          text='Rules', 
          justify='center',
          command=rules
        )
   rulesBtn.pack()
   profileBtn=Button(root,
          width=10,
          height=2,
          relief=FLAT,
          border=0,
          text='Settings',
          justify='center',
          command=settings
        )
   profileBtn.pack()
   quitBtn=Button(root,
          width=10,
          height=2,
          relief=FLAT,
          border=0,
          text='Quit',
          justify='center',
          command=quit
        )
   quitBtn.pack()
totalQues=5
indexes=[]
user_answer=[]
num_of_ques=len(q_n_a.questions)

def gen():
   while(len(indexes)<totalQues):
         x=random.randint(0,num_of_ques-1)
         if x in indexes:
                  continue
         else:
                  indexes.append(x)
                  
def showResult(show):
      clean()
      messagebox.showinfo('Result','You scored '+str(int((score/totalQues)*100))+'%')
      Label(root,
            text='Leaderboad',
            justify='center',
            font=('Arial',20,'italic')
            ).place(x=80,y=5)
      quitBtn=Button(root,
                      command=quit,
                      text='Quit',
                      relief=FLAT
                     )
      quitBtn.place(x=50,y=350)
      mainMenu=Button(root,
                       command=back,
                       justify='center',
                       text='Main Menu',
                       relief=FLAT
                     )
      mainMenu.place(x=160,y=350)
      showLeaderboard()
      
def showLeaderboard():
    for i in range(2,len(show)+2):
        for j in range(1,3):
            Label(root,
                  text=(show[i-2][j-1])
                  ).place(y=(i+(25*i)),x=(j*95))
        Label(root,
               text=('\n')
               ).grid(row=5,column=3)
        
def calc():
      global score
      score=0
      n=0
      for i in indexes:
         if user_answer[n]==q_n_a.answers[i]:
            score+=1
         n+=1
      leaderboard()
      
ques=1

def selected():  
        global radioVar, questionLabel, r1, r2, r3, r4, ques   
        x=radioVar.get()
        user_answer.append(x)
        radioVar.set(-1)      
        if ques<totalQues:
                questionLabel.config(text=q_n_a.questions[indexes[ques]])
                r1['text']=q_n_a.choice_answers[indexes[ques]][0]
                r2['text']=q_n_a.choice_answers[indexes[ques]][1]
                r3['text']=q_n_a.choice_answers[indexes[ques]][2]
                r4['text']=q_n_a.choice_answers[indexes[ques]][3]
                ques+=1
        else:
                calc()
                
def rules():
   clean()
   head=Label(root,
         font=('Arial',30,'bold'),
         text='Rules',
        )
   head.pack()
   Label(root,
         text='''1. There are a total of 5 questions\n\n2. Questions are of Multiple Choice\n\n3. Each question carries one mark\n\n4. No negative marking for wrong answers\n\n5. Send an E mail to skalpasi7@gmail.com for any guidance''',
         wraplength=270,
         ).place(x=20,y=70)
   backBtn=Button(root,
          width=10,
          height=2,
          relief=FLAT,
          border=0,
          text='Back',
          command=back,
        )
   backBtn.place(x=95,y=350)
   
def start():   
        clean()
        gen()   
        global  radioVar, questionLabel, r1, r2, r3, r4, score
        questionLabel= Label(root,
                             text=q_n_a.questions[indexes[0]],
                             justify='center',
                             wraplength=250,
                        )
        questionLabel.pack(pady=(30,40))
        radioVar=IntVar()
        radioVar.set(-1)

        r1=Radiobutton(root,
                       text=q_n_a.choice_answers[indexes[0]][0],
                       value=0,
                       variable=radioVar,
                       justify='left',
                       command=selected                 
                     )
        r1.pack(pady=5)        
        r2=Radiobutton(root,
                       text=q_n_a.choice_answers[indexes[0]][1],
                       value=1,
                       variable=radioVar,
                       justify='left',
                       command=selected
                     )
        r2.pack(pady=5)        
        r3=Radiobutton(root,
                       text=q_n_a.choice_answers[indexes[0]][2],
                       value=2,
                       variable=radioVar,
                       justify='left',
                       command=selected
                     )
        r3.pack(pady=5)        
        r4=Radiobutton(root,
                       text=q_n_a.choice_answers[indexes[0]][3],
                       value=3,
                       variable=radioVar,
                       justify='left',
                       command=selected
                     )
        r4.pack(pady=5)
        backBtn=Button(root,
                       command=back,
                       justify='center',
                       text='Main Menu',
                       relief=FLAT
                     )
        backBtn.place(x=95,y=350)
        
def back():
   global ques,indexes,user_answers  
   clean()
   ques=1
   score=0
   indexes=[]
   user_answers=[]
   main()
   
def init():
   root.title('Quiz')
   root.resizable(height=FALSE, width=FALSE)
   root.geometry('300x400')
   login_register()
   
def leaderboard():
   global show,cx,conn
   conn = sqlite3.connect('sqldb.db')
   cx = conn.cursor()
   cx.execute('CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, usrname CHAR(10), score INT(2))')
   usersList=[]
   cx.execute('SELECT usrname FROM data')
   check=cx.fetchall()
   for i in range(len(check)):
       usersList.append(check[i][0])
   if name.get() in usersList:
       cx.execute('SELECT score FROM data WHERE usrname=(?)',(name.get(),))
       user_score=cx.fetchall()[0][0]
       if score>user_score:
           cx.execute('UPDATE data SET score=(?) WHERE usrname=(?)',(score,name.get()))       
   else:
       cx.execute('INSERT INTO data(usrname,score) VALUES (?,?)',(name.get(),score))
   cx.execute('SELECT usrname,score FROM data ORDER BY score DESC')
   show=cx.fetchall()
   conn.commit()
   conn.close()
   showResult(show)
   showLeaderboard()
   
def createDB():
    global show,cx,conn
    conn = sqlite3.connect('sqldb.db')
    cx = conn.cursor()
    cx.execute('CREATE TABLE IF NOT EXISTS users(usrname CHAR(10),pass CHAR(10))')
    cx.execute('CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, usrname CHAR(10), score INT(2))')

createDB()
init()
root.mainloop()
