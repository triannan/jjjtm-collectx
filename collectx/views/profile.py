"""
Collectx user view.

URLs include:
/
"""
import flask
import collectx
from collectx.config import UPLOAD_FOLDER

@collectx.app.route('/profile/<username>/')
def show_profile(username):
    """Display /profile route."""
    connection = collectx.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname1 = flask.session['username']
    currr = connection.execute(
        "SELECT users.username "
        "FROM users "
        "WHERE users.username == ? ",
        (username, )
    )
    user_exists = currr.fetchone()
    if user_exists is None:
        flask.abort(404)
    cur = connection.execute(
        "SELECT users.username, users.filename, users.bio, users.name "
        "FROM users "
        "WHERE users.username == ? ",
        (username, )
    )
    users = cur.fetchone()

    cur = connection.execute(
        "SELECT collections.collectionname, collections.collectionid, collections.filename "
        "FROM collections "
        "WHERE collections.owner == ?",
        (username, )
    )
    collections = cur.fetchall()
    context = {"logname": logname1, "username": username,
               "users": users, "collections": collections}
    return flask.render_template("profile.html", **context)
