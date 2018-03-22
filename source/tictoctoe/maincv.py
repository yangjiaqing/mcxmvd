import numpy as np
import cv2
import time
import tictactoe as tic

CARD_COLOR_UP = np.array([255,255,255],dtype="uint8")
CARD_COLOR_LOW = np.array([165,165,165],dtype="uint8")
FONTE = cv2.FONT_HERSHEY_SIMPLEX
global choose_user, player, computer,points,fields,line,column
KERNEL = np.ones((3,3),np.uint8)
choose_user = True
game = True
init = False
last_time = 0
points = []  # 16 points in chess board
fields = []  # 9 fields in chess board

def findBiggestContour(mask):
    temp_bigger = []
    img1, cont, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(cont) == 0:
        return False
    for cnt in cont:
        temp_bigger.append(cv2.contourArea(cnt))
    greatest = max(temp_bigger)
    index_big = temp_bigger.index(greatest)
    key = 0
    for cnt in cont:
        if key == index_big:
            return cnt
            break
        key += 1

def getField(coord, frame):
    crop_img = frame[int(coord[0]):int(coord[1]), int(coord[2]):int(coord[3])]
    return crop_img

def getContoursHSV(img):
    print("into getContoursHSV")
    cv2.imshow('img',img)
    hsvimg=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvimg, CARD_COLOR_LOW, CARD_COLOR_UP)
    cv2.imshow('mask',mask)
    if len(mask) > 0:
        print("len mask greater than 0")
        dilation = cv2.dilate(mask,KERNEL,iterations = 2)
        cnt = findBiggestContour(dilation)
        return cnt
    else:
        return False

def compareContourHSV(cnt):
    print("into compareContorHSV")
    if cnt is False:
        return False
    patternX = cv2.cvtColor(cv2.imread('X.png'), cv2.COLOR_BGR2GRAY)
    patternX = findBiggestContour(patternX)
    resX = cv2.matchShapes(patternX, cnt, 1, 0.0)
    patternO = cv2.cvtColor(cv2.imread('O.png'), cv2.COLOR_BGR2GRAY)
    patternO = findBiggestContour(patternO)
    resO = cv2.matchShapes(patternO, cnt, 1, 0.0)
    print("resX is %f  resO is %f" %(resX,resO))
    if resX < 0.9:
        return 1
    if resO < 0.9:
        return 2
    return 0

def getPlayerMove(points, frame):
    global choose_user, init, last_time,fields
    for fieldid in range(0,9):
        chess =tic.readPosition(fieldid)
        if chess == 1 or chess ==2:  #already have chess in gameboard, pass
             print("position %d have chess %d,pass" %(fieldid,chess))
             continue
        print("try to find chess in %d" %fieldid)
        field=fields[fieldid]
        cropped = getField(field, frame)  #cell image of 9 fields
        cnt = getContoursHSV(cropped)
        value = compareContourHSV(cnt)
        print("found chess value %d in field%d" %(value,fieldid))
        if value == 1 or value == 2:
            tic.writePosition(fieldid,1)
            return value
    return False

def chessFieldInit():
    global fields,points,column,line
    x,y,h,w=30,30,480,480
    column = int(w/3)
    line = int(h/3)
    for num_column in range(0,4):
        for num_line in range(0,4):
            points.append((int((num_line*line)+x),int((num_column*column)+y)))
    for number in range(0, 11):
        if number != 3 and number != 7:
            #        upperleft y   ,    lowerright y ,      upperleft x,     lowerright x
            field = [points[number][1], points[number+5][1], points[number][0],points[number+5][0]]
            fields.append(field)

def drawChessInField(frame,fieldid,playerid):
#   put text in the middle of field
    global fields,line,column
    if playerid==1:
        text = "X"
    elif playerid ==2:
        text = "O"
    else:
        text =""
    field=fields[fieldid]
    textbig=3
    textfat=5
    coord=(field[2]+int(line/2)-textbig*10,field[0]+int(column/2)+textbig*10)
    cv2.putText(frame, text,coord, FONTE, textbig,(0,0,255),textfat,cv2.LINE_AA)

def drawChessBoard(frame):
    global fields
    for field in fields:
        cv2.circle(frame, (int(field[2]), int(field[0])), 1, (0,255,255), -1)     #draw 9 circle in chess board on field upperleft corner
        cv2.rectangle(frame,(int(field[2]), int(field[0])),(int(field[3]), int(field[1])),(0,255,0),2)

def drawChessInBoard(frame):
    for fieldid in range(0,9):
        drawChessInField(frame,fieldid,tic.readPosition(fieldid))

def screenprint(frame,disptext):
      hW,wW = frame.shape[0:2]
      cv2.line(frame,(0,hW-25),(wW,hW-25),(35,35,155),25)
      cv2.putText(frame, disptext,(150, hW-20), FONTE, 0.7,(0,255,0),2,cv2.LINE_AA)

def matchshapeslearn():
    patternX = cv2.cvtColor(cv2.imread('X.png'), cv2.COLOR_BGR2GRAY)
    patternX = findBiggestContour(patternX)
    patternO = cv2.cvtColor(cv2.imread('O.png'), cv2.COLOR_BGR2GRAY)
    patternO = findBiggestContour(patternO)
    resXX = cv2.matchShapes(patternX, patternX, 1, 0.0)
    resXO = cv2.matchShapes(patternX, patternO, 1, 0.0)
    resOO = cv2.matchShapes(patternO, patternO, 1, 0.0)
    print(resXX,resXO,resOO)

#Main start from There

write_comp = False
cap = cv2.VideoCapture(0) #capture from 1st webcam
chessFieldInit()
tic.gameinit()
key = 0
win = False
winner = 4
print("Start tic tac toe, enjoy...............................")
tic.displayboard()
while(game):
    ret, frame = cap.read()
    drawChessBoard(frame)
    drawChessInBoard(frame)
    print("waiting for player move.................................")
    if win :
        if winner==3:
            screenprint(frame,'No body win')
        elif winner==1:
            screenprint(frame,'You win !')
        elif winner==2:
            screenprint(frame,'Computer Win !')
        else:
            screenprint(frame,'Please play')
    result=False
    if (win==False):  #if win ,just show current board, no more move will be get
        result = getPlayerMove(fields, frame)
    if result != False:  #There is a player move
        tic.displayboard()
        win=tic.verifyWinner(1) #player always be 1
        if win:
            winner=1
        tic.inteligence(2)
        print("computer played")
        tic.displayboard()
        win = tic.verifyWinner(2)
        if win:
            winner=2
        if win == "EMPATE":
            winner=3
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Exemplo',frame)
cap.release()
cv2.destroyAllWindows()
