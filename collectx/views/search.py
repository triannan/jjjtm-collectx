"""
collectx search view.

URLs include:
/
"""
from os import path
import flask
import collectx
from collectx.config import UPLOAD_FOLDER


@collectx.app.route('/search/', methods=['POST'])
def search():
    """Search."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    
    req = flask.request.form
    query = req.get("q").split()
    print(query)
    connection = collectx.model.get_db()
    cur = connection.execute(
        "SELECT item.itemid, item.itemname, item.filename "
        "FROM item "
    )
    items = cur.fetchall()
    filt = []
    if query:
        for item in items:
            for q in query:
                if q.lower() in item['itemname'].lower():
                    filt.append(item)
                    break
    context = {"items": filt}
    return flask.render_template("search.html", **context)
