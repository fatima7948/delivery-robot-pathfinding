# Delivery Robot - AI Path Planning Simulation

A Python simulation of an intelligent delivery robot navigating a city grid using classic AI search algorithms. Built with Tkinter for real-time visual animation.

## What It Does

The robot operates on a randomly generated 15x15 urban grid and must deliver packages to 5 locations. It uses search algorithms to find the best path while avoiding buildings and deciding whether to take shortcuts through expensive traffic zones.


## Features

- **15x15 grid environment** with roads, buildings, traffic zones, and delivery points
- **4 search algorithms** to compare side by side
- **Animated robot movement** — watch the robot move step by step in real time
- **Live stats panel** showing cost, nodes explored, and time per delivery
- **Randomized environment** — click "New Environment" to generate a fresh city layout
- **Traffic zones** with higher traversal cost to simulate real-world conditions



## Algorithms Implemented

| Algorithm         | Type       | Optimal?     | Notes  
|-----------        |------      |----------    |-------
| BFS               | Uninformed | No (by cost) | Finds shortest path by hops 
| DFS               | Uninformed | No           | Fast but may find long paths 
| UCS               | Uninformed | Yes ,        | Finds lowest cost path 
| Greedy Best-First | Informed   | No           | Uses Manhattan distance heuristic, fast but not always optimal 

---

## Grid Legend

| Symbol            | Meaning 
|--------           |---------
| HOME              | Base station (robot starts here) 
| PKG               | Package delivery destination 
| B                 | Building (obstacle, cannot pass) 
| Orange cell       | Traffic zone (cost 10–20) 
| Light cell        | Normal road (cost 1–5) 
| Blue cell         | Planned path 
| Yellow circle (R) | Robot 

---


Built as an AI path planning project to demonstrate and compare classic search algorithms in a visual, interactive environment.
