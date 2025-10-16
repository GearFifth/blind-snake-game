import math

def rectangular_spiral_generator(p, q, growth_fn):
    moves = [
        ("RIGHT", p), ("DOWN", q),
        ("LEFT", p), ("UP", q)
    ]
    leg_length = 1
    move_index = 0
    while True:
        move1_dir, move1_factor = moves[move_index]
        for _ in range(leg_length * move1_factor):
            yield move1_dir

        move2_dir, move2_factor = moves[move_index + 1]
        for _ in range(leg_length * move2_factor):
            yield move2_dir

        leg_length = growth_fn(leg_length)
        move_index = (move_index + 2) % 4

def send_signal(command):
    print(f"Sending command: {command}")
    return False

def solve():
    # 3 types of growth functions
    arithmetic_growth = lambda length: length + 1
    jittery_growth = lambda length: math.floor(length * 1.5) + 1
    geometric_growth = lambda length: length * 2

    spiral_params = [
        # Slow, dense spirals for square-like grids
        {'p': 1, 'q': 1, 'fn': arithmetic_growth},
        {'p': 2, 'q': 1, 'fn': arithmetic_growth},
        {'p': 1, 'q': 2, 'fn': arithmetic_growth},
        # Medium-growth spirals for balance
        {'p': 4, 'q': 1, 'fn': jittery_growth},
        {'p': 1, 'q': 4, 'fn': jittery_growth},
        # Fast, sparse spirals for extreme aspect ratios
        {'p': 8, 'q': 1, 'fn': geometric_growth},
        {'p': 1, 'q': 8, 'fn': geometric_growth}
    ]

    # Array of 7 generators - one for each spiral
    spirals = [rectangular_spiral_generator(p['p'], p['q'], p['fn']) for p in spiral_params]
    num_spirals = len(spirals)
    current_spiral_index = 0

    # Main loop: interleave moves from each spiral generator
    while True:
        # Get the next move from the current spiral in the cycle.
        move = next(spirals[current_spiral_index])

        has_won = send_signal(move)

        if has_won:
            print("Apple found! Game won.")
            break

        # Move to the next spiral for the next turn.
        current_spiral_index = (current_spiral_index + 1) % num_spirals


