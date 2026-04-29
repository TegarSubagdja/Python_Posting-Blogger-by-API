import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QListWidget, QLineEdit, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class Worker(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, links):
        super().__init__()
        self.links = links
        self.running = True

    def run(self):
        while self.running:
            for link in self.links:
                if not self.running:
                    break
                self.log_signal.emit(f"🚀 Processing: {link}")
                time.sleep(2)
            self.log_signal.emit("🔁 Loop selesai, ulang lagi...\n")

    def stop(self):
        self.running = False

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autoblogger")
        self.setMinimumWidth(500)
        self.setMinimumHeight(750)

        # Layout Utama (Satu Kolom Vertikal)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        # --- HEADER SECTION ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Autoblogger Gemini 3 Flash Preview")
        title_label.setObjectName("appTitle")
        subtitle_label = QLabel("v1.0 Pro")
        subtitle_label.setObjectName("appSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        main_layout.addLayout(header_layout)

        # --- SEPARATOR (Perbaikan Error QFrame) ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setObjectName("separatorLine")
        main_layout.addWidget(line)

        # --- INPUT SECTION ---
        main_layout.addWidget(QLabel("Masukkan Tautan Baru:"))
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("https://contoh.com/api/v1")
        main_layout.addWidget(self.input_box)

        # --- MOZAIC BUTTONS (TAMBAH/CLEAR) ---
        input_btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Tambah Ke Antrean")
        self.add_btn.clicked.connect(self.add_link)
        
        self.clear_btn = QPushButton("Bersihkan")
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.clicked.connect(lambda: self.list_widget.clear())

        input_btn_layout.addWidget(self.add_btn, 2)
        input_btn_layout.addWidget(self.clear_btn, 1)
        main_layout.addLayout(input_btn_layout)

        # --- LIST SECTION ---
        main_layout.addWidget(QLabel("Daftar Antrean Proses:"))
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        # --- CONTROL BUTTONS (START/STOP) ---
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("START ENGINE")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.clicked.connect(self.start_loop)

        self.stop_btn = QPushButton("STOP ENGINE")
        self.stop_btn.setObjectName("secondaryBtn")
        self.stop_btn.clicked.connect(self.stop_loop)

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        main_layout.addLayout(control_layout)

        # --- LOG SECTION ---
        main_layout.addWidget(QLabel("Log Aktivitas Real-time:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)
        self.worker = None
        self.setStyleSheet(self.get_style())

    def add_link(self):
        link = self.input_box.text().strip()
        if link:
            self.list_widget.addItem(link)
            self.input_box.clear()

    def start_loop(self):
        links = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if not links:
            self.log("⚠️ Peringatan: Tidak ada tautan.")
            return
        self.worker = Worker(links)
        self.worker.log_signal.connect(self.log)
        self.worker.start()
        self.log("🔥 Mesin dijalankan...")

    def stop_loop(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
            self.log("⛔ Mesin dihentikan.")

    def log(self, text):
        self.log_output.append(text)

    def get_style(self):
        return """
        QWidget {
            background-color: #101015;
            color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        #appTitle { font-size: 20px; font-weight: bold; color: #FFFFFF; }
        #appSubtitle { font-size: 12px; color: #888888; }
        #separatorLine { background-color: #2A2A30; max-height: 1px; }
        
        QLabel { color: #AAAAAA; font-weight: 500; }

        QLineEdit, QTextEdit, QListWidget {
            background-color: #1A1A20;
            border: 1px solid #2A2A30;
            border-radius: 8px;
            padding: 10px;
            color: #FFFFFF;
        }

        QPushButton {
            background-color: #FF5C35;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        QPushButton:hover { background-color: #FF7B5A; }
        
        #secondaryBtn {
            background-color: #1A1A20;
            border: 1px solid #3A3A40;
        }
        #secondaryBtn:hover {
            border: 1px solid #FF5C35;
            color: #FF5C35;
        }
        
        #startBtn { padding: 15px; font-size: 14px; }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())