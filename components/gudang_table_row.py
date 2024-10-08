from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QEvent, QObject

from components.gudang_detail import InformasiBarang
from components.gudang_kelola import GudangKelola

class GudangTableRow:
    def __init__(self, gudang, index, data):
        self.__gudang = gudang
        self.__index = index
        self.__data = data
        self.__double_click_listener = DoubleClickListener(self.__show_detail__)

    def __create_and_get_no__(self):
        self.__no = QLabel(f'{self.__index}')
        self.__no.setMinimumWidth(40)
        self.__no.setMaximumWidth(40)
        self.__no.setStyleSheet('''
            font-size: 14px;
            color: rgb(30, 30, 30);
        ''')
        self.__no.installEventFilter(self.__double_click_listener)
        return self.__no

    def __create_and_get_kode__(self):
        self.__kode = QLabel(f'{self.__data[1]}')
        self.__kode.setMinimumWidth(90)
        self.__kode.setMaximumWidth(160)
        self.__kode.setStyleSheet('''
            font-size: 14px;
            color: rgb(30, 30, 30);
        ''')
        self.__kode.installEventFilter(self.__double_click_listener)
        return self.__kode

    def __create_and_get_nama__(self):
        self.__nama = QLabel(f'{self.__data[2]}')
        self.__nama.setMinimumWidth(250)
        self.__nama.setStyleSheet('''
            font-size: 14px;
            color: rgb(30, 30, 30);
        ''')
        self.__nama.installEventFilter(self.__double_click_listener)
        return self.__nama

    def __create_and_get_kuantiti__(self):
        self.__kuantiti = QLabel(f'{self.__data[3]}')
        self.__kuantiti.setMinimumWidth(70)
        self.__kuantiti.setMaximumWidth(70)
        self.__kuantiti.setStyleSheet('''
            font-size: 14px;
            color: rgb(30, 30, 30);
        ''')
        self.__kuantiti.installEventFilter(self.__double_click_listener)
        return self.__kuantiti

    def __create_and_get_kelola__(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addWidget(self.__create_and_get_ambil__())
        layout.addWidget(self.__create_and_get_tambah__())

        container = QWidget()
        container.setMinimumWidth(160)
        container.setMaximumWidth(160)
        container.setLayout(layout)
        container.installEventFilter(self.__double_click_listener)
        return container

    def __create_and_get_ambil__(self):
        ambil = QPushButton('Ambil')
        ambil.setStyleSheet('''
            QPushButton {
                padding: 4px 0;
                font-size: 12px;
                color: rgb(255, 255, 255);
                background-color: rgb(88, 0, 169);
                border: 1px solid rgb(88, 0, 169);
            }

            QPushButton:hover {
                background-color: rgb(69, 0, 133);
            }
        ''')
        ambil.setCursor(Qt.PointingHandCursor)
        ambil.clicked.connect(lambda: self.__kelola_clicked__('Ambil'))
        return ambil

    def __create_and_get_tambah__(self):
        tambah = QPushButton('Tambah')
        tambah.setStyleSheet('''
            QPushButton {
                padding: 4px 0;
                font-size: 12px;
                color: rgb(88, 0, 169);
                border: 1px solid rgb(88, 0, 169);
            }

            QPushButton:hover {
                background-color: rgb(180, 180, 180);
            }
        ''')
        tambah.setCursor(Qt.PointingHandCursor)
        tambah.clicked.connect(lambda: self.__kelola_clicked__('Tambah'))
        return tambah

    def __kelola_clicked__(self, tipe):
        dialog = GudangKelola(self.__gudang, self.__data[0], int(self.__kuantiti.text()), tipe)
        if (dialog.exec_() == QtWidgets.QDialog.Accepted):
            self.__kuantiti.setText(f'{dialog.new_kuantiti}')
            self.__set_new_kuantiti__(dialog.new_kuantiti)

    def __show_detail__(self):
        dialog = InformasiBarang(self.__gudang, self.__data)
        if (dialog.exec_() == QtWidgets.QDialog.Accepted):
            if (dialog.status == 'deleted'):
                self.__gudang.delete_row()
            elif (dialog.status == 'edited'):
                self.__edit_information__(dialog.data)
                self.redisplay(self.__index, self.__data)
                self.__show_detail__()

    def __set_new_kuantiti__(self, kuantiti):
        data_list = list(self.__data)
        data_list[3] = kuantiti
        self.__data = tuple(data_list)

    def __edit_information__(self, data):
        data_list = list(self.__data)

        data_list[1] = data[0]
        data_list[2] = data[1]
        data_list[4] = data[2]

        self.__data = tuple(data_list)

    def create_row(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(32)

        layout.addWidget(self.__create_and_get_no__())
        layout.addWidget(self.__create_and_get_kode__(), 1)
        layout.addWidget(self.__create_and_get_nama__(), 2)
        layout.addWidget(self.__create_and_get_kuantiti__())
        layout.addWidget(self.__create_and_get_kelola__())

        container = QWidget()
        container.setObjectName(f'row{self.__index}')
        color = 255 if (self.__index % 2) else 230
        container.setStyleSheet(f'''
            #{container.objectName()} {{
                background-color: rgb({color}, {color}, {color});
            }}

            #{container.objectName()}:hover {{
                background-color: rgb(210, 210, 210);
            }}
        ''')
        container.setLayout(layout)
        container.installEventFilter(self.__double_click_listener)

        return container

    def redisplay(self, index, data):
        self.__index = index
        self.__data = data

        self.__no.setText(f'{index}')
        self.__kode.setText(f'{data[1]}')
        self.__nama.setText(f'{data[2]}')
        self.__kuantiti.setText(f'{data[3]}')

class DoubleClickListener(QObject):
    def __init__(self, callback):
        super().__init__()
        self.__callback = callback

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.MouseButtonDblClick and (isinstance(obj, QLabel) or isinstance(obj, QWidget))):
            self.__callback()
            return True
        return False