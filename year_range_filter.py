from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QSpinBox, QPushButton, QLineEdit, QGroupBox)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject

class YearRangeFilterDialog(QDialog):
    def __init__(self, parent=None):
        super(YearRangeFilterDialog, self).__init__(parent)
        self.setWindowTitle("Year Range Filter")
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create property name inputs
        property_group = QGroupBox("Property Names")
        property_layout = QVBoxLayout()
        
        # From property
        from_prop_layout = QHBoxLayout()
        from_prop_label = QLabel("From Property:")
        self.from_property = QLineEdit()
        self.from_property.setText("year_from")
        from_prop_layout.addWidget(from_prop_label)
        from_prop_layout.addWidget(self.from_property)
        
        # To property
        to_prop_layout = QHBoxLayout()
        to_prop_label = QLabel("To Property:")
        self.to_property = QLineEdit()
        self.to_property.setText("year_to")
        to_prop_layout.addWidget(to_prop_label)
        to_prop_layout.addWidget(self.to_property)
        
        property_layout.addLayout(from_prop_layout)
        property_layout.addLayout(to_prop_layout)
        property_group.setLayout(property_layout)
        layout.addWidget(property_group)
        
        # Create year range inputs
        year_group = QGroupBox("Year Range")
        year_layout = QVBoxLayout()
        
        # From year
        from_layout = QHBoxLayout()
        from_label = QLabel("From Year:")
        self.from_year = QSpinBox()
        self.from_year.setRange(1900, 2100)
        self.from_year.setValue(2000)
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.from_year)
        
        # To year
        to_layout = QHBoxLayout()
        to_label = QLabel("To Year:")
        self.to_year = QSpinBox()
        self.to_year.setRange(1900, 2100)
        self.to_year.setValue(2023)
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_year)
        
        year_layout.addLayout(from_layout)
        year_layout.addLayout(to_layout)
        year_group.setLayout(year_layout)
        layout.addWidget(year_group)
        
        # Create buttons
        button_layout = QHBoxLayout()
        
        # Increase buttons
        increase_from_btn = QPushButton("+")
        increase_from_btn.clicked.connect(lambda: self.from_year.setValue(self.from_year.value() + 1))
        increase_to_btn = QPushButton("+")
        increase_to_btn.clicked.connect(lambda: self.to_year.setValue(self.to_year.value() + 1))
        
        button_layout.addWidget(increase_from_btn)
        button_layout.addWidget(increase_to_btn)
        layout.addLayout(button_layout)
        
        # Apply and Cancel buttons
        action_buttons = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_filter)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        action_buttons.addWidget(apply_btn)
        action_buttons.addWidget(cancel_btn)
        layout.addLayout(action_buttons)
        
        self.setLayout(layout)
    
    def apply_filter(self):
        from_year = self.from_year.value()
        to_year = self.to_year.value()
        from_property = self.from_property.text()
        to_property = self.to_property.text()
        
        # Get all layers
        project = QgsProject.instance()
        layers = project.mapLayers().values()
        
        for layer in layers:
            # Check if layer has the specified properties
            if hasattr(layer, from_property) and hasattr(layer, to_property):
                layer_from_year = getattr(layer, from_property)
                layer_to_year = getattr(layer, to_property)
                
                # Show layer if year range overlaps with specified range
                layer.setVisibility(
                    (layer_from_year <= to_year and layer_to_year >= from_year)
                )
            else:
                # Hide layers without the required properties
                layer.setVisibility(False)
        
        self.accept()

def classFactory(iface):
    return YearRangeFilterPlugin(iface)

class YearRangeFilterPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dialog = None
    
    def initGui(self):
        from qgis.PyQt.QtWidgets import QAction
        self.action = QAction('Year Range Filter', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu('Year Range Filter', self.action)
    
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu('Year Range Filter', self.action)
    
    def run(self):
        if not self.dialog:
            self.dialog = YearRangeFilterDialog(self.iface.mainWindow())
        self.dialog.show() 