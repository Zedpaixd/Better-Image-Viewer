from PhotoViewer import *

class Window(QtWidgets.QWidget):
    def __init__(self, path=None):
        super(Window, self).__init__()

        self.setWindowIcon(QtGui.QIcon("./assets/appIcon.png"))
        self.setWindowTitle("Simplistic Windows Image Viewer")

        self.givenPath = None
        
        try:
            self.givenPath = path[1]
            rev = self.givenPath[::-1]
            self.givenPath=self.givenPath[:len(rev)-rev.index('\\')-1]

            print(self.givenPath)
            print(os.getcwd())
        except:
            pass

        # self.menuBar = QMenuBar()
        # self.setMenuBar(self.menuBar)
        # self.fileMenu = self.menuBar.addMenu("&File")
                                                                        #??????????????????????????????????????????????????????????
        # self.actionOpen_Image = QtGui.QAction('Open Image', self)
        # self.fileMenu.addAction(self.actionOpen_Image)
        # self.actionOpen_Image.triggered.connect(self.openImg)
                                                                        # seriously why does this not work
        # self.actionOpen_Folder = QtGui.QAction('Open Folder', self)
        # self.fileMenu.addAction(self.actionOpen_Folder)
        # self.actionOpen_Folder.triggered.connect(self.openFolder)

        self.graphicsView = PhotoViewer(self)

        self.setStyleSheet("background-color: white;")

        self.nextButton = QtWidgets.QToolButton(self)
        self.nextButton.setText("→")
        self.nextButton.clicked.connect(self.next_image)
        self.nextButton.setStyleSheet("border-radius: 5px; \
                                       border : 1px solid black; \
                                       width: 40px; \
                                       height: 15px; \
                                       font-size: 20px; \
                                       padding-top:-5px; \
                                       Text-align: center")

        self.prevButton = QtWidgets.QToolButton(self)
        self.prevButton.setText("←")
        self.prevButton.clicked.connect(self.prev_image)
        self.prevButton.setStyleSheet("border-radius: 5px; \
                                       border : 1px solid black; \
                                       width: 40px; \
                                       height: 15px; \
                                       font-size: 20px; \
                                       padding-top:-5px; \
                                       Text-align: center")

        self.zoomOutButton = QtWidgets.QToolButton(self)
        # self.zoomOutButton.setText("Zoom out")
        self.zoomOutButton.clicked.connect(self.on_zoom_out)
        self.zoomOutButton.setIcon(QtGui.QIcon("./assets/zoom_out.png"))
        self.zoomOutButton.setStyleSheet("margin-left:10px; \
                                          border-radius: 5px; \
                                          border : 1px solid black;")

        self.zoomInButton = QtWidgets.QToolButton(self)
        # self.zoomInButton.setText("Zoom in")
        self.zoomInButton.clicked.connect(self.on_zoom_in)
        self.zoomInButton.setIcon(QtGui.QIcon("./assets/zoom_in.png"))
        self.zoomInButton.setStyleSheet("margin-left:3px; \
                                         border-radius: 5px; \
                                         border : 1px solid black;")

        self.openImageButton = QtWidgets.QToolButton(self)
        self.openImageButton.setText("Open Image")
        self.openImageButton.clicked.connect(self.openImg)
        self.openImageButton.setStyleSheet("margin-right: 3px; \
                                            border-radius: 5px; \
                                            border : 1px solid black;")

        self.openFolderButton = QtWidgets.QToolButton(self)
        self.openFolderButton.setText("Open Folder")
        self.openFolderButton.clicked.connect(self.openFolder)
        self.openFolderButton.setStyleSheet("margin-right: 10px; \
                                             border-radius: 5px; \
                                             border : 1px solid black;")

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

        if self.givenPath is not None:
            self.file_list = [self.givenPath + "/" + file for file in os.listdir(self.givenPath)
                          if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]
            self.file_counter = len(self.file_list) -1 if len(self.file_list) > 0 else None
            self.current_file = path[1]
            self.displayImage(path[1])
        else:
            self.file_list = [os.getcwd() + "/" + file for file in os.listdir(os.getcwd())
                          if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg")]
            self.file_counter = len(self.file_list) -1 if len(self.file_list) > 0 else None
            self.next_image()

        QtWidgets.QShortcut(QKeySequence(QtCore.Qt.Key_Right),self,activated=self.next_image)
        QtWidgets.QShortcut(QKeySequence(QtCore.Qt.Key_Left),self,activated=self.prev_image)

    def displayImage(self, image):
        self.pixmap = QtGui.QPixmap(image)
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.graphicsView.displayPicture(QtGui.QPixmap(self.current_file))

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