# professional_bot_final.py

import sys
import time
import random
import pyautogui
import pyperclip
from pynput import mouse
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QSpinBox, QListWidget, 
                             QGroupBox, QGridLayout, QCheckBox, QLineEdit, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtGui import QIcon, QPixmap

SVG_ADD = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
"""
SVG_REMOVE = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
"""

APP_STYLESHEET = """
    * {
        font-family: Segoe UI, sans-serif;
        color: #e0e0e0;
    }
    QMainWindow {
        background-color: #1e2124;
    }
    QGroupBox {
        font-weight: bold;
        font-size: 10pt;
        background-color: #282b30;
        border: 1px solid #424549;
        border-radius: 6px;
        margin-top: 20px;
        padding-top: 20px;
    }
    QGroupBox::title {
        subcontrol-origin: border;
        subcontrol-position: top left;
        padding: 4px 12px;
        margin-left: 15px;
        background-color: #00a896;
        color: #ffffff;
        border-radius: 4px;
    }
    QLabel, QCheckBox {
        font-size: 10pt;
    }
    QLineEdit, QListWidget, QSpinBox {
        background-color: #36393e;
        border: 1px solid #424549;
        border-radius: 4px;
        padding: 8px;
        font-size: 10pt;
    }
    QLineEdit:focus, QListWidget:focus, QSpinBox:focus {
        border: 1px solid #00a896;
    }
    QListWidget::item:hover {
        background-color: #424549;
    }
    QListWidget::item:selected {
        background-color: #00a896;
        color: #ffffff;
    }
    QPushButton {
        font-size: 10pt;
        font-weight: bold;
        background-color: #40444b;
        border: 1px solid #5d6167;
        padding: 10px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #5d6167;
    }
    QPushButton:pressed {
        background-color: #4f5359;
    }
    QPushButton#start_button {
        background-color: #00a896;
        border: 1px solid #00a896;
        color: #ffffff;
    }
    QPushButton#start_button:hover {
        background-color: #00c4ac;
    }
    QPushButton#remove_comment_button {
        background-color: #992b2b;
        border: 1px solid #992b2b;
    }
    QPushButton#remove_comment_button:hover {
        background-color: #a83232;
    }
    QPushButton:disabled {
        background-color: #282b30;
        color: #5d6167;
        border: 1px solid #424549;
    }
    QLabel#credit_label {
        font-size: 8pt;
        color: #5d6167;
    }
    QLabel#credit_label:hover {
        color: #8e9297;
    }
"""
def create_svg_icon(svg_data):
    pixmap = QPixmap()
    pixmap.loadFromData(svg_data.encode('utf-8'))
    return QIcon(pixmap)

class BotWorker(QThread):
    status_update = pyqtSignal(str)
    def __init__(self, chat_coords, button_coords, comments, interval):
        super().__init__()
        self.chat_coords = chat_coords
        self.button_coords = button_coords
        self.comments = comments
        self.interval = interval
        self.is_running = True
    def run(self):
        self.status_update.emit("Iniciando robô...")
        while self.is_running:
            try:
                comment_to_post = random.choice(self.comments)
                self.status_update.emit(f"Clicando no chat: {self.chat_coords}")
                pyautogui.moveTo(self.chat_coords[0], self.chat_coords[1], duration=0.2)
                pyautogui.click()
                time.sleep(0.5)
                self.status_update.emit(f"Enviando: '{comment_to_post[:25]}...'")
                pyperclip.copy(comment_to_post)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                self.status_update.emit(f"Clicando no botão: {self.button_coords}")
                pyautogui.moveTo(self.button_coords[0], self.button_coords[1], duration=0.2)
                pyautogui.click()
                self.status_update.emit(f"Ação concluída. Aguardando {self.interval}s...")
            except Exception as e:
                self.status_update.emit(f"Erro no loop: {e}")
            for _ in range(self.interval):
                if not self.is_running: break
                time.sleep(1)
        self.status_update.emit("Robô parado.")
    def stop(self):
        self.is_running = False
        self.status_update.emit("Parando robô...")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartBot Pro")
        self.setGeometry(100, 100, 500, 650)
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowIcon(create_svg_icon(SVG_ADD))
        self.chat_coords = None
        self.button_coords = None
        self.current_interval = 30
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 5, 15, 15)
        main_layout.setSpacing(10)
        capture_group = QGroupBox("1. Posições do Mouse")
        capture_layout = QGridLayout()
        capture_layout.setContentsMargins(10, 10, 10, 10)
        self.capture_chat_button = QPushButton("Capturar Chat")
        self.chat_status_label = QLabel("Não definida")
        self.capture_button_button = QPushButton("Capturar Botão")
        self.button_status_label = QLabel("Não definida")
        capture_layout.addWidget(self.capture_chat_button, 0, 0)
        capture_layout.addWidget(self.chat_status_label, 0, 1, Qt.AlignmentFlag.AlignRight)
        capture_layout.addWidget(self.capture_button_button, 1, 0)
        capture_layout.addWidget(self.button_status_label, 1, 1, Qt.AlignmentFlag.AlignRight)
        capture_group.setLayout(capture_layout)
        comments_group = QGroupBox("2. Lista de Comentários")
        comments_layout = QVBoxLayout()
        self.comment_list_widget = QListWidget()
        comment_input_layout = QHBoxLayout()
        self.new_comment_input = QLineEdit()
        self.new_comment_input.setPlaceholderText("Digite um novo comentário aqui...")
        self.add_comment_button = QPushButton()
        self.add_comment_button.setIcon(create_svg_icon(SVG_ADD))
        self.add_comment_button.setToolTip("Adicionar Comentário")
        comment_input_layout.addWidget(self.new_comment_input)
        comment_input_layout.addWidget(self.add_comment_button)
        self.remove_comment_button = QPushButton("Remover Selecionado")
        self.remove_comment_button.setObjectName("remove_comment_button")
        self.remove_comment_button.setIcon(create_svg_icon(SVG_REMOVE))
        comments_layout.addWidget(self.comment_list_widget)
        comments_layout.addLayout(comment_input_layout)
        comments_layout.addWidget(self.remove_comment_button)
        comments_group.setLayout(comments_layout)
        time_group = QGroupBox("3. Intervalo de Tempo")
        time_layout = QVBoxLayout()
        self.predefined_time_buttons = {}
        predefined_layout = QGridLayout()
        times = [5, 10, 15, 20, 30, 45, 60, 90]
        for i, t in enumerate(times):
            btn = QPushButton(f"{t} s")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, time=t: self.set_predefined_time(time))
            self.predefined_time_buttons[t] = btn
            predefined_layout.addWidget(btn, i // 4, i % 4)
        time_layout.addLayout(predefined_layout)
        custom_time_layout = QHBoxLayout()
        self.custom_time_checkbox = QCheckBox("Personalizado")
        self.custom_interval_input = QSpinBox()
        self.custom_interval_input.setRange(1, 10000)
        self.custom_interval_input.setEnabled(False)
        custom_time_layout.addWidget(self.custom_time_checkbox)
        custom_time_layout.addWidget(self.custom_interval_input, 1)
        time_layout.addLayout(custom_time_layout)
        time_group.setLayout(time_layout)
        control_group = QGroupBox("4. Controle")
        control_layout = QVBoxLayout()
        self.start_button = QPushButton("INICIAR ROBÔ")
        self.start_button.setObjectName("start_button")
        self.stop_button = QPushButton("PARAR")
        self.status_label = QLabel("Pronto para capturar posições.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.status_label)
        control_group.setLayout(control_layout)
        self.credit_label = QLabel("SmartBot Pro - Desenvolvido com ❤ Por Luan Dev")
        self.credit_label.setObjectName("credit_label")
        self.credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credit_label.mousePressEvent = self.show_credits
        main_layout.addWidget(capture_group)
        main_layout.addWidget(comments_group)
        main_layout.addWidget(time_group)
        main_layout.addWidget(control_group)
        main_layout.addStretch()
        main_layout.addWidget(self.credit_label)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.connect_signals()
        self.set_predefined_time(30)
    def connect_signals(self):
        self.capture_chat_button.clicked.connect(lambda: self.start_capture('chat'))
        self.capture_button_button.clicked.connect(lambda: self.start_capture('button'))
        self.add_comment_button.clicked.connect(self.add_comment)
        self.new_comment_input.returnPressed.connect(self.add_comment)
        self.remove_comment_button.clicked.connect(self.remove_comment)
        self.custom_time_checkbox.toggled.connect(self.toggle_custom_time)
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button.clicked.connect(self.stop_bot)
    def show_credits(self, event):
        QMessageBox.about(self, "Sobre o SmartBot Pro",
            "<h2>SmartBot Pro v1.0</h2>"
            "<p>Este aplicativo foi criado para automação visual de tarefas repetitivas, usando captura de coordenadas e controle de mouse/teclado.</p>"
            "<p>Desenvolvido por Luan Dev 09/09/25.</p>"
        )
    def set_predefined_time(self, time):
        self.current_interval = time
        for t, btn in self.predefined_time_buttons.items():
            btn.setChecked(t == time)
        self.status_label.setText(f"Intervalo definido para {time} segundos.")
    def toggle_custom_time(self, checked):
        self.custom_interval_input.setEnabled(checked)
        for btn in self.predefined_time_buttons.values():
            btn.setEnabled(not checked)
        if not checked:
            self.set_predefined_time(self.current_interval)
        else:
            for btn in self.predefined_time_buttons.values():
                btn.setChecked(False)
    def add_comment(self):
        comment = self.new_comment_input.text().strip()
        if comment:
            self.comment_list_widget.addItem(comment)
            self.new_comment_input.clear()
    def remove_comment(self):
        selected_items = self.comment_list_widget.selectedItems()
        if not selected_items: return
        for item in selected_items:
            self.comment_list_widget.takeItem(self.comment_list_widget.row(item))
    def start_bot(self):
        if not self.chat_coords or not self.button_coords:
            self.update_status("Erro: Capture as duas posições!")
            return
        comments = [self.comment_list_widget.item(i).text() for i in range(self.comment_list_widget.count())]
        if not comments:
            self.update_status("Erro: Adicione pelo menos um comentário à lista!")
            return
        if self.custom_time_checkbox.isChecked():
            interval = self.custom_interval_input.value()
        else:
            interval = self.current_interval
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.worker = BotWorker(self.chat_coords, self.button_coords, comments, interval)
        self.worker.status_update.connect(self.update_status)
        self.worker.finished.connect(self.bot_finished)
        self.worker.start()
    def start_capture(self, target):
        self.status_label.setText(f"Modo de Captura: Clique no local do '{target}'...")
        self.hide()
        listener = mouse.Listener(on_click=lambda x, y, btn, p: self.on_click_capture(x, y, btn, p, target))
        listener.start()
        self.capture_listener = listener
    def on_click_capture(self, x, y, button, pressed, target):
        if pressed:
            if target == 'chat':
                self.chat_coords = (x, y)
                self.chat_status_label.setText(f"OK ({x}, {y})")
            elif target == 'button':
                self.button_coords = (x, y)
                self.button_status_label.setText(f"OK ({x}, {y})")
            self.status_label.setText(f"Posição de '{target}' capturada!")
            self.show()
            self.capture_listener.stop()
    def stop_bot(self):
        if self.worker: self.worker.stop()
    def update_status(self, message):
        self.status_label.setText(message)
    def bot_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    def closeEvent(self, event):
        self.stop_bot()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())