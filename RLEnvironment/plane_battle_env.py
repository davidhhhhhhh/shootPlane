import gymnasium as gym
import numpy as np
import random
import pygame
from gymnasium import spaces

# Define plane shapes for different orientations
PLANE_SHAPES = {
    'up': [
        (0, 0),  # Head
        (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),  # Wings
        (-2, 0),  # Body
        (-3, -1), (-3, 0), (-3, 1)  # Tail
    ],
    'down': [
        (0, 0),  # Head
        (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),  # Wings
        (2, 0),  # Body
        (3, -1), (3, 0), (3, 1)  # Tail
    ],
    'left': [
        (0, 0),  # Head
        (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),  # Wings
        (0, -2),  # Body
        (-1, -3), (0, -3), (1, -3)  # Tail
    ],
    'right': [
        (0, 0),  # Head
        (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),  # Wings
        (0, 2),  # Body
        (-1, 3), (0, 3), (1, 3)  # Tail
    ]
}


class PlaneBattleEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, num_planes=3):
        super(PlaneBattleEnv, self).__init__()

        self.grid_size = 10
        self.num_planes = num_planes
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.initialize_game()

        # Action space: Click any cell (10x10 = 100 possible actions)
        self.action_space = spaces.Discrete(self.grid_size * self.grid_size)

        # Observation space: 10x10 grid with values {0,1,2,3,4,5}
        self.observation_space = spaces.Box(low=0, high=5, shape=(self.grid_size, self.grid_size), dtype=np.int8)

    def initialize_game(self):
        """Randomly place planes on the grid."""
        self.grid.fill(0)
        self.planes = []
        for _ in range(self.num_planes):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 9)
                orientation = random.choice(['up', 'down', 'left', 'right'])
                if self.can_place_plane(x, y, orientation):
                    self.place_plane(x, y, orientation)
                    break

    def can_place_plane(self, x, y, orientation):
        """Check if a plane can be placed."""
        shape = PLANE_SHAPES.get(orientation, [])
        for dx, dy in shape:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < 10 and 0 <= ny < 10) or self.grid[nx, ny] != 0:
                return False
        return True

    def place_plane(self, x, y, orientation):
        """Place a plane on the grid."""
        shape = PLANE_SHAPES.get(orientation, [])
        for i, (dx, dy) in enumerate(shape):
            nx, ny = x + dx, y + dy
            self.grid[nx, ny] = 2 if i == 0 else 1  # 2 = Head, 1 = Body

    def step(self, action):
        """Apply an action and return new state, reward, and done flag."""
        x, y = divmod(action, self.grid_size)  # Convert 1D action to 2D coordinates
        reward = -1  # Default penalty for a miss

        # Check if the selected cell was already clicked
        if self.grid[x, y] in {3, 4, 5}:  # Already clicked body (3), empty (4), or head (5)
            reward = -5  # Additional penalty for choosing an already selected cell
            return self.grid.copy(), reward, False, False, {}

        # Check the current state of the cell
        if self.grid[x, y] == 1:  # Hit body
            self.grid[x, y] = 3
            reward = 5
        elif self.grid[x, y] == 2:  # Hit head
            self.grid[x, y] = 5
            reward = 10
        elif self.grid[x, y] == 0:  # Miss
            self.grid[x, y] = 4  # Mark as clicked empty cell
            reward = -1  # Small penalty for missing

        # Check if the game is won
        done = self.check_win()
        if done:
            reward += 100  # Winning reward

        return self.grid.copy(), reward, done, False, {}

    def check_win(self):
        """Check if all plane heads are hit."""
        return np.count_nonzero(self.grid == 2) == 0

    def reset(self, seed=None, options=None):
        """Reset the game for a new episode."""
        self.initialize_game()
        return self.grid.copy(), {}

    def render(self, mode='human', last_action=None):
        """Render only the updated cell instead of redrawing the entire grid."""
        cell_size = 40
        if not hasattr(self, 'screen'):
            pygame.init()
            self.screen = pygame.display.set_mode((400, 400))
            self.screen.fill((255, 255, 255))
            pygame.display.flip()

        # If this is the first render, draw the entire grid
        if last_action is None:
            self.screen.fill((255, 255, 255))  # Clear the screen

            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self._draw_cell(i, j, cell_size)

            # Draw grid lines
            for i in range(11):  # 11 lines to cover 10 cells
                pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (400, i * cell_size))  # Horizontal lines
                pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, 400))  # Vertical lines
        else:
            # Convert action index to grid coordinates
            x, y = divmod(last_action, self.grid_size)
            self._draw_cell(x, y, cell_size)  # Update only the selected cell

        pygame.display.flip()  # Refresh only affected parts

    def _draw_cell(self, i, j, cell_size):
        """Helper function to draw an individual cell based on its value."""
        value = self.grid[i][j]

        if value == 0:  # Unclicked empty cell
            color = (255, 255, 255)  # White
        elif value == 1:  # Unclicked plane body
            color = (255, 255, 255)  # Keep it white (hidden)
        elif value == 2:  # Unclicked plane head
            color = (255, 255, 255)  # Keep it white (hidden)
        elif value == 3:  # Hit plane body
            color = (0, 0, 255)  # Blue
        elif value == 4:  # Clicked empty cell
            color = (128, 128, 128)  # Grey
        elif value == 5:  # Hit plane head
            color = (0, 255, 0)  # Green

        pygame.draw.rect(self.screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
        pygame.draw.rect(self.screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)  # Draw border

    def close(self):
        pygame.quit()