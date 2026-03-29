# encoding: utf-8
import tkinter as tk
import random
import time
import heapq
import math
from collections import deque
 
GRID_SIZE = 15
CELL_SIZE = 45
 
ROAD     = 0
BUILDING = 1
TRAFFIC  = 2
DELIVERY = 3
BASE     = 4
 
COLORS = {
    ROAD:     "#f0f0f0",
    BUILDING: "#4a4a4a",
    TRAFFIC:  "#f4a261",
    DELIVERY: "#2a9d8f",
    BASE:     "#e76f51",
}
 
def make_grid():
    grid = [[ROAD] * GRID_SIZE for _ in range(GRID_SIZE)]
    building_cells = random.sample(
        [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)],
        k=int(GRID_SIZE * GRID_SIZE * 0.20)
    )
    for r, c in building_cells:
        grid[r][c] = BUILDING
    road_cells = [(r, c) for r in range(GRID_SIZE)
                  for c in range(GRID_SIZE) if grid[r][c] == ROAD]
    traffic_cells = random.sample(road_cells, k=int(len(road_cells) * 0.15))
    for r, c in traffic_cells:
        grid[r][c] = TRAFFIC
    return grid
 
def make_costs(grid):
    costs = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == BUILDING:
                costs[r][c] = float('inf')
            elif grid[r][c] == TRAFFIC:
                costs[r][c] = random.randint(10, 20)
            else:
                costs[r][c] = random.randint(1, 5)
    return costs
 
def get_neighbors(r, c, grid):
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            if grid[nr][nc] != BUILDING:
                result.append((nr, nc))
    return result
 
def bfs(grid, costs, start, goal):
    queue = deque([[start]])
    visited = {start}
    nodes_explored = 0
    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_explored += 1
        if node == goal:
            total = sum(costs[r][c] for r, c in path[1:])
            return path, total, nodes_explored
        for nb in get_neighbors(node[0], node[1], grid):
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None, 0, nodes_explored
 
def dfs(grid, costs, start, goal):
    stack = [[start]]
    visited = {start}
    nodes_explored = 0
    while stack:
        path = stack.pop()
        node = path[-1]
        nodes_explored += 1
        if node == goal:
            total = sum(costs[r][c] for r, c in path[1:])
            return path, total, nodes_explored
        for nb in get_neighbors(node[0], node[1], grid):
            if nb not in visited:
                visited.add(nb)
                stack.append(path + [nb])
    return None, 0, nodes_explored
 
def ucs(grid, costs, start, goal):
    heap = [(0, start, [start])]
    visited = {}
    nodes_explored = 0
    while heap:
        cost, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited[node] = cost
        nodes_explored += 1
        if node == goal:
            return path, cost, nodes_explored
        for nb in get_neighbors(node[0], node[1], grid):
            if nb not in visited:
                new_cost = cost + costs[nb[0]][nb[1]]
                heapq.heappush(heap, (new_cost, nb, path + [nb]))
    return None, 0, nodes_explored
 
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
 
def greedy(grid, costs, start, goal):
    heap = [(manhattan(start, goal), start, [start])]
    visited = {start}
    nodes_explored = 0
    while heap:
        _, node, path = heapq.heappop(heap)
        nodes_explored += 1
        if node == goal:
            total = sum(costs[r][c] for r, c in path[1:])
            return path, total, nodes_explored
        for nb in get_neighbors(node[0], node[1], grid):
            if nb not in visited:
                visited.add(nb)
                heapq.heappush(heap, (manhattan(nb, goal), nb, path + [nb]))
    return None, 0, nodes_explored
 
ALGORITHMS = {
    "BFS":    bfs,
    "DFS":    dfs,
    "UCS":    ucs,
    "Greedy": greedy,
}
 
class DeliveryRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Robot - Path Planning Simulation")
        self.root.resizable(False, False)
        self.algo_var = tk.StringVar(value="UCS")
        self.status_var = tk.StringVar(value="Press Start to begin simulation.")
        self._build_ui()
        self._new_environment()
 
    def _build_ui(self):
        self.canvas = tk.Canvas(
            self.root,
            width=GRID_SIZE * CELL_SIZE,
            height=GRID_SIZE * CELL_SIZE,
            bg="white", bd=2, relief="sunken"
        )
        self.canvas.grid(row=0, column=0, rowspan=20, padx=10, pady=10)
 
        panel = tk.Frame(self.root, padx=10, pady=10)
        panel.grid(row=0, column=1, sticky="n")
 
        tk.Label(panel, text="Delivery Robot", font=("Arial", 14, "bold")).pack(pady=(0,10))
        tk.Label(panel, text="Algorithm:", font=("Arial", 10, "bold")).pack(anchor="w")
        for algo in ALGORITHMS:
            tk.Radiobutton(panel, text=algo, variable=self.algo_var,
                           value=algo, font=("Arial", 10)).pack(anchor="w")
 
        tk.Label(panel, text="").pack()
        tk.Button(panel, text=">> Start Simulation", font=("Arial", 10, "bold"),
                  bg="#2a9d8f", fg="white", width=18,
                  command=self.run_simulation).pack(pady=4)
        tk.Button(panel, text="New Environment", font=("Arial", 10),
                  width=18, command=self._new_environment).pack(pady=4)
 
        tk.Label(panel, text="\nLegend", font=("Arial", 10, "bold")).pack()
        legend = [
            ("#e76f51", "Base (HOME)"),
            ("#2a9d8f", "Delivery (PKG)"),
            ("#f4a261", "Traffic Zone"),
            ("#4a4a4a", "Building (B)"),
            ("#f0f0f0", "Road"),
            ("#3a86ff", "Path"),
            ("yellow",  "Robot (R)"),
        ]
        for color, label in legend:
            row = tk.Frame(panel)
            row.pack(anchor="w")
            tk.Label(row, bg=color, width=3, relief="solid").pack(side="left", padx=4, pady=1)
            tk.Label(row, text=label, font=("Arial", 9)).pack(side="left")
 
        tk.Label(panel, text="\nStats", font=("Arial", 10, "bold")).pack()
        self.stats_text = tk.Text(panel, width=22, height=14, font=("Courier", 8),
                                  state="disabled", bg="#f8f8f8")
        self.stats_text.pack()
 
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 9),
                 bd=1, relief="sunken", anchor="w").grid(
            row=20, column=0, columnspan=2, sticky="we", padx=10, pady=(0,5))
 
    def _new_environment(self):
        self.grid = make_grid()
        self.costs = make_costs(self.grid)
        open_cells = [(r, c) for r in range(GRID_SIZE)
                      for c in range(GRID_SIZE)
                      if self.grid[r][c] in (ROAD, TRAFFIC)]
        random.shuffle(open_cells)
        self.base = open_cells[0]
        self.grid[self.base[0]][self.base[1]] = BASE
        self.deliveries = open_cells[1:6]
        for r, c in self.deliveries:
            self.grid[r][c] = DELIVERY
        self.robot_pos = self.base
        self._clear_stats()
        self.status_var.set("New environment ready. Press Start to simulate.")
        self._draw_grid()
 
    def _draw_grid(self, path=None, robot=None):
        self.canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
                cell = self.grid[r][c]
                color = COLORS[cell]
                if path and (r, c) in path and cell not in (BASE, DELIVERY):
                    color = "#3a86ff"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ccc")
                if cell in (ROAD, TRAFFIC):
                    self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2,
                        text=str(self.costs[r][c]), font=("Arial", 7), fill="#888")
                elif cell == BUILDING:
                    self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2,
                        text="B", font=("Arial", 11, "bold"), fill="white")
                elif cell == BASE:
                    self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2,
                        text="HOME", font=("Arial", 7, "bold"), fill="white")
                elif cell == DELIVERY:
                    self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2,
                        text="PKG", font=("Arial", 7, "bold"), fill="white")
 
        pos = robot if robot else self.robot_pos
        rx = pos[1]*CELL_SIZE + CELL_SIZE//2
        ry = pos[0]*CELL_SIZE + CELL_SIZE//2
        self.canvas.create_oval(rx-14, ry-14, rx+14, ry+14,
                                fill="yellow", outline="orange", width=2)
        self.canvas.create_text(rx, ry, text="R", font=("Arial", 11, "bold"))
 
    def _animate_path(self, path):
        for pos in path:
            self._draw_grid(path=set(path), robot=pos)
            self.root.update()
            time.sleep(0.12)
        self.robot_pos = path[-1]
 
    def _clear_stats(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", "end")
        self.stats_text.config(state="disabled")
 
    def _add_stats(self, text):
        self.stats_text.config(state="normal")
        self.stats_text.insert("end", text)
        self.stats_text.config(state="disabled")
        self.stats_text.see("end")
 
    def run_simulation(self):
        algo_name = self.algo_var.get()
        algo_fn   = ALGORITHMS[algo_name]
        self._clear_stats()
        self._add_stats(f"Algorithm: {algo_name}\n")
        self._add_stats("-" * 22 + "\n")
        current_pos = self.base
        total_cost  = 0
        total_nodes = 0
        total_time  = 0.0
        for i, dest in enumerate(self.deliveries):
            self.status_var.set(f"Delivery {i+1}/5 -> {dest}  [{algo_name}]")
            self.root.update()
            t0 = time.perf_counter()
            path, cost, nodes = algo_fn(self.grid, self.costs, current_pos, dest)
            elapsed = time.perf_counter() - t0
            if path is None:
                self._add_stats(f"D{i+1}: NO PATH FOUND\n")
                continue
            total_cost  += cost
            total_nodes += nodes
            total_time  += elapsed
            self._add_stats(
                f"D{i+1}: {current_pos}->{dest}\n"
                f"  Cost : {cost}\n"
                f"  Nodes: {nodes}\n"
                f"  Time : {elapsed*1000:.2f} ms\n\n"
            )
            self._animate_path(path)
            current_pos = dest
        self._add_stats("-" * 22 + "\n")
        self._add_stats(
            f"TOTAL\n"
            f"  Cost : {total_cost}\n"
            f"  Nodes: {total_nodes}\n"
            f"  Time : {total_time*1000:.2f} ms\n"
        )
        self.status_var.set(f"All deliveries done! Total cost: {total_cost} | Nodes: {total_nodes}")
 
if __name__ == "__main__":
    root = tk.Tk()
    app  = DeliveryRobotApp(root)
    root.mainloop()