import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


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
        if(len(self.cells) == self.count):
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells
        return None


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)

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
        """a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as 
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        del_sen = []
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if len(sentence.cells) == 0:
                del_sen.append(sentence)
        self.knowledge = [x for x in self.knowledge if x not in del_sen]
    
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
        # step 1
        self.moves_made.add(cell)
        print("step 1:")
        print(self.moves_made)

        # step 2
        self.mark_safe(cell)
        print("safes")
        print(self.safes)

        # step 3
        temp = self.neighbors(cell)
        result_set = temp - self.safes
        size = len(result_set)
        result_set = result_set - self.mines
        count = count - (size - len(result_set))
        print("new sentence")
        print(Sentence(result_set,count))
        if len(result_set) != 0 :
            self.knowledge.append(Sentence(result_set,count))

        #Step 4
        for sentence in self.knowledge:
            if sentence.known_mines() != None:
                print(sentence.known_mines())
                mines_lst = [mine for mine in sentence.known_mines()]
                print('Known Mines')
                print('--------------')
                for x in mines_lst:
                    print(x)
                    self.mark_mine(x)
            if sentence.known_safes() != None:
                safes_lst = [safe for safe in sentence.known_safes()]
                print('Known Safes')
                print('--------------')
                for y in safes_lst:
                    print(y)
                    self.mark_safe(y)
         #step 5
        print(len(self.knowledge))
        added_kh = []
        del_kh = []
        for sent1 in self.knowledge:
            for sent2 in self.knowledge:
                if sent1 != sent2 and sent1.cells.issubset(sent2.cells):
                    set1 = sent2.cells -sent1.cells
                    count = sent2.count -sent1.count
                    del_kh.append(sent2)

                    print("sentence 2")
                    print(sent2.cells)
                    print("sentence 1")
                    print(sent1.cells)
                    print("set1 added , sent2 -sent1")
                    print(set1)
                    if len(sent1.cells) > 0:
                        print("nooo")
                        added_kh.append(Sentence(set1, count))

        self.knowledge = [x for x in self.knowledge if x not in del_kh]
        self.knowledge.extend(added_kh) 

        

        

          

    def neighbors(self , cell):

        neighb = set()
        i = cell[0]
        j = cell[1]
        if j-1 >= 0:
            neighb.add((i,j-1))
            if i-1 >= 0 :
                neighb.add((i-1,j-1))
            if i+1 < 8:
                neighb.add((i+1,j-1))

        if j+1 < 8 :
            neighb.add((i,j+1))
            if i-1 >= 0 :
                neighb.add((i-1,j+1))
            if i+1 < 8:
                neighb.add((i+1,j+1))

        if i+1 < 8:
            neighb.add((i+1,j))
        if i-1 >= 0:
            neighb.add((i-1,j))

        return neighb 

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for s in self.safes:
            if s not in self.moves_made:
                return s
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        temp = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    temp.add((i,j))
        if len(temp) == 0:
            return None
        return random.choice(list(temp))
                

        
