#!/usr/bin/env python

import click
import random
import string
import sys

@click.command()
@click.option('-a', '--animals', required=True,
              help='Path to input dictionary of animals')
@click.option('-d', '--adjectives', required=True,
              help='Path to input dictionary of adjectives')
@click.option('-u', '--used_names', required=True,
              help='Path to list of already used names')
@click.option('-s', '--starting_letter',
              help='Choose starting letter. Might not work with uncommon ones, such as X')
def main(animals, adjectives, used_names, starting_letter):
    #Read in the already used names into a list
    with open(used_names) as f:
        usedWords = [word.lower() for line in f for word in line.split()]

    #Read in the animal list
    with open(animals) as animal_file:
        animal_list = animal_file.read().splitlines()

    #Read in the animal list
    with open(adjectives) as adjectives_file:
        adjectives_list = adjectives_file.read().splitlines()

    #Loop until a good combo is found
    foundWord = 0
    while (foundWord == 0):
        #Get a starting letter for both words
        if (starting_letter):
            if starting_letter.isalpha():
                startLetter = starting_letter
            else:
                sys.exit("ERROR: Provided starting letter is not alpha-numerical, exiting.")
        else:
            startLetter = random.choice(string.ascii_letters.lower())

        if startLetter == 'x' or startLetter == 'z': #skip the ones starting with X and Z
            continue

        #Trim list of only contain values starting with startLetter
        animal_list_single = [idx for idx in animal_list if idx[0].lower() == startLetter.lower()]
        adjectives_list_single = [idx for idx in adjectives_list if idx[0].lower() == startLetter.lower()]

        #Generate a random combination
        animalIndex = random.randint(0, len(animal_list_single)-1)
        adjectiveIndex = random.randint(0, len(adjectives_list_single)-1)
        animal = animal_list_single[animalIndex].capitalize()
        adjective = adjectives_list_single[adjectiveIndex].capitalize()
        combo = adjective + " " + animal

        # Check if any of the items in the combo has been used before, and if so, skip it
        if animal.lower() in usedWords or adjective.lower() in usedWords:
            continue

        #Make a suggestion
        questionList = ['How about',
                        'Perhaps',
                        'Maybe',
                        'Would you try',
                        'Do you like',
                        'Could you consider',
                        'Why not',
                        'Wanna use']

        print("")
        question = questionList[random.randint(0,len(questionList)-1)] + " '" + combo + "'? [yes/NO]: "

        #Ask for user inpiut
        answer = input(question)
        if (answer.startswith(('y', 'Y'))):
            print("")
            print("Congratulations!!")
            print("You've selected '" + combo + "'. Adding it to used combinations.")
            print("")

            #Add the seleected combo to used combinations
            f = open(used_names, "a")
            f.write(combo + "\n")
            f.close()

            #Stop the loop
            foundWord = 1
        else:
            continue

if __name__ == '__main__':
    main()
