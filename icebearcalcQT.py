import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("icebearcalcQT")
        self.setGeometry(100, 100, 300, 400)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(50)
        font = self.display.font()
        font.setPointSize(24)
        self.display.setFont(font)
        main_layout.addWidget(self.display)

        buttons_grid = QGridLayout()
        main_layout.addLayout(buttons_grid)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('CE', 4, 1)
        ]

        self.current_input = ""
        self.operator = None
        self.first_operand = None
        self.new_input = True

        for label, row, col in buttons:
            button = QPushButton(label)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn_font = button.font()
            btn_font.setPointSize(18)
            button.setFont(btn_font)
            button.clicked.connect(lambda _, l=label: self.on_button_clicked(l))
            buttons_grid.addWidget(button, row, col)

    def on_button_clicked(self, button_label):
        if button_label.isdigit() or button_label == '.':
            if self.new_input:
                self.current_input = button_label
                self.new_input = False
            else:
                if button_label == '.' and '.' in self.current_input:
                    return
                self.current_input += button_label
            self.display.setText(self.current_input)

        elif button_label in ('+', '-', '*', '/'):
            if self.first_operand is None:
                try:
                    self.first_operand = float(self.current_input)
                except ValueError:
                    self.display.setText("Error")
                    self.reset_calculator()
                    return
            else:
                self.calculate_result()
            self.operator = button_label
            self.new_input = True
            self.display.setText(str(self.first_operand))

        elif button_label == '=':
            self.calculate_result()
            self.operator = None
            self.new_input = True

        elif button_label == 'C':
            self.reset_calculator()
            self.display.setText("0")

        elif button_label == 'CE':
            self.current_input = ""
            self.display.setText("0")
            self.new_input = True

    def calculate_result(self):
        if self.first_operand is None or self.operator is None or not self.current_input:
            return

        try:
            second_operand = float(self.current_input)
            result = 0

            if self.operator == '+':
                result = self.first_operand + second_operand
            elif self.operator == '-':
                result = self.first_operand - second_operand
            elif self.operator == '*':
                result = self.first_operand * second_operand
            elif self.operator == '/':
                if second_operand == 0:
                    self.display.setText("Error: Div by 0")
                    self.reset_calculator()
                    return
                result = self.first_operand / second_operand

            if result == int(result):
                self.display.setText(str(int(result)))
            else:
                self.display.setText(str(result))

            self.first_operand = result
            self.current_input = str(result)
            self.new_input = True

        except ValueError:
            self.display.setText("Error")
            self.reset_calculator()
        except Exception as e:
            self.display.setText(f"Error: {e}")
            self.reset_calculator()

    def reset_calculator(self):
        self.current_input = ""
        self.operator = None
        self.first_operand = None
        self.new_input = True

def main():
    app = QApplication(sys.argv)
    win = CalculatorWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
