import sys
import matplotlib.pyplot as plt

WHITE_U = -0.04
WALL_U = 0
DISCOUNT_RATE = 0.99

def get_bellman(board, u_board, i, j):
    #Utility of the four directions
    actions = [u_board[i][j] for x in range(4)]
    
    if i > 0:
        if board[i - 1][j] != WALL_U:
            actions[0] = u_board[i - 1][j]
    if j > 0:
        if board[i][j - 1] != WALL_U:
            actions[1] = u_board[i][j - 1]
    if i < len(board) - 1:
        if board[i + 1][j] != WALL_U:
            actions[2] = u_board[i + 1][j]
    if j < len(board[0]) - 1:
        if board[i][j + 1] != WALL_U:
            actions[3] = u_board[i][j + 1]

    utilities = []
    for i in range(4):
        utilities.append(0.8 * actions[i] + 0.1 * actions[(i + 1) % 4] + 0.1 * actions[(i + 3) % 4])
    return board[i][j] + DISCOUNT_RATE * max(utilities)

def get_initial_utility(board):
    u_board = [[0.0 for x in range(len(board[0]))] for x in range(len(board))]
    white_spaces = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != WHITE_U:
                u_board[i][j] = board[i][j]
            else:
                white_spaces += 1
    return u_board, white_spaces

def cal_MDP(board, terminal):
    u_board, white_spaces = get_initial_utility(board)
    converged = 0
    utility_estimates = [[0 for x in range(50)] for x in range(36)]
    #Treat rewards as terminal states
    for iteration in range(50):
        for i in range(len(board)):
            for j in range(len(board[0])):
                #print(u_board[i][j])
                if terminal:
                    if board[i][j] != WHITE_U:
                        continue
                if board[i][j] != WALL_U:
                    bellman_u = get_bellman(board, u_board, i, j)
                    #print("bellman " + str(bellman_u))
                    #print(u_board[i][j] - bellman_u)
                    '''
                    if round(u_board[i][j], 2) == round(bellman_u, 2):
                        converged += 1
                    else:
                    '''
                    u_board[i][j] = bellman_u

                utility_estimates[i * 6 + j][iteration] = bellman_u
        #print_matrix(u_board)
        #print(u_board)
    return u_board, utility_estimates

def build_board():
    return [[WHITE_U, -1, WHITE_U, WHITE_U, WHITE_U, WHITE_U],
            [WHITE_U, WHITE_U, WHITE_U, WALL_U, -1, WHITE_U],
            [WHITE_U, WHITE_U, WHITE_U, WALL_U, WHITE_U, 3],
            [WHITE_U, WHITE_U, WHITE_U, WALL_U, WHITE_U, WHITE_U],
            [WHITE_U, WHITE_U, WHITE_U, WHITE_U, WHITE_U, WHITE_U],
            [1, -1, WHITE_U, WALL_U, -1, -1]]

def print_matrix(matrix):
    for row in matrix:
        row_str = ""
        for cell in row:
            row_str += " & " + str(cell)
        row_str += "\\\\"
        print(row_str)

if __name__ == "__main__":
    #Part 1.1
                                                    
    board = build_board()
    u_matrix, utility_estimates = cal_MDP(board, True)
    u_matrix, utility_estimates = cal_MDP(board, False)
    print_matrix(u_matrix)
    for cell in utility_estimates:
        plt.plot(cell)
    plt.show()
        
    #Part 1.2
    blackbox_utility = build_board()
    
