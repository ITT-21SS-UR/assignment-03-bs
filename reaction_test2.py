#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets, QtCore
import random
import time
import pandas as pd
from datetime import datetime

FIELDS = ["id", "condition", "mode", "run", "pressed_key",
          "pressed_correct_key", "reaction_time_in_sec", "time_waited_in_sec", "time_stamp"]


class SpaceRecorder(QtWidgets.QWidget):

    def __init__(self, isDarkmode, id):
        super().__init__()
        self.id = id
        self.black = QtGui.QColor(0, 0, 0)
        self.white = QtGui.QColor(255, 255, 255)
        self.width = 1200
        self.height = 800
        self.minRectWidth = 40
        self.maxRectWidth = 200
        self.rectAppeared = False
        self.isDarkmode = isDarkmode
        self.initUI()
        self.timer = QtCore.QTimer()
        self.round = 1
        self.timerStarted = False
        self.color = self.white if self.isDarkmode else self.black
        self.df = pd.DataFrame(columns=FIELDS)
        self.circleAppeared = False
        self.timeWaited = 0
        self.timeWaitedFalse = 0


    def showRect(self):
        self.update()
        self.timerStarted = False

    def initUI(self):
        # set the text property of the widget we are inheriting
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowTitle('Darkmode vs Lightmode Test 2')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.__setBackgroundColor()
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            if self.round <= 20:
                if not self.timerStarted:
                    self.__modeOne()

    def paintEvent(self, event):
        if not self.timerStarted:
            self.__paintRectOrText(event)

    def drawText(self, event, qp):
        if self.rectAppeared:
          self.rectAppeared = False
        elif self.circleAppeared:
          self.circleAppeared = False
        qp.setPen(self.color)
        qp.setFont(QtGui.QFont('Decorative', 32))
        if self.round == 1:
          self.text = "Press 'Space' to start. \nPress 'Space' only if a RECTANGLE appears"
        if self.round > 1:
            self.text = f'Press "Space" to start round {str(self.round)}'
        if self.round == 21:
            self.text = "You have finished the first test. \nThank you!"
            self.df = self.df.to_csv(
                f'/home/erik/assignments/assignment-03-bs/test2_{self.id}.csv', index=False)
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRect(self, event, qp):
      randNum = random.randint(0, 1)
      qp.setBrush(self.color)
      rect = self.__getRandomRect()
      if randNum == 0:
        qp.drawRect(rect)
        self.rectAppeared = True
      else:
        qp.drawEllipse(rect)
        self.circleAppeared = True
        self.timer.singleShot(3000, lambda: self.__drawAgain())


    def __getRandomRect(self):
        xPos = random.randint(0, self.width - self.maxRectWidth)
        yPos = random.randint(0, self.height - self.maxRectWidth)
        height = random.randint(self.minRectWidth, self.maxRectWidth)
        return QtCore.QRect(xPos, yPos, height, height)

    def __drawAgain(self):
        self.circleAppeared = False
        self.update()

    def __setColorScheme(self):
        if self.round == 10:
            self.__changeColorTheme()

    def __changeColorTheme(self):
        self.isDarkmode = not self.isDarkmode
        self.color = self.white if self.isDarkmode else self.black
        self.__setBackgroundColor()

    def __setBackgroundColor(self):
        if self.isDarkmode:
            self.setStyleSheet('background-color: black')
        else:
            self.setStyleSheet('background-color: white')

    def __modeOne(self):
        if not self.rectAppeared and not self.circleAppeared:
            self.timerStarted = True
            self.update()
            self.timeWaited = random.randint(1, 6)
            self.timer.singleShot(self.timeWaited*1000, lambda: self.showRect())
        else:
            # catch reation time here
            self.__addRow()
            self.__setColorScheme()
            self.round += 1
            self.update()

    def __paintRectOrText(self, event):
        if not self.rectAppeared and not self.circleAppeared:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawRect(event, qp)
            qp.end()
            self.startTime = time.time()
        else:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawText(event, qp)
            qp.end()

    def __addRow(self):
        condition = "dark" if self.isDarkmode else "light"
        reactionTime = time.time() - self.startTime
        timeStamp = datetime.now()
        run = self.round if self.round <= 10 else self.round-10
        d = {
            'id': self.id,
            'condition': condition,
            'mode': 2,
            'run': run,
            'pressed_key': 'space',
            'pressed_correct_key': True if self.rectAppeared else False,
            'reaction_time_in_sec': reactionTime,
            'time_waited_in_sec': self.timeWaited,
            'time_stamp': timeStamp
        }
        print(d)
        self.df = self.df.append(d, ignore_index=True)


def main():
    isDarkmode = False
    if len(sys.argv) == 3:
        if sys.argv[1] in ('True', 'False'):
            if sys.argv[1] == 'True':
                isDarkmode = True
        else:
            print("Argument has to be 'True' or 'False'")
            sys.exit()
    else:
        print("Set second argument to 'True' to start with dark mode or 'False' to start with light mode and third argument should be the participantID")
        sys.exit()
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    space = SpaceRecorder(isDarkmode, sys.argv[2])
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
