import mysql.connector
from flask import Flask,request,render_template


app = Flask(__name__)

con = mysql.connector.connect(
    user = 'root',
    password = '',
    host = 'localhost',
    database = 'revenue'
)

cur = con.cursor()

@app.route("/database")
def home():
    return render_template("add_data.html")

@app.route("/add",methods = ['POST'])

def add_data():
    date = request.form["date"]
    amnt = request.form["amt"] #string
    source = request.form["src"]

    if (date == "") or (amnt == "") or (source == ""):
         return render_template("add_data.html",null_factor = True)
    else:
        amount = int(amnt) #now it is in integer
        cur.execute("insert into revenue_details(transaction_date, amount, source, Time) values (%s,%s,%s,NOW())",(date,amount,source))
        con.commit()
        return render_template("add_data.html",x = amount)
    


    

@app.route("/choose",methods = ["POST"])
def main():
    x = request.form["opt"]
    if x == "Daily":
            cur.execute("SELECT transaction_date, SUM(amount) FROM revenue_details GROUP BY transaction_date ORDER BY transaction_date")
            sum1 = cur.fetchall()
            if not sum1 :
                 return render_template("add_data.html",value1 = True)
            else:
                sum = [(date, int(amount)) for date, amount in sum1]
                return render_template("add_data.html",sum = sum,selected = x)
    
    elif x == "Monthly":
        cur.execute( "SELECT YEAR(transaction_date), MONTHNAME(transaction_date),SUM(amount) FROM revenue_details GROUP BY YEAR(transaction_date), MONTH(transaction_date) ORDER BY YEAR(transaction_date), MONTH(transaction_date)")
        monthly = cur.fetchall()
        month1 = [(year ,month,int(amount)) for year , month , amount in monthly]
        if not monthly:
             return render_template("add_data.html",value2 = True)
        else:
                return render_template("add_data.html",month = month1,selected = x)
        
    elif x == "Yearly":
        cur.execute("SELECT YEAR(transaction_date), SUM(amount) FROM revenue_details GROUP BY YEAR(transaction_date)")
        year1 = cur.fetchall()
        year = [(year,int(amount)) for year,amount in year1]
        if not year1:
             return render_template("add_data.html",value3 = True)
        else:
            
            return render_template("add_data.html",year = year,selected = x)
        
    elif x == "Total_revenue": 
         cur.execute("SELECT SUM(amount) FROM revenue_details")
         total1 = cur.fetchone()
         total1 = total1[0] if total1[0] else 0
         if not total1:
             return render_template("add_data.html",value4 = True)
         else:
             
             return render_template("add_data.html",total2 = total1,selected = x)
    
    elif x == "Revenue_btw":

        s_date = request.form["start"]
        e_date = request.form["end"]
        print("start date",s_date)
        print("end date",e_date)        

        if (s_date == "") or  (e_date == "") :  
             return render_template("add_data.html",null_date = True)
        
        elif s_date > e_date:
            return render_template("add_data.html",s_date = s_date,e_date = e_date)
        elif  s_date < e_date:

            cur.execute("SELECT SUM(amount) FROM revenue_details WHERE transaction_date BETWEEN %s AND %s",(s_date, e_date))
            sum1 = cur.fetchone()
            sum = sum1[0] if sum1[0] else 0
            cur.execute("SELECT AVG(amount) FROM revenue_details WHERE transaction_date BETWEEN %s AND %s",(s_date, e_date))
            avg1 = cur.fetchone()
            avg = avg1[0] if avg1[0] else 0
            if not avg:
             return render_template("add_data.html",value5 = True)
            else:
             return render_template("add_data.html",total = sum,start = s_date,end = e_date,average = avg,selected = x)
    

@app.route("/source",methods = ["POST"])
def source():
     cur.execute("SELECT source, SUM(amount) FROM revenue_details GROUP BY source")
     source1 = cur.fetchall()
     source = [(source , int(amount)) for source,amount in source1]

     if not source1:
             return render_template("add_data.html",value6 = True)
     else:
        return render_template("add_data.html",source = source)



app.run(debug=True)