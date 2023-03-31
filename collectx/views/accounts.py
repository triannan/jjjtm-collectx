"""
collectx accounts view.

URLs include:
/
"""
import os
import pathlib
import hashlib
import uuid
import flask
import collectx


@collectx.app.route('/accounts/landing/', methods=['GET'])
def landing():
    """Landing."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for("show_index"))
    return flask.render_template("landing.html")

@collectx.app.route('/accounts/login/', methods=['GET'])
def login():
    """Login."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for("show_index"))
    return flask.render_template("login.html")


@collectx.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('landing'))


@collectx.app.route('/accounts/create/', methods=['GET'])
def create():
    """Create."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for("edit"))
    return flask.render_template("create.html")

def hash_pass(salt, passw):
    """Hash pass."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + passw
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    pass_db_string = "$".join([algorithm, salt, password_hash])
    return pass_db_string

def login_post(req):
    """Login POST."""
    username = req.get("username")
    passw = req.get("password")
    connection = collectx.model.get_db()
    if username is None:
        flask.abort(400)
    if passw is None:
        flask.abort(400)
    cur = connection.execute(
        "SELECT users.username, users.password "
        "FROM users "
        "WHERE users.username == ? ",
        (username, )
    )
    user = cur.fetchone()
    if user is None:
        flask.abort(403)
    pass_db_string = hash_pass(user['password'][7:39], passw)
    if user['username'] == username and user['password'] == pass_db_string:
        flask.session["username"] = username
        flask.session['password'] = pass_db_string
    else:
        flask.abort(403)

def create_post(req):
    """Create POST."""
    req = flask.request.form
    username = req.get("username")
    passw = req.get("password")
    connection = collectx.model.get_db()
    if [x for x in (username, passw) if x is None]:
        flask.abort(400)

    password_db_string = hash_pass(uuid.uuid4().hex, passw)

    cur = connection.execute(
        "SELECT users.username "
        "FROM users "
        "WHERE users.username == ? ",
        (username, )
    )
    user = cur.fetchall()
    if not user:
        cur = connection.execute(
            "INSERT INTO users "
            "(username, password, filename) "
            "VALUES (?, ?, ?) ",
            (username, password_db_string, 'profile_picture.png')
        )
        connection.commit()
    else:
        flask.abort(409)
    flask.session["username"] = username
    flask.session['password'] = password_db_string

@collectx.app.route('/accounts/edit/', methods=['GET'])
def edit():
    """Edit."""
    if 'username' not in flask.session:
        flask.abort(403)
    connection = collectx.model.get_db()
    cur = connection.execute(
            "SELECT users.username, users.bio, users.name "
            "FROM users "
            "WHERE users.username == ? ",
            (flask.session['username'], )
        )
    user = cur.fetchone()
    bio = user['bio']
    name = user['name']
    context = {"logname": flask.session['username'], "bio": bio,
               "name": name}
    return flask.render_template("edit_profile.html", **context)

def edit_account_post(req):
    """Edit POST."""
    if 'username' not in flask.session:
        flask.abort(403)
    name = req.get("name")
    bio = req.get("bio")
    connection = collectx.model.get_db()
    if [x for x in (name, bio) if x is None]:
        flask.abort(400)
    fileobj1 = flask.request.files["file"]
    filename = fileobj1.filename
    if filename is None:
        connection.execute(
            "UPDATE users "
            "SET name = ?, bio = ? "
            "WHERE username == ? ",
            (name, bio, flask.session['username'])
        )
    else:
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        path = collectx.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj1.save(path)
        connection.execute(
            "UPDATE users "
            "SET name = ?, bio = ?, filename = ? "
            "WHERE username == ? ",
            (name, bio, uuid_basename, flask.session['username'])
        )
    connection.commit()

@collectx.app.route('/accounts/', methods=['POST'])
def account():
    """Account."""
    data = flask.request.args.get("target")
    req = flask.request.form

    if req.get("operation") == "login":
        login_post(req)
        return flask.redirect(flask.url_for('show_index'))
    if req.get("operation") == "create":
        create_post(req)
        return flask.redirect(flask.url_for('show_index'))
    if req.get("operation") == "edit_account":
        edit_account_post(req)
        return flask.redirect(flask.url_for('show_profile', username=flask.session['username']))
    return flask.redirect(data)
