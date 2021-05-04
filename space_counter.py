#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets, QtCore
import random
import time


class SpaceRecorder(QtWidgets.QWidget):
    """ Counts how often the 'space' key is pressed and displays the count.

    Every time the 'space' key is pressed, a visual indicator is toggled, too.
    """
    def __init__(self, isDarkmode):
        super().__init__()
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

    def showRect(self):
        print("timer started")
        self.update()
        self.timerStarted = False

    def initUI(self):
        # set the text property of the widget we are inheriting
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowTitle('Darkmode vs Lightmode')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.__setBackgroundColor()
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            if self.round <= 4:
                if not self.timerStarted:
                    self.__showRectOrText()

    def paintEvent(self, event):
        if not self.timerStarted:
            self.__paintRectOrText(event)

    def drawText(self, event, qp):
        print("draw text")
        self.rectAppeared = False
        qp.setPen(self.color)
        qp.setFont(QtGui.QFont('Decorative', 32))
        if self.round > 0:
            self.text = f'Press "Space" to start round {str(self.round)}'
        if self.round == 4:
            self.text = "You finished the first test. Now press space only if a RECTANGLE appears"
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRect(self, event, qp):
        print("draw rect")
        rect = self.__getRandomRect()
        qp.setBrush(self.color)
        qp.drawRect(rect)

    def __getRandomRect(self):
        xPos = random.randint(0, self.width - self.maxRectWidth)
        yPos = random.randint(0, self.height - self.maxRectWidth)
        height = random.randint(self.minRectWidth, self.maxRectWidth)
        return QtCore.QRect(xPos, yPos, height, height)

    def __setColorScheme(self):
        if self.round == 2:
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


    def __showRectOrText(self):
        if not self.rectAppeared:
            print("start timer")
            self.timerStarted = True
            self.update()
            self.timer.singleShot(random.randint(
                1, 6)*1000, lambda: self.showRect())
        else:
            # catch reation time here
            reactionTime = time.time() - self.startTime
            print(reactionTime)
            self.__setColorScheme()
            self.round += 1
            self.update()

    def __paintRectOrText(self, event):
        if not self.rectAppeared:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawRect(event, qp)
            qp.end()
            self.rectAppeared = True
            self.startTime = time.time()
        else:
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawText(event, qp)
            qp.end()


def main():
    isDarkmode = False
    if len(sys.argv) == 2:
        if sys.argv[1] in ('True', 'False'):
            if sys.argv[1] == 'True':
                isDarkmode = True
        else:
            print("Argument has to be 'True' or 'False'")
            sys.exit()
    else:
        print("Set second argument to 'True' to start with dark mode or 'False' to start with light mode")
        sys.exit()
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    space = SpaceRecorder(isDarkmode)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
