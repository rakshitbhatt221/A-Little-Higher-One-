from tkinter import *
import sqlite3,sys

def connection():
    try:
        conn=sqlite3.connect("student.db")
    except:
        print("Can't Connect to the Database. File not Found !")
    return conn    


def verifier():
    a=b=c=d=e=f=0

    if not student_name.get():
        t1.insert(END,"<>Student's name is necessary to update<>\n")
        a=1
    if not roll_no.get():
        t1.insert(END,"<>Roll no is necessary to update<>\n")
        b=1
    if not branch.get():
        t1.insert(END,"<>Branch is necessary to update<>\n")
        c=1
    if not phone.get():
        t1.insert(END,"<>Phone number is necessary to update<>\n")
        d=1
    if not father.get():
        t1.insert(END,"<>Father name is necessary to update<>\n")
        e=1
    if not address.get():
        t1.insert(END,"<>Address is necessary to update<>\n")
        f=1

    if a==1 or b==1 or c==1 or d==1 or e==1 or f==1:
        return 1
    else:
        return 0

#function to add thhe student in the preset .db file
def add_student():
            ret=verifier()
            if ret==0:
                conn=connection()
                cur=conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS STUDENTS(NAME TEXT,ROLL_NO INTEGER,BRANCH TEXT,PHONE_NO INTEGER,FATHER TEXT,ADDRESS TEXT)")
                cur.execute("insert into STUDENTS values(?,?,?,?,?,?)",(student_name.get(),int(roll_no.get()),branch.get(),int(phone.get()),father.get(),address.get()))
                conn.commit()
                conn.close()
                t1.insert(END,"ADDED SUCCESSFULLY\n")

#function to view the existing entries in the .db file
def view_student():
    conn=connection()
    cur=conn.cursor()
    cur.execute("select * from STUDENTS")
    data=cur.fetchall()
    conn.close()
    for i in data:
        t1.insert(END,str(i)+"\n")

#function to delete thhe existing entries: NEED UPDATION TO DELETE ONE ENTRY/ ALL ENTRIES WALI CHOICE:
def delete_student():
    ret=verifier()
    if ret==0:
        conn=connection()
        cur=conn.cursor()
        cur.execute("DELETE FROM STUDENTS WHERE ROLL_NO=?",(int(roll_no.get()),))
        conn.commit()
        conn.close()
        t1.insert(END,"SUCCESSFULLY DELETED THE USER\n")

#function to update the entreis. NEED UPDATION TO UPDATE ONE ENTRY/ ALL ENTRIES WALI CHOICE:
def update_student():
    ret=verifier()
    if ret==0:
        conn=connection()
        cur=conn.cursor()
        cur.execute("UPDATE STUDENTS SET NAME=?,ROLL_NO=?,BRANCH=?,PHONE_NO=?,FATHER=?,ADDRESS=? where ROLL_NO=?",(student_name.get(),int(roll_no.get()),branch.get(),int(phone.get()),father.get(),address.get(),int(roll_no.get())))
        conn.commit()
        conn.close()
        t1.insert(END,"UPDATED SUCCESSFULLY\n")


def clse():
    sys.exit() 


if __name__=="__main__":
    root=Tk()
    root.title("Students Record Management System")
     
    student_name=StringVar()
    roll_no=StringVar()
    branch=StringVar()
    phone=StringVar()
    father=StringVar()
    address=StringVar()
    
    label1=Label(root,text="STUDENT NAME:")
    label1.place(x=0,y=0)

    label2=Label(root,text="ROLL NUMBER:")
    label2.place(x=0,y=30)

    label3=Label(root,text="BRANCH:")
    label3.place(x=0,y=60)

    label4=Label(root,text="PHONE NUMBER:")
    label4.place(x=0,y=90)

    label5=Label(root,text="FATHER'S NAME:")
    label5.place(x=0,y=120)

    label6=Label(root,text="LOCAL ADDRESS:")
    label6.place(x=0,y=150)

    e1=Entry(root,textvariable=student_name)
    e1.place(x=100,y=0)

    e2=Entry(root,textvariable=roll_no)
    e2.place(x=100,y=30)

    e3=Entry(root,textvariable=branch)
    e3.place(x=100,y=60)

    e4=Entry(root,textvariable=phone)
    e4.place(x=100,y=90)
    
    e5=Entry(root,textvariable=father)
    e5.place(x=100,y=120)

    e6=Entry(root,textvariable=address)
    e6.place(x=100,y=150)
    
    t1=Text(root,width=80,height=20)
    t1.grid(row=10,column=1)
   

    b1=Button(root,text="ADD ENTRY ",command=add_student,width=40)
    b1.grid(row=11,column=0)

    b2=Button(root,text="VIEW ENTRIES",command=view_student,width=40)
    b2.grid(row=12,column=0)

    b3=Button(root,text="DELETE ENTRY",command=delete_student,width=40)
    b3.grid(row=13,column=0)

    b4=Button(root,text="UPDATE ENTRY",command=update_student,width=40)
    b4.grid(row=14,column=0)

    b5=Button(root,text="CLOSE APPLICATION",command=clse,width=40)
    b5.grid(row=15,column=0)


    root.mainloop()
