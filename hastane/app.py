from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.models import db, Kullanici, Doktor, Hasta, Randevu  # models.py'yi doğru şekilde import ettik

# Flask Uygulaması
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gizli_anahtar'  # Flash mesajları için
db.init_app(app)

# Ana sayfa
@app.route("/")
def index():
    return render_template("index.html")

# Kayıt ol
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        email = request.form.get("email")
        sifre = request.form.get("sifre")

        # Kullanıcıyı veritabanına ekle (şifreyi şifrelemeden kaydediyoruz)
        yeni_kullanici = Kullanici(ad=ad, soyad=soyad, email=email, sifre=sifre, rol="hasta")
        db.session.add(yeni_kullanici)
        db.session.commit()
        flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Giriş yap
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        sifre = request.form.get("sifre")

        # Kullanıcıyı veritabanında bul
        kullanici = Kullanici.query.filter_by(email=email).first()
        if not kullanici:
            flash("Kullanıcı bulunamadı.", "danger")
            return render_template("login.html")

        if kullanici.sifre != sifre:
            flash("Şifre hatalı.", "danger")
            return render_template("login.html")

        # Giriş başarılı
        session["kullanici_id"] = kullanici.id
        session["kullanici_ad"] = kullanici.ad
        session["rol"] = kullanici.rol
        flash(f"Hoş geldiniz, {kullanici.ad}!", "success")

        # Rol bazlı yönlendirme
        if kullanici.rol == "hasta":
            return redirect(url_for("patient_dashboard"))
        elif kullanici.rol == "doktor":
            return redirect(url_for("doctor_dashboard"))
        elif kullanici.rol == "admin":
            return redirect(url_for("admin_dashboard"))

    return render_template("login.html")


# Hasta paneli
@app.route("/patient_dashboard")
def patient_dashboard():
    if "kullanici_id" not in session:
        flash("Lütfen giriş yapın.", "warning")
        return redirect(url_for("login"))

    kullanici_id = session["kullanici_id"]
    hasta = Hasta.query.filter_by(id=kullanici_id).first()

    if not hasta:
        flash("Bu panele erişim yetkiniz yok.", "danger")
        return redirect(url_for("index"))

    # Kullanıcının randevularını al
    randevular = Randevu.query.filter_by(hasta_id=hasta.id).all()

    return render_template("patient_dashboard.html", kullanici_ad=session.get("kullanici_ad"), randevular=randevular)

# Doktor paneli
@app.route("/doctor_dashboard")
def doctor_dashboard():
    if "kullanici_id" not in session or session.get("rol") != "doktor":
        flash("Lütfen giriş yapın.", "warning")
        return redirect(url_for("login"))
    return render_template("doctor_dashboard.html", kullanici_ad=session.get("kullanici_ad"))

# Admin paneli
@app.route("/admin_dashboard")
def admin_dashboard():
    if "kullanici_id" not in session or session.get("rol") != "admin":
        flash("Lütfen giriş yapın.", "warning")
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html", kullanici_ad=session.get("kullanici_ad"))

# Çıkış yap
@app.route("/logout")
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız.", "info")
    return redirect(url_for("index"))

@app.route("/randevu_al", methods=["GET", "POST"])
def randevu_al():
    if "kullanici_id" not in session:
        flash("Lütfen giriş yapın.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        doktor_id = request.form.get("doktor_id")
        tarih = request.form.get("tarih")
        saat = request.form.get("saat")

        yeni_randevu = Randevu(
            hasta_id=session["kullanici_id"],
            doktor_id=doktor_id,
            tarih=tarih,
            saat=saat
        )
        db.session.add(yeni_randevu)
        db.session.commit()
        flash("Randevunuz başarıyla oluşturuldu.", "success")
        return redirect(url_for("patient_dashboard"))

    doktorlar = Doktor.query.all()  # Tüm doktorları listele
    return render_template("randevu_al.html", doktorlar=doktorlar)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
