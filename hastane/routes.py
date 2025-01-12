from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from models import db, Kullanici

routes = Blueprint('routes', __name__)

@routes.route('/kayit', methods=['POST', 'GET'])
def kayit():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        email = request.form['email']
        sifre = request.form['sifre']

        yeni_kullanici = Kullanici(ad=ad, soyad=soyad, email=email, sifre=sifre, rol='hasta')
        db.session.add(yeni_kullanici)
        db.session.commit()

        flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
        return redirect(url_for('routes.giris'))
    return render_template('register.html')

@routes.route('/giris', methods=['POST', 'GET'])
def giris():
    if request.method == 'POST':
        email = request.form['email']
        sifre = request.form['sifre']

        kullanici = Kullanici.query.filter_by(email=email).first()

        if kullanici and kullanici.sifre == sifre:
            session['user_id'] = kullanici.id
            session['rol'] = kullanici.rol

            if kullanici.rol == 'hasta':
                return redirect(url_for('routes.hasta_paneli'))
            elif kullanici.rol == 'doktor':
                return redirect(url_for('routes.doktor_paneli'))
            elif kullanici.rol == 'admin':
                return redirect(url_for('routes.admin_paneli'))
        else:
            flash("Hatalı e-posta veya şifre", "danger")
            return render_template('login.html')

    return render_template('giris.html')

@routes.route('/hasta')
def hasta_paneli():
    return "Hasta Paneline Hoş Geldiniz!"

@routes.route('/doktor')
def doktor_paneli():
    return "Doktor Paneline Hoş Geldiniz!"

@routes.route('/admin')
def admin_paneli():
    return "Admin Paneline Hoş Geldiniz!"
