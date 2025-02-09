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
            orientation = random.choice(['up', 'down', 'left', 'right'])
            if can_place_plane(grid, x, y, orientation):
                place_plane(grid, x, y, orientation)
                planes.append((x, y, orientation))
                break
    return grid, planes

# 定义飞机的形状（相对坐标）
PLANE_SHAPES = {
    'up': [
        (0, 0),  # 机头
        (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),  # 机翼
        (-2, 0),  # 机身
        (-3, -1), (-3, 0), (-3, 1)  # 机尾
    ],
    'down': [
        (0, 0),  # 机头
        (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),  # 机翼
        (2, 0),  # 机身
        (3, -1), (3, 0), (3, 1)  # 机尾
    ],
    'left': [
        (0, 0),  # 机头
        (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),  # 机翼
        (0, -2),  # 机身
        (-1, -3), (0, -3), (1, -3)  # 机尾
    ],
    'right': [
        (0, 0),  # 机头
        (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),  # 机翼
        (0, 2),  # 机身
        (-1, 3), (0, 3), (1, 3)  # 机尾
    ]
}

# 检查是否可以放置飞机
def can_place_plane(grid, x, y, orientation):
    # 获取飞机的形状
    shape = PLANE_SHAPES.get(orientation)
    if not shape:
        raise ValueError("Invalid orientation. Must be 'up', 'down', 'left', or 'right'.")

    # 检查所有格子是否在棋盘范围内且未被占用
    for dx, dy in shape:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= 10 or ny < 0 or ny >= 10:  # 超出边界
            return False
        if grid[nx][ny] != 0:  # 格子已被占用
            return False
    return True

# 放置飞机
def place_plane(grid, x, y, orientation):
    # 获取飞机的形状
    shape = PLANE_SHAPES.get(orientation)
    if not shape:
        raise ValueError("Invalid orientation. Must be 'up', 'down', 'left', or 'right'.")

    # 遍历飞机的所有部分，更新网格
    for i, (dx, dy) in enumerate(shape):
        nx, ny = x + dx, y + dy
        if i == 0:  # 机头
            grid[nx][ny] = 2
        else:  # 机身
            grid[nx][ny] = 1
    return grid

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
def check_win(grid, planes, hits):
    # hits 是一个集合，存储玩家点击过的机头坐标
    # planes 是一个列表，存储三架飞机的机头坐标
    plane_heads = {(x, y) for (x, y, _) in planes}  # 提取所有机头坐标
    return hits.issuperset(plane_heads)  # 检查是否命中所有机头

'''# 主游戏循环
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    grid, planes = initialize_game()
    hits = set()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_input(event, grid)
                if check_win(grid, planes,hits):
                    print("You win!")
                    running = False
        draw_grid(screen, grid)
        pygame.display.flip()
    pygame.quit()'''

def test_initialize_game():
    grid, planes = initialize_game()
    print("Grid after placing planes:")
    print(grid)
    print("\nPlanes' positions and orientations:")
    for i, (x, y, orientation) in enumerate(planes):
        print(f"Plane {i + 1}: Head at ({x}, {y}), Orientation: {orientation}")

# 运行测试


if __name__ == "__main__":
    test_initialize_game()