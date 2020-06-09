import os
import sys
from comics import COMICParser, add_comic, unzip, unrar
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLabel, QWidget, QTabWidget, QScrollArea, QTableWidget, QAbstractItemView, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QCoreApplication, QSize, QRect
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 850, 600)
        self.setWindowTitle('Comics')
        self.init_GUI()
        self.comics_tabs = {}
        self.comics_tabs_index = {}
        self.comics_pictures = {}
        self.comics_current_page = {}
        self.comics_picture_label = {}

    def init_GUI(self):
        # create toolbar
        self.toolbar = QToolBar('Fonctionnalités')
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(32, 32))

        # add "add a comic" button to toolbar
        self.add_action = QAction(
            QIcon('icons/add.png'), 'Nouvelle bande déssinée', self)
        self.add_action.setStatusTip('Ajouter une nouvelle bande déssinée')
        self.add_action.triggered.connect(add_comic)
        self.add_action.setShortcut(QKeySequence('Ctrl+N'))
        self.toolbar.addAction(self.add_action)

        # add "previous" button to toolbar
        self.previous_action = QAction(
            QIcon('icons/previous.png'), 'Page précédente', self)
        self.previous_action.setStatusTip('Passer à la page précédente')
        self.previous_action.triggered.connect(self.previous_page)
        self.previous_action.setShortcut(QKeySequence('Ctrl+L'))
        self.toolbar.addAction(self.previous_action)

        # add "next" button to toolbar
        self.next_action = QAction(
            QIcon('icons/next.png'), 'Page suivante', self)
        self.next_action.setStatusTip('Passer à la page suivante')
        self.next_action.triggered.connect(self.next_page)
        self.next_action.setShortcut(QKeySequence('Ctrl+O'))
        self.toolbar.addAction(self.next_action)

        # add main view
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName('centralwidget')
        self.setCentralWidget(self.centralwidget)

        # add tabs widget
        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QRect(0, 0, 850, 600))
        self.tab_widget.setObjectName('tab_widget')
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(lambda index: self.remove_tab(index))

        # add library tab
        self.library_tab = QWidget()
        self.library_tab.setObjectName('library_tab')
        self.tab_widget.addTab(self.library_tab, 'Bibliothèque')

        # show library in library tab
        self.scroll_area = QScrollArea(self.library_tab)
        self.scroll_area.setGeometry(QRect(0, 0, 850, 600))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName('scroll_area')
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 850, 600))
        self.scroll_area_widget_contents.setObjectName(
            'scroll_area_widget_contents')
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.table_widget = QTableWidget(self.scroll_area_widget_contents)
        self.table_widget.setGeometry(QRect(0, 0, 850, 600))
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(8)
        self.table_widget.setObjectName('table_widget')
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setItem(0, 0, QTableWidgetItem())
        self.table_widget.item(0, 0).setText('Cover')
        self.table_widget.setItem(0, 1, QTableWidgetItem())
        self.table_widget.item(0, 1).setText('Titre')
        self.table_widget.setItem(0, 2, QTableWidgetItem())
        self.table_widget.item(0, 2).setText('Auteur')
        self.table_widget.setItem(0, 3, QTableWidgetItem())
        self.table_widget.item(0, 3).setText('Année')
        self.table_widget.setItem(0, 4, QTableWidgetItem())
        self.table_widget.item(0, 4).setText('Tags')
        self.table_widget.setItem(0, 5, QTableWidgetItem())
        self.table_widget.item(0, 5).setText('Quality')

        self.library_files = get_library_files()
        index = 0
        for comic in self.library_files:
            if os.path.splitext(comic)[1].lower() == '.cbz':
                unzip('library/' + comic, 'library/' + os.path.splitext(comic)[0])
            else:
                unrar('library/' + comic, 'library/' + os.path.splitext(comic)[0])
            index += 1
            self.table_widget.insertRow(index)
            cover_widget = QWidget()
            self.table_widget.setCellWidget(index, 0, cover_widget)
            self.table_widget.setRowHeight(index, 150)
            comicParser = COMICParser('library/' + comic)
            pictures = comicParser.read_book()
            cover_label = QLabel(cover_widget)
            cover_label.setGeometry(
                    QRect(0, 0, 100, 150))
            cover_label.setScaledContents(True)
            cover_label.setAlignment(Qt.AlignCenter)
            cover_label.setObjectName(comic)
            cover_label.setPixmap(QPixmap('library/' + os.path.splitext(comic)[0] + '/' + pictures[0]))
            self.table_widget.setItem(index, 1, QTableWidgetItem())
            self.table_widget.item(index, 1).setText(os.path.splitext(comic)[0])
            metadata = comicParser.getMetadata(os.path.splitext(comic)[0])
            self.table_widget.setItem(index, 2, QTableWidgetItem())
            self.table_widget.item(index, 2).setText(metadata['author'])
            self.table_widget.setItem(index, 3, QTableWidgetItem())
            self.table_widget.item(index, 3).setText(metadata['year'])
            self.table_widget.setItem(index, 4, QTableWidgetItem())
            self.table_widget.item(index, 4).setText(metadata['tags'])
            self.table_widget.setItem(index, 5, QTableWidgetItem())
            self.table_widget.item(index, 5).setText(metadata['quality'])
            read_button = QPushButton(self.table_widget)
            self.table_widget.setCellWidget(index, 6, read_button)
            read_button.setText('Lire la BD')
            read_button.clicked.connect(self.make_read_comic(comic))
            edit_button = QPushButton(self.table_widget)
            self.table_widget.setCellWidget(index, 7, edit_button)
            edit_button.setText('Modifier les infos')
            edit_button.clicked.connect(self.make_read_comic(comic))

    ### actions ###
    def previous_page(self):
        if not self.tab_widget.currentIndex() == 0:
            current_comics = None
            for key, value in self.comics_tabs.items():
                if value == self.tab_widget.currentWidget():
                    current_comics = key
            if self.comics_current_page[current_comics] >= 1:
                self.comics_current_page[current_comics] -= 1
                page = self.comics_current_page[current_comics]
                self.comics_picture_label[current_comics].setPixmap(QPixmap(
                    'library/' + current_comics + '/' + self.comics_pictures[current_comics][page]))

    def next_page(self):
        if not self.tab_widget.currentIndex() == 0:
            current_comics = None
            for key, value in self.comics_tabs.items():
                if value == self.tab_widget.currentWidget():
                    current_comics = key
            if self.comics_current_page[current_comics] < len(self.comics_pictures[current_comics]) - 1:
                self.comics_current_page[current_comics] += 1
                page = self.comics_current_page[current_comics]
                self.comics_picture_label[current_comics].setPixmap(QPixmap(
                    'library/' + current_comics + '/' + self.comics_pictures[current_comics][page]))

    def make_read_comic(self, comic):
        def read_comic():
            comics_title = os.path.splitext(comic)[0]
            if not comics_title in self.comics_tabs_index:
                self.comics_tabs[comics_title] = QWidget()
                self.comics_tabs[comics_title].setObjectName('comic_view_tab')
                self.tab_widget.addTab(
                    self.comics_tabs[comics_title], comics_title)
                self.comics_tabs_index[comics_title] = self.tab_widget.indexOf(self.comics_tabs[comics_title])

                self.comics_picture_label[comics_title] = QLabel(
                    self.comics_tabs[comics_title])
                self.comics_picture_label[comics_title].setGeometry(
                    QRect(0, 0, 350, 500))
                self.comics_picture_label[comics_title].setScaledContents(True)
                self.comics_picture_label[comics_title].setAlignment(Qt.AlignCenter)
                self.comics_picture_label[comics_title].setObjectName(comics_title)

                comicParser = COMICParser('library/' + comic)
                self.comics_pictures[comics_title] = comicParser.read_book()
                self.comics_current_page[comics_title] = 0
                comicParser.generate_metadata()

                self.comics_picture_label[comics_title].setPixmap(QPixmap(
                    'library/' + comics_title + '/' + self.comics_pictures[comics_title][0]))
        return read_comic

    def remove_tab(self, index):
        if index > 0:
            self.tab_widget.removeTab(index)
            comics_to_close = None
            for key, value in self.comics_tabs_index.items():
                if value == index:
                    comics_to_close = key
            del self.comics_tabs[comics_to_close]
            del self.comics_current_page[comics_to_close]
            del self.comics_picture_label[comics_to_close]
            del self.comics_pictures[comics_to_close]
            self.comics_tabs_index = {}
            for key, value in self.comics_tabs.items():
                self.comics_tabs_index[key] = self.tab_widget.indexOf(value)



def get_library_files():
    files = []
    comics = []
    for (dirpath, dirnames, filenames) in os.walk('library'):
        files.extend(filenames)
        break
    for file in files:
        if is_comic_file(file):
            comics.append(file)
    return comics


def is_comic_file(filename):
    valid_image_extensions = ['.cbz', '.cbr']
    if os.path.splitext(filename)[1].lower() in valid_image_extensions:
        return True
    else:
        return False


app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
