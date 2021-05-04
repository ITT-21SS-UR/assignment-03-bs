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
    black = QtGui.QColor(0, 0, 0)
    white = QtGui.QColor(255, 255, 255)
    width = 1200
    height = 800
    minRectWidth = 40
    maxRectWidth = 200
    rectAppeared = False
    isActive = True
    hasStarted = False

    def __init__(self, isDarkmode):
        super().__init__()
        self.isDarkmode = isDarkmode
        self.initUI()
        self.timer = QtCore.QTimer()
        self.counter = 0
        self.timerStarted = False
        #self.color = self.white

    def showRect(self):
        print("timer")
        self.update()
        self.timerStarted = False

    def initUI(self):
        # set the text property of the widget we are inheriting
        self.text = "Please press 'space' if a new rectangle appears"
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowTitle('ClickRecorder')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        if self.isDarkmode:
            self.setStyleSheet('background-color: black')
        else:
            self.setStyleSheet('background-color: white')
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            if self.timerStarted:
                #self.update()
                print("self.timerstartet is true")
            else: 
                self.__showRectOrText()

    def start(self, event):
        print("event start")
        print(self.timer.isActive())
        self.update()


    def paintEvent(self, event):
        if not self.timerStarted:
            if not self.rectAppeared:
                qp = QtGui.QPainter()
                qp.begin(self)
                self.drawRect(event, qp)
                qp.end()
            else:
                qp = QtGui.QPainter()
                qp.begin(self)
                self.drawText(event, qp)
                qp.end()
        else:
            print("blackscreen")

    def drawText(self, event, qp):
        print("draw text")
        self.rectAppeared = False
        if self.isDarkmode:
            qp.setPen(self.white)
        else:
            qp.setPen(self.black)
        qp.setFont(QtGui.QFont('Decorative', 32))
        if self.counter > 0:
            self.text = f'Press "Space" to start (Round {str(self.counter)})'
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRect(self, event, qp):
        print("draw rect")
        rect = self.__getRandomRect()
        if self.isDarkmode:
            qp.setBrush(self.white)
        else:
            qp.setBrush(self.black)
        qp.drawRect(rect)
        self.rectAppeared = True

    def __getRandomRect(self):
        xPos = random.randint(0, self.width - self.maxRectWidth)
        yPos = random.randint(0, self.height - self.maxRectWidth)
        height = random.randint(self.minRectWidth, self.maxRectWidth)
        return QtCore.QRect(xPos, yPos, height, height)

    def __showRectOrText(self):
        if not self.rectAppeared:
            print("start timer")
            self.timerStarted = True
            self.update()
            self.timer.singleShot(random.randint(2,5)*1000, lambda: self.showRect())
        else:
            # catch reation time here
            self.counter += 1
            print("space pressed to catch reaction")
            self.update()



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
