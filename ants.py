import numpy as np

distances = []
dlina = 0
while True:
    s = input()
    r = [int(x) for x in s.split()]                 # вводим матрицу расстояний 
    dlina += 1
    if dlina == len(r)+1:
        break;
    for m in range(len(r)):
        if r[m]==0:
            r[m]=np.inf                             
    distances.append(r)
    if len(r)==dlina:
        break;
distances = np.array(distances)

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        
        """
        Args:
            distances: матрица расстояний
            n_ants (int): количество муравьев, работающих за итерацию
            n_best (int): количество лучших муравьев, внесших феромон
            n_iteration (int): количество итераций
            decay (float): испарение феромона
            alpha (int или float): exponenet на феромоне
            beta (int или float): показатель степени на расстоянии
            
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
# поиск кратчайшего пути
    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone * self.decay            
        return all_time_shortest_path
# распределение феромонов
    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]
# пройденное расстояние
    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist
#все пути и их расстояния
    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths
# построение пути
    def gen_path(self, start):
        path = []
        visited = []
        visited.append(start)
        prev = start
        for i in range(len(self.distances) - 1):
                move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
                path.append((prev, move))
                prev = move
                visited.append(move)
        path.append((prev, start))     
        return path
#выбираем куда идти
    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[visited] = 0
      
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move
    

ant_colony = AntColony(distances, 40, 1, 100, 0.50, alpha=1, beta=2)
shortest_path = ant_colony.run()
print (int(shortest_path[-1]))