"""Project Overview:
Stack: Single-file Python 3 console app built on the standard library (`time`, `os`, `datetime`) with plain-text data files (Login.txt, Wins.txt, Loss.txt, Draw.txt, Elo.txt, GameHistory.txt) providing persistence.
Flow: The program launches an ASCII-art animation, lands on a main menu (`choices()`), and branches into gameplay, tutorials, account management, or leaderboard views based on user input.
Gameplay: `setboard()` seeds an 8x8 board stored as coordinate-keyed dict entries, `getmoves()`/`checktest()` compute legal chess moves (incl. castling, en passant, promotion), and `news()` applies moves, enforces check/mate logic, logs history, and rotates turns.
Accounts & Stats: `login()`/`signup()` manage credentials while Elo, win/loss/draw tallies, game logs, and replays are read/written via the text files; `account_view()`, `database()`, and `halloffame()` surface this information for players.
Overall: OFF Chess delivers an offline two-player chess experience with educational material and simple persistence, all orchestrated through command-line prompts and global state.
"""

import time
import os
from datetime import date
# Importing relevant packages
def setboard():
    # Initialise the chessboard dictionary with string coordinates -> piece codes
    global board
    board = {
        "12":"wP",
        "22":"wP",
        "32":"wP",
        "42":"wP" ,
        "52":"wP",
        "62":"wP",
        "72":"wP",
        "82":"wP",
        "11":"wR",
        "81":"wR",
        "21":"wN",
        "71":"wN",
        "31":"wB",
        "61":"wB",
        "41":"wQ",
        "51":"wK",

        "17":"bP",
        "27":"bP",
        "37":"bP",
        "47":"bP",
        "57":"bP",
        "67":"bP",
        "77":"bP",
        "87":"bP",
        "18":"bR",
        "88":"bR",
        "28":"bN",
        "78":"bN",
        "38":"bB",
        "68":"bB",
        "48":"bQ",
        "58":"bK",
    }

#Here we are initialising the board, each square is a key value pair of two numbers from 1-8. Squares with pieces are defined in this dictionary, as thier colour and then piece. Any time a piece moves, its old square is deleted, and a new definition is added for the square its moved to. Undefined squares are considered unoccupied

filecondict = {
    # Maps numeric file indices to algebraic file letters for display/logging
    1:"a",
    2:"b",
    3:"c",
    4:"d",
    5:"e",
    6:"f",
    7:"g",
    8:"h"
}

fileinputdict = {
    # Converts algebraic file letters back to numeric indices for internal lookups
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8
}

#These are used in a variety of features to translte between the letters on the board and the numbers used when computing moves

ascii = {
    # Unicode glyphs used when rendering the board in the terminal
    "bR": "♜",
    "bN": "♞",
    "bB": "♝",
    "bP": "♟",
    "bQ": "♛",
    "bK": "♚",
    "wR": "♖",
    "wN": "♘",
    "wB": "♗",
    "wP": "♙",
    "wQ": "♕",
    "wK": "♔",
}

#This ascii is used to change the pieces into vieweable icons for display

def print_chessboard(board):
    # Render the current board state using rank/file axes and unicode pieces
    for rank in range(8, 0, -1):
        print(rank, end=" | ")
        for file in range(1, 9):
            square1 = board.get(f'{file}{rank}', '.') 
            square2 = ascii.get(f'{square1}', '.')      
            print(square2, end=" ")
        print()
    print("   ----------------")
    print("    a b c d e f g h")

#This function prints every square in the board, and prints pieces on it when it finds a piece, otherwise leaves a dot to denote a blank piece.

def getmoves(checks,dontAddKing):
    # Build the legal move list for the currently selected piece, optionally reusing state during check evaluation
    global possible_moves
    global enpassant_moves
    global check_moves
    global newfile
    global newranks
    global ogx
    global castlewk
    global wkingmoved
    global castlebk
    global bkingmoved
    global castlewq
    global castlebq
    global K_moves
    global secondValueList
    global bkrookmoved
    global bqrookmoved
    global wkrookmoved
    global wqrookmoved

    castlebk = False
    castlewk = False
    castlewq = False
    castlebq = False


    if checks == False:
        # Fresh move generation: reset tracking lists and remember original square
        check_moves = []
        K_moves = []
        secondValueList = []
        ogx = x
    #Rows
    possible_moves = []  
    enpassant_moves = []
    if food == 'R':
        # Rook: scan vertically and horizontally until blocked by own piece or capture
        newranks = 0
        newfile = 0

        for i in range(7):
            i += 1
            # Step up the file increasing rank until collision
            newranks = int(rank) + i
            if f'{file}{newranks}' in board:
                collisioncol = board[f'{file}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:

                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))
                    break
            elif newranks < 9:

                possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Step down the file decreasing rank until collision
            newranks = int(rank) - i
            if f'{file}{newranks}' in board:
                collisioncol = board[f'{file}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:

                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

                    break
            elif newranks > 0:

                possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # March right along the rank until we hit a piece or board edge
            newfile = int(file) + i
            if f'{newfile}{rank}' in board:
                collisioncol = board[f'{newfile}{rank}']
                if x[0] == collisioncol[0]:
                    break
                else:

                    possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

                    break

            elif newfile < 9:

                possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))


        for i in range(7):
            i += 1
            # March left along the rank until we hit a piece or board edge
            newfile = int(file) - i
            if f'{newfile}{rank}' in board:
                collisioncol = board[f'{newfile}{rank}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    

                    possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

                    break
            elif newfile > 0:

                possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

    if food == 'B':
        # Bishop: explore diagonal rays in all four directions
        newfile = 0
        newranks = 0

        for i in range(7):
            i += 1
            # Northeast diagonal sweep
            newfile = int(file) + i
            newranks = int(rank) + i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
                    break
            elif newfile < 9 and newranks < 9:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Southeast diagonal sweep
            newfile = int(file) + i
            newranks = int(rank) - i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile < 9 and newranks > 0:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Northwest diagonal sweep
            newfile = int(file) - i
            newranks = int(rank) + i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile > 0 and newranks < 9:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Southwest diagonal sweep
            newfile = int(file) - i
            newranks = int(rank) - i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile > 0 and newranks > 0:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


    if food == "Q":
        # Queen: combine rook and bishop directional scans
        newfile = 0
        newranks = 0
        for i in range(7):
            i += 1
            # Reuse rook logic: push forward ranks
            newranks = int(rank) + i
            if f'{file}{newranks}' in board:
                collisioncol = board[f'{file}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

                    break
            elif newranks < 9:
                possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Reuse rook logic: pull backward ranks
            newranks = int(rank) - i
            if f'{file}{newranks}' in board:
                collisioncol = board[f'{file}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

                    break
            elif newranks > 0:
                possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Horizontal scan moving right
            newfile = int(file) + i
            if f'{newfile}{rank}' in board:
                collisioncol = board[f'{newfile}{rank}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

                    break
            elif newfile < 9:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

        for i in range(7):
            i += 1
            # Horizontal scan moving left
            newfile = int(file) - i
            if f'{newfile}{rank}' in board:
                collisioncol = board[f'{newfile}{rank}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))

                    break
            elif newfile > 0:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))


        for i in range(7):
            i += 1
            # Diagonal sweep northeast
            newfile = int(file) + i
            newranks = int(rank) + i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile < 9 and newranks < 9:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Diagonal sweep southeast
            newfile = int(file) + i
            newranks = int(rank) - i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
                    break
            elif newfile < 9 and newranks > 0:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Diagonal sweep northwest
            newfile = int(file) - i
            newranks = int(rank) + i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile > 0 and newranks < 9:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


        for i in range(7):
            i += 1
            # Diagonal sweep southwest
            newfile = int(file) - i
            newranks = int(rank) - i
            if f'{newfile}{newranks}' in board:
                collisioncol = board[f'{newfile}{newranks}']
                if x[0] == collisioncol[0]:
                    break
                else:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

                    break
            elif newfile > 0 and newranks > 0:
                possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


    if food == "P":
        # Pawn: handle forward pushes, captures, initial double steps, and en passant for both colors

        if x[0] == 'w':
            newranks = 0
            newfile = 0

            if rank == "2":
                # Starting rank: allow single or double push if clear
                for i in range(2):
                    i += 1
                    newranks = int(rank) + i
                    if f'{file}{newranks}' in board:
                        break
                    if newranks < 9:
                        possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                        check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

            else:
                newranks = int(rank) + 1
                if newranks < 9 and f'{file}{newranks}' not in board:
                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))
            
            newranks = int(rank)
            newfile = int(file)
            newranks += 1
            newfile += 1
            # Diagonal capture to the right if an enemy piece exists
            if f'{newfile}{newranks}' in board:
                pawntake = board[f'{newfile}{newranks}']
                if pawntake[0] != x[0]:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
            
            newranks = int(rank)
            newfile = int(file)
            newranks += 1
            newfile -= 1
            # Diagonal capture to the left if an enemy piece exists
            if f'{newfile}{newranks}' in board:
                pawntake = board[f'{newfile}{newranks}']
                if pawntake[0] != x[0]:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

            if rank == '5':
                newranks = int(rank)
                newfile = int(file)
                newfile -= 1
                # En passant capture to the left for white pawns
                if f'{newfile}{newranks}' in board:
                    pawntake = board[f'{newfile}{newranks}']
                    if (pawntake[0] != x[0]) and pawntake[-1] == 'P':
                        newranks += 1
                        enpassant_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')

            if rank == '5':
                newranks = int(rank)
                newfile = int(file)
                newfile += 1
                # En passant capture to the right for white pawns
                if f'{newfile}{newranks}' in board:
                    pawntake = board[f'{newfile}{newranks}']
                    if (pawntake[0] != x[0]) and pawntake[-1] == 'P':
                        newranks += 1
                        enpassant_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')




        elif x[0] == 'b':

            newranks = 0
            newfile = 0
            if str(rank) == "7":
                # Black starting rank: allow single or double push if clear
                for i in range(2):
                    i += 1
                    newranks = int(rank) - i
                    if f'{file}{newranks}' in board:
                        break
                    if newranks > 0:
                        possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                        check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

            else:
                newranks = int(rank) - 1
                if newranks > 0 and f'{file}{newranks}' not in board:
                    possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))

            newranks = int(rank)
            newfile = int(file)
            newranks -= 1
            newfile += 1
            # Diagonal capture to the right for black (toward smaller ranks)
            if f'{newfile}{newranks}' in board:
                pawntake = board[f'{newfile}{newranks}']
                if pawntake[0] != x[0]:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

            newranks = int(rank)
            newfile = int(file)
            newranks -= 1
            newfile -= 1
            # Diagonal capture to the left for black
            if f'{newfile}{newranks}' in board:
                pawntake = board[f'{newfile}{newranks}']
                if pawntake[0] != x[0]:
                    possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
                    check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

            if rank == '4':
                newranks = int(rank)
                newfile = int(file)
                newfile -= 1
                # En passant capture to the left for black pawns
                if f'{newfile}{newranks}' in board:
                    pawntake = board[f'{newfile}{newranks}']
                    if (pawntake[0] != x[0]) and pawntake[-1] == 'P':
                        newranks -= 1
                        enpassant_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')

            if rank == '4':
                newranks = int(rank)
                newfile = int(file)
                newfile += 1
                # En passant capture to the right for black pawns
                if f'{newfile}{newranks}' in board:
                    pawntake = board[f'{newfile}{newranks}']
                    if (pawntake[0] != x[0]) and pawntake[-1] == 'P':
                        newranks -= 1
                        enpassant_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
 
    if food == "N":
        # Knight: test all eight L-shaped jumps, ignoring blocking pieces
        newfile = 0
        newranks = 0
        newfile = int(file) + 2
        newranks = int(rank) - 1   
        if newfile < 9 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
        newfile = 0
        newranks = 0
        newfile = int(file) + 2
        newranks = int(rank) + 1   
        if newfile < 9 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) - 2
        newranks = int(rank) + 1   
        if newfile > 0 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) - 2
        newranks = int(rank) - 1   
        if newfile > 0 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) + 1
        newranks = int(rank) + 2   
        if newfile < 9 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) - 1
        newranks = int(rank) + 2   
        if newfile > 0 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) + 1
        newranks = int(rank) - 2   
        if newfile < 9 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))

        newfile = 0
        newranks = 0
        newfile = int(file) - 1
        newranks = int(rank) - 2   
        if newfile > 0 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))


    if food == "K":

        if x[0] == 'w':
            # White king: determine castling availability before testing standard moves
            newfile = 0
            newranks = 0
            if f'{file}{rank}' == '51' and wkingmoved == False:
                newfile = int(file) + 1
                if f'{newfile}{rank}' not in board:
                    newfile = int(newfile) + 1
                    if f'{newfile}{rank}' not in board:
                        castlewk = True

                newfile = int(file) - 1
                if f'{newfile}{rank}' not in board:
                    newfile = int(newfile) - 1
                    if f'{newfile}{rank}' not in board:
                        castlewq = True

        if x[0] == 'b':
            newfile = 0
            newranks = 0
            # Black king: mirror the castling eligibility checks
            if f'{file}{rank}' == '58' and bkingmoved == False:
                newfile = int(file) + 1
                if f'{newfile}{rank}' not in board:
                    newfile = int(newfile) + 1
                    if f'{newfile}{rank}' not in board:
                        castlebk = True
                    

                newfile = int(file) - 1
                if f'{newfile}{rank}' not in board:
                    newfile = int(newfile) - 1
                    if f'{newfile}{rank}' not in board:
                        castlebq = True

        newfile = 0
        newranks = 0
        newranks = int(rank) + 1
        # King can step one square up if not blocked by own piece
        if newranks < 9 and board.get(f'{file}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
            

        newfile = 0
        newranks = 0
        newranks = int(rank) - 1
        # King can step one square down if target not friendly
        if newranks > 0 and board.get(f'{file}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(file)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(file)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(file)]}{str(newranks)}')


        newfile = 0
        newranks = 0
        newfile = int(file) + 1
        # Check the square to the right of the king
        if newfile < 9 and board.get(f'{newfile}{rank}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')



        newfile = 0
        newranks = 0
        newfile = int(file) - 1
        # Check the square to the left of the king
        if newfile > 0 and board.get(f'{newfile}{rank}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(rank)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(rank)}')



        newfile = 0
        newranks = 0
        newfile = int(file) + 1
        newranks = int(rank) + 1
        # Up-right diagonal
        if newfile < 9 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')



        newfile = 0
        newranks = 0
        newfile = int(file) + 1
        newranks = int(rank) - 1
        # Down-right diagonal
        if newfile < 9 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')



        newfile = 0
        newranks = 0
        newfile = int(file) - 1
        newranks = int(rank) + 1
        # Up-left diagonal
        if newfile > 0 and newranks < 9 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')


 
        newfile = 0
        newranks = 0
        newfile = int(file) - 1
        newranks = int(rank) - 1
        # Down-left diagonal
        if newfile > 0 and newranks > 0 and board.get(f'{newfile}{newranks}',"1")[0] != x[0]:
            possible_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')
            if dontAddKing == False:
                check_moves.append((f'{filecondict[int(file)]}{str(rank)}',f'{filecondict[int(newfile)]}{str(newranks)}'))
            K_moves.append(f'{filecondict[int(newfile)]}{str(newranks)}')



    if checks == False:
        if possible_moves == []:
            # No legal moves available for the selected piece; force player to choose again
            print("Sorry, this piece cannot move anywhere, please choose another one")
            Pieceinput()

def GetElo(Ra,Rb,wresult,bresult):
    # Apply the Elo rating formula to both players and persist the new results
    global changedscore
    global word
    global oldstuff
    Ra = float(Ra)
    Rb = float(Rb)

    if wresult == 'w':
        Sa = float(1)
    elif wresult == 'l':
        Sa = float(0)
    elif wresult == 'd':
        Sa = float(0.5)

    Qa = 10**(Ra/400)
    Qb = 10**(Rb/400)
    Ea = Qa/(Qa + Qb)
    # Standard Elo expectation + update with 32 as the K-factor
    NewRa = Ra + 32*(Sa - Ea)
    oldstuff = str(int(Ra))
    changedscore = str(int(NewRa))
    print(f"{p1name}'s rating is now {changedscore}")
    word = p1name
    write("Elo.txt")

    if bresult == 'w':
        Sa = float(1)
    elif bresult == 'l':
        Sa = float(0)
    elif bresult == 'd':
        Sa = float(0.5)

    Qa = 10**(Ra/400)
    Qb = 10**(Rb/400)
    Eb = Qb/(Qa + Qb)
    NewRb = Rb + 32*(Sa - Eb)
    oldstuff = str(int(Rb))
    changedscore = str(int(NewRb))
    print(f"{p2name}'s rating is now {changedscore}")
    word = p2name
    write("Elo.txt")

def Addwins(dox): #This is generic and recieves designated import
    # Increment the appropriate stat counter (wins/losses/draws) for the active `word`
    global oldstuff
    global changedscore
    with open(dox, "r") as fp: #Open predetermined txt file
        lines = fp.readlines()
        for line in lines:
            if line.find(word) != -1: #Finds the specified username in the document
                res = (line.split(",", 1))
                oldstuff = res[1] #Find the preexisting value in that document as set it to a universal variable
                if dox == 'Wins.txt' or dox == 'Loss.txt' or dox == 'Draw.txt':
                    changedscore = f'{str(int(oldstuff)+1)}\n'
                    write(dox)

def write(dox): #A generic write function
    # Replace the old stat value with the new value inside the given document
    global changedscore
    global oldstuff
    with open(dox, 'r') as file: #Open the specified document
        file_contents = file.read() #Read it all
    combold = f'{word},{oldstuff}' #The previous combination is the players name and their old value
    combonew = f'{word},{changedscore}' #The thing it is replaced with is their name with the new value
    updated_contents = file_contents.replace(combold,combonew) #Replace the old value with the new

    with open(dox, 'w') as file:
        file.write(updated_contents)

def checktest(chm):
    #At the end of your turn, just before a piece move is submitted, check if the king is in check, by running through all the pieces
    # When `chm` is True we gather enemy attacks; when False we gather friendly attacks for validation
    global check_moves
    global selfking
    global K_moves
    global secondValueList
    global firstValueList
    check_moves = []
    secondValueList = []
    firstValueList = []
    K_moves = []

    for index,sqr in enumerate(board):
        # Iterate over every occupied square, treating each piece as potential attacker or king candidate
        global food
        global name
        global file
        global rank
        global x

        file = sqr[0]
        rank = sqr[-1]
        x = board[sqr]


        if x[-1] == "R":
            # Evaluate rook moves depending on whose attacks we are gathering
            food = "R"
            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)
            else:
                if chm == True:
                    getmoves(True,False)

        elif x[-1] == "B":
            # Evaluate bishop moves
            food = "B"

            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)
            else:
                if chm == True:
                    getmoves(True,False)

        elif x[-1] == "Q":
            # Evaluate queen moves
            food = "Q"
            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)
            else:
                if chm == True:
                    getmoves(True,False)

        elif x[-1] == "P":
            # Evaluate pawn moves, including en passant threats
            food = 'P'
            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)          
            else:
                if chm == True:
                    getmoves(True,False)

        elif x[-1] == "N":
            # Evaluate knight moves
            food = 'N'
            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)
            else:
                if chm == True:
                    getmoves(True,False)
                    
        elif x[-1] == "K":
            # Track the friendly king's square and gather opposing king moves
            food = "K"
            if ((whom == True and x[0] == 'w') or (whom == False and x[0] == 'b')):
                selfking = f'{file}{rank}'
                if chm == True:
                    getmoves(True,True)
            if ((whom == True and x[0] == 'b') or (whom == False and x[0] == 'w')):
                if chm == False:
                    getmoves(True,False)

def mate():

    global ismate
    # Assume mate until we find a legal move that escapes check
    ismate = True
    checktest(True) #Get list of own colour pieces possible moves
    for a in check_moves:
        # Try every non-king move and see if any remove the king from danger
        secondValueList.append(a[-1])
        firstValueList.append(a[0])
        originalPiece = 0
        oldmove = f'{fileinputdict[a[0][0]]}{a[0][-1]}'
        move = f'{fileinputdict[a[-1][0]]}{a[-1][-1]}'
        if move in board:
            originalPiece = board[move]
        movedPiece = board[oldmove] 
        board.pop(oldmove)
        board[move] = movedPiece
        checktest(False)
        for b in check_moves:
            secondValueList.append(b[-1])

        if f'{filecondict[int(selfking[0])]}{selfking[-1]}' not in secondValueList:
            ismate = False
        if originalPiece == 0:
            board.pop(move)
        else:
            board[move] = originalPiece
        board[oldmove] = movedPiece

    checktest(True)
    for b in K_moves: #loop For all the moves in the list
        # Explicitly test each king move against future attacks
        originalPiece = 0
        move = f'{fileinputdict[b[0]]}{b[-1]}' #figure out each move in the list
        if move in board:
            originalPiece = board[move]
        if whom == True:
            board[move] = 'wK'
        elif whom == False:
            board[move] = 'bK'
        checktest(False)
        for a in check_moves:
            secondValueList.append(a[-1])
        if f'{filecondict[int(move[0])]}{move[-1]}' not in secondValueList:
            ismate = False
        if originalPiece == 0:
            board.pop(move)
        else:
            board[move] = originalPiece

def start():
    # Increment the global turn counter and announce whose move it is
    global turns
    turns += 1
    global whom
    if turns % 2 != 0: #Whites move
        # Odd-numbered turns belong to White
        whom = True
        print(f"It is now white ({p1name})'s move")
        time.sleep(1)
    else:
        # Even-numbered turns belong to Black
        whom = False
        print(f"It is now black ({p2name})'s move")
        time.sleep(1)
    Pieceinput()

def Pieceinput():  
    # Prompt the active player for a piece to move, validate that choice, and seed move generation
    global food
    global name
    global piece  
    global x
    global word
    food = 0
    piece = 0
    checktest(False)
    # Populate attack maps to identify checks and current legal responses
    for a in check_moves:
            secondValueList.append(a[-1])
    if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:
        # If the king's square is attacked, determine whether the position is checkmate
        mate()
        if ismate == True:
            print("CHECKMATE")
            time.sleep(1)
            print("Game over")

            if whom == True:
                print(f"Black, {p2name}, has won the game")

                word = p1name
                Addwins("Elo.txt")
                Ra = oldstuff
                word = p2name
                Addwins("Elo.txt")
                Rb = oldstuff
                GetElo(Ra,Rb,'l','w')
                word = p2name
                Addwins("Wins.txt")
                word = p1name
                Addwins("Loss.txt")
                with open('GameHistory.txt','a') as p:
                    p.write(f'¿{p2name} wins')

            if whom == False:
                print(f"White, {p1name}, has won the game")
                
                word = p1name
                Addwins("Elo.txt")
                Ra = oldstuff
                word = p2name
                Addwins("Elo.txt")
                Rb = oldstuff
                GetElo(Ra,Rb,'w','l')
                word = p1name
                Addwins("Wins.txt")
                word = p2name
                Addwins("Loss.txt")
                with open('GameHistory.txt','a') as p:
                    p.write(f'¿{p1name} wins')
            time.sleep(1)
            choices()

        else:
            if whom == True:
                print("White is in check")
            elif whom == False:
                print("Black is in check")
    
    if f'{filecondict[int(selfking[0])]}{selfking[-1]}' not in secondValueList:

        mate()
        # When the king is safe, we still check for stalemate (no legal moves)
        if ismate == True:
            print("STALEMATE")
            time.sleep(1)
            print("Game over")
            print("Both players have drawn")
            word = p1name
            Addwins("Elo.txt")
            Ra = oldstuff
            word = p2name
            Addwins("Elo.txt")
            Rb = oldstuff
            GetElo(Ra,Rb,'d','d')
            word = p1name
            Addwins('Draw.txt')
            word = p2name
            Addwins('Draw.txt')
            with open('GameHistory.txt','a') as p:
                p.write('¿Both players draw')
            time.sleep(1)
            choices()                

    piece = input("Name the square of the piece you wish to move; ")
    # Allow text commands for draw or resign before validating coordinates
    if piece.lower() == 'draw':
        # Interpret special command to offer a draw to the opponent
        if whom == True:
            print(f"{p1name} has offered a draw")
            time.sleep(1)
            print(f"{p2name}, will you accept (Y or N)?")
        if whom == False:
            print(f"{p2name} has offered a draw")
            time.sleep(1)
            print(f"{p1name}, will you accept (Y or N)?")
        draw = input("")
        if draw.lower() == 'y':
            print("Game over")
            print("Both players have drawn")
            word = p1name
            Addwins("Elo.txt")
            Ra = oldstuff
            word = p2name
            Addwins("Elo.txt")
            Rb = oldstuff
            GetElo(Ra,Rb,'d','d')
            word = p1name
            Addwins('Draw.txt')
            word = p2name
            Addwins('Draw.txt')
            with open('GameHistory.txt','a') as p:
                p.write('¿Both players draw')
            time.sleep(1)
            choices()
        else:
            if whom == True:
                print(f"{p2name} has declined the draw")
                time.sleep(1)
                print(f"{p1name}, please make a move")
            if whom == False:
                print(f"{p1name} has declined the draw")
                time.sleep(1)
                print(f"{p2name}, please make a move")
            Pieceinput()
    
    if piece.lower() == 'resign':
        # Resignation flow grants victory to the opponent after confirmation
        die = input("Are you sure you wish to resign (Y or N)? ")
        if die.upper() == 'N':
            Pieceinput()
        if die.upper() == 'Y':
            if whom == True:
                print(f"Black, {p2name}, has won the game")
                word = p1name
                Addwins("Elo.txt")
                Ra = oldstuff
                word = p2name
                Addwins("Elo.txt")
                Rb = oldstuff
                GetElo(Ra,Rb,'l','w')
                word = p2name
                Addwins("Wins.txt")
                word = p1name
                Addwins("Loss.txt")
                with open('GameHistory.txt','a') as p:
                    p.write(f'¿{p2name} wins')
                time.sleep(1)
                choices()

            if whom == False:
                print(f"White, {p1name}, has won the game")
                word = p1name
                Addwins("Elo.txt")
                Ra = oldstuff
                word = p2name
                Addwins("Elo.txt")
                Rb = oldstuff
                GetElo(Ra,Rb,'w','l')
                word = p1name
                Addwins("Wins.txt")
                word = p2name
                Addwins("Loss.txt")
                with open('GameHistory.txt','a') as p:
                    p.write(f'¿{p1name} wins')
                time.sleep(1)
                choices()
        else:
            print("Please enter a valid answer")
            time.sleep(1)
            Pieceinput()
            choices()
    if ((piece.lower()[0] or piece.lower()[1]) not in fileinputdict) or len(piece) != 2 or f'{fileinputdict[piece[0]]}{piece[-1]}' not in board:
        # Reject malformed input or empty squares
        print("Please enter a valid piece")
        Pieceinput()
    x = board.get(f'{fileinputdict[piece[0]]}{piece[1]}')
    if (whom == True and x[0] == 'w') or (whom == False and x[0] == 'b'):
        # Ensure the chosen piece belongs to the current player
        if x[-1] == "R":
            food = "R"
            name = "Rook"
        elif x[-1] == "B":
            food = "B"
            name = "Bishop"
        elif x[-1] == "Q":
            food = "Q"
            name = "Queen"
        elif x[-1] == "P":
            food = 'P'
            name = "Pawn"
        elif x[-1] == "N":
            food = 'N'
            name = "Knight"
        elif x[-1] == "K":
            food = "K"
            name = "King"
        else:
            print("w")

        time.sleep(1)
        print(f'You have selected a {name}')
        time.sleep(1)
        global file
        global rank
        file = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
        rank = piece[-1] #Second number is rank (4th rank, 5th rank, 6th rank etc)
        # Calculate possible moves for the selected piece
        getmoves(False,False)

    else:
        print('Wrong colour piece!')
        time.sleep(1)
        Pieceinput()       
    # Pass control to the destination selection prompt
    news()

def promotion():
    # Convert a pawn that reached the back rank into the piece chosen by the player
    global ogx
    global prom
    global prop
    promote = input("Your pawn has promoted! What piece will it become? ")
    if promote.upper() == 'Q' or promote.upper() == 'R' or promote.upper() == 'B' or promote.upper() == 'N':
        ogx = f'{ogx[0]}{promote.upper()}'
        prom = True
        if whom == True:
            prop = promote.lower()
        if whom == False:
            prop = promote.upper()
    else:
        print("Invalid syntax please enter algebraic notation of piece")
        time.sleep(1)
        promotion()

def news():
    # Handle the target square entry, enforce special move rules, and finalize the move
    global prom 
    prom = False
    new = input("What square do you wish to move this piece? ")
    time.sleep(1)
    if new.lower() == "cancel":
        # Give players a way to re-select a piece
        Pieceinput()
    elif ((new.lower()[0] or new.lower()[1]) not in fileinputdict) or len(new) != 2:
        # Guard against malformed destination coordinates
        print("Unreadable syntax, please re-enter the square you would like in Algebraic notation, or else, enter cancel")
        news()

    else:
        global wkingmoved
        global bkingmoved
        global bqrookmoved
        global bkrookmoved
        global wkrookmoved
        global wqrookmoved
        if castlewk == True and f'{fileinputdict[new[0]]}{new[-1]}' == '71' and wkrookmoved == False:
            # Execute white king-side castling after verifying path is not in check
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if 'f1' in secondValueList:
                print("Still Check")
                time.sleep(1)
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '71'
            board.pop('51')
            board[difnew] = ogx
            
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '61'
            board.pop('81')
            board[difnew] = 'wR'

            print('White castled')
            with open('GameHistory.txt', 'a') as enter_games:
                ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                ogrank = piece[-1]
                enter_games.write(f'{ogfile}{ogrank}wk')
            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            wkingmoved = True
            start()

        if castlewq == True and f'{fileinputdict[new[0]]}{new[-1]}' == '31' and wqrookmoved == False:
            # Execute white queen-side castling with safety checks
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if 'd1' in secondValueList:
                print("Check")
                time.sleep(1)
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '31'
            board.pop('51')
            board[difnew] = ogx
            
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '41'
            board.pop('11')
            board[difnew] = 'wR'

            print('White castled')
            with open('GameHistory.txt', 'a') as enter_games:
                ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                ogrank = piece[-1]
                enter_games.write(f'{ogfile}{ogrank}wq')
            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            wkingmoved = True
            start()

        if castlebk == True and f'{fileinputdict[new[0]]}{new[-1]}' == '78' and bkrookmoved == False:
            # Execute black king-side castling when legal
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if 'f8' in secondValueList:
                print("Check")
                time.sleep(1)
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '78'
            board.pop('58')
            board[difnew] = ogx
            
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '68'
            board.pop('88')
            board[difnew] = 'bR'

            print('Black castled')
            with open('GameHistory.txt', 'a') as enter_games:
                ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                ogrank = piece[-1]
                enter_games.write(f'{ogfile}{ogrank}bk')
            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            bkingmoved = True
            start()

        if castlebq == True and f'{fileinputdict[new[0]]}{new[-1]}' == '38' and bqrookmoved == False:
            # Execute black queen-side castling when legal
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if 'd8' in secondValueList:
                print("Check")
                time.sleep(1)
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '38'
            board.pop('58')
            board[difnew] = ogx
            
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            difnew = '48'
            board.pop('18')
            board[difnew] = 'bR'

            print('Black castled')
            with open('GameHistory.txt', 'a') as enter_games:
                ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                ogrank = piece[-1]
                enter_games.write(f'{ogfile}{ogrank}bq')
            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            bkingmoved = True
            start()

        if new in enpassant_moves:

            # Resolve en passant capture by removing the passed pawn and placing ours diagonally
            difnew = f'{fileinputdict[new[0]]}{new[1]}'
            board.pop(f'{fileinputdict[piece[0]]}{piece[1]}')
            if x[0] == 'w':
                board.pop(f'{fileinputdict[new[0]]}{int(new[-1])-1}')
            if x[0] == 'b':
                board.pop(f'{fileinputdict[new[0]]}{int(new[-1])+1}')
            board[difnew] = ogx

            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                if x[0] == 'w':
                    board[f'{fileinputdict[new[0]]}{int(new[-1])+1}'] = 'bP'
                if x[0] == 'b':
                    board[f'{fileinputdict[new[0]]}{int(new[-1])-1}'] = 'wP'

                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()

            print(f'The {name} has been moved to {new}')
            with open('GameHistory.txt', 'a') as enter_games:
                ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                ogrank = piece[-1]
                if whom == True:
                    enter_games.write(f'{ogfile}{ogrank}{fileinputdict[new[0]]}e')
                if whom == False:
                    enter_games.write(f'{ogfile}{ogrank}{fileinputdict[new[0]]}E')
            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            start()

        if new in possible_moves:

            # Default movement path: update board, handle promotion flags, and ensure move is legal
            if ogx == 'wP' and new[-1] == '8' or ogx == 'bP' and new[-1] == '1':
                promotion()

            difnew = f'{fileinputdict[new[0]]}{new[1]}'
            board.pop(f'{fileinputdict[piece[0]]}{piece[1]}')
            board[difnew] = ogx
            checktest(False)
            for a in check_moves:
                secondValueList.append(a[-1])
            if f'{filecondict[int(selfking[0])]}{selfking[-1]}' in secondValueList:

                print("Check")
                time.sleep(1)
                board.pop(difnew)
                board[f'{fileinputdict[piece[0]]}{piece[1]}'] = ogx
                print("Please play a legal move to not be in check")
                time.sleep(1)
                Pieceinput()
                
            if name == 'King':
                if whom == True:
                    wkingmoved = True
                else:
                    bkingmoved = True
            
            if name == 'Rook':
                if f'{file}{rank}' == '11' and x[0] == 'w':
                    wqrookmoved = True
                if f'{file}{rank}' == '81' and x[0] == 'w':
                    wkrookmoved = True
                if f'{file}{rank}' == '18' and x[0] == 'b':
                    bqrookmoved = True
                if f'{file}{rank}' == '88' and x[0] == 'b':
                    bkrookmoved = True

            print(f'The {name} has been moved to {new}')
            with open('GameHistory.txt', 'a') as enter_games:
                # Record the move in the compact history notation for later replay
                if prom == True:
                    ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                    ogrank = piece[-1]
                    enter_games.write(f'{ogfile}{ogrank}{fileinputdict[new[0]]}{prop}')
                else:
                    ogfile = fileinputdict[piece[0]] #First number is file (a file, b file, c file etc)
                    ogrank = piece[-1]
                    enter_games.write(f'{ogfile}{ogrank}{fileinputdict[new[0]]}{new[-1]}')

            time.sleep(1)
            print_chessboard(board)
            time.sleep(1)
            start()
                
        else:
            # Destination square rejected; ask for another
            print("Not a possible move dummy")
            news()

def login(): #Check the players login
    # Validate submitted username/password pair and load the player's rating
    global p1ready
    global p2ready
    global word
    global p1name
    global p2name
    username = input("Enter your username; ")  #Ask for username
    time.sleep(1)
    password = input("Enter your password; ") #Ask for password
    with open('Login.txt') as f:
        if f'{username}, {password}¿' in f.read(): #Look for these two together in the login doc, and, if found;
            if who == "White player":
                p1name = username #Set those universal variables to be their name and password
                word = p1name
                p1ready = True
                Addwins("Elo.txt")
                rat = oldstuff
            elif who == "Black player":
                p2name = username 
                word = p2name
                p2ready = True
                Addwins("Elo.txt")
                rat = oldstuff
            print(f'Success, welcome {username}, {who}') #Print a success
            print(f"You have a rating of {rat} ")
            
        else: #Accout not found
            print("Sorry, this account does not exist, please resubmit your username and password, or create a new account") 
            entry()   #Restart their entry          

def signup(): #Let the player sign up
    # Create a new account, persisting credentials and initial stat lines
    global p1ready
    global p2ready
    global p1name
    global p2name
    with open('Login.txt') as f:
            newusername = input("Enter a new username: ") #input a new username
            time.sleep(1)
            if f'{newusername}' in f.read(): #If it is already found on the document;
                print("Sorry, this username is taken, please select a new one") #Tell them to change it
                signup() #Restart the signup
            elif ',' in newusername or '¿' in newusername or ';' in newusername: #commas break detection of username in other documents
                print("Sorry, no commas, upside down question marks or semicolons are permitted in your username")
                signup()
            if (who == "White player" and p1ready == False) or (who == "Black player" and p2ready == False): #If we are looking for player 1 and they are not already in OR we are looking for player 2 and they are not already in then continue;
                newpassword = input("Now make a password: ") #Input password
                fileop = open('Login.txt', 'a+') #Open doc to append
                fileop.write (f"\n{newusername}, {newpassword}¿") #Write in the combo of their username and password
                if who == "White player": #If the person logging in is p1
                    p1name = newusername #Set those  variables to be their name and password
                    p1ready = True #State boolean to say they are ready
                elif who == "Black player": #Likewise for player 2
                    p2name =  newusername #Set those  variables to be their name and password
                    p2ready = True
                print(f"Success, welcome {newusername}, {who}") #Welcome them
                print("Your rating is 100")
                fileop = open('Wins.txt', 'a+') 
                fileop.write (f"\n{newusername},0")
                fileop = open('Loss.txt', 'a+') 
                fileop.write (f"\n{newusername},0") 
                fileop = open('Draw.txt', 'a+') 
                fileop.write (f"\n{newusername},0")
                fileop = open('Elo.txt', 'a+') 
                fileop.write (f"\n{newusername},100")

def entry(): # At the start of the game, offers the choice of entry to the player
    # Loop until the user chooses login or signup for their seat
    New = input(f"{who}: Login or Signup; ").lower() #Inputs whether to login or signup, not case sensitive
    if New == "login": # If they login;
        login() #Direct to login function
    elif New == "signup":  # If they signup;
        signup() # Direct to signup function
    else:
        entry() #If they do a dumb answer restart this entry

def playgame(): #Starts the P1 and P2 login / signup sequence
    # Reset the board, fetch both players, then kick off a new game session
    setboard()
    global who
    global p1ready
    global p2ready
    time.sleep(1)
    print("Get 2 players to play!")
    time.sleep(1)
    who = "White player"
    p1ready = False
    p2ready = False
    entry()
    who = "Black player"
    entry()
    if p1ready == True and p2ready == True: #If both players are ready start
        begin() #Play begin sequence

def want_to_continue():
    # Common prompt gate used by the tutorial sections to pace the narration
    usercon = input("Press enter to proceed ")
    if "cancel" in usercon:
        choices()
    if "" in usercon:
        return True

def learn_pieces(LearnedPiece,Value,PossibleMoves,VisMoves):
    # Educational helper that displays piece values and example move patterns
    if want_to_continue() == True:
        print(f"The {LearnedPiece} is worth {Value}")
        time.sleep(1)
        print(f"The {LearnedPiece} can move {PossibleMoves}")
        time.sleep(1)
        print("This is illustrated by the board;")
        time.sleep(1)
        print(VisMoves)
        print("   ----------------")
        print("    a b c d e f g h")

def check_or_stale(teach,info,matepositions):
    # Show an explanatory scenario for check or stalemate, depending on `teach`
    if want_to_continue() == True:
        print(info)
        time.sleep(2)
        print(f"This is an example of a {teach}... it is white's move and they are {teach}d")
        time.sleep(1)
        print(matepositions)
        print("   ----------------")
        print("    a b c d e f g h")
        time.sleep(2)

def special_moves(special,info,specialpositions1,specialpositions2):
    # Walk through the narrative and board state change for a special move (castle, en passant, etc.)
    if want_to_continue() == True:
        print(f"This special move is {special}")
        time.sleep(1)
        print(info)
        time.sleep(2)
        print(f"An example of when {special} is applicable is illustrated below")
        time.sleep(1)
        print("It is white's move")
        time.sleep(1)
        print(specialpositions1)
        print("   ----------------")
        print("    a b c d e f g h")
        time.sleep(2)
        print(f"After playing {special}, the position now becomes")
        time.sleep(1)
        print(specialpositions2)
        print("   ----------------")
        print("    a b c d e f g h")

def new_to_chess():
        # Provide a scripted walkthrough of chess fundamentals for new players
        if want_to_continue() == True:
            time.sleep(1)
            print("Chess is played on an 8x8 grid")
            time.sleep(1)
            print("letters indicate the file, or x coordinate, and numbers indicate the rank, or y coordinate")
            time.sleep(1)
            print("8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . . . . . ")
            print("   ----------------")
            print("    a b c d e f g h")
        if want_to_continue() == True:
                time.sleep(1)
                print("Chess is a two player game, played by the white (♖) and black (♜) pieces")    
                time.sleep(1)
                print("Each side has 16 pieces, worth different point values. They are;\nPawn(x8): ♙ (worth 1 point)\nRook(x2): ♖ (worth 5 points)\nKnight(x2): ♘ (worth 3 points)\nBishop(x2): ♗ (worth 3 points)\nQueen(x1): ♕ (worth 9 points)\nKing(x1): ♔ (worth the entire game)")
                time.sleep(3)
                print("They are set up on the board at the start of the game like so;")
                time.sleep(1)
                print("8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ \n1 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ ")
                print("   ----------------")
                print("    a b c d e f g h")
                print("Lets learn about the pieces")
                learn_pieces('King','The game','one square up, down, left, right, and diagonally',"8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . o o o . . \n4 | . . . o ♔ o . . \n3 | . . . o o o . . \n2 | . . . . . . . . \n1 | . . . . . . . . ")
                learn_pieces('Queen','Nine points','Any amount of squares up, down, left, right and diagonal\nIt cannot jump over any pieces',"8 | o . . . o . . . \n7 | . o . . o . . o \n6 | . . o . o . o . \n5 | . . . o o o . . \n4 | o o o o ♕ o o o \n3 | . . . o o o . . \n2 | . . o . o . o . \n1 | . o . . o . . o ")
                learn_pieces('Rook','Five points','Any amount of squares up, down, left or right\nIt cannot jump over any pieces',"8 | . . . . o . . . \n7 | . . . . o . . . \n6 | . . . . o . . . \n5 | . . . . o . . . \n4 | o o o o ♖ o o o \n3 | . . . . o . . . \n2 | . . . . o . . . \n1 | . . . . o . . . ")   
                learn_pieces('Bishop','Three points','Any amount of squares diagonally\nIt cannot jump over any pieces',"8 | o . . . . . . . \n7 | . o . . . . . o \n6 | . . o . . . o . \n5 | . . . o . o . . \n4 | . . . . ♗ . . . \n3 | . . . o . o . . \n2 | . . o . . . o . \n1 | . o . . . . . 0 ")
                learn_pieces('Knight','Three points','Two squares in one direction, and then one square in a direction at 90° angle, like an L\nIt is the only piece that can jump over pieces, and it can be pieces of any colour',"8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . o . o . . \n5 | . . o . . . o . \n4 | . . . . ♘ . . . \n3 | . . o . . . o . \n2 | . . . o . o . . \n1 | . . . . . . . . ")
                learn_pieces('Pawn','One point','only forward one square, except on their first move, when they can move forward two squares\nA pawn can only take a piece diagonally forward, but otherwise it cannot move diagonally',"8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . o . . . . . . \n5 | . ♙ . . . . . . \n4 | . . . . o . . . \n3 | . . . . o . . . \n2 | . . . . ♙ . . . \n1 | . . . . . . . . ")
                if want_to_continue() == True:
                    time.sleep(1)
                    print("To win a chess game, you must put your opponent in checkmate")
                    time.sleep(1)
                    print("A check is where you attack your opponents king")
                    time.sleep(1)
                    print("If you are in check, you must end your turn without being in check, ie, your king can no longer be taken")
                    time.sleep(1)
                    print("If it is your move and you can take your opponent's king, there move is an illegal move")
                    time.sleep(1)
                    print("These are all the legal moves in this position for white;")
                    time.sleep(1)
                    print("8 | . . . . . . . . \n7 | . . . ♛ . . . . \n6 | . . . o . . . . \n5 | . . o . . . . . \n4 | . . o ♔ . ♗ . . \n3 | . . o o . . . . \n2 | . . . . . . . . \n1 | ♚ . . . ♜ . . . ")
                    time.sleep(1)
                    print("Note that when you are in check you can either;\nTake the piece giving check\nBlock the pieces line of attack towards the king (not for Knights)\nMove the king away")
                    time.sleep(2)
                    check_or_stale('checkmate',"If you cannot do any of these, meaning that every single possible move on the board will end your turn still in check, it is checkmate, and you lose","8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . ♚ . . . . \n2 | . . . ♛ . . . . \n1 | . . . ♔ . . . . ")
                    check_or_stale('stalemate',"If, all of your legal moves result in you ending your turn in check, but you are not currently in check, it is called a stalemate, and it is a draw","8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . ♚ . . . . \n2 | . . . . . ♛ . . \n1 | . . . . . . . ♔ ")
                    print("Both players may also mutually agree to a draw")
                    if want_to_continue() == True:
                        time.sleep(1)
                        print("There are a few special moves in chess which are important to learn")
                        time.sleep(1)
                        special_moves('castling','Castling occurs as a double move of the king, and a move with the rook.\nCastling is only allowed if the king has not moved yet, and the rook being castled with has not either.\nThe king moves two squares horizontally towards the rook, and the rook jumps over the king and lands next to it.\nYou may not castle through check, meaning if the king were to stop partway through, it would not be in check, neither can you castle to escape from check',"8 | . . . ♚ . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . ♔ . . ♖ ","8 | . . . ♚ . . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . . ♖ ♔ . ")
                        special_moves('En passant','En passant occurs between two pawns.\nIf a pawn moves two squares upwards, and it is directly next to a pawn from the opposition, they may capture the pawn as if it had moved one square\nIt is important to note that this capture is only avalaible for one move',"8 | . . . . ♚ . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . ♙ ♟ . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . ♔ . . . ","8 | . . . . ♚ . . . \n7 | . . . . . . . . \n6 | . . . . . . ♙ . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . ♔ . . . ")
                        special_moves('Promotion','Promotion occurs when a pawn reaches the last rank\n If it is a white pawn, the eigth rank, if it is a black pawn, the first rank\nThat pawn instantly becomes transformed into a piece of your choice, either a knight, bishop, rook or queen',"8 | . . . . ♚ . . . \n7 | ♙ . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . ♔ . . . ","8 | ♕ . . . ♚ . . . \n7 | . . . . . . . . \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | . . . . . . . . \n1 | . . . . ♔ . . . ")
                        if want_to_continue() == True:
                            time.sleep(1)
                            print("Finally, some other general information about playing chess")
                            time.sleep(1)
                            print("Each turn, you may move one piece (except when castling) to a legal square")
                            time.sleep(1)
                            print("It is now your opponents turn")
                            time.sleep(1)
                            print("The player with the white pieces always plays the first move")
                            time.sleep(1)
                            print("Each player will be given a rating upon creating an account")
                            time.sleep(1)
                            print("You will gain points for a win, and lose points for a loss")
                            time.sleep(1)
                            print("If you play someone with a much higher rating, a win will give you a lot more points then a loss would lose points")
                            time.sleep(1)
                            print("Similarly, by playing a much worse opponent, if you win, you will go up a lot less than the amount you would lose if you lost")
                            time.sleep(1)
                            print("And thats it! Those are the rules of chess, good luck!")

def new_to_website():
    if want_to_continue() == True:
        time.sleep(1)
        print("This is an offline chess website, two player play each other over one device")
        time.sleep(1)
        print("To start a game, select the choice to play a game")
        time.sleep(1)
        print("To select something, state the number it is listed as and press enter")
        time.sleep(1)
        print("You may, at any time you are asked to proceed, enter cancel to return to the original choices")
        if want_to_continue() == True:
            print("When playing, there are a few things that you must take into consideration")
            time.sleep(1)
            print("To make a move, first, state the square of the piece you wish to move, in algebraic notation")
            time.sleep(1)
            print("Algebraic notaiton is the letter of the file it is on, followed by the number of the rank")
            time.sleep(1)
            print("8 | . . . . . . . . \n7 | . . . . . . . . \n6 | . . . . . . ▲ . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . o . . . . . \n2 | . . . . . x . . \n1 | . . . . . . . . ")
            print("   ----------------")
            print("    a b c d e f g h")
            time.sleep(2)
            print("The ▲ is on g6")
            time.sleep(1)
            print("The o is on c3")
            time.sleep(1)
            print("The x is on f2")
            time.sleep(1)
            print("Enter the square the piece is on to select it, in the same form as above")
            if want_to_continue() == True:
                time.sleep(1)
                print("Once you have selected a piece, you may then select a legal square that the piece can move to, and enter it in in the same way you selected the piece")
                time.sleep(1)
                print("The piece will be moved there and your turn will end")
                if want_to_continue() == True:
                    time.sleep(1)
                    print("To offer a draw, instead of selecting a piece, type in draw instead. Your opponent will then decide whether they agree to draw or not")
                    time.sleep(1)
                    print("Similarly, to resign, simply type the word resign instead of selecting a piece")
                    time.sleep(1)
                    print("Whenever you are asked a yes or no question (e.g. accepting a draw), please respond with either a Y or N")
                    time.sleep(1)
                    print("Any invalid syntax entered will not be recognised and you will have to resubmit")
                    if want_to_continue() == True:
                        time.sleep(1)
                        print("To play a game, login to your account, or create a new one")
                        time.sleep(1)
                        print("Enter / make the appropriate details and don't forget them!")
                        time.sleep(1)
                        print("And thats it! Try out the website and play your friends.")

def get_rules():
    # Prompt the user for which tutorial set to launch
    print("RULES")
    time.sleep(1)
    choice = input("Do you wish to learn;\n1. Rules of chess\n2. Rules of the website\n3. Rules of both\n")
    time.sleep(1)
    if choice.lower() == '1':
        new_to_chess()
        choices()                
    elif choice.lower() == '2':
        new_to_website()
        choices()
    elif choice.lower() == '3':
        new_to_chess()
        new_to_website()
        choices()
    elif choice.lower() == 'back' or 'cancel':
        choices()
    else:
        print("Invalid syntax, please respond with the number of the option you wish to choose")
        get_rules()

def statlook(stat,speaking):
    # Fetch a particular stat line for the authenticated user and print with a label
    word = uzername #Sets the key word to be found
    with open(stat, 'r') as fp: #Open the designated document
        lines = fp.readlines()

        for line in lines:
            if line.find(word) != -1: 

                res = (line.split(",", 1)) #set variable to everything right of the comma, which will be the value we want
                talk = res[1]
                print(f'{speaking}{talk}') #Print score 
                return talk 

def database():
    # Replay and display a chosen game from the history log for the logged-in user
    setboard()
    print('\n')
    word1 = uzername #Sets the key word to be found
    noposgames = []
    yesposgames = []
    mylist = []
    listpi1 = []
    listpi2 = []
    nogames = 0
    with open('GameHistory.txt', 'r') as fp: #Open the designated document
        lines = fp.readlines()
        for line in lines:
            if line.find(word1) != -1:
                # Accumulate all games involving the current user
                gameselect = line.split(';')[0]
                res = line.split('¿')[-1]
                nogames += 1
                print(f'{nogames}. {gameselect}, {res}')
                noposgames.append(str(nogames))
                yesposgames.append(gameselect)
        print('\n')
        choosegame = input("Please select the game you would like to view ")

        if choosegame in noposgames:

            word2 = yesposgames[int(choosegame) - 1]

            for line in lines:
                    if line.find(word2) != -1:
                            # Extract the compact move record for the selected game
                            fakegam = line.split(';')[-1]
                            games = fakegam.split('¿')[0]
                            res = fakegam.split('¿')[-1]

                            for z in games[0::2]:
                                listpi1.append(z)
                            for i in games[1::2]:
                                listpi2.append(i)
                            for a in range(int(len(games)/2)):
                                mylist.append(f'{listpi1[a]}{listpi2[a]}')
                            selormov = 0
                            for simpie in mylist:
                                    # Reconstruct the board by applying recorded moves in sequence
                                    selormov += 1
                                    if selormov % 2 != 0:
                                        picsim = board[simpie]
                                        board.pop(simpie)
                                    
                                    else:

                                        if simpie == 'wk':
                                            # Special tokens represent castling events
                                            board.pop('81')
                                            board['71'] = 'wK'
                                            board['61'] = 'wR'
                                        if simpie == 'wq':
                                            board.pop('11')
                                            board['31'] = 'wK'
                                            board['41'] = 'wR'
                                        if simpie == 'bk':
                                            board.pop('88')
                                            board['78'] = 'bK'
                                            board['68'] = 'bR'
                                        if simpie == 'bq':
                                            board.pop('18')
                                            board['38'] = 'bK'
                                            board['48'] = 'bR'

                                        if (simpie[-1] == 'q' or simpie[-1] == 'r' or simpie[-1] =='b' or simpie[-1] =='n') and (simpie[0] != 'w' or simpie[0] != 'b'):
                                            # Lowercase markers mean a white pawn promoted on that file
                                            prompic = str(simpie[-1]).upper()
                                            promfil = simpie[0]
                                            board[f'{promfil}8'] = f'w{prompic}'
                                            
                                        if (simpie[-1] == 'Q' or simpie[-1] == 'R' or simpie[-1] =='B' or simpie[-1] =='N') and (simpie[0] != 'w' or simpie[0] != 'b'):
                                            # Uppercase markers mean a black pawn promotion
                                            prompic = str(simpie[-1]).upper()
                                            promfil = simpie[0]
                                            board[f'{promfil}1'] = f'b{prompic}'
                                        
                                        if simpie[-1] == 'e':
                                            # Lowercase e/E encode en passant captures in the log
                                            board.pop(f'{simpie[0]}5')
                                            board[f'{simpie[0]}6'] = 'wP'

                                        if simpie[-1] == 'E':
                                            board.pop(f'{simpie[0]}4')
                                            board[f'{simpie[0]}3'] = 'bP'

                                        board[simpie] = picsim
                                        if want_to_continue() == True:
                                            print_chessboard(board)
                                        time.sleep(1)
                                        
                            print(res)

def account_view():
    # Authenticate a user then show aggregate stats, rating, and optionally game history
    global uzername
    nogames = 0
    percentwins = 0
    uzername = input("Enter your username; ") #Takes username
    password = input("Enter your password; ") #Takes password
    with open('Login.txt') as f:
        if f'{uzername}, {password}¿' in f.read(): 
            print(f'Success, welcome {uzername} \n')
            time.sleep(1)
            w = statlook("Wins.txt","You have won ")
            time.sleep(1)
            l = statlook("Loss.txt","You have lost ")
            time.sleep(1)
            d = statlook("Draw.txt", "You have drawn ")
            time.sleep(1)
            nogames = int(w)+int(l)+int(d)
            print(f"You have played {nogames}\n")
            time.sleep(1)
            # Convert raw totals into a simple win percentage
            percentwins = int((int(w) / nogames) * 100)
            print(f"You have won {percentwins}% of your games\n")
            time.sleep(1)
            statlook("Elo.txt","Your rating is ")
            time.sleep(1)
            Look_at_games = input("Do you wish to look at your games database (Y or N)? ")
            if Look_at_games.lower() == 'y':
                database()
            choices()

        else: 
            print("Sorry, this account does not exist, please resubmit your username and password")
            time.sleep(2)
            choices() 

def halloffame():
    # Rank players by Elo and print the top N entries requested by the user
    deep = input("How many far down the rankings do you wish to go? ")
    print('\n')
    try:
        int(deep)
    except:
        time.sleep(1)
        print("Please enter a number")
        halloffame()
    halllist = []
    namlist = []
    with open('Elo.txt','r') as hall:
        content = hall.readlines()
        for line in content:
            elo = str(line).split(',')[-1]
            elo = int(elo.split('\n')[0])
            # Gather every player's rating so we can rank them numerically
            halllist.append(elo)
            namlist.append(line)
    halllist.sort() #Sort in ascending order
    halllist.reverse()
    # Trim the list to the number of ranks requested by the user
    lin = len(halllist)
    while lin > int(deep):
        halllist.pop(-1)
        lin = len(halllist)
    ranking = 0
    for hall in halllist:
        ranking += 1
        for nam in namlist:
            if hall == int(str(nam).split(',')[-1]):
                print(f'{ranking}. {nam}')
    choices()

def choices():
    # Root menu hub that routes the player to gameplay, tutorials, accounts, or rankings
    time.sleep(1)
    choice = input("Would you like to;\n1. Play a game\n2. See the rules\n3. View an account\n4. View the leaderboard\n")
    if choice.lower() == '1':
        playgame()
    elif  choice.lower() == '2':
        get_rules()
    elif choice.lower() == '3':
        account_view()
    elif choice.lower() == '4':
        print("Welcome to the global leaderboard")
        time.sleep(1)
        print("The top players are represented on the leaderboard")
        time.sleep(1)
        halloffame()
    else:
        time.sleep(1)
        print("Invalid syntax, please respond with the number of the option you wish to choose")
        choices()

def openingAnimation():
    # Play the ASCII splash screen and a quick move animation before showing the menu
    OFFchess = '████▄ ▄████  ▄████      ▄█▄     ▄  █ ▄███▄     ▄▄▄▄▄    ▄▄▄▄▄ \n█   █ █▀   ▀ █▀   ▀     █▀ ▀▄  █   █ █▀   ▀   █     ▀▄ █     ▀▄ \n█   █ █▀▀    █▀▀        █   ▀  ██▀▀█ ██▄▄   ▄  ▀▀▀▀▄ ▄  ▀▀▀▀▄   \n▀████ █      █          █▄  ▄▀ █   █ █▄   ▄▀ ▀▄▄▄▄▀   ▀▄▄▄▄▀    \n       █      █         ▀███▀     █  ▀███▀                      \n        ▀      ▀                 ▀                              \n                                                                '
    time.sleep(2)
    for i in range(9):
        time.sleep(1)
        if i == 0:
            anim = "8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . . . . . \n3 | . . . . . . . . \n2 | ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ \n1 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ "
        if i == 1:
            anim = "8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ \n6 | . . . . . . . . \n5 | . . . . . . . . \n4 | . . . . ♙ . . . \n3 | . . . . . . . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ "
        elif i == 2:
            anim = "8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♟ ♟ ♟ \n6 | . . . . . . . . \n5 | . . . . ♟ . . . \n4 | . . . . ♙ . . . \n3 | . . . . . . . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ "
        elif i == 3:
            anim = "8 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♟ ♟ ♟ \n6 | . . . . . . . . \n5 | . . . . ♟ . . . \n4 | . . . . ♙ . . . \n3 | . . . . . ♕ . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ . ♔ ♗ ♘ ♖ "
        elif i == 4:
            anim = "8 | ♜ . ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♟ ♟ ♟ \n6 | . . ♞ . . . . . \n5 | . . . . ♟ . . . \n4 | . . . . ♙ . . . \n3 | . . . . . ♕ . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ . ♔ ♗ ♘ ♖ "
        elif i == 5:
            anim = "8 | ♜ . ♝ ♛ ♚ ♝ ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♟ ♟ ♟ \n6 | . . ♞ . . . . . \n5 | . . . . ♟ . . . \n4 | . . ♗ . ♙ . . . \n3 | . . . . . ♕ . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ . ♔ . ♘ ♖ "
        elif i == 6:
            anim = "8 | ♜ . ♝ ♛ ♚ . ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♟ ♟ ♟ \n6 | . . ♞ . . . . . \n5 | . . ♝ . ♟ . . . \n4 | . . ♗ . ♙ . . . \n3 | . . . . . ♕ . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ . ♔ . ♘ ♖ "
        elif i == 7:
            anim = "8 | ♜ . ♝ ♛ ♚ . ♞ ♜ \n7 | ♟ ♟ ♟ ♟ . ♕ ♟ ♟ \n6 | . . ♞ . . . . . \n5 | . . ♝ . ♟ . . . \n4 | . . ♗ . ♙ . . . \n3 | . . . . . . . . \n2 | ♙ ♙ ♙ ♙ . ♙ ♙ ♙ \n1 | ♖ ♘ ♗ . ♔ . ♘ ♖ "
        elif i == 8:
            anim = ""
        os.system('clear')  # Clear the terminal screen 
        print(OFFchess)
        print(anim)
        print("   ----------------")
        print("    a b c d e f g h")
    os.system('clear')
    print(OFFchess)
    time.sleep(1)
    print("CHESS TIME")
    time.sleep(2)
    print("Welcome to OFF Chess, on offline chess program")
    choices()

def begin():
    # Final pre-game setup: show board, log matchup, and start the move loop
    time.sleep(1)
    print("Get ready...")
    time.sleep(1)
    print_chessboard(board)
    time.sleep(1)
    with open('GameHistory.txt', 'a') as enter_games:
        enter_games.write(f'\n{p1name} VS {p2name} ({date.today()});')
    start()
            
global wkingmoved
global bkingmoved
global bkrookmoved
global bqrookmoved
global wkrookmoved
global wqrookmoved
global turns
# Track castling eligibility and turn order flags across the session
bkingmoved = False
wkingmoved = False
wkrookmoved = False
wqrookmoved = False
bkrookmoved = False
bqrookmoved = False
turns = 0
setboard()
# Show the splash screen and launch the interactive menu loop
openingAnimation()
