from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "activo": self.is_active
            # do not serialize the password, its a security breach
        }

class Ciudad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    himno = db.Column(db.String(250), nullable=False)
    color_bandera = db.Column(db.String(250), nullable=False)
    teams = db.relationship('Equipo', backref='ciudad', lazy=True)

    def __repr__(self):
        return '<Ciudad  %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "himno":self.himno
            # do not serialize the password, its a security breach
        }    


class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)
    estadios = db.Column(db.String(250), nullable=False)  
    ciudad_id = db.Column(db.Integer, db.ForeignKey('ciudad.id'),
        nullable=False)

    def __repr__(self):
        return '<Equipos Team %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estadios":self.estadios
            # do not serialize the password, its a security breach
        }
    

    
