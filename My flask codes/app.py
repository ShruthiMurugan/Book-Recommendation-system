from flask import Flask, request, render_template

import rsmodel as rs
import pymysql as pms
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("login.html")

@app.route("/check", methods=['Post'])
def check():
    username = request.form['username']
    password = request.form['password']
    #return "Success!"

    conn=pms.connect(host="localhost",port=3306,password="Shru@123",user="root",db="employees")
    cur=conn.cursor() #object for accessing queries
    cur.execute("select * from login")
    for i in cur.fetchall():
        if i[0]==username and i[1]==password:
            return render_template("success.html")
    return render_template("login.html",data="INVALID USER CREDENTIALS")

@app.route("/recommend", methods=['Post'])
def recommend():

    input_books = request.form['books']
    rec = rs.get_recommendations(input_books)
    return render_template("success.html",data=rec)

if __name__=='__main__':

    app.run(host='localhost',port=5022)