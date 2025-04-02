from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton
from qgis.utils import iface

def apply_filter(from_year, to_year):
    for layer in QgsProject.instance().mapLayers().values():
        if layer.type() == QgsMapLayer.VectorLayer:
            year_from = layer.customProperty("year_from", None)
            year_to = layer.customProperty("year_to", None)
            
            if year_from is not None and year_to is not None:
                if not (int(year_from) <= to_year and int(year_to) >= from_year):
                    layer.setOpacity(0)  # Hide layer
                else:
                    layer.setOpacity(1)  # Show layer

class YearFilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filter Layers by Year")
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("From Year:"))
        self.from_year = QSpinBox()
        self.from_year.setRange(1900, 2100)
        self.from_year.setValue(2000)
        self.layout.addWidget(self.from_year)

        self.layout.addWidget(QLabel("To Year:"))
        self.to_year = QSpinBox()
        self.to_year.setRange(1900, 2100)
        self.to_year.setValue(2023)
        self.layout.addWidget(self.to_year)

        self.increase_btn = QPushButton("Increase Years")
        self.increase_btn.clicked.connect(self.increase_years)
        self.layout.addWidget(self.increase_btn)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply)
        self.layout.addWidget(self.apply_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.layout.addWidget(self.cancel_btn)

        self.setLayout(self.layout)

    def increase_years(self):
        self.from_year.setValue(self.from_year.value() + 1)
        self.to_year.setValue(self.to_year.value() + 1)

    def apply(self):
        apply_filter(self.from_year.value(), self.to_year.value())
        self.close()

# Run the dialog
filter_dialog = YearFilterDialog()
filter_dialog.exec_()
