from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from app.filehandlers import load, save


class FileDialog(QApplication):
    def __init__(self):
        super().__init__([])
        self.title = 'FileDialog'
        self.init_ui()
    
    def init_ui(self):
        self.widget = QWidget()
        self.widget.setWindowTitle(self.title)
        
    def open_file_dialog(self, filter=None):
        path, _ = QFileDialog.getOpenFileName(self.widget, filter=filter)
        if path:
            load(path)
    
    def save_file_dialog(self, filter=None):
        path, _ = QFileDialog.getSaveFileName(self.widget, filter=filter)
        if path:
            save(path)


if __name__ == '__main__':
    app = FileDialog()
    app.open_file_dialog()
    app.exec_()
