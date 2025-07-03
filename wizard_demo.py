import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("WIZZARD Demo")

    layout = QVBoxLayout()
    label = QLabel("Willkommen zum WIZZARD Tool!")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
