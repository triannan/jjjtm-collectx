"""Views, one for each collectx page."""
from os import access
from collectx.views.index import show_index
from collectx.views.accounts import login
from collectx.views.accounts import create
from collectx.views.accounts import landing
from collectx.views.collections import create_collections_page
from collectx.views.collections import show_collection
from collectx.views.collections import create_item_page
from collectx.views.collections import show_item
from collectx.views.search import search
from collectx.views.profile import show_profile