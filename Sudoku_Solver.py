from random import randint, shuffle

empty_board = [
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0]
]

numberList=[1,2,3,4,5,6,7,8,9]

def fill_board(board):
	find = find_empty(board)

	if not find:
		return True
	else:
		row,col = find

	shuffle(numberList)

	for i in numberList:
		if check_valid(board,i,(row,col)):
			board[row][col] = i

			if fill_board(board):
				return True

			board[row][col] = 0

	return False

def generate_sudoku(board,level):
	counter = 20
	fill_board(board)

	print_board(board)

	while level > 0 :
		row = randint(0,len(board)-1)
		col = randint(0,len(board)-1)

		while board[row][col] == 0:
			row = randint(0,len(board)-1)
			col = randint(0,len(board)-1)

		backup = board[row][col]
		board[row][col] = 0

		copy_board = []

		for i in range(0,len(board)):
			copy_board.append([])
			for j in range(0,len(board)):
				copy_board[i].append(board[i][j])

		if not solve_sudoku(copy_board) & counter > 0 :
			board[row][col] = backup
			counter -= 1
		else :
			level -=1
			print("Level: ",level)



def print_board(board):
	print("")
	print("- - - - - - - - - - - -")
	print("")

	for i in range(len(board)):
		if i % 3 == 0 and i != 0 :
			print("- - - - - - - - - - - -")

		for j in range(len(board)):
			if j % 3 == 0 and j != 0:
				print(" | ", end="")
			
			print(board[i][j], end="")
					
			if j != 8: 
				print(" ", end = "")

			else:
				print("")
	print("")
	print("- - - - - - - - - - - -")	
	print("")



def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				return (i,j)

	return None

def check_valid(board, num, pos):
	#Check column
	for i in range(len(board)):
		if board[i][pos[1]] == num and pos[0] != i:
			return False

	#Check row
	for i in range(len(board[0])):
		if board[pos[0]][i] == num and pos[1] != i:
			return False

	#Check 3x3 box:
	box_x = pos[1]//3
	box_y = pos[0]//3

	for i in range(box_y * 3, box_y * 3 + 3):
		for j in range(box_x * 3, box_x * 3 + 3):
			if board[i][j] == num and (i,j) != pos:
				return False

	return True

def solve_sudoku(board):
	find = find_empty(board)

	if not find:
		return True
	else:
		row, col = find

	for i in range(1,10):
		if check_valid(board, i, (row, col)):
			board[row][col] = i

			if solve_sudoku(board):
				return True

			board[row][col] = 0

	return False

print_board(empty_board)
generate_sudoku(empty_board,20)
print_board(empty_board)
solve_sudoku(empty_board)
print_board(empty_board)
