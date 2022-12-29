import pygame,sys
import datetime
import json
from dokusan import generators
import numpy as np
from math import inf 

pygame.init()

WIDTH,HEIGHT = 450,700
block = WIDTH/9

DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sudoku")

img = pygame.image.load("back.jpg")
img = pygame.transform.scale(img,(WIDTH,HEIGHT))

img2 = pygame.image.load("backscore.jpg")
img2 = pygame.transform.scale(img2,(WIDTH,HEIGHT))


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BROWN = (207, 194, 157)
color_backg = WHITE

FPS = 60
fpsClock = pygame.time.Clock()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class Background():
    def __init__(self):
        pass
    def draw(self):
        pygame.draw.line(DISPLAYSURF,GREEN,(0,3*block),(9*block,3*block),4)
        pygame.draw.line(DISPLAYSURF,GREEN,(0,6*block),(9*block,6*block),4)
        pygame.draw.line(DISPLAYSURF,GREEN,(3*block,0),(3*block,9*block),4)
        pygame.draw.line(DISPLAYSURF,GREEN,(6*block,0),(6*block,9*block),4)

class InputBox():
    def __init__(self, x, y, text=''):
        self.rect = pygame.Rect(x, y, block, block)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.size = self.txt_surface.get_size()
    def handle_event(self,event,ls,const):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                a = self.rect.x /block
                b = self.rect.y /block   
                x = 9*b + a
                if x not in const:
                   self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    print(ls)
                    print(sett)
                    print(new)                    
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:      
                    if event.unicode in sett:    
                        self.text = event.unicode
                        a = self.rect.x /block
                        b = self.rect.y /block   
                        x = 9*b + a
                        ls[int(x)] = str(self.text)

                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                self.size = self.txt_surface.get_size()
    def draw(self):    
        DISPLAYSURF.blit(self.txt_surface,(self.rect.x + (block-self.size[0])/2,self.rect.y + (block-self.size[1])/2))
        pygame.draw.rect(DISPLAYSURF,self.color,self.rect,1)

now = datetime.datetime.now().timestamp()
class Clock():
    def __init__(self):
        self.ti = 0
    def tyn(self):
        now2 = datetime.datetime.now().timestamp()
        self.ti = int(now2 - now)
        hours = self.ti //3600
        mins = (self.ti //60)%60   
        secs = self.ti %60
        fon = pygame.font.SysFont("consolas",50)
        fon = fon.render("Time <{}:{}:{}>".format(hours,mins,secs),True,RED)
        font_size = fon.get_size()        
        DISPLAYSURF.blit(fon,(15,550+(50-font_size[1])/2))
 

sett = set()
for i in range(1,10):
    sett.add(str(i))

set33 = set()
lsm = [set33 for i in range(9)]
ls_row = [set33 for i in range(81)]
ls_column = [set33 for i in range(81)]

chls = [set33 for i in range(81)]

class Board():
    def __init__(self,arr):
        
        self.ls = []
        
        for i in range(81):
            self.ls.append(arr[i])

        for i in range(81):
            if self.ls[i] == "0":
               self.ls[i] = ""
            
        self.const = []
        for a,b in enumerate(self.ls):
            if b != '':
                self.const.append(a) 
    def reset(self):
        for i in range(81):
            if i not in self.const:
                self.ls[i] = ""
  
                                                   
new = set()
new2 = set()
new3 = set()

class Check():
    def __init__(self):
        self.sc_row = [False,False,False,False,False,False,False,False,False]
        self.sc_column = [False,False,False,False,False,False,False,False,False]
        self.sc_33 = [False,False,False,False,False,False,False,False,False]
    
    def check(self,ls):
            for a in range(9):  
               m = 0 + 9*a
               n = 9 + 9*a  
               new.clear()
               for b in range(m,n):
                   s = str(ls[b])
                   new.add(s)
                   if new == sett:
                       self.sc_row[a] = True  
                   else:
                       self.sc_row[a] = False
            if all(self.sc_row):
                print("row")
                return True

    def check2(self,ls):
            for a in range(9):        
               new2.clear()
               for b in range(9):
                   s2 = str(ls[b*9+a])
                   new2.add(s2)
                   if new2 == sett:
                       self.sc_column[a] = True
                   else:
                       self.sc_column[a] = False
            if all(self.sc_column) : 
                print("column")
                return True
            
    def check3(self,ls):
        for d in range(3):

            for c in range(3):
                new3.clear()
                for a in range(3):
                    for b in range(3):
                        s3 = str(ls[b + a*9 + c*3 + d*27])
                        new3.add(s3)
                        if new3 == sett:
                            self.sc_33[c+3*d] = True
                        else:
                            self.sc_33[c+3*d] = False
        if all(self.sc_33) :
              print("3x3")
              return True

data = [[inf]*10 for i in range(3)]

try:
    with open("score.txt") as sco:
         data = json.load(sco)
except:
    print("No file score")  

def HighScore(data):
    global high,start
    
    def draw(data,text_level): 
        if text_level == "Easy":
            dt = data[0]
        elif text_level == "Medium":
            dt = data[1]
        else:
            dt = data[2]        
        box1 = []
        font1 = []
        for i in range(10): 
            hours = dt[i] //3600
            mins = (dt[i]//60)%60
            secs = dt[i]%60
            if dt[i] != inf:
                font1.append( pygame.font.SysFont("consolas",40).render("{}:{}:{}".format(hours,mins,secs),True,RED) )
                font_size1 = ( font1[i].get_size() )
            else:
                font1.append( pygame.font.SysFont("consolas",40).render("None",True,RED) )
                font_size1 = ( font1[i].get_size() )
            x = (-font_size1[0])/2
            y = (HEIGHT-font_size1[1])/2
            box1.append( pygame.Rect(300+x,85+40*i,font_size1[0],font_size1[1]) )
        
            DISPLAYSURF.blit(font1[i],(box1[i].x,box1[i].y))
           
    name_stt = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th"]
    box2 = []
    font2 = []
    
    for i in range(len(data[0])): 
        font2.append ( pygame.font.SysFont("consolas",40).render("{}:".format(name_stt[i]),True,RED) )
        font_size2 = ( font2[i].get_size() )
        x = (-font_size2[0])/2
        y = (HEIGHT-font_size2[1])/2
        box2.append( pygame.Rect(150+x,85+40*i,font_size2[0],font_size2[1]) )

    font_back = pygame.font.SysFont("consolas",50).render("Back",True,RED)
    font_size = font_back.get_size() 
    x = (WIDTH-font_size[0])/2
    y = (HEIGHT-font_size[1])/2
    box = pygame.Rect( x,550,font_size[0],font_size[1] )

    text_level = "Easy"
    

    while True:
        colorright = RED
        colorleft = RED
        for event in pygame.event.get():
                if event.type == pygame.QUIT:                   
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if box.collidepoint(event.pos):
                        high = False
                        start = True
                        return 
                    if box_right.collidepoint(event.pos):
                       if text_level == "Easy":
                          colorright = WHITE
                          text_level  = "Medium"  
                       elif text_level == "Medium":
                            colorright = WHITE
                            text_level  = "Hard" 
                       else:
                           colorright = WHITE
                           text_level = "Easy" 
                    if box_left.collidepoint(event.pos):
                       if text_level == "Easy":
                          colorleft = WHITE
                          text_level  = "Hard"  
                       elif text_level == "Medium":
                            colorleft = WHITE
                            text_level  = "Easy" 
                       else:
                           colorleft = WHITE
                           text_level = "Medium" 
                         
        font_lv = pygame.font.SysFont("consolas",50).render(text_level,True,RED)
        font_lv_size = font_lv.get_size() 
        x = (WIDTH-font_lv_size[0])/2
        y = (HEIGHT-font_lv_size[1])/2
        box3 = pygame.Rect( x,500,font_lv_size[0],font_lv_size[1] )

        font_right = pygame.font.SysFont("consolas",50).render(">>",True,colorright)
        font_right_size = font_right.get_size() 
        x = (WIDTH-font_right_size[0])/2
        y = (HEIGHT-font_right_size[1])/2
        box_right = pygame.Rect( x+120,500,font_right_size[0],font_right_size[1] )      
    
        font_left = pygame.font.SysFont("consolas",50).render("<<",True,colorleft)
        font_left_size = font_left.get_size() 
        x = (WIDTH-font_left_size[0])/2
        y = (HEIGHT-font_left_size[1])/2
        box_left = pygame.Rect( x-120,500,font_left_size[0],font_left_size[1] )   

        DISPLAYSURF.blit(img2,(0,0))
        DISPLAYSURF.blit(font_back,(box.x,box.y))
        DISPLAYSURF.blit(font_lv,(box3.x,box3.y))

        DISPLAYSURF.blit(font_right,(box_right.x,box_right.y))
        DISPLAYSURF.blit(font_left,(box_left.x,box_left.y))

        draw(data,text_level)        
        
        for i in range(len(data[0])):            
            DISPLAYSURF.blit(font2[i],(box2[i].x,box2[i].y))

        pygame.display.update()
        fpsClock.tick(FPS)
        
def GameStart():  
    global high,start,lev

    font = pygame.font.SysFont("consolas",50).render("Start",True,RED)
    font_size = font.get_size() 
    x = (WIDTH-font_size[0])/2
    y = (HEIGHT-font_size[1])/2
    box1 = pygame.Rect( x,y,font_size[0],font_size[1] )

    font2 = pygame.font.SysFont("consolas",45).render("HighScore",True,RED)
    font_size2 = font2.get_size() 
    x = (WIDTH-font_size2[0])/2
    y = (HEIGHT-font_size2[1])/2
    box2 = pygame.Rect( x,y+50,font_size2[0],font_size2[1] )

    font3 = pygame.font.SysFont("consolas",40).render("Quit",True,RED)
    font_size3 = font3.get_size() 
    x = (WIDTH-font_size3[0])/2
    y = (HEIGHT-font_size3[1])/2
    box3 = pygame.Rect( x,y+100,font_size3[0],font_size3[1] )


    while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if box1.collidepoint(event.pos):
                    lev = True
                    start = False                   
                    return 
                if box2.collidepoint(event.pos):
                    start = False
                    high = True
                    return 
                if box3.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
         DISPLAYSURF.blit(img,(0,0))

         DISPLAYSURF.blit(font,(box1.x,box1.y))
         DISPLAYSURF.blit(font2,(box2.x,box2.y))
         DISPLAYSURF.blit(font3,(box3.x,box3.y))

         pygame.display.update()
         fpsClock.tick(FPS)

def Level():
    global start,play,lev,level

    font = pygame.font.SysFont("consolas",50).render("Easy",True,RED)
    font_size = font.get_size() 
    x = (WIDTH-font_size[0])/2
    y = (HEIGHT-font_size[1])/2
    box1 = pygame.Rect( x,y,font_size[0],font_size[1] )

    font2 = pygame.font.SysFont("consolas",45).render("Medium",True,RED)
    font_size2 = font2.get_size() 
    x = (WIDTH-font_size2[0])/2
    y = (HEIGHT-font_size2[1])/2
    box2 = pygame.Rect( x,y+50,font_size2[0],font_size2[1] )

    font3 = pygame.font.SysFont("consolas",40).render("Hard",True,RED)
    font_size3 = font3.get_size() 
    x = (WIDTH-font_size3[0])/2
    y = (HEIGHT-font_size3[1])/2
    box3 = pygame.Rect( x,y+100,font_size3[0],font_size3[1] )

    while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if box1.collidepoint(event.pos):
                    level  = 50
                    play = True
                    lev = False
                    return 
                elif box2.collidepoint(event.pos):
                    level  = 100
                    play = True
                    lev = False
                    return 
                elif box3.collidepoint(event.pos):
                    level  = 150
                    play = True
                    lev = False
                    return 
                else:
                    start = True
                    lev = False
                    return 
        
         DISPLAYSURF.blit(img,(0,0))

         DISPLAYSURF.blit(font,(box1.x,box1.y))
         DISPLAYSURF.blit(font2,(box2.x,box2.y))
         DISPLAYSURF.blit(font3,(box3.x,box3.y))

         pygame.display.update()
         fpsClock.tick(FPS)

M = 9
def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j],end = " ")
        print()
def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
            
    for x in range(9):
        if grid[x][col] == num:
            return False
 
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True
 
def Suduko(grid, row, col):
 
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
     
        if solve(grid, row, col, num):
         
            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

def GamePlay(bg,ch,cl,bo,data):
    bg.__init__()
    ch.__init__()
    cl.__init__()
    
    global now,start,play,gameW,gameL,level,tool
    now = datetime.datetime.now().timestamp()  

    ib = []
    for i in range(81):
      a = (i%9)*block
      b = (i//9)*block 
      ib.append( InputBox(a,b,bo.ls[i]) )  

    fon = pygame.font.SysFont("consolas",50)
    fon = fon.render("~MENU~",True,RED)
    font_size = fon.get_size()  
    x = (WIDTH-font_size[0])/2
    y = 650+(50-font_size[1])/2
    box_menu = pygame.Rect(x,y,font_size[0],font_size[1])  
   
    ton = ""
    def tool(ls):
                    lsm = [[0]*9 for i in range(9)]
                    for i in range(81):
                        if ls[i] != "":
                             a = int(ls[i])
                             b = i//9
                             c = i%9
                             lsm[b][c] = a
                    grid = lsm              
                    Suduko(grid, 0, 0)
                    op =[]  
                    for listn in grid:
                         for i in listn:
                             op.append(str(i))             
                    return op
                   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if box_menu.collidepoint(event.pos): 
                    start = True
                    play = False
                    return    
            for i in ib:           
               i.handle_event(event,bo.ls,bo.const)   
            if event.type == pygame.KEYDOWN:   
               
                    ton += event.unicode
                    if len(ton) >6:
                        ton = ton[1:]
                    if ton == "maimeo":
                        bo.reset()
                        bo.ls = tool(bo.ls)
                 
                             
        DISPLAYSURF.fill(color_backg)

        for box in ib:
              box.draw()

        bg.draw()
        cl.tyn()
        DISPLAYSURF.blit(fon,(box_menu.x,box_menu.y)) 
      
        
        def draw(text_level):
            font_lv = pygame.font.SysFont("consolas",50).render("Level <{}>".format(text_level),True,RED)
            font_lv_size = font_lv.get_size() 
            x = (WIDTH-font_lv_size[0])/2
            y = (1250-font_lv_size[1])/2
            box_lv = pygame.Rect( 15,y,font_lv_size[0],font_lv_size[1] )
            DISPLAYSURF.blit(font_lv,(box_lv.x,box_lv.y))        

        if level == 50: 
            draw("Easy")
        elif level == 100: 
            draw("Medium")
        else: 
            draw("Hard")

        if ch.check(bo.ls) and ch.check2(bo.ls) and ch.check3(bo.ls): 
           with open("score.txt","w") as sco:
                 if level == 50:
                    if cl.ti < data[0][9]:
                        data[0].append( cl.ti)
                        data[0].sort()
                        data[0].pop(10)
                        json.dump(data,sco)
                 elif level == 100:
                     if cl.ti < data[1][9]:
                        data[1].append( cl.ti)
                        data[1].sort()
                        data[1].pop(10)
                        json.dump(data,sco)
                 else:
                     if cl.ti < data[2][9]:
                        data[2].append( cl.ti)
                        data[2].sort()
                        data[2].pop(10)
                        json.dump(data,sco)

           gameW = True
           play = False
           return 
        if cl.ti == inf:
           gameL = True
           play = False
           return 
        
        

        pygame.display.update()
        fpsClock.tick(FPS)

def GameEnd(cl,tex,bo,bg):
    t_over = cl.ti
    mins = t_over//60
    secs = t_over%60

    fon = pygame.font.SysFont("consolas",50)
    fon =  fon.render("Time: {}:{}".format(mins,secs),True,RED)
    fon_size = fon.get_size()  

    fon2 = pygame.font.SysFont("consolas",50) 
    fon2 = fon2.render(tex,True,RED)   
    fon2_size = fon2.get_size()

    fon3 = pygame.font.SysFont("consolas",50) 
    fon3 = fon3.render("\"Play again!\"",True,RED)   
    fon3_size = fon3.get_size()
    x = (WIDTH-fon3_size[0])/2
    y = 500+(50-fon3_size[1])/2
    box1 = pygame.Rect(x,y,fon3_size[0],fon3_size[1])

    ib = []
    for i in range(81):
      a = (i%9)*block
      b = (i//9)*block 
      ib.append( InputBox(a,b,bo.ls[i]) )  
    
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if box1.collidepoint(event.pos):
                         bo.reset()
                         return

        DISPLAYSURF.fill(color_backg)

        DISPLAYSURF.blit(fon, ((WIDTH-fon_size[0])/2,550+(50-fon_size[1])/2))
        DISPLAYSURF.blit(fon2,((WIDTH-fon2_size[0])/2,450+(50-fon2_size[1])/2))
        DISPLAYSURF.blit(fon3,(box1.x,box1.y))

        for box in ib:
             box.draw() 

        bg.draw()
         
        pygame.display.update()
        fpsClock.tick(FPS)

high,start,play,gameW,gameL,lev,tool = False,True,False,False,False,False,False
level = 0
def main():
    arr = np.array(list(str(generators.random_sudoku(avg_rank=0))))
    bg = Background()           
    ch = Check()    
    cl = Clock()
    global high,start,play,gameW,gameL,lev,level
    while True:        
        if lev:
           Level()
           arr = np.array(list(str(generators.random_sudoku(avg_rank=level))))

        bo = Board(arr)
        if start:
           GameStart()
           bo.reset()
        if high:
           HighScore(data)         
        if play:                        
             GamePlay(bg,ch,cl,bo,data)
             
        if gameW:     
               tex = "Victory"
               GameEnd(cl,tex,bo,bg)
               start = True
               gameW = False
        if gameL:   
               tex = "Run out of time"
               GameEnd(cl,tex,bo,bg) 
               start = True
               gameL = False

if __name__ == "__main__":
    main()