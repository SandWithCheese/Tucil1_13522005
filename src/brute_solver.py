import time


def find_paths(grid, buffer_size):
    rows, cols = len(grid), len(grid[0])
    paths = []

    for c in range(cols):
        stack = [((0, c), [(0, c)])]
        while stack:
            (r, c), path = stack.pop()
            if len(path) < buffer_size:
                last_r, last_c = path[-1]

                if len(path) % 2 == 0:
                    for new_c in range(cols):
                        if new_c != last_c and (last_r, new_c) not in path:
                            stack.append(((last_r, new_c), path + [(last_r, new_c)]))
                else:
                    for new_r in range(rows):
                        if new_r != last_r and (new_r, last_c) not in path:
                            stack.append(((new_r, last_c), path + [(new_r, last_c)]))

            elif len(path) == buffer_size:
                paths.append(path)
                # Batesin biar array of pathsnya ga terlalu besar,
                # artinya kemungkinannya sangat banyak sampe bikin laptop mokad
                if len(paths) >= 10_000_000:
                    return None

    return paths


def find_possible_paths(m, paths, sequences, weights):
    max_path = []
    max_weight = 0
    for path in paths:
        seq = ""
        for r, c in path:
            seq += m[r][c]

        weight = 0
        for s in sequences:
            if "".join(s) in seq:
                weight += weights[sequences.index(s)]

        if weight > max_weight:
            max_weight = weight
            max_path = [path]
        elif weight == max_weight:
            max_path.append(path)

    return max_path, max_weight


def find_shortest_path(m, max_path, sequences, buffer_size):
    short_path = []
    for i, path in enumerate(max_path):
        seq = ""
        for r, c in path:
            seq += m[r][c]

        found = False
        while not found:
            for s in sequences:
                for token in s:
                    if seq[-2:] == token:
                        found = True
                        break
                if found:
                    break
            else:
                seq = seq[:-2]
                max_path[i] = max_path[i][:-1]

        short_path.append(seq)

    shortest_path = min(short_path, key=len)
    shortest_coordinate = max_path[short_path.index(shortest_path)]
    shortest_path = " ".join(
        shortest_path[i : i + 2] for i in range(0, len(shortest_path), 2)
    )

    return shortest_path, shortest_coordinate


def brute_solve(data):
    start = time.time()

    paths = find_paths(data["m"], data["buffer_size"])
    if paths is None:
        return None

    max_path, max_weight = find_possible_paths(
        data["m"], paths, data["sequences"], data["weights"]
    )
    shortest_path, shortest_coordinate = find_shortest_path(
        data["m"], max_path, data["sequences"], data["buffer_size"]
    )

    end = time.time()

    return {
        "shortest_path": shortest_path,
        "shortest_coordinate": shortest_coordinate,
        "max_weight": max_weight,
        "time": end - start,
    }
