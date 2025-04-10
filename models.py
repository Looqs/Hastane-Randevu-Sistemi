from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Departman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    doktorlar = db.relationship('Kullanici', backref='departman', lazy=True)

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    sifre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, doktor, hasta
    aktif = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Doktor-spesifik alanlar
    uzmanlik = db.Column(db.String(100))
    calisma_saatleri = db.Column(db.String(50))  # Format: "08:00 - 17:00"
    departman_id = db.Column(db.Integer, db.ForeignKey('departman.id'), nullable=True)
    
    # İlişkiler
    doktor_randevulari = db.relationship('Randevu', backref='doktor', lazy=True, foreign_keys='Randevu.doktor_id')
    hasta_randevulari = db.relationship('Randevu', backref='hasta', lazy=True, foreign_keys='Randevu.hasta_id')

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hasta_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    doktor_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    tarih = db.Column(db.Date, nullable=False)
    saat = db.Column(db.String(5), nullable=False)  # Format: "14:30"
    durum = db.Column(db.String(20), nullable=False, default='beklemede')  # beklemede, onaylandı, iptal_edildi
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 