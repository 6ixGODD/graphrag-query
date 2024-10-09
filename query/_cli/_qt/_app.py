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
    QCloseEvent,
    QColor,
    QFont,
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
QTextEdit {
    background-color: #2F2F2F; 
    color: #FFFFFF;  /* White font color */
    border: none;
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border-top-right-radius: 8px;
}
QTextEdit:focus {
    border: 1px solid #FFFFFF;  /* White border */
}
QPushButton {
    background-color: #808080;  /* Gray background */
    color: #FFFFFF;  /* White font color */
    border: none;
    padding: 5px;
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border-top-right-radius: 8px;
}
QPushButton:hover {
    background-color: #696969;  /* Dark gray hover effect */
}
"""

USER_MESSAGE_STYLE = """
QLabel {
    background-color: #808080;  /* Gray background */
    padding: 5px;
    color: #FFFFFF;  /* White font color */
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border-top-right-radius: 0px;  
}
QLabel:hover {
    background-color: #696969;  /* Dark gray hover effect */
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


# noinspection PyUnresolvedReferences
class ChatWorker(QObject):
    finished = pyqtSignal()
    responseReady = pyqtSignal(str)

    def __init__(self, message: str, cli) -> None:
        super().__init__()
        self.message: str = message
        self.cli = cli

    def run(self) -> None:
        response = self.cli.chat(self.message)
        if self.cli.stream:
            response = typing.cast(typing.Iterator[str], response)
            for chunk in response:
                self.responseReady.emit(chunk)
        else:
            response = typing.cast(str, response)
            self.responseReady.emit(response)
        self.finished.emit()


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
    def __init__(self, cli: _api.GraphRAGCli) -> None:
        super().__init__()
        self.cli = cli

        self.assistant_label: typing.Optional[QWidget] = None
        self.assistant_response_text: str = ''
        self.setWindowTitle('Chat with GraphRAG')
        self.resize(600, 500)
        self.layout_ = QVBoxLayout()

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

        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.send_message)

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inputText)
        inputLayout.addWidget(self.sendButton)

        self.layout_.addWidget(self.chatScrollArea)
        self.layout_.addLayout(inputLayout)
        self.setLayout(self.layout_)
        self.thread_: typing.Optional[QThread] = None
        self.worker: typing.Optional[ChatWorker] = None

        self.setStyleSheet(CHAT_WINDOW_STYLE)

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
        self.worker = ChatWorker(message, cli=self.cli)
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


def main(cli: _api.GraphRAGCli) -> None:
    app = QApplication(sys.argv)

    # Set application palette to dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(23, 23, 23))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)

    window = ChatWindow(cli)
    window.show()
    sys.exit(app.exec())
