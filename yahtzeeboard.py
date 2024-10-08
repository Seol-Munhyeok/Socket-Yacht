from tkinter import *
from tkinter import font
import tkinter.messagebox
from player import *
from dice import *
from configuration import *
from network import Network
import threading
import queue

# 이 클래스는 실제로 게임 창을 띄우는데 사용됩니다.
n = Network()  # 각 클라이언트의 Network 객체 생성


class YahtzeeBoard:
    # 각 카테고리에 해당하는 인덱스를 나타내는 상수
    UPPERTOTAL = 6
    UPPERBONUS = 7
    LOWERTOTAL = 15
    TOTAL = 16
    dice = []  # dice 객체 리스트
    diceButtons = []  # diceButton 리스트
    fields = []  # 각 플레이어 점수판 2차원 리스트
    # 열은 플레이어의 수, 행은 각 카테고리 13행 + upperScore + upperBouns + LowerScore + Total
    players = [Player('Alice'), Player('Bob')]  # player 객체 리스트
    numPlayers = 0
    player = 0  # 플레이어 순서 제어
    round = 0  # 13 라운드를 제어
    roll = 0  # 각 라운드 마다 3번 roll을 할 수 있음. 이를 제어.

    def __init__(self):
        self.initPlayers()
        # 백그라운드 스레드에서 메인 스레드로 데이터를 전달하기 위한 큐
        self.data_queue = queue.Queue()

    def initPlayers(self):
        """ player window를 생성하고 """
        self.pwindow = Tk()
        self.Tempfont = font.Font(size=16, weight='bold', family='Consolas')
        Button(self.pwindow, text="설정 완료!", font=self.Tempfont, command=self.connectToServer).grid(row=11, column=0)
        self.pwindow.mainloop()

    def connectToServer(self):
        """ 플레이어 설정 완료 버튼 누르면 실행되는 함수 """
        # 네트워크 객체 생성 후 서버와 연결
        global n
        n.connect()
        self.numPlayers = 2
        self.pwindow.destroy()
        self.initInterface()  # Yacht 보드판 생성

    def initInterface(self):
        """ Yacht 보드 윈도우 생성 """
        self.window = Tk("Yacht Dice Online!")
        self.window.geometry("1000x800")
        self.Tempfont = font.Font(size=16, weight='bold', family='Consolas')

        # dice 객체 5개 생성
        for i in range(5):
            self.dice.append(Dice())

        self.rollDice = Button(self.window, text="Roll Dice", font=self.Tempfont, command=self.rollDiceListener)
        self.rollDice.grid(row=0, column=0)

        # 상대방의 점수를 가져오는 버튼 생성
        Button(self.window, text='점수 가져오기', font=self.Tempfont, command=self.startThread2).grid(row=6, column=0)

        # Dice 버튼 5개 생성
        for i in range(5):
            # 각 dice 버튼에 대한 이벤트를 diceListener와 연결한다.
            self.diceButtons.append(Button(self.window, text="?", font=self.Tempfont, width=8,
                                           command=lambda row=i: self.diceListener(row)))
            self.diceButtons[i].grid(row=i + 1, column=0)

        for i in range(self.TOTAL + 2):  # i행의 점수를 나타냄
            Label(self.window, text=Configuration.configs[i], font=self.Tempfont).grid(row=i, column=1)
            for j in range(self.numPlayers):  # ME 플레이어만 버튼을 누를 수 있음.
                if i == 0:  # 플레이어 이름 표시
                    Label(self.window, text=self.players[j].toString(), font=self.Tempfont).grid(row=i, column=2 + j)
                else:
                    if j == 0:  # 각 행마다 한 번씩 리스트 추가
                        self.fields.append(list())
                    # i-1행에 플레이어 개수 만큼 버튼 추가하고, 이벤트 Listener를 설정
                    self.fields[i - 1].append(Button(self.window, text="", font=self.Tempfont, width=8,
                                                     command=lambda row=i - 1: self.startThread(row)))
                    self.fields[i - 1][j].grid(row=i, column=2 + j)

                    # 입력할 수 없는 버튼을 disable 시킴
                    if (j != self.player or (i - 1) == self.UPPERTOTAL or (i - 1) == self.UPPERBONUS
                            or (i - 1) == self.LOWERTOTAL or (i - 1) == self.TOTAL):
                        self.fields[i - 1][j]['state'] = 'disabled'
                        self.fields[i - 1][j]['bg'] = 'light gray'
        # 상태 메시지 출력
        self.bottomLabel = Label(self.window, text=self.players[self.player].toString() +
                                                   " 차례: Roll Dice 버튼을 누르세요", width=40, font=self.Tempfont)
        self.bottomLabel.grid(row=self.TOTAL + 2, column=0)
        self.window.mainloop()

    def rollDiceListener(self):
        for i in range(5):
            # keep하기로 한 주사위 눈을 disabled로 변경하고 다시 주사위를 굴힌다.
            if self.diceButtons[i]['state'] != 'disabled':
                self.dice[i].rollDie()
                self.diceButtons[i].configure(text=str(self.dice[i].getRoll()))
        self.undo()

        # 주사위는 최대 3번까지 다시 굴릴 수 있다.
        if self.roll == 0 or self.roll == 1:
            self.roll += 1
            self.rollDice.configure(text="Roll Again")
            self.bottomLabel.configure(text="Reroll or 카테고리 선택")

        # 최대 횟수 까지 굴린 경우, 카테고리를 선택해야한다.
        elif self.roll == 2:
            self.bottomLabel.configure(text="카테고리를 선택하세요")
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'
            # 주사위를 더 이상 선택할 수 없게한다.
            for i in range(5):
                self.diceButtons[i]["state"] = "disabled"
                self.diceButtons[i]["bg"] = "light gray"

    def undo(self):
        for i in range(5):
            self.diceButtons[i]["state"] = "normal"
            self.diceButtons[i]["bg"] = "white"

    def nextTurn(self):
        for i in range(5):
            self.diceButtons[i]["text"] = "?"
        self.roll = 0
        self.rollDice["state"] = "normal"
        self.rollDice["bg"] = "white"
        self.undo()
        self.player = (self.player + 1) % self.numPlayers
        self.bottomLabel.configure(text=self.players[self.player].toString() + "차례: Roll Dice 버튼을 누르세요.")

        for i in range(self.TOTAL + 1):
            for j in range(self.numPlayers):
                if j != self.player or i == self.UPPERTOTAL or i == self.UPPERBONUS\
                        or i == self.LOWERTOTAL or i == self.TOTAL:
                    self.fields[i][j]["state"] = "disabled"
                    self.fields[i][j]["bg"] = "light gray"
                else:
                    self.fields[i][j]["state"] = "normal"
                    self.fields[i][j]["bg"] = "white"
        for i in range(6):
            if self.players[self.player].getUsed(i):
                self.fields[i][self.player]["state"] = "disabled"
                self.fields[i][self.player]["bg"] = "light gray"
        for i in range(8, 15):
            if self.players[self.player].getUsed(i - 2):
                self.fields[i][self.player]["state"] = "disabled"
                self.fields[i][self.player]["bg"] = "light gray"
        # 라운드 수 체크
        if self.player == 0:
            self.round += 1
        # 라운드 종료 후 점수 계산
        if self.round == 13:
            tmp = 0
            winner = 0
            for i in range(self.numPlayers):
                if tmp < self.players[i].getTotalScore() + self.players[i].bonus:
                    tmp = self.players[i].getTotalScore() + self.players[i].bonus
                    winner = i
            tkinter.messagebox.showinfo("결과", "승자는 " + self.players[winner].toString() + " 입니다.\n\t" + str(tmp) + "점")

    def diceListener(self, row):
        """ keep할 주사위를 선택할 때 사용, 선택한 주사위의 버튼을 비활성화 한다. """
        if self.roll >= 1:
            self.diceButtons[row]['state'] = 'disabled'
            self.diceButtons[row]['bg'] = 'light gray'

    def calculateSpecialScore(self):
        # UPPER category가 전부 사용되었으면, UpperScore, UpperBonus 계산
        if self.players[self.player].allUpperUsed():
            self.fields[self.UPPERTOTAL][self.player].configure(text=str(self.players[self.player].getUpperScore()))
            if self.players[self.player].getUpperScore() > 63:
                self.fields[self.UPPERBONUS][self.player].configure(text="35")
            else:
                self.fields[self.UPPERBONUS][self.player].configure(text="0")

        # LOWER category가 전부 사용되었으면, LowerScore 계산
        if self.players[self.player].allLowerUsed():
            self.fields[self.LOWERTOTAL][self.player].configure(
                text=str(self.players[self.player].getLowerScore()))

        # 모든 category가 전부 사용되었으면 Total 계산
        if self.players[self.player].allUpperUsed() and self.players[self.player].allLowerUsed():
            if self.players[self.player].getUpperScore() > 63:
                self.fields[self.TOTAL][self.player].configure(text=str(self.players[self.player].getUpperScore()
                                                                        + self.players[self.player].getLowerScore()
                                                                        + 35))
            else:
                self.fields[self.TOTAL][self.player].configure(text=str(self.players[self.player].getUpperScore() +
                                                                        self.players[self.player].getLowerScore()))

    def receiveOpponentScore(self):
        # 상대방의 점수 업데이트
        global n
        opponent_data = n.receive()
        opponent_data = opponent_data.split(',')
        opponent_score = opponent_data[0]
        opponent_index = opponent_data[1]  # index는 족보를 순서대로 나열했을 때의 인덱스를 의미
        print(opponent_score, opponent_index)

        self.players[self.player].setScore(int(opponent_score), int(opponent_index))
        self.players[self.player].setAtUsed(int(opponent_index))
        # GUI 상에는 인덱스 대신 행 번호로 접근하므로, 하위 카테고리는 행 번호로 조정한다.
        if int(opponent_index) >= 6:
            self.fields[int(opponent_index) + 2][self.player].configure(text=str(opponent_score))
        else:
            self.fields[int(opponent_index)][self.player].configure(text=str(opponent_score))
        self.calculateSpecialScore()
        self.nextTurn()

    def categoryListener(self, row):
        """ 계산한 점수를 각 카테고리에 맞게 표시한다. """
        global n
        if self.roll >= 1:
            score = Configuration.score(row, self.dice)  # 점수 계산
            index = row
            # UpperScore, UpperBonus 때문에 7보다 큰 인덱스는 2를 빼주어야 함.
            if row > 7:
                index = row - 2

            # 선택한 카테고리 점수 적고 disable 시킴
            self.players[self.player].setScore(score, index)
            self.players[self.player].setAtUsed(index)
            self.fields[row][self.player].configure(text=str(score))
            
            # 상대방에게 선택한 카테고리의 점수와 인덱스를 전송
            try:
                n.send(str(score) + ',' + str(index))
            except Exception as e:
                print(e)

            self.calculateSpecialScore()
            self.nextTurn()

    def startThread(self, row):
        thread = threading.Thread(target=self.categoryListener, args=(row,))
        thread.daemon = True
        thread.start()

    def startThread2(self):
        thread = threading.Thread(target=self.receiveOpponentScore, args=())
        thread.daemon = True
        thread.start()

Y = YahtzeeBoard()
