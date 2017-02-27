#######################################################################
##
##   SETUP
##
#######################################################################

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [c+d for c in A for d in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [ cross(r, cols) for r in rows ]

column_units = [ cross(rows, c) for c in cols ]

square_units = [ cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789') ]

diagonal_units = [["".join(z) for z in zip(rows, cols)] , ["".join(z) for z in zip(reversed(rows), cols)]]

unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s,[u for u in unitlist if s in u]) for s in boxes)

peers = dict( (s, set(sum(units[s],[])) - set([s]))  for s in boxes )

assignments = []

#######################################################################
##
##   CONSTRAINTS
##
#######################################################################

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        naked_twins_dict = find_naked_twins(unit, values)
        for naked_twin_value in naked_twins_dict:
            naked_twin_list = naked_twins_dict[naked_twin_value] 
            for b in unit:
                if b not in naked_twin_list:
                    for v in naked_twin_value:
                        assign_value(values, b, values[b].replace(v, ''))
    return values

def eliminate(values):
    solved_values = [(k, values[k]) for k in values if len(values[k]) == 1]
    for k,v in solved_values:
        for p in peers[k]:
            if v in values[p]:
                assign_value(values, p, values[p].replace(v, ''))
    return values

def only_choice(values):
    listofvalues = '123456789'
    for unit in unitlist:
        for value in listofvalues:
            boxes_with_value = [box for box in unit if value in values[box]]
            if len(boxes_with_value) == 1:
                assign_value(values, boxes_with_value[0], value)

#######################################################################
##
##   SOLVER
##
#######################################################################

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        eliminate(values)
        only_choice(values)
        naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    node = values
    solve_puzzle(node)
    if puzzle_solved(node):
        return node
    else:
        child_nodes = get_child_nodes(node)
        for child_node in child_nodes:
            result = search(child_node)
            if result is not False:
                return result
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

#######################################################################
##
##   HELPER METHODS
##
#######################################################################

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    gv = {}
    for i in range(0, len(grid)):
        r = i // 9
        c = i % 9
        if grid[i] == '.':
            gv[row_units[r][c]] = '123456789'
        else:
            gv[row_units[r][c]] = grid[i]
    return gv

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def solve_puzzle(node):
    values = node
    result = reduce_puzzle(values)
    return result

def puzzle_solved(values):
    if values is False:
        return False
    non_one_values = [(key, values[key]) for key in values if len(values[key]) != 1]
    return len(non_one_values) == 0

def get_possibilities(node):
    values = node
    non_one_values = [(key, values[key]) for key in values if len(values[key]) != 1]
    non_one_values = sorted(non_one_values, key=lambda kv: len(kv[1]))
    kv = non_one_values[0]
    return kv
    
def get_child_nodes(node):
    # find a node with fewest possibilities
    # generate N child nodes for each of the N possibilities
    possible_key, possible_values = get_possibilities(node)
    n = len(possible_values)
    child_nodes = [None] * n
    for i in range(n):
        possible_node = node.copy()
        possible_node[possible_key] = possible_values[i]
        child_nodes[i] = possible_node
    return child_nodes

def find_naked_twins(unit, values):
    result = {}
    suspects = [b for b in unit if len(values[b]) == 2]
    for s in suspects:
        value = values[s]
        if value in result:
            result[value].append(s)
        else:
            result[value] = [ s ]
    result = dict((k, result[k]) for k in result if len(result[k]) == 2)
    return result

#######################################################################
##
##   main
##
#######################################################################
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except Exception as e:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        print(e)