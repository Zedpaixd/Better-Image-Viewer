from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)

        self.zoom = 0
        self.has_pic = True
        self.gvScene = QtWidgets.QGraphicsScene(self)
        self.gvPhoto = QtWidgets.QGraphicsPixmapItem()
        self.gvScene.addItem(self.gvPhoto)

        self.setScene(self.gvScene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        

    def noPictureDisplayed(self):
        return self.has_pic

    def fitInView(self, scale=True):
        imageSquare = QtCore.QRectF(self.gvPhoto.pixmap().rect())
        if not imageSquare.isNull():
            self.setSceneRect(imageSquare)
            if not self.noPictureDisplayed():
                viewedSquare = self.viewport().rect()
                imageScene = self.transform().mapRect(imageSquare)
                scaleFactor = min(viewedSquare.width() / imageScene.width(),
                             viewedSquare.height() / imageScene.height())
                self.scale(scaleFactor, scaleFactor)
            self.zoom = 0

    def displayPicture(self, pixmap=None):
        self.zoom = 0
        if pixmap:
            self.has_pic = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.gvPhoto.setPixmap(pixmap)
        else:
            self.has_pic = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.gvPhoto.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if not self.noPictureDisplayed():
            if event.angleDelta().y() > 0:
                factor = 1.15
                self.zoom += 1
            else:
                factor = 0.9
                self.zoom -= 1
            if self.zoom > 0:
                self.scale(factor, factor)
            elif self.zoom == 0:
                self.fitInView()
            else:
                self.zoom = 0

    def zoomIn(self):
        factor = 1.15
        self.zoom += 1
        if self.zoom > 0:
            self.scale(factor, factor)
        elif self.zoom == 0:
            self.fitInView()
        else:
            self.zoom = 0

    def zoomOut(self):
        factor = 0.9
        self.zoom -= 1
        if self.zoom > 0:
            self.scale(factor, factor)
        elif self.zoom == 0:
            self.fitInView()
        else:
            self.zoom = 0


    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self.gvPhoto.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self.gvPhoto.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowIcon(QtGui.QIcon("./assets/appIcon.png"))
        self.setWindowTitle("Simplistic Image Viewer")

        self.graphicsView = PhotoViewer(self)
        self.nextButton = QtWidgets.QToolButton(self)
        self.nextButton.setText("Next")
        self.nextButton.clicked.connect(self.next_image)

        self.prevButton = QtWidgets.QToolButton(self)
        self.prevButton.setText("Prev")
        self.prevButton.clicked.connect(self.prev_image)

        self.zoomOutButton = QtWidgets.QToolButton(self)
        # self.zoomOutButton.setText("Zoom out")
        self.zoomOutButton.clicked.connect(self.on_zoom_out)
        self.zoomOutButton.setIcon(QtGui.QIcon("./assets/zoom_out.png"))

        self.zoomInButton = QtWidgets.QToolButton(self)
        # self.zoomInButton.setText("Zoom in")
        self.zoomInButton.clicked.connect(self.on_zoom_in)
        self.zoomInButton.setIcon(QtGui.QIcon("./assets/zoom_in.png"))

        self.openImageButton = QtWidgets.QToolButton(self)
        self.openImageButton.setText("Open Image")
        self.openImageButton.clicked.connect(self.openImg)

        self.openFolderButton = QtWidgets.QToolButton(self)
        self.openFolderButton.setText("Open Folder")
        self.openFolderButton.clicked.connect(self.openFolder)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.graphicsView)
        VBlayout.setContentsMargins(0,0,0,5)

        HBlayoutMain = QtWidgets.QHBoxLayout(self)
        HBlayoutMain.setContentsMargins(0,0,0,0)

        HBlayout = QtWidgets.QGridLayout()
        HBlayout.addWidget(self.zoomOutButton,0,0)
        HBlayout.addWidget(self.zoomInButton,0,1)

        HBlayout2 = QtWidgets.QGridLayout()
        HBlayout2.addWidget(self.prevButton,0,0)
        HBlayout2.addWidget(self.nextButton,0,1)

        HBlayout3 = QtWidgets.QGridLayout()
        HBlayout3.addWidget(self.openImageButton, 0, 0)
        HBlayout3.addWidget(self.openFolderButton, 0, 1)

        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout2.setAlignment(QtCore.Qt.AlignCenter)
        HBlayout3.setAlignment(QtCore.Qt.AlignRight)

        HBlayoutMain.addLayout(HBlayout)
        HBlayoutMain.addLayout(HBlayout2)
        HBlayoutMain.addLayout(HBlayout3)
        VBlayout.addLayout(HBlayoutMain)

        self.current_file = None
        self.file_list = [os.getcwd() + "/" + file for file in os.listdir(os.getcwd())
                          if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]
        self.file_counter = len(self.file_list) -1 if len(self.file_list) > 0 else None

        self.next_image()
        
        

    def displayImage(self, image):
        self.pixmap = QtGui.QPixmap(image)
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.graphicsView.displayPicture(QtGui.QPixmap(self.current_file))

    def resizeEvent(self, event):
        self.graphicsView.fitInView()

    def openImg(self):
        output1, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "Image Files (*.png, *.jpeg, *.jpg)")

        if output1 != "":
            self.current_file = output1
            self.displayImage(self.current_file)
            self.file_list = [os.path.dirname(os.path.realpath(output1)) + "/" 
                            + file for file in os.listdir(os.path.dirname(os.path.realpath(output1)))
                                    if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]

    def openFolder(self):
        try:
            directory = str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory"))
            self.file_list = [directory + "/" + file for file in os.listdir(directory) if file.endswith(".png") or
                            file.endswith(".jpg") or
                            file.endswith("jpeg")]
            self.file_counter = 0
            self.current_file = self.file_list[self.file_counter]
            self.displayImage(self.current_file)
        except:
            directory = ""
            self.file_list = []
            self.file_counter = None
            self.pixmap = QtGui.QPixmap()
            self.graphicsView.displayPicture(self.pixmap)

    def next_image(self):
        if self.file_counter is not None:
            self.file_counter += 1
            self.file_counter = self.file_counter % len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.displayImage(self.current_file)

    def prev_image(self):
        if self.file_counter is not None:
            self.file_counter += -1
            self.file_counter = self.file_counter % len(self.file_list)
            self.current_file = self.file_list[self.file_counter]
            self.displayImage(self.current_file)

    def on_zoom_in(self, event):
        self.graphicsView.zoomIn()

    def on_zoom_out(self, event):
        self.graphicsView.zoomOut()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(300,100,600, 800)
    window.show()
    window.graphicsView.zoomIn()           # Fix for some weird
    window.graphicsView.zoomOut()          # issue caused by ???
    sys.exit(app.exec_())
