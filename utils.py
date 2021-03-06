import argparse
import numpy as np
import re

def	get_args_argparse():
	"""Initialisation et ajout des arguments"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--hamming', '-a', action='store_true', help='hamming distance heuristic')
	parser.add_argument('--manhattan', '-m', action='store_true', help='manhattan distance heuristic')
	parser.add_argument('--linear_conflict', '-l', action='store_true', help='linear conflict heuristic ')
	parser.add_argument('--visual', '-v', action='store_true', help='trigger visualisation')
	parser.add_argument('--file', '-f', action='store', help='open a selected file')
	parser.add_argument('--states', '-s', action='store_true', help='print grid states')
	options = parser.parse_args()
	return options

"""def get_args_argparse():
	""Initialisation et ajout des arguments""
	parser = argparse.ArgumentParser()
	parser.add_argument('--hamming', '-a', action='store_true', help='hamming distance heuristic')
	parser.add_argument('--manhattan', '-m', action='store_true', help='manhattan distance heuristic')
	parser.add_argument('--linear_conflict', '-l', action='store_true', help='linear conflict heuristic')
	parser.add_argument('--visual', '-v', action='store_true', help='trigger visualisation')
	parser.add_argument('--file', '-f', action='store', help='open a selected file')
	parser.add_argument('--states', '-s', action='store_ture', help='print grid states')
    options = parser.parse_args()
	return options"""

def get_heuristic_type(options):
    """Parsing types heuristiques en arguments"""
    h_type = []
    if options.hamming:
        h_type.append("hamming")
    if options.manhattan:
        h_type.append("manhattan")
    if options.linear_conflict:
        h_type.append("linear_conflict")
    if len(h_type) > 1:
        return None
    elif len(h_type) == 0:
        h_type.append("linear_conflict")
    return str(h_type)

def get_file_info(tmp):
    tmpstr = ""
    for i in range(len(tmp) - 1):
        tmpstr += tmp[i] + '/'
    return tmpstr + "infos.txt"

def set_dico_infos(options):
    """Build du dictionnaire avec les informations
    sur le puzzle etc"""
    dico = {"size" : 0, "solvable" : None, "unsolvable" : None, "iteration" : 10000}
    try:
        if options.file:
            tmp = options.file.split('/')
            info = get_file_info(tmp)
            fd = open(info, "r+")
        else:
            fd = open("data/infos.txt", "r+")
    except:
        print("Look like there's some trouble with infos.txt")
        exit(1)
    infos = []
    for elem in fd:
        infos.append(elem)
    for i in range(len(infos)):
        infos[i] = infos[i].split('=')
    try:
        try:
            dico["size"] = int(infos[0][1])
            dico["iteration"] = int(infos[3][1])
        except:
            print("Error with casting size or iteration to integer types, please enter a valid input.")
            sys.exit()
        dico["solvable"] = infos[1][1].replace('\n', '')
        dico["unsolvable"] = infos[2][1].replace('\n', '')
    except:
        print("Error in one of the parameters, please enter a valid input.")
        sys.exit()
    return dico

def cast_list_to_numpy_array(grid, size):
    """Cast de list en array numpy"""
    npgrid = np.zeros((size, size), dtype='int16')
    test = str(grid).split()
    if (len(test) != size**2):
        print("It seems like the infos.txt is wrong about the size")
        exit(1)
    l = 0
    n = 0
    new = []
    for i in test:
        tmp = re.sub('[^0-9]', '', i)
        if tmp.isdigit():
            new.append(int(tmp))
    if len(new) < size * size:
        print("Missing elements in grid..")
        return None
    elif len(new) > size * size:
        print("Too many elements in grid.")
        return None
    elif check_duplicate_numbers_in_grid(new) is True:
        print("Duplicates found inside the grid.")
        return None
    return new

def load_grid(dico, options):
    """Chargement de la grille depuis le fichier .txt"""
    grid = []
    error = False
    if options.file:
        file_name = options.file
        error = True
    else:
        file_name = 'data/puzzle-{}-1.txt'.format(str(dico["size"]))
    try:
        fd = open(file_name, 'r+')
    except:
        if error is False:
            print("Infos file does not match the grid.")
        elif error is True:
            print("Look like we can't find '{}'".format(file_name))
        exit(1)
    i = 0
    for row in fd:
        if i == 0:
            i += 1
        else:
            grid.append(row.replace('\n', ''))
    return grid

def check_duplicate_numbers_in_grid(grid):
    elems = []
    for elem in grid:
        if elem not in elems:
            elems.append(elem)
        else:
            return True
    return False

def get_0_pos(grid):
    """Recuperation de la position de la case 0 dans
    la grille"""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                return i, j
    return -1, -1

def print_taquin(grid, dico, mode):
	if mode == "final":
		print("\nFinal grid: ", end='')
	for i in range(len(grid)):
		if (i % dico['size'] == 0):
			print()
		print(grid[i], end=' ')
	print()

def	print_states(path, dico):
	for grid in path:
		print_taquin(grid, dico, 'current')
