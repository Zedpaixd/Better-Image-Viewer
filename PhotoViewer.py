from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
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
        # pass

    def displayPicture(self, pixmap=None):
        self.zoom = 0
        if pixmap:# and not pixmap.isNull():
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