# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'encoder-widget2.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeenEncoderWidget(object):
    def setupUi(self, DeenEncoderWidget):
        DeenEncoderWidget.setObjectName("DeenEncoderWidget")
        DeenEncoderWidget.resize(922, 654)
        self.gridLayout = QtWidgets.QGridLayout(DeenEncoderWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.content_area_layout_widget = QtWidgets.QWidget(DeenEncoderWidget)
        self.content_area_layout_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.content_area_layout_widget.setObjectName("content_area_layout_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.content_area_layout_widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.content_area_layout = QtWidgets.QVBoxLayout()
        self.content_area_layout.setObjectName("content_area_layout")
        self.verticalLayout_5.addLayout(self.content_area_layout)
        self.gridLayout.addWidget(self.content_area_layout_widget, 0, 1, 4, 1)
        self.search_group = QtWidgets.QGroupBox(DeenEncoderWidget)
        self.search_group.setMaximumSize(QtCore.QSize(16777215, 115))
        self.search_group.setTitle("")
        self.search_group.setObjectName("search_group")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.search_group)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.search_progress_bar = QtWidgets.QProgressBar(self.search_group)
        self.search_progress_bar.setProperty("value", 24)
        self.search_progress_bar.setObjectName("search_progress_bar")
        self.gridLayout_2.addWidget(self.search_progress_bar, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.search_group)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.search_area = QtWidgets.QLineEdit(self.search_group)
        self.search_area.setObjectName("search_area")
        self.horizontalLayout_3.addWidget(self.search_area)
        self.search_button = QtWidgets.QPushButton(self.search_group)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_3.addWidget(self.search_button)
        self.search_clear_button = QtWidgets.QPushButton(self.search_group)
        self.search_clear_button.setObjectName("search_clear_button")
        self.horizontalLayout_3.addWidget(self.search_clear_button)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.search_matches_label = QtWidgets.QLabel(self.search_group)
        self.search_matches_label.setObjectName("search_matches_label")
        self.gridLayout_2.addWidget(self.search_matches_label, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.search_group, 6, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.content_length_label = QtWidgets.QLabel(DeenEncoderWidget)
        self.content_length_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.content_length_label.setObjectName("content_length_label")
        self.verticalLayout_4.addWidget(self.content_length_label)
        self.selection_length_label = QtWidgets.QLabel(DeenEncoderWidget)
        self.selection_length_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.selection_length_label.setObjectName("selection_length_label")
        self.verticalLayout_4.addWidget(self.selection_length_label)
        self.gridLayout.addLayout(self.verticalLayout_4, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(DeenEncoderWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.plugin_tree_view = QtWidgets.QTreeWidget(DeenEncoderWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plugin_tree_view.sizePolicy().hasHeightForWidth())
        self.plugin_tree_view.setSizePolicy(sizePolicy)
        self.plugin_tree_view.setMinimumSize(QtCore.QSize(0, 125))
        self.plugin_tree_view.setMaximumSize(QtCore.QSize(300, 16777215))
        self.plugin_tree_view.setObjectName("plugin_tree_view")
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        item_0 = QtWidgets.QTreeWidgetItem(self.plugin_tree_view)
        self.gridLayout.addWidget(self.plugin_tree_view, 0, 0, 1, 1)
        self.error_message_layout_widget = QtWidgets.QWidget(DeenEncoderWidget)
        self.error_message_layout_widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.error_message_layout_widget.setObjectName("error_message_layout_widget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.error_message_layout_widget)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.error_message_layout = QtWidgets.QVBoxLayout()
        self.error_message_layout.setObjectName("error_message_layout")
        self.verticalLayout_8.addLayout(self.error_message_layout)
        self.gridLayout.addWidget(self.error_message_layout_widget, 4, 1, 1, 1)
        self.side_menu = QtWidgets.QWidget(DeenEncoderWidget)
        self.side_menu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.side_menu.setObjectName("side_menu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.side_menu)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout.addWidget(self.side_menu, 0, 2, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.toggle_text_view = QtWidgets.QPushButton(DeenEncoderWidget)
        self.toggle_text_view.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toggle_text_view.setObjectName("toggle_text_view")
        self.verticalLayout_6.addWidget(self.toggle_text_view)
        self.toggle_hex_view = QtWidgets.QPushButton(DeenEncoderWidget)
        self.toggle_hex_view.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toggle_hex_view.setObjectName("toggle_hex_view")
        self.verticalLayout_6.addWidget(self.toggle_hex_view)
        self.toggle_formatted_view = QtWidgets.QPushButton(DeenEncoderWidget)
        self.toggle_formatted_view.setObjectName("toggle_formatted_view")
        self.verticalLayout_6.addWidget(self.toggle_formatted_view)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 0, 1, 1)

        self.retranslateUi(DeenEncoderWidget)
        QtCore.QMetaObject.connectSlotsByName(DeenEncoderWidget)

    def retranslateUi(self, DeenEncoderWidget):
        _translate = QtCore.QCoreApplication.translate
        DeenEncoderWidget.setWindowTitle(_translate("DeenEncoderWidget", "Form"))
        self.label_2.setText(_translate("DeenEncoderWidget", "Search:"))
        self.search_button.setText(_translate("DeenEncoderWidget", "Search"))
        self.search_clear_button.setText(_translate("DeenEncoderWidget", "Clear"))
        self.search_matches_label.setText(_translate("DeenEncoderWidget", "Matches: 0"))
        self.content_length_label.setText(_translate("DeenEncoderWidget", "Length:"))
        self.selection_length_label.setText(_translate("DeenEncoderWidget", "Selection:"))
        self.plugin_tree_view.headerItem().setText(0, _translate("DeenEncoderWidget", "Plugins"))
        __sortingEnabled = self.plugin_tree_view.isSortingEnabled()
        self.plugin_tree_view.setSortingEnabled(False)
        self.plugin_tree_view.topLevelItem(0).setText(0, _translate("DeenEncoderWidget", "Decode"))
        self.plugin_tree_view.topLevelItem(1).setText(0, _translate("DeenEncoderWidget", "Encode"))
        self.plugin_tree_view.topLevelItem(2).setText(0, _translate("DeenEncoderWidget", "Uncompress"))
        self.plugin_tree_view.topLevelItem(3).setText(0, _translate("DeenEncoderWidget", "Compress"))
        self.plugin_tree_view.topLevelItem(4).setText(0, _translate("DeenEncoderWidget", "Disassemble"))
        self.plugin_tree_view.topLevelItem(5).setText(0, _translate("DeenEncoderWidget", "Assemble"))
        self.plugin_tree_view.topLevelItem(6).setText(0, _translate("DeenEncoderWidget", "Hash"))
        self.plugin_tree_view.topLevelItem(7).setText(0, _translate("DeenEncoderWidget", "Miscellaneous"))
        self.plugin_tree_view.topLevelItem(8).setText(0, _translate("DeenEncoderWidget", "Format"))
        self.plugin_tree_view.setSortingEnabled(__sortingEnabled)
        self.toggle_text_view.setText(_translate("DeenEncoderWidget", "Te&xt view"))
        self.toggle_hex_view.setText(_translate("DeenEncoderWidget", "He&x view"))
        self.toggle_formatted_view.setText(_translate("DeenEncoderWidget", "Formatted View"))


