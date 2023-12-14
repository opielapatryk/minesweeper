#https://cs50.harvard.edu/ai/2023/projects/1/minesweeper/
#https://cs50.harvard.edu/ai/2023/notes/1/
#https://www.youtube.com/watch?v=HWQLez87vqM
# na podstawie knowledge udowodnij ze A === true
#   sprawdz if KB and not A jest sprzeczne 
#   jezeli jest sprzeczne => KB entails A
#   else => no entailment 

# gdy komórka zostanie oznaczona jako bezpieczna, to powinna zostać usunięta ze zbioru 
# If cell is safe => remove this cell from knowledge
# If move was made => remove this cell from knowledge

import itertools
import random
import logic 

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        for x in self.cells:
            # if cell = mine then return 
            # if set items count is equal to count then all cells are mines 
            mines.add(x)
        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        for x in self.cells:
            # if cell = safe then return 
            safes.add(x)
        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # remove cell from the set and decrease count by one 

        return self.cells(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # remove cell from the set 
        return self.cells(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        print('mark_mine cell: ', cell)
        print('moves_made: ',self.moves_made)
        print('mines: ',self.mines)
        print('safes: ',self.safes)
        print('knowledge: ',self.knowledge)
        self.mines.add(cell)
        print('MINES: ',self.mines)



    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        print('marked cell as safe: ', cell)
        self.safes.add(cell)
        for sentence, (cells,count) in self.knowledge:
            if cell in cells:
                self.knowledge[sentence] = (cells-cell,count)
        # Think why cell is not removed from knowledge if its safe
        # - check if it is correctly marked as safe | YES, IT IS 
                


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.safes.add(cell)
        
        # (2,4) = (y,x) idk who wrote this map :) 

        # if the cell is not on the border
        if cell[0] != 0 and cell[1] != 0 and cell[0] != self.height-1 and cell[1] != self.width-1:
            self.knowledge.append(({(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]-1),(cell[0],cell[1]+1),(cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1)},count))
            if count == 0:
                self.safes.add((cell[0]-1,cell[1]-1))
                self.safes.add((cell[0]-1,cell[1]))
                self.safes.add((cell[0]-1,cell[1]+1))
                self.safes.add((cell[0],cell[1]-1))
                self.safes.add((cell[0],cell[1]+1))
                self.safes.add((cell[0]+1,cell[1]-1))
                self.safes.add((cell[0]+1,cell[1]))
                self.safes.add((cell[0]+1,cell[1]+1))

        # if the cell is in the top left corner
        if cell[0] == 0 and cell[1] == 0:
            self.knowledge.append(({(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1),(cell[0],cell[1]+1)},count))
            if count == 0:
                self.safes.add((cell[0]+1,cell[1]))
                self.safes.add((cell[0]+1,cell[1]+1))
                self.safes.add((cell[0],cell[1]+1))

        # if the cell is in the top right corner
        if cell[0] == 0 and cell[1] == self.width-1:
            self.knowledge.append(({(cell[0]+1,cell[1]),(cell[0]+1,cell[1]-1),(cell[0],cell[1]-1)},count))
            if count == 0:
                self.safes.add((cell[0]+1,cell[1]))
                self.safes.add((cell[0]+1,cell[1]-1))
                self.safes.add((cell[0],cell[1]-1))

        # if the cell is in the bottom left corner
        if cell[0] == self.height-1 and cell[1] == 0:
            self.knowledge.append(({(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]+1)},count))
            if count == 0:
                self.safes.add((cell[0]-1,cell[1]))
                self.safes.add((cell[0]-1,cell[1]+1))
                self.safes.add((cell[0],cell[1]+1))

        # if the cell is in the bottom right corner
        if cell[0] == self.height-1 and cell[1] == self.width-1:
            self.knowledge.append(({(cell[0],cell[1]-1),(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1])},count))
            if count == 0:
                self.safes.add((cell[0],cell[1]-1))
                self.safes.add((cell[0]-1,cell[1]-1))
                self.safes.add((cell[0]-1,cell[1]))

        # if the cell is on the left border 
        if cell[1] == 0 and cell[0] != 0 and cell[0] != self.height-1:
            self.knowledge.append(({(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]+1),(cell[0]+1,cell[1]+1),(cell[0]+1,cell[1])},count))
            if count == 0:
                self.safes.add((cell[0]-1,cell[1]))
                self.safes.add((cell[0]-1,cell[1]+1))
                self.safes.add((cell[0],cell[1]+1))
                self.safes.add((cell[0]+1,cell[1]+1))
                self.safes.add((cell[0]+1,cell[1]))

         # if the cell is on the right border 
        if cell[1] == self.width-1 and cell[0] != 0 and cell[0] != self.height-1:
            self.knowledge.append(({(cell[0]-1,cell[1]),(cell[0]-1,cell[1]-1),(cell[0],cell[1]-1),(cell[0]+1,cell[1]-1),(cell[0]+1,cell[1])},count))
            if count == 0:
                self.safes.add((cell[0]-1,cell[1]))
                self.safes.add((cell[0]-1,cell[1]-1))
                self.safes.add((cell[0],cell[1]-1))
                self.safes.add((cell[0]+1,cell[1]-1))
                self.safes.add((cell[0]+1,cell[1]))

        # if the cell is on the top border 
        if cell[0] == 0 and cell[1] != self.width-1 and cell[1] != 0:
            self.knowledge.append(({(cell[0],cell[1]-1),(cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]),(cell[0]+1,cell[1]+1),(cell[0],cell[1]+1)},count))
            if count == 0:
                self.safes.add((cell[0],cell[1]-1))
                self.safes.add((cell[0]+1,cell[1]-1))
                self.safes.add((cell[0]+1,cell[1]))
                self.safes.add((cell[0]+1,cell[1]+1))
                self.safes.add((cell[0],cell[1]+1))

        # if the cell is on the bottom border 
        if cell[0] == self.height-1 and cell[1] != 0 and cell[1] != self.width-1:
            self.knowledge.append(({(cell[0],cell[1]-1),(cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]),(cell[0]-1,cell[1]+1),(cell[0],cell[1]+1)},count))
            if count == 0:
                self.safes.add((cell[0],cell[1]-1))
                self.safes.add((cell[0]-1,cell[1]-1))
                self.safes.add((cell[0]-1,cell[1]))
                self.safes.add((cell[0]-1,cell[1]+1))
                self.safes.add((cell[0],cell[1]+1))

        
        new_knowledge = []

        for sentence in self.knowledge:
            sets, count = sentence
            new_set = set()
            for pair in sets:
                if pair not in self.safes:
                    new_set.add(pair)
            new_knowledge.append((new_set, count))

        self.knowledge = new_knowledge
                
        for sentence in self.knowledge:
            sets, count = sentence
            if len(sets) == count:
                for pair in sets:
                    self.mark_mine(pair)
        
        # sentences with count equal to 1
        count_one_sentences = []
        for sentence in self.knowledge:
            sets, count = sentence
            if count == 1:
                count_one_sentences.append(sentence)
                self.knowledge.remove(sentence)
        
        # zbiory = [({(5, 3), (3, 3), (4, 3)}, 1), ({(5, 3), (4, 3)}, 1)] =
        # = [({(5, 3), (4, 3)}, 1), ({(5, 3), (4, 3)}, 1)] = [({(5, 3), (4, 3)},1)]
        # self.safes.add((3,3))
        # jezeli zbior a jest podzbiorem jakiegos zbioru to obetnij roznice z wiekszego zbioru i dodaj ją do safes cells

        #sets without count
        one_count_sets = [] # [{(5, 3), (3, 3), (4, 3)},{(5, 3), (4, 3}]
        for sentence in count_one_sentences:
            sets, count = sentence
            one_count_sets.append(sets)

        # MUSZE DODAC DO SELF.KNOWLEDGE WSZYSTKIE SENTENCES WITH COUNT == 1 WITHOUT SAFES.CELLS
        # ZANIM TO ZROBIE MUSZE STWORZYC (TUPLE Z SETÓW BEZ SAFE CELLS, COUNT == 1 )
        set_of_safes = set()
        addThisToKnwldg = []
        for my_subset in one_count_sets:
            for my_set in one_count_sets: 
                if my_subset in my_set:
                    for x in my_set:
                        set_of_safes.add(x)
                    for x in my_subset:
                        set_of_safes.remove(x)
            
            addThisToKnwldg.append(my_subset)
            addThisToKnwldg.append(1)
            addThisToKnwldg = tuple(addThisToKnwldg)
            if addThisToKnwldg not in self.knowledge:
                self.knowledge.append(addThisToKnwldg)
            addThisToKnwldg = []

        for x in set_of_safes:
            self.safes.add(x)
                    
        # remove item from knowledge if there is ({set()},0)

        for sentence in self.knowledge:
            my_set, count = sentence
            if count == 0:
                self.knowledge.remove(sentence)


        print('moves_made: ',self.moves_made)
        print('mines: ',self.mines)
        print('safes: ',self.safes)
        print('knowledge: ',self.knowledge)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print('moves_made: ',self.moves_made)
        print('mines: ',self.mines)
        print('safes: ',self.safes)
        print('knowledge: ',self.knowledge)
        for x in self.safes:
            if x not in self.moves_made:
                return x

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            randmove = (random.randint(0,self.height-1),random.randint(0,self.width-1))
            print('randmove: ',randmove)
            print('self.moves_made: ',self.moves_made)
            print('self.safes: ',self.safes)
            if randmove not in self.moves_made and randmove not in self.safes and randmove not in self.mines:
                break
        return randmove

({(6, 6), (6, 7), (5, 5), (6, 5)}, 3),
({(5, 5), (6, 4), (6, 5), (6, 3)}, 2),
({(0, 2), (1, 2), (2, 2)}, 2),
({(6, 2), (6, 3), (6, 4)}, 1),
({(6, 2), (7, 2)}, 1), ({(0, 7), (0, 5), (0, 6)}, 1),
({(6, 6), (6, 7)}, 1), ({(0, 2), (1, 2)}, 1),
({(0, 4), (0, 5), (0, 6)}, 1),
({(6, 2), (6, 3)}, 1),
({(0, 7), (0, 6)}, 1),
({(0, 3), (1, 3), (0, 5), (0, 4)}, 1)
({(5, 5)}, 1),
({(6, 2)}, 1),
({(1, 2), (1, 3), (2, 2)}, 3),
# if sentence with smaller count is subset of sentence with larger count => remove sentence with smaller count
# if there is a sentence which is known to contain the mines and is the substring of sentence with larger count => remove sentence with smaller count && remove substring from sentence with larger count && substract substring count from sentence with larger count