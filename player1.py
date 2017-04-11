class Player1:
	
	def __init__(self):
		self.ply1 = 'o'
		self.ply2 = 'x'
		self.heuristicMatrix = [[0,-1,-10,-100,-1000],[1,0,0,0,0],[10,0,0,0,0],[100,0,0,0,0],[1000,0,0,0,0]]
		self.winCombinations = [[[0,0],[0,1],[0,2],[0,3]],[[1,0],[1,1],[1,2],[1,3]],[[2,0],[2,1],[2,2],[2,3]],[[3,0],
		[3,1],[3,2],[3,3]],[[0,0],[1,0],[2,0],[3,0]],[[0,1],[1,1],[2,1],[3,1]],[[0,2],[1,2],[2,2],[3,2]],[[0,3],[1,3],
		[2,3],[3,3]],[[0,0],[1,1],[2,2],[3,3]],[[0,3],[1,2],[2,1],[3,0]]]
		self.blocks = []
		self.boardscore = 0
		self.temp = []

	def update(self, board, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguements
		board.board_status[new_move[0]][new_move[1]] = ply 
		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0 
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (board.board_status[4*x+i][4*y] == board.board_status[4*x+i][4*y+1] == board.board_status[4*x+i][4*y+2] ==\
			 board.board_status[4*x+i][4*y+3]) and (board.board_status[4*x+i][4*y] == ply):
				board.block_status[x][y] = ply 
				return 1
			#checking for vertical pattern(i'th column)
			if (board.board_status[4*x][4*y+i] == board.board_status[4*x+1][4*y+i] == board.board_status[4*x+2][4*y+i] ==\
			 board.board_status[4*x+3][4*y+i]) and (board.board_status[4*x][4*y+i] == ply):
				board.block_status[x][y] = ply 
				return 1

		#checking for diagnol pattern
		if (board.board_status[4*x][4*y] == board.board_status[4*x+1][4*y+1] == board.board_status[4*x+2][4*y+2] == \
			board.board_status[4*x+3][4*y+3]) and (board.board_status[4*x][4*y] == ply):
			board.block_status[x][y] = ply 
			return 1
		if (board.board_status[4*x+3][4*y] == board.board_status[4*x+2][4*y+1] == board.board_status[4*x+1][4*y+2] ==\
		 board.board_status[4*x][4*y+3]) and (board.board_status[4*x+3][4*y] == ply):
			board.block_status[x][y] = ply 
			return 1

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if board.board_status[4*x+i][4*y+j] =='-':
					return 0
		board.block_status[x][y] = 'd'
		return 0

	def evaluateboard(self, board):
		score = 0
		for line in self.winCombinations:
			play ,other = 0,0
			for cell in line:
				if board.block_status[cell[0]][cell[1]] == self.ply1:
					play += 1
				elif board.block_status[cell[0]][cell[1]] == self.ply2:
					other += 1
			score += 1000*self.heuristicMatrix[play][other]
		
		return score
	
	def evaluatelinescore(self, board, move):
		score = 0
		x = move[0]/4*4
		play, other = 0, 0
		for i in range(x, x+4):
			if board.board_status[i][move[1]] == self.ply1:
				play += 1
			elif board.board_status[i][move[1]] == self.ply2:
				other += 1
		score += self.heuristicMatrix[play][other]

		x = move[1]/4*4
		play, other = 0, 0
		for i in range(x, x+4):
			if board.board_status[move[0]][i] == self.ply1:
				play += 1
			elif board.board_status[move[0]][i] == self.ply2:
				other += 1
		score += self.heuristicMatrix[play][other]

		if move[0] == move[1]:
			x = move[0]/4*4
			y = move[1]/4*4
			play, other = 0, 0
			for i in range(4):
				if board.board_status[x+i][y+i] == self.ply1:
					play += 1
				elif board.board_status[x+i][y+i] == self.ply2:
					other += 1
			score += self.heuristicMatrix[play][other]
		elif (move[0]+move[1])%4 == 3:
			x = move[0]/4*4
			y = move[1]/4*4+3
			play, other = 0, 0
			for i in range(4):
				if board.board_status[x+i][y-i] == self.ply1:
					play += 1
				elif board.board_status[x+i][y-i] == self.ply2:
					other += 1
			score += self.heuristicMatrix[play][other]
		return score
			

	def alphabeta(self, node, depth, board, alpha, beta, maximizingPlayer):

		if depth == 0: 
			return self.boardscore+sum(self.blocks)
		
		elif maximizingPlayer:
			v = float("-inf")
			cells = board.find_valid_move_cells(node)
			stack = []
			for cell in cells:
				x = [cell[0], cell[1], self.linescorechange(board, cell, self.ply1)]
				stack.append(x)
 
			sorted(stack, key=lambda x: x[2])

			for x in stack:
				flag = self.update(board, x, self.ply1)
				if flag != 0:
					self.temp.append(self.boardscore)
					self.boardscore = self.evaluateboard(board)
				self.blocks.append(x[2])
				v = max(v, self.alphabeta(x, depth-1, board, alpha, beta, False))
				self.blocks.pop()
				if flag != 0:
					self.boardscore = self.temp.pop()
				board.board_status[x[0]][x[1]] = '-'
				board.block_status[x[0]/4][x[1]/4] = '-'
				alpha = max(alpha, v)
				if beta <= alpha :
					break
			return v

		else:
			v = float("inf")
			cells = board.find_valid_move_cells(node)
			stack = []

			for cell in cells:
				x = [cell[0], cell[1], self.linescorechange(board, cell, self.ply2)]
				stack.append(x)

			sorted(stack, key=lambda x: x[2], reverse = True)

			for x in stack:
				flag = self.update(board, x, self.ply2)
				if flag != 0:
					self.temp.append(self.boardscore)
					self.boardscore = self.evaluateboard(board)
				self.blocks.append(x[2])
				v = min(v, self.alphabeta(x, depth-1, board, alpha, beta, True))
				self.blocks.pop()
				if flag != 0:
					self.boardscore = self.temp.pop()
				board.board_status[x[0]][x[1]] = '-'
				board.block_status[x[0]/4][x[1]/4] = '-'
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v
	
	def linescorechange(self, board, cell, ply):
		board.board_status[cell[0]][cell[1]] = ply
		x = self.evaluatelinescore(board, cell)
		board.board_status[cell[0]][cell[1]] = '-'
		x -= self.evaluatelinescore(board, cell)
		return x

	def move(self, board, old_move, flag):
		if old_move == (-1,-1):
			self.ply1 = 'x'
			self.ply2 = 'o'
		self.boardscore = self.evaluateboard(board)
		cells = board.find_valid_move_cells(old_move)
		bestValue = float("-inf")
		stack = []
		for cell in cells:
			x = [cell[0], cell[1], self.linescorechange(board, cell, self.ply1)]
			stack.append(x)
		sorted(stack, key=lambda x: x[2])

		for x in stack:
			flag = self.update(board, x, self.ply1) #Draw move
			if flag != 0:
				self.temp.append(self.boardscore)
				self.boardscore = self.evaluateboard(board)
			self.blocks.append(x[2])
			Value =	self.alphabeta(x, 2, board, float("-inf"), float("inf"), False)
			self.blocks.pop()
			if flag != 0:
				self.boardscore = self.temp.pop()
			board.board_status[x[0]][x[1]] = '-'	#delete move
			board.block_status[x[0]/4][x[1]/4] = '-' 
			
			if Value >= bestValue :
				bestValue = Value
				bestMove = (x[0], x[1])

		return bestMove
