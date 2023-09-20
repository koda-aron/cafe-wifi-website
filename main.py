from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AddCafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    has_sockets = BooleanField("Has sockets", validators=[DataRequired()])
    has_wifi = BooleanField("Has wi-fi", validators=[DataRequired()])
    can_take_calls = BooleanField("Can take calls", validators=[DataRequired()])
    has_toilet = BooleanField("Has toilet", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    map_url = StringField("Google Maps URL", validators=[DataRequired(), URL()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    coffee_price = StringField("Price of coffee", validators=[DataRequired()])
    img_url = StringField("Cafe Photo URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Add Cafe")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    cafes = [cafe.to_dict() for cafe in cafes]
    return render_template("index.html", cafes=cafes)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add-cafe", methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            has_sockets=form.has_sockets.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            has_toilet=form.has_toilet.data,
            location=form.location.data,
            map_url=form.map_url.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            img_url=form.img_url.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_cafe.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
