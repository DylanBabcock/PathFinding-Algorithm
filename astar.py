import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))#setting up display
pygame.display.set_caption("A* Path Finding Algorithm")#A* search algorithm caption



#Color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:#each cube on the grid
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width#Help determine cube coordinates by multiplying the current row by the width of all the cubs 
		self.y = col * width
		self.color = WHITE#to start have all white cubes
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows


	## Methods to tell us the state of each cube. 
	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN


	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED


	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):#win is the window
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))#.rect draws a rectangle


	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):#compare two spots
		return False


def h(p1, p2):#point one and point two
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)#return distance between two points



def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()



def algorithm(draw, grid, start, end):

	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))#put is like push or append . adding to priority queue
	came_from = {}

	g_score = {spot: float("inf") for row in grid for spot in row}#keep track of g and f scores. spot distance
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}#keeps track of things in the priority queue

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#Another quit event
				pygame.quit()

		current = open_set.get()[2]#current node 
		open_set_hash.remove(current)



		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True


		for neighbor in current.neighbors:#neighbors of current node
			temp_g_score = g_score[current] + 1#find shortest path and add one

			if temp_g_score < g_score[neighbor]:#if you find a shorter path then update it 
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):#draw a line for each row
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)#draw colors

	draw_grid(win, rows, width)
	pygame.display.update()#update what we have drawn on the screen


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col#find where is clicked by finding position x and y of your mouse and and dividing it by the cubes 


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():#loop through events and check what they are
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # Left mouse
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)#which spot in our 2d list did we click on 
				spot = grid[row][col]
				if not start and spot != end:#getting the start and end position cubes
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:#make barrier 
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # Right mouse
				
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:#reset cubes
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:#start if pressed space bar
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)#lambda is an anon. function

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)