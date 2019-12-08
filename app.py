from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from sqlalchemy.sql import func         
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
import re     

app = Flask(__name__)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app.secret_key = "it's a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///band_underground.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate= Migrate(app,db)


#DB's

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255)) 
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


    
    
class Bands(db.Model):
    __tablename__ = "bands"
    id = db.Column(db.Integer, primary_key=True)
    band_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))#,nullable=False)
    author = db.relationship("Users", foreign_keys=[author_id], backref="users_bands")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    



#ROUTES


#INITIAL PAGE
@app.route("/")
def home():
    
    return render_template("home.html")


#CREATE ACCNT ROUTE
@app.route("/create_account")
def create_account_page():
    
    return render_template("account_creation.html")


#ACCOUNT TO DB ROUTE
@app.route("/add_user", methods = ["POST"])
def add_user():

    is_valid = True
    
    if len(request.form["fname"]) <2 or not request.form["fname"].isalpha():
        is_valid = False
        flash("Please enter your first name.")
    
    if len(request.form["lname"]) <2 or not request.form["lname"].isalpha():
        is_valid = False
        flash("Please enter your last name.")
    
    if len(request.form["em"]) <1:
        is_valid = False
        flash("Email cannot be blank.")
    if not EMAIL_REGEX.match(request.form["em"]):
        is_valid = False
        flash("Enter a valid Email.")
        
    if len(request.form["username"])<3 or len(request.form["username"])>30:
        is_valid = False
        flash("Username must be at least 3 characters long, and no longer than 30 characters. ")
    
    if len(request.form["pass"]) < 5:
        is_valid = False
        flash("Password must be at least 5 characters long.")
    
    if request.form["pass"] != request.form["con_pw"]:
        is_valid = False
        flash("Password does not match.")
    if not is_valid:
        return redirect("/create_account")
    
    if is_valid:
            
        pw_hash = bcrypt.generate_password_hash(request.form["pass"])

        register_user = Users(
            first_name = request.form["fname"],
            last_name = request.form["lname"],
            email = request.form["em"],
            username = request.form["username"],
            password = pw_hash,    
        )
        
        db.session.add(register_user)
        db.session.commit()
        
        session["user_id"] = register_user.id
        
        
    return redirect("/underground/dashboard")

#LOGIN ROUTE
@app.route("/login", methods=["POST"])
def login():
    
    is_valid=True
    
    if len(request.form["em"]) <1:
        is_valid=False
        flash("Enter your Email.")
    
 
    if len(request.form["pw"]) <1: 
        is_valid=False
        flash("Enter your password.")
    
    if not is_valid:
        return redirect("/")
    
    else:
    
        user_to_login = Users.query.filter_by(email=request.form["em"]).first()
        
    
        if user_to_login:
            
            if bcrypt.check_password_hash(user_to_login.password, request.form["pw"]):
                session["user_id"] = user_to_login.id
                
                return redirect("/underground/dashboard")
            else:
                flash("Invalid password.")
                return redirect("/")
        else:
            flash("Invalid email.")
            return redirect("/")




#FRONT PAGE ROUTE
@app.route("/underground/dashboard")
def main_dashboard():
    if "user_id" not in session:
        flash("Please sign in!")
        return redirect("/")
    
    else:
        #TODO FIND RIGHT QUERY

        user_id = Users.query.get(session["user_id"])
        
        # posts = Bands.query.filter_by(author_id=session["user_id"]).order_by(Bands.created_at.desc()).all()
        
        posted_by = Bands.query.filter_by(author_id=Users.id).all()
        all_bands_posted = Bands.query.order_by(Bands.created_at.desc()).all()
        
    
        
        
        return render_template("main.html", user_id = user_id, poster=posted_by, posts=all_bands_posted)



#PROFILE ROUTE
@app.route("/profile/<user_id>")
def user_profile(user_id):
    if "user_id" not in session:
        flash("Please sign in!")
        return redirect("/")
    else:
        user = Users.query.get(session["user_id"])
        
        bands_by_user = Bands.query.filter_by(author_id = session["user_id"]).all()
        print(bands_by_user)
        
        
        return render_template("your_profile.html", user = user , bands = bands_by_user)


#EDIT PROFILE INFO ROUTE
@app.route("/edit/<user_id>")
def edit_user(user_id):
    if "user_id" not in session:
        flash("Please sign in!")
        return redirect("/")
    else:
        user = Users.query.get(session["user_id"])
        
        return render_template("edit_profi.html", user = user)
    
#UPDATE PROFILE INFO
@app.route("/update_user/<user_id>", methods=["POST"])
def update_user(user_id):
    
    is_valid = True
    
    if len(request.form["fname"]) <2 or not request.form["fname"].isalpha():
        is_valid = False
        flash("Please enter your first name.")
    
    if len(request.form["lname"]) <2 or not request.form["lname"].isalpha():
        is_valid = False
        flash("Please enter your last name.")
    
    if len(request.form["em"]) <1:
        is_valid = False
        flash("Email cannot be blank.")
    if not EMAIL_REGEX.match(request.form["em"]):
        is_valid = False
        flash("Enter a valid Email.")
        
    if len(request.form["username"])<3 or len(request.form["username"])>30:
        is_valid = False
        flash("Username must be at least 3 characters long, and no longer than 30 characters. ")
    if not is_valid:
        return redirect("/create_account")
    
    if is_valid:
        
        updated_user = Users.query.get(session["user_id"])
        
        updated_user.first_name = request.form["fname"]
        updated_user.last_name = request.form["lname"]
        updated_user.email = request.form["em"]
        updated_user.username = request.form["username"]

        db.session.commit()
        flash("Info Updated!")   
    return redirect(f"/profile/{user_id}")



#POST BAND PAGE ROUTE
@app.route("/post_band")
def post_page():
    if "user_id" not in session:
        flash("Please log in!")
        return redirect("/")
    else:
        user_id= Users.query.get(session["user_id"])
    
        return render_template("post_band.html", user_id = user_id)


#POST & SAVE BAND TO DB
@app.route("/create_post", methods=["POST"])
def create_band_post():
    if "user_id" not in session:
        flash("Please log in!")
        return redirect("/")
    
    is_valid = True

    if len(request.form["band_name"])<1:
        is_valid = False
        flash("Please enter a band name!")
        return redirect("/post_band")
    if len(request.form["local"])<1:
        is_valid = False
        flash("Please enter bands location!")
        return redirect("/post_band")
    if len(request.form["descrip"])<10 or len(request.form["descrip"])>300:
        is_valid = False
        flash("Description can't be less than 10 characters and can't be longer than 300 characters.")
        return redirect("/post_band")

    if is_valid:
        
        band_post = Bands(
            band_name = request.form["band_name"],
            location = request.form["local"],
            description = request.form["descrip"],
            author_id = session["user_id"]
        )
        
        db.session.add(band_post)
        db.session.commit()
        
        flash("Band Posted!")
        return redirect("/underground/dashboard")



#EDIT BAND INFO
@app.route("/edit_band/<bandid>")  
def edit_band_page(bandid):        
    if "user_id" not in session:
        flash("Please sign in!")
        return redirect("/")
    else:
        user = Users.query.get(session["user_id"])
        
        #FIND RIGHT QUERY
        bands = Bands.query.get(bandid)
        
        return render_template("edit_band_post.html", user = user, bands = bands)



#UPDATE BAND INFO
@app.route("/update_band/<bandid>", methods=["POST"]) 
def update_band(bandid):                              
    
    if "user_id" not in session:
        flash("Please log in!")
        return redirect("/")
    
    is_valid = True

    if len(request.form["band_name"])<1:
        is_valid = False
        flash("Please enter a band name!")
        return redirect("/edit_band/<bandid>")
    if len(request.form["local"])<1:
        is_valid = False
        flash("Please enter bands location!")
        return redirect("/edit_band/<bandid>")
    if len(request.form["descrip"])<10 or len(request.form["descrip"])>300:
        is_valid = False
        flash("Description can't be less than 10 characters and can't be longer than 300 characters.")
        return redirect("/edit_band/<bandid>")

    if is_valid:
        
        updated_post = Bands.query.get(bandid)
        
        updated_post.band_name = request.form["band_name"]
        updated_post.location = request.form["local"]
        updated_post.description = request.form["descrip"]
        
        db.session.commit()

        flash("Info Updated!")   
        return redirect("/profile/<user>")



#DELETE BAND INFO
@app.route("/delete_band/<bandid>") 
def delete_band(bandid):           
    if "user_id" not in session:
        flash("Please sign in!")
        return redirect("/")
    else:
        
        
        delete_band = Bands.query.get(bandid)
        db.session.delete(delete_band)
        db.session.commit()
        
        flash("Band deleted. Guess they broke up...")
        return redirect("/profile/<user>")



#LOGOUT ROUTE
@app.route("/logout")
def logout():
    
    session.clear()
    flash("Logged out!")
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
    