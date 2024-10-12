# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

import json
import sys
import typing

import markdown  # type: ignore
from PyQt6.QtCore import (
    pyqtSignal,
    QObject,
    Qt,
    QThread,
)
from PyQt6.QtGui import (
    QClipboard,
    QCloseEvent,
    QColor,
    QPalette,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .. import _api

CHAT_WINDOW_STYLE = """
QWidget {
    background-color: #212121;
}
QScrollArea {
    background-color: transparent; 
    border: none;
}
QScrollBar:vertical {
    background-color: #2F2F2F;
    width: 12px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #808080;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar:horizontal {
    background-color: #2F2F2F;
    height: 12px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #808080;
    min-width: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
QTextEdit {
    background-color: #2F2F2F; 
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
}
QTextEdit:focus {
    border: 1px solid #FFFFFF;
}
QPushButton {
    background-color: #808080;
    color: #FFFFFF;
    border: none;
    padding: 5px;
    border-radius: 8px;
}
QPushButton:hover {
    background-color: #696969;
}
"""

USER_MESSAGE_STYLE = """
QLabel {
    background-color: #808080;  
    padding: 5px;
    color: #FFFFFF;  
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border-top-right-radius: 0px;  
}
QLabel:hover {
    background-color: #696969; 
}
"""

ASSISTANT_MESSAGE_STYLE = """
QTextBrowser {
    color: #FFFFFF;  /* White font color */
    background-color: transparent; 
    border: none;
}
AutoResizingTextBrowser {
    color: #FFFFFF;  /* White font color */
    background-color: transparent; 
    border: none;
}
"""

COPY_BUTTON_STYLE = """
QPushButton {
    background-color: transparent;
    border-radius: 10px;  
}
QPushButton:hover {
    background-color: #696969;
}
"""


# noinspection PyUnresolvedReferences
class ChatWorker(QObject):
    finished = pyqtSignal()
    responseReady = pyqtSignal(str)

    def __init__(
        self,
        message: str,
        cli: _api.GraphRAGCli,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None
    ) -> None:
        super().__init__()
        self.message: str = message
        self.cli = cli
        self._stop = False
        self._stream_response: typing.Optional[typing.Generator[str, None, None]] = None
        self.params = params

    def run(self) -> None:
        response = self.cli.chat(self.message, **(self.params or {}))
        self._stream_response = typing.cast(typing.Generator[str, None, None], response)
        for chunk in self._stream_response:
            if self._stop:
                break
            self.responseReady.emit(chunk)
        self.finished.emit()

    def stop(self) -> None:
        self._stop = True
        self.finished.emit()
        if self._stream_response:
            try:
                self._stream_response.close()
            except ValueError:
                pass


# noinspection PyUnresolvedReferences
class AutoResizingTextBrowser(QTextBrowser):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        document = self.document()
        if document:
            document.contentsChanged.connect(self.adjust_height)

    def adjust_height(self) -> None:
        document = self.document()
        if not document:
            return
        docHeight = document.size().height()
        margins = self.contentsMargins()
        totalHeight = docHeight + margins.top() + margins.bottom() + self.frameWidth() * 2
        self.setFixedHeight(int(totalHeight))


# noinspection PyUnresolvedReferences
class AutoResizingTextEdit(QTextEdit):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        document = self.document()
        if document:
            document.contentsChanged.connect(self.adjust_height)

    def adjust_height(self) -> None:
        document = self.document()
        if not document:
            return
        docHeight = document.size().height()
        margins = self.contentsMargins()
        totalHeight = docHeight + margins.top() + margins.bottom() + self.frameWidth() * 2
        self.setFixedHeight(min(100, int(totalHeight)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.parent().send_message()
        else:
            super().keyPressEvent(event)


# noinspection PyUnresolvedReferences
class ChatWindow(QWidget):
    def __init__(self, cli: _api.GraphRAGCli, **kwargs: typing.Any) -> None:
        super().__init__()
        self.cli = cli
        self.params = kwargs

        self.assistant_label: typing.Optional[QWidget] = None
        self.assistant_response_text: str = ''
        self.setWindowTitle('Chat with GraphRAG')
        self.resize(600, 500)
        self.layout_ = QVBoxLayout()

        # Toolbar
        self.toolbar = QWidget()
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.copyButton = QPushButton('Copy')
        self.copyButton.setStyleSheet(COPY_BUTTON_STYLE)
        self.copyButton.clicked.connect(self.copy_conversation)
        self.toolbarLayout.addWidget(self.copyButton)
        self.toolbar.setLayout(self.toolbarLayout)
        self.layout_.addWidget(self.toolbar)

        # Chat area
        self.chatScrollArea = QScrollArea()
        self.chatScrollArea.setWidgetResizable(True)
        self.chatWidget = QWidget()
        self.chatLayout = QVBoxLayout()
        self.chatLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chatWidget.setLayout(self.chatLayout)
        self.chatScrollArea.setWidget(self.chatWidget)

        # Input area
        self.inputText = AutoResizingTextEdit()
        self.inputText.setPlaceholderText('Type your message here...')
        self.inputText.adjust_height()

        # Send button
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.send_message)

        # Clear button
        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clear_history)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.sendButton)

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inputText)
        inputLayout.addLayout(buttonLayout)

        self.layout_.addWidget(self.chatScrollArea)
        self.layout_.addLayout(inputLayout)
        self.setLayout(self.layout_)
        self.thread_: typing.Optional[QThread] = None
        self.worker: typing.Optional[ChatWorker] = None

        self.setStyleSheet(CHAT_WINDOW_STYLE)

    def copy_conversation(self) -> None:
        conversation = self.cli.conversation_history()
        conversation_text = json.dumps(conversation, ensure_ascii=False, indent=4)
        typing.cast(QClipboard, QApplication.clipboard()).setText(conversation_text)

    def send_message(self) -> None:
        message = self.inputText.toPlainText().strip()
        if not message:
            return

        # Display user's message
        user_message_widget = self.create_message_widget(message, sender='User')
        self.chatLayout.addWidget(user_message_widget)
        self.inputText.clear()

        # Add an empty assistant message container
        self.assistant_label = self.create_message_widget("", sender='Assistant')
        self.chatLayout.addWidget(self.assistant_label)
        self.assistant_response_text = ''

        # Start worker thread to process simulated response
        self.thread_ = QThread()
        self.worker = ChatWorker(message, cli=self.cli, params=self.params)
        self.worker.moveToThread(self.thread_)

        # Connect signals and slots
        self.thread_.started.connect(self.worker.run)
        self.worker.responseReady.connect(self.update_response)
        self.worker.finished.connect(self.thread_.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_.finished.connect(self.thread_.deleteLater)

        # Disable send button until response is finished
        self.sendButton.setEnabled(False)
        self.thread_.finished.connect(lambda: self.sendButton.setEnabled(True))
        self.thread_.start()

    def clear_history(self) -> None:
        try:
            if self.worker:
                self.worker.stop()
                self.worker.responseReady.disconnect(self.update_response)
        except (RuntimeError, TypeError):
            pass

        self.cli.clear_history()
        while self.chatLayout.count():
            child = self.chatLayout.takeAt(0)
            if child and child.widget():
                typing.cast(QWidget, child.widget()).deleteLater()

        self.chatWidget.update()
        self.chatScrollArea.update()
        self.sendButton.setEnabled(True)

    @staticmethod
    def create_message_widget(text: str, sender: str = 'User') -> QWidget:
        message_widget: typing.Union[QLabel, AutoResizingTextBrowser]
        # Create message container
        if sender == 'Assistant':
            message_widget = AutoResizingTextBrowser()
            message_widget.setReadOnly(True)
            message_widget.setStyleSheet(ASSISTANT_MESSAGE_STYLE)
            message_widget.setOpenExternalLinks(True)
            message_widget.setOpenLinks(True)
            message_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            message_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            html_content = markdown.markdown(text)
            message_widget.setHtml(html_content)
        else:
            message_widget = QLabel(text)
            message_widget.setWordWrap(True)
            message_widget.setStyleSheet(USER_MESSAGE_STYLE)
            message_widget.setFixedHeight(message_widget.sizeHint().height())
            message_widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        # Create a container to set alignment
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(10, 5, 10, 5)

        # Set alignment
        if sender == 'User':
            container_layout.addWidget(message_widget, 0, Qt.AlignmentFlag.AlignRight)
        else:
            container_layout.addWidget(message_widget, 0, Qt.AlignmentFlag.AlignTop)

        container.setLayout(container_layout)
        return container

    def update_response(self, chunk: str) -> None:
        if self.assistant_label:
            self.assistant_response_text += chunk
            # Update the content of the message widget
            message_widget = self.assistant_label.findChild(AutoResizingTextBrowser)
            if isinstance(message_widget, AutoResizingTextBrowser):
                html_content = markdown.markdown(self.assistant_response_text)
                message_widget.setHtml(html_content)
            # Auto-scroll to the bottom
            scroll_bar = self.chatScrollArea.verticalScrollBar()
            if scroll_bar:
                scroll_bar.setValue(scroll_bar.maximum())

    def closeEvent(self, event: typing.Optional[QCloseEvent]) -> None:
        if event:
            event.accept()


def main(cli: _api.GraphRAGCli, **kwargs: typing.Any) -> None:
    app = QApplication(sys.argv)

    # Set application palette to dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(23, 23, 23))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)

    window = ChatWindow(cli, **kwargs)
    window.show()
    sys.exit(app.exec())
