from database_functions import *
from init_database import *

conn, cur = connect()
add_link(conn, cur, 10, 102)