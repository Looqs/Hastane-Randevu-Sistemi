from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Veritabanı nesnesi
db = SQLAlchemy()

class Departman(db.Model):
    """Hastane departmanlarını tutan model"""
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    doktorlar = db.relationship('Kullanici', backref='departman', lazy=True)

    def __repr__(self):
        return f"<Departman {self.ad}>"

class Kullanici(db.Model):
    """Kullanıcı bilgilerini tutan model"""
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(20))
    sifre = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'hasta', 'doktor', 'admin'
    aktif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Doktor-spesifik alanlar
    departman_id = db.Column(db.Integer, db.ForeignKey('departman.id'))
    uzmanlik = db.Column(db.String(100))
    calisma_saatleri = db.Column(db.String(500))
    
    def __repr__(self):
        return f"<Kullanici {self.ad} {self.soyad} ({self.rol})>"

class Randevu(db.Model):
    """Randevu bilgilerini tutan model"""
    id = db.Column(db.Integer, primary_key=True)
    hasta_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    doktor_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    tarih = db.Column(db.Date, nullable=False)
    saat = db.Column(db.String(5), nullable=False)
    durum = db.Column(db.String(20), default='beklemede')  # 'beklemede', 'onaylandı', 'iptal_edildi'
    notlar = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    hasta = db.relationship('Kullanici', foreign_keys=[hasta_id], 
                          backref=db.backref('hasta_randevulari', lazy=True))
    doktor = db.relationship('Kullanici', foreign_keys=[doktor_id], 
                           backref=db.backref('doktor_randevulari', lazy=True))

    def __repr__(self):
        return f"<Randevu {self.tarih} {self.saat} - Durum: {self.durum}>"
