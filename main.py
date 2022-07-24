from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtCore import *
import os


class GUI(QMainWindow):
    def __init__(self):

        super(GUI, self).__init__()
        loadUi("ui.ui", self)

        try:
            self.current_file = "default.png"
            self.pixmap = QPixmap(self.current_file)
            self.pixmap = self.pixmap.scaled(self.width(), self.height())
            self.label.setPixmap(self.pixmap)
        except:
            pass

        self.label.setMinimumSize(1, 1)

        #self.file_list = None
        #self.file_counter = None
        self.file_list = [os.getcwd() + "/" + file for file in os.listdir(os.getcwd())
                          if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]
        self.file_counter = len(self.file_list) - \
            1 if len(self.file_list) > 0 else None

        self.actionOpen_Image.triggered.connect(self.openImg)
        self.actionOpen_Folder.triggered.connect(self.openFolder)
        self.pushButton.clicked.connect(self.next_image)
        self.pushButton_2.clicked.connect(self.prev_image)
        self.pushButton_3.clicked.connect(self.on_zoom_out)
        self.pushButton_4.clicked.connect(self.on_zoom_in)

        self.scale = 1

        self.next_image()

        self.show()

    def displayImage(self, image):
        self.pixmap = QPixmap(image)
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(self.pixmap)

    def resizeEvent(self, event):
        try:
            self.pixmap = QPixmap(self.current_file)
        except:
            self.pixmap = QPixmap("default.png")
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())

    def openImg(self):
        output1, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Image Files (*.png, *.jpeg, *.jpg)")

        if output1 != "":
            self.current_file = output1
            self.displayImage(self.current_file)
            self.file_list = [os.path.dirname(os.path.realpath(output1)) + "/" + file for file in os.listdir(os.path.dirname
                (os.path.realpath(output1))) if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]

    def openFolder(self):
        directory = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        self.file_list = [directory + "/" + file for file in os.listdir(directory) if file.endswith(".png") or
                          file.endswith(".jpg") or
                          file.endswith("jpeg")]
        self.file_counter = 0
        self.current_file = self.file_list[self.file_counter]
        self.displayImage(self.current_file)

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
        self.scale *= 1.3
        self.scale(self.scale,1)
        #self.resize_image()

    def on_zoom_out(self, event):
        #self.scale /= 1.3
        #self.resize_image()
        x = self.label.x()
        y = self.label.y()
        self.label.move(x+5,y)

    def wheelEvent(self, event: QWheelEvent):
        self.scale = self.scale*1.3 if event.angleDelta().y() > 0 else self.scale/1.3
        self.resize_image()

    def resize_image(self):
        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.label.setPixmap(scaled_pixmap)


def main():
    app = QApplication([])
    window = GUI()
    app.exec_()


if __name__ == "__main__":
    main()