from flask import Flask, request, render_template, redirect ,flash, url_for
from flask_session import Session
import psycopg2

conn=psycopg2.connect(database='myduka',user='postgres',host='localhost',password='23126158',port='5432')
# conn = psycopg2.connect(database='d4eg9sklm38cmt', user='ibjyctkrxoaeta', host='ec2-52-210-120-210.eu-west-1.compute.amazonaws.com', password='ea2fdcc20c84a48ea8c07555cbb71d90df53b4cdcf9fea97296f99c4d896b7ed', port='5432')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS product1(id serial PRIMARY KEY, name VARCHAR(100), buying_price INT, selling_price INT, stock_quantity INT)")
cur.execute("CREATE TABLE IF NOT EXISTS sale1(id serial PRIMARY KEY, product_id INT, quantity INT,created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW())")
cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,user_name VARCHAR(20),email VARCHAR(25),password VARCHAR(15))")
conn.commit()


app = Flask(__name__)
app.config['SECRET_KEY'] = "THISISSECRET"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventor():
    if request.method == "POST":
        cur = conn.cursor()
        g = request.form["name"]
        h = request.form["BP"]
        i = request.form["SP"]
        j = request.form["stock"]
        cur.execute("""INSERT INTO product1(name,buying_price,selling_price,stock_quantity)VALUES(%(g)s,%(h)s,%(i)s,%(j)s)""", {
                    "g": g, "h": h, "i": i, "j": j})
        conn.commit()
        print(g, h, i, j)
        return redirect("/inventory")
    else:
        cur = conn.cursor()
        cur.execute("""SELECT * from product1 ORDER BY id ASC""")
        y = cur.fetchall()
        print(y)
        return render_template("inventory.html", y=y)


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "POST":
        cur = conn.cursor()
        k = request.form["item_id"]
        l = request.form["item_quantity"]
        cur.execute(
            """SELECT stock_quantity from product1 where id=%(k)s""", {"k": k})
        m = cur.fetchone()
        l = int(l)
        print(type(m))
        print(type(m[0]))
        print(type(l))
        print(type(l))
        n = m[0]-l
        if l >= 0:
            cur.execute("""UPDATE product1 SET stock_quantity=%(n)s WHERE id=%(k)s""", {
                        "n": n, "k": k})
            cur.execute("""INSERT INTO sale1(product_id,quantity)VALUES(%(k)s,%(l)s)""", {
                        "k": k, "l": l})
            conn.commit()
            return redirect("/sales")
        else:
            pass
    else:
        cur = conn.cursor()
        cur.execute("""SELECT * from sale1""")
        x = cur.fetchall()
        return render_template("sales.html", x=x)


@app.route("/dashboard")
def dash():
    cur = conn.cursor()
    cur.execute("""SELECT sum((product1.selling_price-product1.buying_price)*sale1.quantity) as profit,name FROM product1 JOIN sale1 on sale1.product_id=product1.id group by product1.name""")
    s = cur.fetchall()
    q = []
    r = []
    for p in s:
        q.append(p[0])
        r.append(p[1])
    cur.execute("""SELECT product1.name,SUM(sale1.quantity) FROM product1 JOIN sale1 on sale1.product_id=product1.id group by product1.name""")  
    t = cur.fetchall() 
    u=[]
    v=[]
    for w in s:
        u.append(w[0])
        v.append(w[1])
    print(u)
    print(v)
    return render_template("dashboard.html", s=s, q=q, r=r, t=t, u=u, v=v)

@app.route("/login",methods=["GET", "POST"])
def log():
    if request.method == "POST":
        cur = conn.cursor()
        a = request.form["email"]
        b = request.form["password"]
        cur.execute(
            """SELECT * from users where email=%(a)s OR password=%(b)s""", {"a": a,"b":b})
        c = cur.fetchone()
        if c:
            print("present")
            print(c)
            if c[2]==a and c[3]==b:
                print("correct credentials")
                return redirect(url_for('dash'))
            else:
                print("wrong input.please try again")
                return redirect(url_for('log'))
        else:
            print("user does not exist")

    else:    
        return render_template("login.html")

@app.route("/signin",methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        cur = conn.cursor()
        x = request.form["email"]
        y = request.form["username"]
        z = request.form["password"]
        print("my details", x,y,z)
        cur.execute("""INSERT INTO users(user_name,email,password)VALUES(%(x)s,%(y)s,%(z)s)""", {
                    "x": x, "y": y, "z": z})
        conn.commit()
        
        return redirect("/dashboard")
    else:     
        return render_template("signin.html")


if __name__ == "__main__":
    app.run(debug=True)
