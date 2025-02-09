import numpy as np
import random
import pygame

# 初始化游戏
def initialize_game():
    grid = np.zeros((10, 10), dtype=int)
    planes = []
    for _ in range(3):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            orientation = random.choice(['horizontal', 'vertical'])
            if can_place_plane(grid, x, y, orientation):
                place_plane(grid, x, y, orientation)
                planes.append((x, y, orientation))
                break
    return grid, planes

# 检查是否可以放置飞机
def can_place_plane(grid, x, y, orientation):
    # 根据飞机形状和方向检查是否超出边界或与其他飞机重叠
    pass

# 放置飞机
def place_plane(grid, x, y, orientation):
    # 根据飞机形状和方向更新网格
    pass

# 绘制游戏界面
def draw_grid(screen, grid) -> None:
    # 使用Pygame绘制网格
    cell_size = 40

    # fill color
    for i in range(10):
        for j in range(10):
            if grid[i][j] < 3: # no click grid
                color = (255, 255, 255) # white
            elif grid[i][j] == 3: # part of body
                color = (0, 0, 255) # blue
            elif grid[i][j] == 4: # click but empty
                color = (128, 128, 128) # grey
            else:
                color = (0, 255, 0) # find the head green

            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    # Draw grid lines
    for i in range(11):  # 11 lines to cover 10 cells
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_size), (400, i * cell_size))  # Horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, 400))  # Vertical lines


# 处理用户输入
def handle_input(event, grid) -> None:
    # 根据鼠标点击更新网格状态
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        cell_size = 40
        i, j = y // cell_size, x // cell_size
        # case for clicking showed grid
        if grid[i][j] > 2:
            return # terminate the function
        if grid[i][j] == 1: # in case being part of the plane
            grid[i][j] = 3 # hit the body
        elif grid[i][j] == 2: # in case being plane head
            grid[i][j] = 5 # hit the head
        else:
            grid[i][j] = 4 # hit nothing

# 判断游戏状态
def check_win(grid, planes):
    # 检查是否所有飞机头部都被找到
    pass

# 主游戏循环
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    # grid, planes = initialize_game()
    grid = np.zeros((10,10), dtype=int)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_input(event, grid)
                '''if check_win(grid, planes):
                    print("You win!")
                    running = False'''
        draw_grid(screen, grid)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()