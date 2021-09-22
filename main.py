from flask import Flask,request,render_template,redirect
import psycopg2

conn=psycopg2.connect(database='myduka',user='postgres',host='localhost',password='23126158',port='5432')
# conn=psycopg2.connect(database='d4eg9sklm38cmt',user='ibjyctkrxoaeta',host='ec2-52-210-120-210.eu-west-1.compute.amazonaws.com',password='ea2fdcc20c84a48ea8c07555cbb71d90df53b4cdcf9fea97296f99c4d896b7ed',port='5432')
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS product1(id serial PRIMARY KEY, name VARCHAR(100), buying_price INT, selling_price INT, stock_quantity INT)")
cur.execute("CREATE TABLE IF NOT EXISTS sale1(id serial PRIMARY KEY, product_id INT, quantity INT,created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW())")
conn.commit()


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/inventory",methods=["GET","POST"])
def inventor():
    if request.method=="POST":
        cur=conn.cursor() 
        g=request.form["name"]
        h=request.form["BP"]
        i=request.form["SP"]
        j=request.form["stock"]
        cur.execute("""INSERT INTO product1(name,buying_price,selling_price,stock_quantity)VALUES(%(g)s,%(h)s,%(i)s,%(j)s)""",{"g":g,"h":h,"i":i,"j":j})
        conn.commit()
        print(g,h,i,j)
        return redirect("/inventory")
    else:
        cur=conn.cursor()
        cur.execute("""SELECT * from product1 ORDER BY id ASC""")
        y=cur.fetchall()
        print(y)
        return render_template("inventory.html",y=y)

@app.route("/sales",methods=["GET","POST"])
def sales():
    if request.method=="POST":
        cur=conn.cursor()
        k=request.form["item_id"]
        l=request.form["item_quantity"]
        cur.execute("""SELECT stock_quantity from product1 where id=%(k)s""",{"k":k})
        m=cur.fetchone()
        l=int(l)
        print(type(m))
        print(type(m[0]))
        print(type(l))
        print(type(l))
        n=m[0]-l
        if l>=0:
            cur.execute("""UPDATE product1 SET stock_quantity=%(n)s WHERE id=%(k)s""",{"n":n,"k":k})
            cur.execute("""INSERT INTO sale1(product_id,quantity)VALUES(%(k)s,%(l)s)""",{"k":k,"l":l})
            conn.commit()
            return redirect("/sales")
        else:
            pass 
    else:    
        cur=conn.cursor()
        cur.execute("""SELECT * from sale1""")
        x=cur.fetchall()
        return render_template("sales.html",x=x)

@app.route("/dashboard")
def dash():
    cur=conn.cursor()
    cur.execute("""SELECT sum((product1.selling_price-product1.buying_price)*sale1.quantity) as profit,name FROM product1 JOIN sale1 on sale1.product_id=product1.id group by product1.name""")
    s=cur.fetchall()
    print(s)
    q=[]
    r=[]
    for p in s:
        q.append(p[0])
        r.append(p[1])
    return render_template("dashboard.html",s=s,q=q,r=r)        

if __name__=="__main__":
    app.run(debug=True)
