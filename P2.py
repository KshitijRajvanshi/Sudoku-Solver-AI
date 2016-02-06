import sys
def constraint(example):
    flag=[0 for i in range(9)]
    for i in range(9):    
        if example[i] > 0:
            flag[example[i]-1] += 1
    for i in range(9):
        if flag[i] > 1:
            return True
    return False
    
class Sudoku:
    def __init__(self):
        self.board=[[0 for j in range(9)] for i in range(9)]
        return

    def fileuplaod(self,filename):
        sudokuline=open(filename).readlines()
        sudokuline = [s.replace('.', '0') for s in sudokuline]
        columnline = 0
        for j in range(9):
            line = sudokuline[j]
            for i in range(9):
                self.board[columnline][i]= int(line[i])
            columnline += 1
        return
    def write(self):
         print ("____________________") 
         rowStrings=[]
         for i in range(9):
             rowString=[]
             for j in range(9):
                 rowString.append(str(self.board[i][j])+" ")
            #print rowString
             rowStrings.append(self.formatRow(rowString))
         for i in range(0, len(rowStrings), 3):
             for j in range(0, 3):
                 print (rowStrings[i+j])
             print ("--------------------" )

         return
    def formatRow(self, rowString):
        formattedString=""
        for i in range(0, len(rowString), 3):
            for j in range(0, 3):
                formattedString+=rowString[i+j]
            formattedString+="|"
            
        return formattedString
    def zerovalues(self):
        count=0
        for rows in self.board:
            for k in rows:
                if k==0: count += 1
        return count
    
    def copyboard(self):
        copy=Sudoku()
        for i in range(9):
            for j in range(9):
                copy.board[i][j]=self.board[i][j]
        return copy   
    def validstates(self):
        
        for i in range(3):
            for j in range(3):
                valid=[]
                for k in range(3):
                    for l in range(3):
                        valid.append(self.board[i*3+k][j*3+l])
                if constraint(valid): return False
        
        for i in range(9):
            validrow=[]
            for j in range(9):
                validrow.append(self.board[i][j])
            if constraint(validrow): return False
            
        for i in range(9):
            validcolumn=[]
            for j in range(9):
                validcolumn.append(self.board[j][i])
            if constraint(validcolumn): return False
        return True
    
def minimum_cells(board):
    Minimum = 9 

    flag=[[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            for x in range(3):
                for y in range(3):
                    if board.board[i*3+x][j*3+y] == 0:
                       flag[i][j]+=1    
    for i in range(3):
        for j in range(3):
            if flag[i][j] < Minimum and flag[i][j] > 0:
                Minimum = flag[i][j]
                Minimum_cells=("cell", i, j)
    
    flag=[0,0,0,0,0,0,0,0,0]
    for i in range(9):
        for j in range(9):
            if board.board[i][j] == 0:
                flag[i] += 1
    for i in range(9):
        if flag[i] < Minimum and flag[i]>0:
            Minimum = flag[i]
            Minimum_cells=("row", i)

    flag=[0,0,0,0,0,0,0,0,0]
    for i in range(9):
        for j in range(9):
            if board.board[j][i] == 0:
                flag[i] += 1
    for i in range(9):
        if flag[i] < Minimum and flag[i]>0:
            Minimum = flag[i]
            Minimum_cells=("column", i)
             
    return (Minimum, Minimum_cells)

def combinations(str):
    if len(str) <=1:
        yield str
    else:
        for info in combinations(str[1:]):
            for i in range(len(info)+1):
                yield info[:i] + str[0:1] + info[i:]

def play(board):
    Minimum, Minimum_cells = minimum_cells(board)
    if Minimum == 0: return([])
    
    node = []
    if Minimum_cells[0] == "cell":
        for i in range(3):
            for j in range(3):
                node.append(board.board[Minimum_cells[1]*3+i][Minimum_cells[2]*3+j])
    elif Minimum_cells[0] == "row":
        for i in range(9):
            node.append(board.board[Minimum_cells[1]][i])
    elif Minimum_cells[0] == "column":
        for i in range(9):
            node.append(board.board[i][Minimum_cells[1]])
             
    numbers=[1,2,3,4,5,6,7,8,9]
    numbers_value=[]    
    for i in range(9):
        if node[i] == 0:
            numbers_value.append(i)
        else:
            numbers.pop(numbers.index(node[i]))
    
    played = []
    for p in combinations(numbers):
        node_copy=[i for i in node]
        sudoku_copy=board.copyboard()        
        for i in numbers_value:
            node_copy[i]=p.pop(0)
        
        if Minimum_cells[0] == "cell":
            for i in range(3):
                for j in range(3):
                    sudoku_copy.board[Minimum_cells[1]*3+i][Minimum_cells[2]*3+j]=node_copy.pop(0)
        elif Minimum_cells[0] == "row":
            for i in range(9):
                sudoku_copy.board[Minimum_cells[1]][i]=node_copy.pop(0)
        elif Minimum_cells[0] == "column":
            for i in range(9):
                sudoku_copy.board[i][Minimum_cells[1]]=node_copy.pop(0)
        played.append(sudoku_copy)
    return played
    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print ("P2.py filename")
        sys.exit(0)

    result=[]
    solutionsofgame=[]
    
    board=Sudoku()
    board.fileuplaod(sys.argv[1])
    if board.validstates(): result.append(board)
    else:
        print ("Input game is not valid.")
        sys.exit(0)
    
    count = 0
    while len(result) > 0:
        count += 1
        sudokuboard=result.pop()
        zerosvalue=sudokuboard.zerovalues()
        if zerosvalue == 0:
            sudokuboard.write()
            print
            solutionsofgame.append(sudokuboard)
            print("Solution No:-",len(solutionsofgame))
            continue
        
            
        
        r=play(sudokuboard)
        for new_board in r:
            
            if new_board.validstates():
                result.append(new_board)
