#https://cs50.harvard.edu/ai/2023/projects/1/minesweeper/
#https://cs50.harvard.edu/ai/2023/notes/1/
#https://www.youtube.com/watch?v=HWQLez87vqM
# na podstawie knowledge udowodnij ze A === true
#   sprawdz if KB and not A jest sprzeczne 
#   jezeli jest sprzeczne => KB entails A
#   else => no entailment 
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
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        print('mark safe cell: ', cell)
        print('moves_made: ',self.moves_made)
        print('mines: ',self.mines)
        print('safes: ',self.safes)
        print('knowledge: ',self.knowledge)
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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
        # print('moves_made: ',self.moves_made)
        # print('mines: ',self.mines)
        # print('safes: ',self.safes)
        # print('knowledge: ',self.knowledge)
        while True:
            randmove = (random.randint(0,self.height-1),random.randint(0,self.width-1))
            print('randmove: ',randmove)
            print('self.moves_made: ',self.moves_made)
            print('self.safes: ',self.safes)
            if randmove not in self.moves_made and randmove not in self.safes:
                break
        return randmove
