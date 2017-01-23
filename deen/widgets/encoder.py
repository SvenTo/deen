import logging
import string
try:
    from OpenSSL import crypto
except ImportError:
    crypto = None

from PyQt5.QtCore import QTextCodec, QRegularExpression, Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor, QIcon
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QVBoxLayout, QComboBox,
                             QButtonGroup, QCheckBox, QPushButton, QLineEdit, QProgressBar,
                             QFileDialog, QToolButton)

from deen.widgets.hex import HexViewWidget
from deen.widgets.text import TextViewWidget
from deen.transformers.core import DeenTransformer, X509Certificate
from deen.core import *

LOGGER = logging.getLogger(__name__)


class EncoderWidget(QWidget):
    def __init__(self, parent):
        super(EncoderWidget, self).__init__(parent)
        self.widgets = []
        self.widgets.append(DeenWidget(self))
        self.encoder_layout = QVBoxLayout(self)
        for widget in self.widgets:
            self.encoder_layout.addWidget(widget)
        self.setLayout(self.encoder_layout)

    def set_root_content(self, data):
        if data:
            if isinstance(data, (str, bytes)):
                data = bytearray(data)
            self.widgets[0].content = data


class DeenWidget(QWidget):
    def __init__(self, parent, readonly=False, enable_actions=True):
        super(DeenWidget, self).__init__(parent)
        self.parent = parent
        self.readonly = readonly
        self.current_pick = None
        self.current_combo = None
        self.text_field = TextViewWidget(self, readonly=self.readonly)
        self.text_field.textChanged.connect(self.field_content_changed)
        self.hex_field = HexViewWidget(read_only=self.readonly, parent=self)
        self.hex_field.setHidden(True)
        self.hex_field.bytesChanged.connect(self.field_content_changed)
        self.codec = QTextCodec.codecForName('UTF-8')
        self._content = bytearray()
        self.hex_view = False
        self.view_panel = self.create_view_panel()
        self.action_panel = self.create_action_panel(enable_actions)
        if not enable_actions:
            self.action_panel.hide()
        self.create_search_field()
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.view_panel)
        self.v_layout.addWidget(self.text_field)
        self.v_layout.addWidget(self.hex_field)
        self.v_layout.addLayout(self.search)
        self.h_layout = QHBoxLayout()
        self.h_layout.addLayout(self.v_layout)
        self.h_layout.addWidget(self.action_panel)
        self.setLayout(self.h_layout)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, data):
        assert isinstance(data, bytearray)
        self._content = data
        if self.hex_view:
            self.hex_field.content = self._content
        else:
            # Prevent the field from overwriting itself with invalid
            # characters.
            if not all(chr(c) in string.printable for c in self._content):
                self.text_field.setReadOnly(True)
            self.text_field.setPlainText(self.codec.toUnicode(self._content))
            self.text_field.moveCursor(QTextCursor.End)

    def has_previous(self):
        """Determine if the current widget is the root widget."""
        return True if self.parent.widgets[0] != self else False

    def has_next(self):
        """Determine if there are already new widgets created."""
        return True if self.parent.widgets[-1] != self else False

    def previous(self):
        """Return the previous widget. If the current widget
        is the root widget, this function returns the root
        widget (self)."""
        if not self.has_previous() == self:
            return self
        for i, w in enumerate(self.parent.widgets):
            if w == self:
                return self.parent.widgets[i - 1]

    def next(self):
        """Return the next widget. This is most likely the one
        that is supposed to hold the output of action()'s of
        the current widget."""
        if not self.has_next():
            w = DeenWidget(self.parent, readonly=True, enable_actions=False)
            self.parent.widgets.append(w)
            self.parent.encoder_layout.addWidget(w)
            return w
        for i, w in enumerate(self.parent.widgets):
            if w == self:
                return self.parent.widgets[i + 1]

    def field_content_changed(self):
        """The event handler for the textChanged event of the
        current widget. This will be called whenever the text
        of the QTextEdit() will be changed. Whatever will be
        executed here will most likely differ if it will be
        applied on a root widget or any following widget."""
        if self.action_panel.isHidden():
            self.action_panel.show()
        if self.has_next() and not self.text_field.isReadOnly():
            # If widget count is greater then two,
            # remove all widgets after the second.
            self.remove_next_widgets(offset=2)
        elif self.has_next() and self.text_field.isReadOnly():
            # If the current widget is not the root
            # but there is at least one next widget.
            self.set_content_next(self.content)
        if not self.text_field.isReadOnly():
            if not self.hex_view:
                self._content = bytearray(self.text_field.toPlainText(), 'utf8')
            else:
                self._content = self.hex_field.content
        self.update_length_field(self)
        self.update_readonly_field(self)
        if (self.hex_field.hasFocus() or self.text_field.hasFocus()) \
                and self.current_pick:
            self.action()

    def create_view_panel(self):
        text = QCheckBox('Text')
        text.setChecked(True)
        text.stateChanged.connect(self.view_text)
        hex = QCheckBox('Hex')
        hex.setChecked(False)
        hex.stateChanged.connect(self.view_hex)
        clear = QToolButton()
        clear.setIcon(QIcon.fromTheme('edit-clear'))
        clear.setToolTip('Clear widget content')
        clear.clicked.connect(self.clear_content)
        save = QToolButton()
        save.setIcon(QIcon.fromTheme('document-save-as'))
        save.setToolTip('Save content to file')
        save.clicked.connect(self.save_content)
        copy = QToolButton()
        copy.setIcon(QIcon.fromTheme('edit-copy'))
        copy.setToolTip('Copy content to clipboard')
        copy.clicked.connect(self.copy_to_clipboard)
        move = QToolButton()
        move.setIcon(QIcon.fromTheme('go-up'))
        move.setToolTip('Move content to root widget')
        move.clicked.connect(self.move_content_to_root)
        self.length_field = QLabel()
        self.length_field.setStyleSheet('border: 1px solid lightgrey')
        self.update_length_field(self)
        self.readonly_field = QLabel()
        self.readonly_field.setStyleSheet('border: 1px solid lightgrey')
        self.update_readonly_field(self)
        self.codec_field = QLabel()
        self.codec_field.setStyleSheet('border: 1px solid lightgrey')
        self.codec_field.hide()
        view_group = QButtonGroup(self)
        view_group.addButton(text, 1)
        view_group.addButton(hex, 2)
        view_group.addButton(save, 3)
        view_group.addButton(clear, 4)
        view_group.addButton(move, 5)
        panel = QHBoxLayout()
        panel.addWidget(text)
        panel.addWidget(hex)
        panel.addWidget(self.length_field)
        panel.addWidget(self.readonly_field)
        panel.addWidget(self.codec_field)
        panel.addStretch()
        panel.addWidget(clear)
        panel.addWidget(copy)
        panel.addWidget(save)
        if self.readonly:
            panel.addWidget(move)
        widget = QWidget()
        widget.setLayout(panel)
        return widget

    def create_search_field(self):
        self.search_field = QLineEdit()
        self.search_field.returnPressed.connect(self.search_highlight)
        self.search_field_matches = QLabel()
        self.search_field_matches.hide()
        self.search_field_progress = QProgressBar()
        self.search_field_progress.setGeometry(200, 80, 250, 20)
        self.search_field_progress.hide()
        self.search_bars = QVBoxLayout()
        self.search_bars.addWidget(self.search_field)
        self.search_bars.addWidget(self.search_field_progress)
        self.search = QHBoxLayout()
        self.search.addLayout(self.search_bars)
        self.search.addWidget(self.search_field_matches)

    def search_highlight(self):
        cursor = self.text_field.textCursor()
        b_format = cursor.blockFormat()
        b_format.setBackground(QBrush(QColor('white')))
        cursor.setBlockFormat(b_format)
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor('yellow')))
        regex = QRegularExpression(self.search_field.text())
        matches = regex.globalMatch(self.text_field.toPlainText())
        _matches = []
        while matches.hasNext():
            _matches.append(matches.next())
        self.search_matches = _matches
        self.search_field_matches.setText('Matches: ' + str(len(self.search_matches)))
        self.search_field_matches.show()
        self.search_field_progress.setRange(0, len(self.search_matches))
        if len(self.search_matches) > 100:
            self.search_field_progress.show()
        match_count = 1
        for match in self.search_matches:
            if match_count > 150:
                # TODO: implement proper handling of > 1000 matches
                break
            self.search_field_progress.setValue(match_count)
            match_count += 1
            cursor.setPosition(match.capturedStart())
            cursor.setPosition(match.capturedEnd(), QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)
        #self.field.moveCursor(QTextCursor.Start)
        #self.field.moveCursor(F)
        #self.field.ensureCursorVisible()

    def create_action_panel(self, enable_actions=True):
        self.encoding_combo = QComboBox(self)
        self.encoding_combo.addItem('Encode')
        self.encoding_combo.model().item(0).setEnabled(False)
        for encoding in ENCODINGS:
            self.encoding_combo.addItem(encoding)
        self.encoding_combo.currentIndexChanged.connect(lambda: self.action(self.encoding_combo))

        self.decoding_combo = QComboBox(self)
        self.decoding_combo.addItem('Decode')
        self.decoding_combo.model().item(0).setEnabled(False)
        for encoding in ENCODINGS:
            self.decoding_combo.addItem(encoding)
        self.decoding_combo.currentIndexChanged.connect(lambda: self.action(self.decoding_combo))

        self.compress_combo = QComboBox(self)
        self.compress_combo.addItem('Compress')
        self.compress_combo.model().item(0).setEnabled(False)
        for compression in COMPRESSIONS:
            self.compress_combo.addItem(compression)
        self.compress_combo.currentIndexChanged.connect(lambda: self.action(self.compress_combo))

        self.uncompress_combo = QComboBox(self)
        self.uncompress_combo.addItem('Uncompress')
        self.uncompress_combo.model().item(0).setEnabled(False)
        for compression in COMPRESSIONS:
            self.uncompress_combo.addItem(compression)
        self.uncompress_combo.currentIndexChanged.connect(lambda: self.action(self.uncompress_combo))

        self.hash_combo = QComboBox(self)
        self.hash_combo.addItem('Hash')
        self.hash_combo.model().item(0).setEnabled(False)
        for hash in HASHS:
            self.hash_combo.addItem(hash)
        self.hash_combo.addItem('ALL')
        self.hash_combo.currentIndexChanged.connect(lambda: self.action(self.hash_combo))

        self.misc_combo = QComboBox(self)
        self.misc_combo.addItem('Miscellaneous')
        self.misc_combo.model().item(0).setEnabled(False)
        for misc in MISC:
            self.misc_combo.addItem(misc)
        self.misc_combo.currentIndexChanged.connect(lambda: self.action(self.misc_combo))

        action_panel = QVBoxLayout()
        action_panel.addWidget(self.decoding_combo)
        action_panel.addWidget(self.encoding_combo)
        action_panel.addWidget(self.uncompress_combo)
        action_panel.addWidget(self.compress_combo)
        action_panel.addWidget(self.hash_combo)
        action_panel.addWidget(self.misc_combo)
        action_panel.addStretch()
        widget = QWidget()
        widget.setLayout(action_panel)
        return widget

    def view_text(self):
        self.hex_view = False
        self.text_field.setHidden(False)
        self.hex_field.setHidden(True)
        if self._content:
            self.text_field.setPlainText(self.codec.toUnicode(self._content))

    def view_hex(self):
        self.hex_view = True
        self.text_field.setHidden(True)
        self.hex_field.setHidden(False)
        self.hex_field._read_only = self.text_field.isReadOnly()
        if not self._content:
            self._content = bytearray(self.text_field.toPlainText(), 'utf8')
        self.hex_field.content = self._content

    def clear_content(self, widget=None):
        """Clear the content of widget. If widget
        is not set, clear the content of the current
        widget. This will also remove all widgets
        that follow widget."""
        widget = widget or self
        if self.parent.widgets[0] == widget:
            widget.text_field.clear()
            widget.hex_field.content = bytearray()
            widget._content = bytearray()
            widget.update_length_field(self)
            widget.text_field.setReadOnly(False)
            widget.update_readonly_field(self)
            widget.current_pick = None
        self.remove_next_widgets(widget=widget)

    def copy_to_clipboard(self):
        if not self._content:
            return
        try:
            content = self._content.decode('utf8')
        except UnicodeDecodeError as e:
            LOGGER.error(e)
            LOGGER.error('Cannot copy non-ASCII content to clipboard')
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(content)

    def save_content(self):
        """Save the content of the current widget
        to a file."""
        if not self._content:
            return
        fd = QFileDialog(self)
        name = fd.getSaveFileName(fd, 'Save File')
        if not name or not name[0]:
            return
        with open(name[0], 'wb') as file:
            file.write(self._content)

    def move_content_to_root(self):
        """Moves the content of the current widget
        to the root widget and removes all widgets
        after the root widget."""
        content = self._content
        self.clear_content(self.parent.widgets[0])
        self.parent.widgets[0].content = content

    def update_length_field(self, widget):
        widget.length_field.setText('Length: ' + str(len(widget.content)))

    def update_readonly_field(self, widget):
        widget.readonly_field.setText('R-' if widget.text_field.isReadOnly() else 'RW')

    def remove_next_widgets(self, widget=None, offset=0):
        """Remove all widgets after widget. If widget is not
        set, remove all widgets after the current widget."""
        widget = widget or self
        assert isinstance(offset, int)
        index = self.parent.widgets.index(widget) + offset
        while len(self.parent.widgets) != index:
            if len(self.parent.widgets) == 1:
                break
            self.parent.encoder_layout.removeWidget(self.parent.widgets[-1])
            self.parent.widgets[-1].deleteLater()
            self.parent.widgets[-1] = None
            self.parent.widgets.pop()

    def set_content_next(self, content):
        if isinstance(content, bytes):
            self.next().content = bytearray(content)
        elif isinstance(content, str):
            self.next().content = bytearray(content, 'utf8')
        else:
            self.next().content = content
        self.next().text_field.setPlainText(self.codec.toUnicode(self.next()._content))
        self.update_length_field(self.next())
        if self.next().hex_view:
            self.next().view_hex()

    def set_error_next(self):
        """If an an error occured during transformation
        this function sets the color of the next widget's
        border to red and removes all following widgets."""
        next_widget = self.next()
        next_widget.text_field.setStyleSheet('border: 2px solid red;')
        self.remove_next_widgets(widget=next_widget, offset=1)

    def action(self, combo=None):
        """The main function that is responsible for calling transformers
        on input data. It will use self._content as source and puts the
        result of each transformer into the next widget in line via the
        self.set_content_next() function."""
        error = None
        if not self._content:
            self._content = bytearray(self.text_field.toPlainText(), 'utf8')
        if combo:
            if combo.currentIndex() == 0:
                return
            self.current_combo = combo
            self.current_pick = combo.currentText()
        transformer = DeenTransformer()
        if self.current_pick in ENCODINGS:
            if self.current_combo.model().item(0).text() == 'Encode':
                encoded = transformer.encode(self.current_pick, self._content)
                self.set_content_next(encoded)
            else:
                decoded, error = transformer.decode(self.current_pick, self._content)
                if error:
                    LOGGER.error(error)
                    self.set_error_next()
                self.set_content_next(decoded)
        elif self.current_pick in COMPRESSIONS:
            if self.current_combo.model().item(0).text() == 'Compress':
                compressed = transformer.compress(self.current_pick, self._content)
                self.set_content_next(compressed)
            else:
                uncompressed, error = transformer.uncompress(self.current_pick, self._content)
                if error:
                    LOGGER.error(error)
                    self.set_error_next()
                self.set_content_next(uncompressed)
        elif self.current_pick in HASHS or self.current_pick == 'ALL':
            hashed = transformer.hash(self.current_pick, self._content)
            self.set_content_next(hashed)
        elif self.current_pick in MISC:
            if self.current_pick == 'X509Certificate' and crypto:
                try:
                    transformer = X509Certificate(self._content)
                    self.set_content_next(transformer.decode())
                except crypto.Error as e:
                    LOGGER.error(e)
                    error = e
                    self.set_error_next()
                    self.set_content_next(self._content)
        if self.current_combo:
            self.current_combo.setCurrentIndex(0)
        if self.next().text_field.isReadOnly() and self.current_pick:
            self.next().codec_field.setText('Transformer: ' + self.current_pick)
            self.next().codec_field.show()
        if not error:
            self.next().text_field.setStyleSheet('border: none;')
