from PyQt5.QtWidgets import QApplication
from controller import MainApp


def main():
    app = QApplication([])
    win = MainApp()
    win.show()
    app.exit(app.exec_())

if __name__ == "__main__":
    main()