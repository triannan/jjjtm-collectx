"""
collectx collection view.

URLs include:
/
"""
import os
import pathlib
import uuid
import flask
import arrow
import collectx


@collectx.app.route('/collections/<collectionid>/')
def show_collection(collectionid):
    """Display collection."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']
    connection = collectx.model.get_db()
    cur = connection.execute(
        "SELECT collections.collectionname, collections.collectionid, collections.owner "
        "FROM collections "
        "WHERE collections.collectionid == ?",
        (collectionid, )
    )
    collection = cur.fetchone()
    cur = connection.execute(
        "SELECT item.itemname, item.owner, item.collectionid, item.itemseries, item.filename, item.description, item.condition, item.created, item.itemid "
        "FROM item "
        "WHERE item.collectionid == ? ",
        (collectionid, )
    )
    items = cur.fetchall()
    cur = connection.execute(
        "SELECT users.filename "
        "FROM users "
        "WHERE users.username == ?",
        (collection['owner'], )
    )
    ownerfile = cur.fetchone()
    context = {"ownerfile": ownerfile['filename'], "owner": collection['owner'], "logname": logname, "collectionname": collection['collectionname'], "collectionid": collection['collectionid'], "items": items}
    return flask.render_template("show_collection.html", **context)

@collectx.app.route('/collections/create/')
def create_collections_page():
    """Create collection."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']
    context = {"logname": logname}
    return flask.render_template("create_collection.html", **context)


@collectx.app.route('/collections/', methods=["POST"])
def create_collection():
    """Collections POST."""
    logname = flask.session['username']
    data = flask.request.args.get("target")
    if data is None:
        data = '/'
    req = flask.request.form
    connection = collectx.model.get_db()

    if req.get("operation") == "create":
        if req.get("collectionname") is None:
            flask.abort(400)
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        path = collectx.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection.execute(
            "INSERT INTO collections "
            "(owner, collectionname, filename) "
            "VALUES (?, ?, ?) ",
            (logname, req.get("collectionname"), uuid_basename)
        )
    connection.commit()
    return flask.redirect(data)

@collectx.app.route('/collections/item/<itemid>/')
def show_item(itemid):
    """Display item."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname1 = flask.session['username']
    connection = collectx.model.get_db()
    cur = connection.execute(
        "SELECT item.itemname, item.itemseries, item.filename, item.description, item.condition, item.created, item.owner, item.itemid "
        "FROM item "
        "WHERE item.itemid == ? ",
        (itemid, )
    )
    items = cur.fetchall()[0]
    cur = connection.execute(
        "SELECT users.filename "
        "FROM users "
        "WHERE users.username == ? ",
        (items['owner'], )
    )
    ownerfile = cur.fetchone()
    context = {"ownerfile": ownerfile['filename'], "itemid": items['itemid'], "itemowner": items['owner'], "logname": logname1, "itemname": items['itemname'], "itemseries": items['itemseries'], "filename": items['filename'], 
               "description": items['description'], "condition": items['condition'], "created": arrow.get(items['created']).format('MMM Do, YYYY')}
    return flask.render_template("item_info.html", **context)

@collectx.app.route('/items/create/<collectionid>/', methods=['GET'])
def create_item_page(collectionid):
    """Items page GET."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    connection = collectx.model.get_db()
    cur = connection.execute(
        "SELECT collections.collectionname "
        "FROM collections "
        "WHERE collections.collectionid == ?",
        (collectionid, )
    )
    collection = cur.fetchone()
    context = {"collectionid": collectionid, "collectionname": collection['collectionname']}
    return flask.render_template("create_item.html", **context)

@collectx.app.route('/items/', methods=["POST"])
def create_item():
    """Items POST."""
    logname = flask.session['username']
    data = flask.request.args.get("target")
    if data is None:
        data = '/'
    req = flask.request.form
    connection = collectx.model.get_db()

    if req.get("operation") == "create":
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        path = collectx.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection.execute(
            "INSERT INTO item "
            "(filename, owner, itemname, itemseries, description, condition, collectionid ) "
            "VALUES (?, ?, ?, ?, ?, ?, ?) ",
            (uuid_basename, logname, req.get("itemname"), 
             req.get("itemseries"), req.get("description"), req.get("condition"), req.get("collectionid"))
        )
    if req.get("operation") == "delete":
        cur = connection.execute(
            "SELECT item.owner, item.filename "
            "FROM item "
            "WHERE item.itemid == ? ",
            (req.get("itemid"), )
        )
        item = cur.fetchone()
        if item['owner'] != logname:
            flask.abort(403)
        filename = item['filename']
        path = collectx.app.config["UPLOAD_FOLDER"]/filename
        os.remove(path)
        connection.execute(
            "DELETE FROM item "
            "WHERE itemid == ? ",
            (req.get("itemid"), )
        )
    return flask.redirect(data)