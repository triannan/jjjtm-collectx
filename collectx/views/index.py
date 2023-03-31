"""
collectx index (main) view.

URLs include:
/
"""
from os import path
import flask
import collectx
from collectx.config import UPLOAD_FOLDER


@collectx.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('landing'))
    logname = flask.session['username']
    connection = collectx.model.get_db()
    cur = connection.execute(
        "SELECT collections.collectionid, collections.collectionname, collections.filename "
        "FROM collections "
        "WHERE collections.owner == ?",
        (logname, )

    )
    collections = cur.fetchall()
    context = {"collections": collections, "logname": logname}
    return flask.render_template("index.html", **context)

@collectx.app.route('/uploads/<filename>')
def files(filename):
    """Files."""
    if 'username' not in flask.session:
        flask.abort(403)
    if not path.exists(path.join(UPLOAD_FOLDER, filename)):
        flask.abort(404)
    return flask.send_from_directory(UPLOAD_FOLDER,
                                     filename, as_attachment=True)
