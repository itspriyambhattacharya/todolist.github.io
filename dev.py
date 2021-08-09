from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TodoDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todoApp(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    desc = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

# index.html

@app.route("/")
def hello_world():
    allToDos = todoApp.query.all()
    return render_template('index.html' , alt = allToDos)



@app.route('/form' , methods = ['GET' , 'POST'] )
def form() :
    if request.method == 'POST' :
        t = request.form['title']
        d = request.form['desc']
        send = todoApp(title = t , desc = d)
        db.session.add(send)
        db.session.commit()
    return redirect('/')



# update.html

@app.route('/update/<int:upd>', methods = ['GET' , 'POST'] )
def update(upd):
    update_todo = todoApp.query.filter_by(Sno = upd).first()
    if request.method == "POST" :
        ut = request.form['title']
        udesc = request.form['desc']
        updateobj = todoApp.query.filter_by(Sno = upd).first()
        updateobj.title = ut
        updateobj.desc = udesc
        db.session.add(updateobj)
        db.session.commit()
        return redirect('/')
    return render_template('update.html' , utd = update_todo)



@app.route("/delete/<int:s>")
def delete_rec(s) :
    data = todoApp.query.filter_by(Sno = s).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)