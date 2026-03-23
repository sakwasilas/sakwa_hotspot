from flask import Flask, render_template, request, redirect, url_for, flash
from connections import SessionLocal
from models import Package, Payment

app = Flask(__name__)
app.secret_key = "silas_wifi_secret"


@app.route("/")
def index():
    db = SessionLocal()
    try:
        packages = db.query(Package).all()
        print("PACKAGES:", packages)
        return render_template("index.html", packages=packages)
    finally:
        db.close()

@app.route("/create-packages")
def create_packages():
    db = SessionLocal()
    try:
        packages = [
            Package(name="1 Hour", price=10, duration_minutes=60, description="Affordable browsing for one hour", is_active=True),
            Package(name="2 Hours", price=15, duration_minutes=120, description="Stay connected for two hours", is_active=True),
            Package(name="3 Hours", price=20, duration_minutes=180, description="Great for videos and downloads", is_active=True),
            Package(name="Full Day", price=100, duration_minutes=1440, description="Unlimited access for the whole day", is_active=True),
        ]

        for package in packages:
            db.add(package)

        db.commit()
        return "Packages created successfully"
    finally:
        db.close()


@app.route("/buy/<int:package_id>", methods=["GET", "POST"])
def buy(package_id):
    db = SessionLocal()
    try:
        package = db.query(Package).filter_by(id=package_id, is_active=True).first()

        if not package:
            flash("Package not found")
            return redirect(url_for("index"))

        if request.method == "POST":
            phone = request.form.get("phone")

            if not phone:
                flash("Please enter phone number")
                return redirect(url_for("buy", package_id=package.id))

            new_payment = Payment(
                package_id=package.id,
                phone=phone,
                amount=package.price,
                status="Pending"
            )
            db.add(new_payment)
            db.commit()
            db.refresh(new_payment)

            return redirect(url_for("payment_page", payment_id=new_payment.id))

        return render_template("buy.html", package=package)
    finally:
        db.close()


@app.route("/payment/<int:payment_id>")
def payment_page(payment_id):
    db = SessionLocal()
    try:
        payment = db.query(Payment).filter_by(id=payment_id).first()

        if not payment:
            flash("Payment not found")
            return redirect(url_for("index"))

        package = db.query(Package).filter_by(id=payment.package_id).first()

        return render_template("payment.html", payment=payment, package=package)
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)