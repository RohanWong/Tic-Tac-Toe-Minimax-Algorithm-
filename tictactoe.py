import pygame, sys
#获取特定格的中心坐标
def get_center(i):
	center_x = (ranges[i][0][0] + ranges[i][0][1])/2
	center_y = (ranges[i][1][0] + ranges[i][1][1])/2
	center = [int(center_x), int(center_y)]
	return center

#画一步棋
def draw(turn, i):
	center = get_center(i)
	if turn == 'X':
		pygame.draw.line(screen, [0, 0, 255], 
					[center[0] - 50, center[1] - 50], [center[0] + 50, center[1] + 50], 5)
		pygame.draw.line(screen, [0, 0, 255], 
					[center[0] - 50, center[1] + 50], [center[0] + 50, center[1] - 50], 5)
	elif turn == 'O':
		pygame.draw.circle(screen, [255, 0, 0], center, 50, 5)
	pygame.display.flip()

#检查是否有一条龙
def check_finish(tmp_cells):
	#竖着
	for i in [0,1,2]:
		if tmp_cells[i] == tmp_cells[i+3] == tmp_cells[i+6]!=0:
			return [True,[i,i+3,i+6]]
	#横着
	for i in [0,3,6]:
		if tmp_cells[i] == tmp_cells[i+1] == tmp_cells[i+2]!=0:
			return [True,[i,i+1,i+2]]
	#斜着
	if tmp_cells[0] == tmp_cells[4] == tmp_cells[8]!=0:
		return [True,[0,4,8]]
	if tmp_cells[2] == tmp_cells[4] == tmp_cells[6]!=0:
		return [True,[2,4,6]]
	return [False,[0,0,0]]

#连线
def connect(i_s, turn):
	if turn == 'X':
		color = [0,0,255]
	else:
		color = [255,0,0]
	point_list = [get_center(i_s[0]),get_center(i_s[1]),get_center(i_s[2])]
	pygame.draw.lines(screen, color, False, point_list, 5)
	pygame.display.flip()

#画井字
def draw_jing():
	pygame.draw.line(screen, [0, 0, 255], [0,103], [310,103], 5)
	pygame.draw.line(screen, [0, 0, 255], [0,208], [310,208], 5)
	pygame.draw.line(screen, [0, 0, 255], [103,0], [103,310], 5)
	pygame.draw.line(screen, [0, 0, 255], [208,0], [208,310], 5)
	pygame.display.flip()

#玩家对战
def play_with_friend():
	screen.fill([255, 255, 255])
	draw_jing()
	for t in range(9):
		cells[t] = 0 
	turn = 'X'
	while True:
		if turn == 'E':
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				for i in range(9):
					xy_range = ranges[i]
					x_range = xy_range[0]
					y_range = xy_range[1]
					if x_range[0] < pos[0] < x_range[1] and y_range[0] < pos[1] < y_range[1]:
						if cells[i] == 0:
							cells[i] = 1 if turn == 'X' else -1
							draw(turn,i)
							if check_finish(cells)[0]:
								connect(check_finish(cells)[1], turn)
								turn = 'E'
							else:
								if turn != 'E':
									turn = 'X' if turn == 'O' else 'O'
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				sys.exit()
		
#人工智能先手后手
def ai_first_or_second():
	menu2 = pygame.image.load('menu2.png').convert()
	screen.blit(menu2, (0,0))
	pygame.display.flip()
	one_game = True
	while True:
		if one_game == False:
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if 0 < pos[0] < 155:
					play_with_ai(True)
					one_game = False
					break
				elif 155 < pos[0] < 310:
					play_with_ai(False)
					one_game = False
					break

#一人一步
def play_with_ai(person_first):
	screen.fill([255, 255, 255])
	draw_jing()
	for t in range(9):
		cells[t] = 0
	if person_first == False:
		draw('O',4)
		cells[4] = 1
		start = 1
	else:
		start = 0
	turn = 'X'
	for top_i in range(start, 9, 2):
		if turn == 'E':
			break
		turn = 'X'
		this_turn = True
		while True:
			if turn != 'X' or this_turn == False:
				break
			for event in pygame.event.get():
				if turn != 'X' or this_turn == False:
					break
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = event.pos
					for i in range(9):
						xy_range = ranges[i]
						x_range = xy_range[0]
						y_range = xy_range[1]
						if x_range[0] < pos[0] < x_range[1] and y_range[0] < pos[1] < y_range[1]:
							if cells[i] == 0:
								draw('X',i)
								this_turn = False
								cells[i] = -1
								if check_finish(cells)[0]:
									connect(check_finish(cells)[1], turn)
									turn = 'E'
								else:
									if turn != 'E':
										turn = 'O'		

		if top_i+1 < 9 and turn != 'E':
			index = ai_find(top_i+1)
			# print(index)
			draw('O',index)
			cells[index] = 1
			if check_finish(cells)[0]:
				connect(check_finish(cells)[1], turn)
				break


def ai_find(steps):
	tmp_cells = cells[:]
	#极大极小，下一步是ai（自己)，所以极大
	max_min = 1
	sons = []
	for i in range(0,9):
		if tmp_cells[i] == 0:
			sons.append(max_min_algo(tmp_cells,i,1,steps))
	value = -999
	for son in sons:
		if son[0] > value:
			value = son[0]
			index = son[1]
	return index

def max_min_algo(pre_cells, index, max_min,steps):
	now_cells = pre_cells[:]
	if max_min == 1:
		now_cells[index] = 1
	else:
		now_cells[index] = -1
	steps = steps + 1

	if check_finish(now_cells)[0]:
		# print('finish')
		if max_min == 1:
			return [1,index]
		else:
			return [-1,index]
	elif steps == 9:
		return [0,index]
	else:
		sons = []
		for i in range(0,9):
			if now_cells[i] == 0:
				sons.append(max_min_algo(now_cells,i,-1*max_min,steps))
		if max_min == 1:
			value = 999
			for son in sons:
				if son[0] < value:
					value = son[0]
		else:
			value = -999
			for son in sons:
				if son[0] > value:
					value = son[0]
		return [value,index]



pygame.init()
pygame.display.set_caption("井字棋游戏")
#九宫格范围
ranges = [[[0, 100], [0, 100]], [[105, 205], [0, 100]], [[210, 310], [0, 100]],
		[[0, 100], [105, 205]], [[105, 205], [105, 205]], [[210, 310], [105, 205]],
		[[0, 100], [210, 310]], [[105, 205], [210, 310]], [[210, 310], [210, 310]]]
cells = [0,0,0,
		0,0,0,
		0,0,0,]
size = width, height = [310,310]
screen = pygame.display.set_mode(size)
# screen.fill([255, 255, 255])

def main():
	menu = pygame.image.load('menu.png').convert()
	screen.blit(menu, (0,0))
	pygame.display.flip()
	one_game = True
	while True:
		if one_game == False:
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if 0 < pos[0] < 155 and 155 < pos[1] < 310:
					play_with_friend()
					one_game = False
					break
				if 155 < pos[0] < 310 and 155 < pos[1] < 310:
					ai_first_or_second()
					one_game = False
					break
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
				sys.exit()

main()


	




		