from UI import *

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window(sys.argv)
    window.setGeometry(300,100,600, 800)
    window.show()
    window.graphicsView.zoomIn()           # Fix for some weird
    window.graphicsView.zoomOut()          # issue caused by ???
    sys.exit(app.exec_())