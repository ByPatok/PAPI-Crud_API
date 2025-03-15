# Example with PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
import requests
import sys
import json

class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)

class APIWorker(QRunnable):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.signals = WorkerSignals()
        
    def run(self):
        try:
            response = requests.get(self.url)
            data = response.json()
            self.signals.finished.emit(data)
        except Exception as e:
            self.signals.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("API Client")
        self.setGeometry(100, 100, 800, 500)
        
        # Layout
        layout = QVBoxLayout()
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(self.refresh_button)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Idade"])
        layout.addWidget(self.table)
        
        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Thread pool for async operations
        self.threadpool = QThreadPool()
        
        # Initial data load
        self.refresh_data()
        
    def refresh_data(self):
        worker = APIWorker("http://127.0.0.1:8000/items")
        worker.signals.finished.connect(self.update_table)
        worker.signals.error.connect(self.show_error)
        self.threadpool.start(worker)
    
    def update_table(self, data):
        self.table.setRowCount(0)
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(item["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["idade"])))
    
    def show_error(self, error):
        print(f"Error: {error}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())