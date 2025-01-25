# Import required libraries

import sys
import os
from zipfile import error

import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic, Qt
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from holoviews.examples.reference.apps.bokeh.player import layout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import seaborn as sns

# Create a Class and set basics

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Energy Consumption Dashboard')
        uic.loadUi("energy-consumption-dashboard.ui", self)

        # find and connect the button 01 (cost of energy)
        self.totcostofenergy_btn = self.findChild(QPushButton, 'totcostofenergy_btn')
        self.totcostofenergy_btn.clicked.connect(self.showcostofenergy)
        self.vertical_layout = self.findChild(QVBoxLayout, 'verticalLayout')

        # Create layout to show button 01 (cost of energy)
        self.cost_label = QLabel("")
        self.vertical_layout.addWidget(self.cost_label)

        # find and connect the button 02 (energy consumption):
        self.totenergyconsumption_btn = self.findChild(QPushButton, 'totenergyconsumption_btn')
        self.totenergyconsumption_btn.clicked.connect(self.energyconsumptioncost)
        self.vertical_layout2 = self.findChild(QVBoxLayout, 'verticalLayout')

        # Create layout to show button 02 (energy consumption):
        self.cost_label1 = QLabel("")
        self.vertical_layout2.addWidget(self.cost_label1)

        # find and connect the button 03 (top 5 cities by consumption):
        self.top5byenergy_btn = self.findChild(QPushButton, 'top5byenergy_btn')
        self.top5byenergy_btn.clicked.connect(self.top5byenergy)
        self.vertical_layout3 = self.findChild(QVBoxLayout, 'verticalLayout')

        # Create layout to show graph for button 03 (top 5 cities by consumption):
        self.cost_label3 = QLabel("")
        self.vertical_layout3.addWidget(self.cost_label3)

        # find and connect the button 04 (top 5 cities by cost):
        self.top5bycost_btn = self.findChild(QPushButton, 'top5bycost_btn')
        self.top5bycost_btn.clicked.connect(self.top5bycost)
        self.vertical_layout4 = self.findChild(QVBoxLayout, 'verticalLayout')

        # Create layout to show graph for button 04 (top 5 cities by cost):
        self.cost_label3 = QLabel("")
        self.vertical_layout4.addWidget(self.cost_label)

        # find and connect the reset button (R)
        self.Reset_btn = self.findChild(QPushButton, 'Reset_btn')
        self.Reset_btn.clicked.connect(self.reset)
        self.vertical_layout = self.findChild(QVBoxLayout, 'verticalLayout')

    # Write value to show for cost of energy
    def showcostofenergy(self):
        self.cost_label1.setText("")
        self.clear_graph()
        costofenergy = "USD 994"
        self.cost_label.setText(f"Total Cost of Energy is {costofenergy}")

        # Formatting the text
        self.cost_label.setAlignment(Qt.AlignCenter)
        font = self.cost_label.font()
        font.setBold(True)
        font.setPointSize(40)
        self.cost_label.setFont(font)

    # Write value to show total energy consumption
    def energyconsumptioncost(self):
        self.cost_label.setText("")
        self.clear_graph()
        energyconsumption = "2,808 (kWh)"
        self.cost_label1.setText(f"Total Energy Consumption is {energyconsumption}")

        # Formatting the text
        self.cost_label1.setAlignment(Qt.AlignCenter)
        font = self.cost_label1.font()
        font.setBold(True)
        font.setPointSize(40)
        self.cost_label1.setFont(font)


    def reset(self):
        self.cost_label.setText("")
        self.cost_label1.setText("")
        self.clear_graph()

    def clear_graph(self):
        for i in reversed(range(self.vertical_layout3.count())):
            widget = self.vertical_layout3.itemAt(i).widget()
            if widget and not isinstance(widget, QLabel):
                widget.deleteLater()

    def clear_graph(self):
        for i in reversed(range(self.vertical_layout4.count())):
            widget = self.vertical_layout4.itemAt(i).widget()
            if widget and not isinstance(widget, QLabel):
                widget.deleteLater()




    def top5byenergy(self):
         try:
             # Clear any existing graph in the layout
            self.clear_graph()

             # Clear both texts
            self.cost_label.setText("")
            self.cost_label1.setText("")

            # Run validation
            # self.validation()

            # Read and process the data
            top5byenergy = pd.read_csv("energy_consumption_data.csv")
            top5byenergy = top5byenergy.nlargest(5, "Energy Consumption (kWh)")


            # Create the plot
            figure = plt.figure(figsize=(10, 5))
            ax = figure.add_subplot(111)
            sns.barplot(x="Location", y="Energy Consumption (kWh)", data=top5byenergy, ax=ax, palette=sns.color_palette("RdYlGn", 5))

            # Add formatting
            ax.set_xlabel('Location')
            ax.set_ylabel('Energy Consumption (kWh)')
            ax.set_title('Top 5 Cities by Energy Consumption')

            # Add labels on top of bars
            for index, value in enumerate(top5byenergy['Energy Consumption (kWh)']):
                rounded_value = round(value, 1)
                ax.text(index, value + 20, f'{rounded_value}', ha='center', va='center', fontsize=10)

            # Embed the plot in the GUI
            canvas = FigureCanvas(figure)
            self.vertical_layout3.addWidget(canvas)
            canvas.draw()
         except Exception as e:
            print(f"Error: {e}")


    def top5bycost(self):
         try:
            # Clear any existing graph in the layout
            self.clear_graph()

            # Clear both texts
            self.cost_label.setText("")
            self.cost_label1.setText("")

            # Read and process the data
            top5bycost = pd.read_csv("energy_consumption_data.csv")

            top5bycost = top5bycost.nlargest(5, "Cost")


            # Create the plot
            figure = plt.figure(figsize=(10, 5))
            ax = figure.add_subplot(111)
            sns.barplot(x="Location", y="Cost", data=top5bycost, ax=ax, palette=sns.color_palette("RdYlGn", n_colors=5))

            # Add formatting
            ax.set_xlabel('Location')
            ax.set_ylabel('Cost')
            ax.set_title('Top 5 Cities by Cost (£)')

            # Add labels on top of bars
            for index, value in enumerate(top5bycost['Cost']):
                rounded_value = round(value, 1)
                ax.text(index, value + 20, f'{rounded_value}', ha='center', va='center', fontsize=10)

            # Embed the plot in the GUI
            canvas = FigureCanvas(figure)
            self.vertical_layout3.addWidget(canvas)
            canvas.draw()
         except Exception as e:
            print(f"Error: {e}")

# Initialize application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
