import pandas as pd
from datetime import datetime
import requests
import os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
SHEET_ID=os.getenv("SHEET_ID")   # 🔥 NEW (Google Sheet)

def send_message(text):
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":text})

def format_student(r):
    return f"""
🎉 Birthday Alert 🎂

Name: {r.get('Students Full Name','')}
Branch: {r.get('Branch','')}
College ID: {r.get('College ID','')}
Section: {r.get('Sec','')}
Gender: {r.get('Gender','')}
DoB: {r.get('DoB','')}

SSC: {r.get('SSC %','')}% ({r.get('YOP SSC','')})
HSSC: {r.get('HSSC %','')}% ({r.get('YOP HSSC','')})
Diploma: {r.get('DIPLOMA %','')}% ({r.get('DIPLOMA YOP','')})

SGPA: {r.get('SGPA1','')}, {r.get('SGPA2','')}, {r.get('SGPA3','')}, {r.get('SGPA4','')}, {r.get('SGPA5','')}
AVG: {r.get('AVG','')}

Mobile: {r.get('STUDENT MOBILE NO.','')}
Personal Email: {r.get('Personal Email ID','')}
College Email: {r.get('EMAIL ID','')}
""".strip()

def check_birthdays():

    # =====================================================
    # ❌ OLD METHOD (EXCEL FILE) — KEPT FOR REFERENCE
    # =====================================================
    # df=pd.read_excel("students.xlsx")
    # df.columns=df.columns.str.strip()

    # =====================================================
    # ✅ NEW METHOD (GOOGLE SHEETS) — ACTIVE
    # =====================================================
    url=f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    df=pd.read_csv(url)
    df.columns=df.columns.str.strip()

    today=datetime.now().strftime("%d-%m")
    df["DoB"]=pd.to_datetime(df["DoB"],errors="coerce").dt.strftime("%d-%m")

    today_students=df[df["DoB"]==today]

    # ✅ NO BIRTHDAY CASE
    if today_students.empty:
        send_message("🎂 No birthday today.")
        return

    # ✅ BIRTHDAY FOUND
    for _,r in today_students.iterrows():
        send_message(format_student(r))

if __name__=="__main__":
    check_birthdays()
