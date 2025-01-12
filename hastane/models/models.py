from flask_sqlalchemy import SQLAlchemy

# Veritabanı nesnesi
db = SQLAlchemy()

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50))
    soyad = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20))

    def __repr__(self):
        return f"<Kullanici {self.ad} {self.soyad}>"

class Doktor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50))
    soyad = db.Column(db.String(50))
    uzmanlik = db.Column(db.String(100))

    def __repr__(self):
        return f"<Doktor {self.ad} {self.soyad}>"

class Hasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50))
    soyad = db.Column(db.String(50))
    telefon = db.Column(db.String(15))

    def __repr__(self):
        return f"<Hasta {self.ad} {self.soyad}>"

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hasta_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    doktor_id = db.Column(db.Integer, db.ForeignKey('doktor.id'), nullable=False)
    tarih = db.Column(db.String(20))
    saat = db.Column(db.String(5))

    # İlişkiler
    hasta = db.relationship('Kullanici', backref=db.backref('randevular', lazy=True))
    doktor = db.relationship('Doktor', backref=db.backref('randevular', lazy=True))

    def __repr__(self):
        return f"<Randevu {self.tarih} {self.saat}>"
