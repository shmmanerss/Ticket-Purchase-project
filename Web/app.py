# web/app.py
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from sqlalchemy.orm import selectinload

from event_ticketing.db import Base, engine, SessionLocal
from event_ticketing.models.user import UserDB
from event_ticketing.models.event import EventDB
from event_ticketing.models.ticket import TicketDB
from event_ticketing.qr import generate_qr_png
from event_ticketing.notify import send_mail
from event_ticketing.services.strategy import PaymentStrategy, SimplePaymentStrategy
from event_ticketing.services.factory import TicketFactory

RESERVE_MIN = 15
# ----------------- настройки -----------------
TEMPLATES = Path(__file__).parent / "templates"
app = Flask(__name__, template_folder=str(TEMPLATES))
app.secret_key = "dev-secret"
@app.context_processor
def inject_now():
    return {"now": datetime.now()}

# ----------------- инициализация БД -----------------
Base.metadata.create_all(engine)

# ----------------- Flask-Login -----------------
lm = LoginManager(app)
lm.login_view = "login"

@lm.user_loader
def load_user(uid: str):
    with SessionLocal() as db:
        return db.get(UserDB, int(uid))

# ----------------- маршруты -----------------
@app.route("/")
@app.route("/")
def index():
    with SessionLocal() as db:
        events = db.query(EventDB).all()
        return render_template("index.html",
                               events=events,
                               now=datetime.now())   


# ----- регистрация -----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with SessionLocal() as db:
            if db.query(UserDB).filter_by(email=request.form["email"]).first():
                flash("Email уже зарегистрирован"); return redirect(url_for("register"))
            u = UserDB(name=request.form["name"],
                       email=request.form["email"],
                       phone=request.form["phone"])
            u.set_password(request.form["password"])
            db.add(u); db.commit()
            flash("Регистрация успешна — войдите"); return redirect(url_for("login"))
    return render_template("register.html")

# ----- вход -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with SessionLocal() as db:
            user = db.query(UserDB).filter_by(email=request.form["email"]).first()
            if user and user.check_password(request.form["password"]):
                login_user(user); return redirect(url_for("index"))
            flash("Неверный email или пароль")
    return render_template("login.html")

# ----- выход -----
@app.route("/logout")
@login_required
def logout():
    logout_user(); return redirect(url_for("index"))

# ----- карточка события -----
@app.route("/event/<int:eid>")
def event_page(eid: int):
    with SessionLocal() as db:
        ev = db.get(EventDB, eid)
        return render_template("event.html", ev=ev, RESERVE_MIN=RESERVE_MIN)

# ----- резервирование -----
@app.route("/reserve/<int:eid>", methods=["POST"])
@login_required
def reserve(eid: int):
    try:
        # используем фабрику вместо ручного кода
        ticket = TicketFactory.create(
            event_id=eid,
            user_id=current_user.id,
            price=500
        )
    except Exception as e:
        flash("Нет свободных мест")
        return redirect(url_for("event_page", eid=eid))
    # на оплату — переходим по id созданного билета
    return redirect(url_for("pay", tid=ticket.id))

# ----- страница оплаты -----
@app.route("/pay/<int:tid>")
@login_required
def pay(tid: int):
    with SessionLocal() as db:
        t = db.get(TicketDB, tid)
        if not t or t.user_id != current_user.id:
            return "Ticket not found", 404
        remaining = RESERVE_MIN - int((datetime.now() - t.reserved_at).total_seconds() // 60)
        if remaining <= 0:
            t.event.available_seats += 1
            db.delete(t); db.commit()
            flash("Время брони истекло"); return redirect(url_for("index"))
        return render_template("pay.html", ticket=t,
                               remaining=remaining, RESERVE_MIN=RESERVE_MIN)


@app.route("/pay/<int:tid>/process", methods=["POST"])
@login_required
def process_payment(tid: int):
    with SessionLocal() as db:
        t = db.get(TicketDB, tid)
        if not t: return "Ticket not found", 404

        # таймаут
        if (datetime.now() - t.reserved_at) > timedelta(minutes=RESERVE_MIN):
            t.event.available_seats += 1
            db.delete(t); db.commit()
            flash("Время брони истекло"); return redirect(url_for("index"))

        # имитируем сбой
        if request.form.get("card") == "fail":
            flash("Ошибка оплаты"); return redirect(url_for("pay", tid=tid))

        # успешная оплата
        strategy: PaymentStrategy = SimplePaymentStrategy()
        try:
            strategy.pay(t, request.form.get("card"))
        except Exception:
            flash("Оплата не прошла")
            return redirect(url_for("pay", tid=tid))
       # Если не бросилось исключение — сохраняем факт оплаты
        db.commit()

        t.paid = True
        t.qr_png = generate_qr_png({"ticket": t.id})
        db.commit()

        # письмо с QR
        html = (f"<p>Оплата прошла успешно! Вы приобрели билет №<b>{t.id}</b> на "
                f"<b>{t.event.name}</b>.</p>"
                "<p>QR-код во вложении ниже:</p>"
                "<p><img src=\"cid:qr.png\"></p>")
        send_mail(t.user.email, f"Ваш билет #{t.id}", html_body=html, png_b64=t.qr_png)

    flash("Оплата успешна! Письмо отправлено.")
    return redirect(url_for("ticket_view", tid=tid))

# ----- просмотр билета -----
@app.route("/ticket/<int:tid>")
@login_required
def ticket_view(tid: int):
    with SessionLocal() as db:
        t = db.get(TicketDB, tid)
        if not t or t.user_id != current_user.id:
            return "Ticket not found", 404
        return render_template("ticket.html", ticket=t)

# ----- кабинет -----
@app.route("/cabinet")
@login_required
def cabinet():
    now = datetime.now()
    with SessionLocal() as db:
        tickets = (
            db.query(TicketDB)
              .filter_by(user_id=current_user.id)
              .options(selectinload(TicketDB.event))
              .all()
        )
        # удаляем просроченные не-оплаченные
        for t in list(tickets):
            if (not t.paid) and (now - t.reserved_at > timedelta(minutes=RESERVE_MIN)):
                t.event.available_seats += 1
                tickets.remove(t)
                db.delete(t)
        db.commit()
        return render_template("cabinet.html",
                               tickets=tickets,
                               RESERVE_MIN=RESERVE_MIN,
                               now=now)

# ----------------- запуск -----------------
if __name__ == "__main__":
    app.run(debug=True)
