from flask import Flask, abort, render_template, request
from modules.repos.repository import Repository, Owner, Commit

app = Flask(__name__)

title = "Информация о пользователе Git Hub"


@app.route('/', methods=['GET'])
def home():

    form = render_template("form.html")
    data = {
        "title": title,
        "content": form
    }

    return render_template('index.html', **data)


@app.route('/', methods=['POST'])
def user_info():
    username = request.values.get('username', None)


    usersss = Owner(username)
    user_info = usersss.first()
    user_repos = Repository(username).all().select(["html_url", "name"]).get()
    # commit_count = Commit(username).all().count()

    if not usersss.status == "200 OK":
        abort(404)

    info = {
        "login": user_info.get("login"),
        "avatar": user_info.get("avatar_url"),
        "url": user_info.get("html_url"),
        "id": user_info.get("id"),
        "repos": user_repos,
        "status": usersss.status
    }

    content = render_template("user_info.html", **info)

    data = {
        "title": title,
        "content": content
    }

    return render_template('index.html', **data)

if __name__ == '__main__':
    app.debug = True
    app.run()