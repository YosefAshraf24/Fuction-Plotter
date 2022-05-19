import re
import sys

import numpy as np
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

DEFAULT_FONT = QFont('Times', 14)

# allowed words
allowed_words = ['x','sin','cos','sqrt','exp','/','+','*','^','-']

# for converting from string to mathematical expression
replacements = {'sin': 'np.sin','cos': 'np.cos','exp': 'np.exp','sqrt': 'np.sqrt','^': '**',}

# convert from string to mathematical expression
def StringToFunction(string):

    # find words and check if all are allowed
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise ValueError(
                f"'{word}' is forbidden to use\n"
            )

    for before, after in replacements.items():
        string = string.replace(before, after)

    # if function is constant
    if "x" not in string:
        string = f"{string}+0*x"

    def function(x):
         return eval(string)

    return function

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")
        self.setFixedHeight(750)
        self.setFixedWidth(750)

        #  create widgets
        self.view = FigureCanvas()
        self.axes = self.view.figure.subplots()

        # min and max values of x
        self.n = QLabel("Min x: ")
        self.n.setFont(DEFAULT_FONT)
        self.x = QLabel("Max x: ")
        self.x.setFont(DEFAULT_FONT)
        self.mn = QDoubleSpinBox()
        self.mx = QDoubleSpinBox()
        self.mn.setFixedWidth(275)
        self.mx.setFixedWidth(275)
        self.mn.setMinimum(-9999999)
        self.mn.setMaximum(9999999)
        self.mx.setMinimum(-9999999)
        self.mx.setMaximum(9999999)
        self.mn.setFont(DEFAULT_FONT)
        self.mx.setFont(DEFAULT_FONT)
        self.mn.setValue(0)
        self.mx.setValue(10)

        # Create function of x
        self.function = QLineEdit()
        self.function.setPlaceholderText("Ex: 5*x^3 + 2*x")
        self.function.setFont(DEFAULT_FONT)
        self.func_label = QLabel("f(x): ")
        self.func_label.setFont(DEFAULT_FONT)
        self.submit = QPushButton("Plot")
        self.submit.setFixedHeight(50)
        self.submit.setFixedWidth(275)
        self.submit.setFont(DEFAULT_FONT)

        #  Create layout
        la_func = QHBoxLayout()
        la_func.addWidget(self.func_label)
        la_func.addWidget(self.function)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.view)
        vLayout.addLayout(la_func)
        vLayout.addWidget(self.n)
        vLayout.addWidget(self.mn)
        vLayout.addWidget(self.x)
        vLayout.addWidget(self.mx)
        vLayout.addWidget(self.submit)
        self.setLayout(vLayout)

        self.error_dialog = QMessageBox()
        self.error_dialog.setWindowTitle("Error!!")
        self.error_dialog.setFont(DEFAULT_FONT)
        self.error_dialog.setWindowIcon(QIcon("e.png"))



        # connect inputs with on_change method
        self.mn.valueChanged.connect(lambda _: self.on_change(1))
        self.mx.valueChanged.connect(lambda _: self.on_change(2))
        self.submit.clicked.connect(lambda _: self.on_change(3))

    def on_change(self, idx):
        mn = self.mn.value()
        mx = self.mx.value()

        if idx == 1 and mn >= mx:
            self.mx.setValue(mx - 1)
            self.error_dialog.setText("'min x' should be less than 'max x'.")
            self.error_dialog.show()
            return
        elif idx == 2 and mx <= mn:
            self.mx.setValue(mn + 1)
            self.error_dialog.setText("'max x' should be greater than 'min x'.")
            self.error_dialog.show()
            return
        else :
            x = np.linspace(mn, mx)
            try:
                y = StringToFunction(self.function.text())(x)
            except ValueError as e:
                self.error_dialog.setText(str(e))
                self.error_dialog.show()
                return

            self.axes.clear()
            self.axes.plot(x, y)
            self.view.draw()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PlotWidget()
    w.show()
    sys.exit(app.exec_())