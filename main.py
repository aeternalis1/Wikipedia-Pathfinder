from init_database import *
from database_functions import *
from bfs import *

if __name__ == '__main__':
	#create_info_table()
	#create_links_table()
	print ('\n'.join(bfs('Minecraft', 'Gamecube')))