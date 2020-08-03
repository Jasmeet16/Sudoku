import pygame , sys
from settings import *
from buttonclass import *
from checkValid import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((width , height))
        self.grid = testBoard2
        self.running = True
        self.selected = None
        self.mousepos = None
        self.cellChanged = False
        self.finished = False
        self.lockedcells = []
        self.IncorrectCells = []
        self.font = pygame.font.SysFont( "arial" , cellsize//2 )
        self.load()

    def run(self):
        while self.running:

            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()
############# user ip / events #######################
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseongrid()
                if selected:
                    self.selected = selected
                else:
                    print("Invalid Location")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.solve_gui(self.window)
                if self.selected != None and self.selected not in self.lockedcells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int( event.unicode )
                        self.cellChanged= True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    print(self.IncorrectCells)
                    self.checkrows()
                    self.checkCols()
                    self.checksmallgrid()
                    self.ShadeIncorrectCells(self.window, self.IncorrectCells)
                if self.selected != None and self.selected not in self.lockedcells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int( event.unicode )
                        self.cellChanged= True
    def update(self):
        self.mousepos = pygame.mouse.get_pos()
        if self.cellChanged:
            self.IncorrectCells = []
            if self.allCellsDone():
                self.checkallCells()
                print( self.IncorrectCells )
    # ########
    def draw(self):
        self.window.fill(WHITE)
        if self.selected:
            self.drawSelection( self.window , self.selected)

        self.shadeLockedCells(self.window , self.lockedcells)
        self.ShadeIncorrectCells(self.window, self.IncorrectCells)
        
        self.drawNumbers(self.window , self.grid)

        self.drawgrid(self.window)
        pygame.display.update()
        self.cellChanged =False

######################################################
    def allCellsDone(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        print("congrats")
        return True
    def checkallCells(self):

        self.checkrows()
        self.checkCols()
        self.checksmallgrid()
        

    def checkrows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedcells and [xidx, yidx] not in self.IncorrectCells:
                        self.IncorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.lockedcells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.lockedcells:
                                self.IncorrectCells.append([k, yidx])

    def checkCols(self):
        for xidx in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedcells and [xidx, yidx] not in self.IncorrectCells:
                        self.IncorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.lockedcells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.lockedcells:
                                self.IncorrectCells.append([xidx, k])

    def checksmallgrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for i in range(3):
                    for j in range(3):

                        xidx = x * 3 + i
                        yidx = y * 3 + j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.lockedcells and [xidx, yidx] not in self.IncorrectCells:
                                self.IncorrectCells.append([xidx, yidx])
                            if [xidx, yidx] in self.lockedcells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x * 3 + k
                                        yidx2 = y * 3 + l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2,yidx2] not in self.IncorrectCells:
                                            self.IncorrectCells.append([xidx2, yidx2])


################ gray blue etc shades
    def drawSelection(self , window , spos):
        pygame.draw.rect( window , LIGHTBLUE , ( (spos[0]*cellsize) + 75 , (spos[1]*cellsize) + 100 , cellsize ,cellsize) )
    def shadeLockedCells(self , window , locked):
        for cell in locked:

            pygame.draw.rect(window , LOCKEDCELLCOLOR , ( cell[0]*cellsize + pos[0] , cell[1]*cellsize + pos[1] , cellsize , cellsize ))

    def ShadeIncorrectCells(self , window , incorrect):
        for cell in self.IncorrectCells:
            pygame.draw.rect(window, INCORRECTCOLOR, (cell[0]*cellsize + pos[0] , cell[1]*cellsize + pos[1] , cellsize , cellsize))

### get grid on gui
    def drawNumbers(self , window , numbers):

        for yidx , row in enumerate(numbers):
            for xidx , num in enumerate(row):
                if num != 0:
                    spos = [(xidx*cellsize) + pos[0], (yidx*cellsize )+ pos[1] ]
                    self.textToScreen(str(num), spos , window)

    def drawgrid(self , window ):
        pygame.draw.rect( window , BLACK ,( pos[0] , pos[1], width - 150 , height - 150 ),2 )
        for x in range(9):
            if x % 3 == 0:
                pygame.draw.line( window , BLACK , (pos[0] + x * cellsize , pos[1] ) ,(pos[0] + x * cellsize , pos[1]+450 ) , 2 )
                pygame.draw.line(window, BLACK, ( pos[0] ,pos[1] + x * cellsize ), ( pos[0] + 450 ,pos[1] + x * cellsize),2)
            else :
                pygame.draw.line(window, BLACK, (pos[0] + x * cellsize, pos[1]), (pos[0] + x * cellsize, pos[1] + 450))
                pygame.draw.line(window, BLACK, (pos[0], pos[1] + x * cellsize), (pos[0] + 450, pos[1] + x * cellsize))

    def mouseongrid(self):
        if self.mousepos[0] < pos[0] or self.mousepos[1] < pos[1]:
            return False
        if self.mousepos[0] > gridsize + pos[0] or self.mousepos[1] > pos[1] + gridsize:
            return False
        return ( (self.mousepos[0] - pos[0] ) // cellsize ,( self.mousepos[1] - pos[1] )//cellsize)


    def textToScreen(self, text, spos, window):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        spos[0] += (cellsize-fontWidth)//2
        spos[1] += (cellsize-fontHeight)//2

        window.blit( font , (spos[0] , spos[1]) )

    def load(self):

        for yidx , row in enumerate(self.grid):
            for xidx , num in enumerate(row):
                if num != 0:
                    self.lockedcells.append([ xidx , yidx ])

    def isInt(self , string):
        try:
            int(string)
            return True
        except:
            return False

######## Solve using backtrack ###########

    def solve_gui(self , window):
        find = self.find_empty(self.grid)
        if not find:
            return True
        else:
            [row, col] = find
            spos = find

        for  i in range(1, 10):
            if valid(self.grid, i, (row, col)):
                if self.isInt(i):
                    self.grid[row][col] = int(i)
                    self.cellChanged = True
                self.checkallCells()
                self.textToScreenbacktrack(str(i), spos, window , False)
                pygame.display.update()
                pygame.time.delay(250)

                if self.solve_gui(self.window):
                    return True
                self.grid[row][col] = 0
                self.textToScreenbacktrack(str(0), spos, window , True)
                pygame.display.update()
                pygame.time.delay(250)

        return False

    def find_empty(self , bo):
        for i in range(9):
            for j in range(9):
                if bo[i][j] == 0:
                    return [i, j]  # row, col

        return None
    def textToScreenbacktrack(self, text, spos, window ,bt):
        font = self.font.render(text, False, AUTOFILL)
        font2 = self.font.render("    " , False , WHITE , WHITE)
        x = spos[0] * cellsize -5
        y = spos[1] * cellsize -5
        fontWidth = pos[0] +  x
        fontHeight = pos[1] + y
        fontWi = font.get_width() + font.get_height()
        if not bt:
            window.blit(font, ( fontHeight , fontWidth + fontWi ))
        else:
            window.blit( font2 , ( fontHeight , fontWidth + fontWi ))