import numpy as np

class Canvas:
    def __init__(self, n):
        self.size = n
        self.plan = np.zeros((n,n), dtype=int)

    def print_canvas(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                print(f'{self.plan[i,j]} ', end="")
            print()

    # put the plane
    def put_plane(self) -> None:
        print("haha")

    def is_put_legal(self, plan_pos) -> bool:
        return False

    def is_put_overlap(self, plan_pos) -> bool:
        return False

    def start_game(self) -> None:
        self.print_canvas()

    def choose_pos(self, chosen_pos) -> None:
        self.print_canvas()

# test in main
c = Canvas(10)
c.print_canvas()

