from flask import Flask, render_template, request
import requests
import smtplib
import os


posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
filled_in_info = False

MY_EMAIL = os.environ.get('email')
PASSWORD = os.environ.get('password')

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


def send_email(name, email, phone_num, message):
    message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone Number: {phone_num}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        NAME = request.form['name']
        EMAIL = request.form['email']
        PHONE = request.form['phone']
        MESSAGE = request.form['message']
        send_email(name=NAME, email=EMAIL, phone_num=PHONE, message=MESSAGE)

        return render_template("contact.html", got_info=True)
    else:
        return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
