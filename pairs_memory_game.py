import random
import pandas as pd
import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt
console = Console()

def clear_screen():
    '''
    - This function clears the terminal
    '''
    # For when the user is using a Windows system
    if os.name == 'nt':
        _ = os.system('cls')
    # For when the user is using a macOS or Linux system
    else:
        _ = os.system('clear')

def letter_selecter():
    '''
    - This function randomly selects 8 letters from the alphabet.
    - Duplicates the selected letters before adding them to a list
    - Randomly shuffles the list
    '''
    random_letters =''
    alphabet= 'abcdefghijklmnopqrstuvwxyz'
    for i in range(8):
        random_letters += random.choice(alphabet)
    letters_doubled = random_letters*2
    letter_list =[]
    for letter in letters_doubled:
        letter_list += letter
        random.shuffle(letter_list)
    return letter_list

def dict_generator(output):
    '''
    - This function turns the list of random letters into a dictionary with 'int's as keys
    '''
    letter_dict ={}
    for index, let in enumerate(output,start=1):
        letter_dict[index]=let
    return letter_dict

def matrix_printer(num_list):
    '''
    - This function slices num_list to form a matrix
    '''
    dict_data = {'a': num_list[:4], 'b': num_list[4:8], 'c': num_list[8:12], 'd': num_list[12:]}
    df = pd.DataFrame(dict_data)
    matrix = df.values
    console.rule(title='[bold red on black]Pairs Memory Game', characters='─', style='bold red on black', align='center')
    console.print(matrix, style="bold red on black", justify="center")

def users_guesses(num_list,guess0):
    '''
    - This function requests a user's guess before checking that the guess is:
    -- an integer
    -- a number between 1-16
    -- has not already been matched
    -- is not the same as the first guess
    If any of these conditions are not met a new user guess will be requested
    '''
    gues1 = False
    while gues1 == False:
        gues1 = Prompt.ask('[bold red on black]Pick a number between 1-16')
        if not gues1.isnumeric():
            print("Only integers are allowed! Please try again")
            gues1 =False
        else:
            guess1=int(gues1)
            if guess1 < 1 or guess1 >16:
                print("Sorry only numbers between 1-16! Please try again")
                gues1 =False
            elif guess1 not in num_list:
                print("You've already found this number's match! Please try again")
                gues1 =False
            elif guess0 == guess1:
                print(f"You've already picked {guess0}! Please try again")
                gues1 =False
            else:
                return guess1

def matrix_manipulator(num_list,guess1,guess2):
    '''
    - This function replaces the users int guesses with their letter value equivalents from the pairs_dict 
      in the printed matrix.
    '''
    gues1_indx= num_list.index(guess1)
    num_list[gues1_indx] = pairs_dict[guess1]
    gues2_indx= num_list.index(guess2)
    num_list[gues2_indx] = pairs_dict[guess2]
    return num_list

num_list = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]
matches = 0
guesses = 0
matrix_printer(num_list)
pairs_dict = dict_generator(letter_selecter())

while matches != 8:
    guess1 =users_guesses(num_list,0)
    guess2 =users_guesses(num_list, guess1)
    clear_screen()
    if pairs_dict[guess1] == pairs_dict[guess2]:
        num_list = matrix_manipulator(num_list,guess1,guess2)
        matrix_printer(num_list)
        console.print(f"{pairs_dict[guess1]} and {pairs_dict[guess2]} are a match!", style="bold green on black", justify="center")
        matches += 1
        guesses += 1
    else:
        snum_list = num_list[:]
        snum_list = matrix_manipulator(snum_list,guess1,guess2)
        matrix_printer(snum_list)
        console.print(f"{pairs_dict[guess1]} and {pairs_dict[guess2]} are not a match!", style="bold red on black", justify="center")
        guesses += 1
console.print(f"Game Over You Win! Well Done It Took You {guesses} Guesses!", style="bold green on black", justify="center")
