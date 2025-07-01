import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CalculatorWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Ice Bear's GTK Calculator App")
        self.set_default_size(300, 400)
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.display = Gtk.Entry()
        self.display.set_editable(False)
        self.display.set_text("0")
        self.display.set_alignment(1.0)
        self.display.set_margin_bottom(10)
        vbox.pack_start(self.display, True, True, 0)

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        vbox.pack_start(grid, True, True, 0)

        buttons = [
            ('7', 0, 0), ('8', 1, 0), ('9', 2, 0), ('/', 3, 0),
            ('4', 0, 1), ('5', 1, 1), ('6', 2, 1), ('*', 3, 1),
            ('1', 0, 2), ('2', 1, 2), ('3', 2, 2), ('-', 3, 2),
            ('0', 0, 3), ('.', 1, 3), ('=', 2, 3), ('+', 3, 3),
            ('C', 0, 4), ('CE', 1, 4)
        ]

        self.current_input = ""
        self.operator = None
        self.first_operand = None
        self.new_input = True

        for label, col, row in buttons:
            button = Gtk.Button(label=label)
            button.connect("clicked", self.on_button_clicked, label)
            grid.attach(button, col, row, 1, 1)

    def on_button_clicked(self, widget, button_label):
        if button_label.isdigit() or button_label == '.':
            if self.new_input:
                self.current_input = button_label
                self.new_input = False
            else:
                if button_label == '.' and '.' in self.current_input:
                    return
                self.current_input += button_label
            self.display.set_text(self.current_input)

        elif button_label in ('+', '-', '*', '/'):
            if self.first_operand is None:
                try:
                    self.first_operand = float(self.current_input)
                except ValueError:
                    self.display.set_text("Error")
                    self.reset_calculator()
                    return
            else:
                self.calculate_result()
            self.operator = button_label
            self.new_input = True
            self.display.set_text(f"{self.first_operand} {self.operator}")

        elif button_label == '=':
            self.calculate_result()
            self.operator = None
            self.new_input = True

        elif button_label == 'C':
            self.reset_calculator()
            self.display.set_text("0")

        elif button_label == 'CE':
            self.current_input = ""
            self.display.set_text("0")
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
                    self.display.set_text("Error: Div by 0")
                    self.reset_calculator()
                    return
                result = self.first_operand / second_operand

            if result == int(result):
                self.display.set_text(str(int(result)))
            else:
                self.display.set_text(str(result))

            self.first_operand = result
            self.current_input = str(result)
            self.new_input = True

        except ValueError:
            self.display.set_text("Error")
            self.reset_calculator()
        except Exception as e:
            self.display.set_text(f"Error: {e}")
            self.reset_calculator()

    def reset_calculator(self):
        self.current_input = ""
        self.operator = None
        self.first_operand = None
        self.new_input = True

def main():
    win = CalculatorWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
