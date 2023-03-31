"""collectx development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = (b"\x7f\xff\xfc\x88\xe9\\\xc7\x07\xdbg"
              b"\xc9l\xf0'\x8e\x97oCV\x02\x94K\x9c\xf6")
SESSION_COOKIE_NAME = 'login'
# File Upload to var/uploads/
COLLECTX_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = COLLECTX_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
# Database file is var/collectx.sqlite3
DATABASE_FILENAME = COLLECTX_ROOT/'var'/'collectx.sqlite3'
