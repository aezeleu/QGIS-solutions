from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QSpinBox, QPushButton, QLineEdit, QGroupBox, QMessageBox)
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject, QgsVectorLayer, Qgis
from qgis.gui import QgsMessageBar
import os
import logging

class YearRangeFilterDialog(QDialog):
    def __init__(self, parent=None, iface=None):
        super(YearRangeFilterDialog, self).__init__(parent)
        self.iface = iface
        self.setup_logging()
        self.logger.info("Initializing Year Range Filter Dialog")
        self.setWindowTitle("Kaart Jaar Filter")
        self.setModal(True)
        
        # Check if there's a selected layer before setting up UI
        self.selected_layer = self.get_selected_layer()
        if not self.selected_layer:
            self.logger.warning("No layer selected")
            QMessageBox.warning(self, "Warning", "Please select a layer first!")
            return
            
        # Check if selected layer has required fields
        if not self.check_layer_fields():
            self.logger.warning(f"Layer {self.selected_layer.name()} missing required fields")
            QMessageBox.warning(
                self,
                "Warning",
                f"Layer '{self.selected_layer.name()}' does not have the required fields (beginjaar, eindjaar)!"
            )
            return
            
        self.setup_ui()
    
    def get_selected_layer(self):
        """Get the currently selected layer"""
        if self.iface:
            layer = self.iface.activeLayer()
            self.logger.debug(f"Active layer: {layer.name() if layer else 'None'}")
            return layer
        return None
    
    def check_layer_fields(self):
        """Check if the selected layer has the required fields"""
        if not isinstance(self.selected_layer, QgsVectorLayer):
            self.logger.warning("Selected layer is not a vector layer")
            return False
            
        fields = self.selected_layer.fields()
        field_names = [field.name() for field in fields]
        required_fields = ["beginjaar", "eindjaar"]
        
        has_fields = all(field in field_names for field in required_fields)
        self.logger.debug(f"Layer fields: {field_names}")
        self.logger.debug(f"Has required fields: {has_fields}")
        return has_fields
    
    def setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger('YearRangeFilter')
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        log_file = os.path.join(log_dir, 'year_range_filter.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def setup_ui(self):
        """Setup the user interface components"""
        self.logger.debug("Setting up UI components")
        layout = QVBoxLayout()
        
        # Add selected layer information
        layer_info = QLabel(f"Selected Layer: {self.selected_layer.name()}")
        layer_info.setStyleSheet("font-weight: bold; color: #0066cc;")
        layout.addWidget(layer_info)
        
        # Create property name inputs
        property_group = QGroupBox("Veld Namen")
        property_layout = QVBoxLayout()
        
        # From property
        from_prop_layout = QHBoxLayout()
        from_prop_label = QLabel("Begin Jaar Veld:")
        self.from_property = QLineEdit()
        self.from_property.setText("beginjaar")
        self.from_property.setEnabled(False)  # Make read-only
        from_prop_layout.addWidget(from_prop_label)
        from_prop_layout.addWidget(self.from_property)
        
        # To property
        to_prop_layout = QHBoxLayout()
        to_prop_label = QLabel("Eind Jaar Veld:")
        self.to_property = QLineEdit()
        self.to_property.setText("eindjaar")
        self.to_property.setEnabled(False)  # Make read-only
        to_prop_layout.addWidget(to_prop_label)
        to_prop_layout.addWidget(self.to_property)
        
        property_layout.addLayout(from_prop_layout)
        property_layout.addLayout(to_prop_layout)
        property_group.setLayout(property_layout)
        layout.addWidget(property_group)
        
        # Create year range inputs
        year_group = QGroupBox("Jaar Bereik")
        year_layout = QVBoxLayout()
        
        # From year
        from_layout = QHBoxLayout()
        from_label = QLabel("Van Jaar:")
        self.from_year = QSpinBox()
        self.from_year.setRange(1800, 2100)
        self.from_year.setValue(1842)  # Set to historical start year
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.from_year)
        
        # To year
        to_layout = QHBoxLayout()
        to_label = QLabel("Tot Jaar:")
        self.to_year = QSpinBox()
        self.to_year.setRange(1800, 2100)
        self.to_year.setValue(1900)  # Set to historical end year
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
        
        # Reset Filter button
        reset_btn = QPushButton("Reset Filter")
        reset_btn.clicked.connect(self.reset_filter)
        
        # Apply and Cancel buttons
        action_buttons = QHBoxLayout()
        apply_btn = QPushButton("Toepassen")
        apply_btn.clicked.connect(self.apply_filter)
        cancel_btn = QPushButton("Annuleren")
        cancel_btn.clicked.connect(self.reject)
        
        action_buttons.addWidget(reset_btn)
        action_buttons.addWidget(apply_btn)
        action_buttons.addWidget(cancel_btn)
        layout.addLayout(action_buttons)
        
        self.setLayout(layout)
        self.logger.debug("UI setup completed")
    
    def reset_filter(self):
        """Reset the filter on the selected layer"""
        try:
            if self.selected_layer:
                self.selected_layer.setSubsetString("")
                message = f"Filter reset for layer: {self.selected_layer.name()}"
                self.logger.info(message)
                if self.iface:
                    self.iface.messageBar().pushMessage("Success", message, level=Qgis.Success)
        except Exception as e:
            error_msg = f"Error resetting filter: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            if self.iface:
                self.iface.messageBar().pushMessage("Error", error_msg, level=Qgis.Critical)
    
    def apply_filter(self):
        """Apply the year range filter to the selected layer"""
        try:
            from_year = self.from_year.value()
            to_year = self.to_year.value()
            from_property = self.from_property.text()
            to_property = self.to_property.text()
            
            self.logger.info(f"Applying filter to {self.selected_layer.name()} - "
                           f"Year range: {from_year}-{to_year}")
            
            # Create expression for filtering
            expr = f'"{from_property}" <= {to_year} AND "{to_property}" >= {from_year}'
            self.logger.debug(f"Filter expression: {expr}")
            
            # Apply filter
            self.selected_layer.setSubsetString(expr)
            filtered_count = self.selected_layer.featureCount()
            
            message = f"Filter applied to layer '{self.selected_layer.name()}': {filtered_count} features match"
            self.logger.info(message)
            if self.iface:
                self.iface.messageBar().pushMessage("Success", message, level=Qgis.Success)
            
        except Exception as e:
            error_msg = f"Error applying filter: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            if self.iface:
                self.iface.messageBar().pushMessage("Error", error_msg, level=Qgis.Critical)
        
        self.accept()

class YearRangeFilterPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dialog = None
        
        # Setup logging
        self.logger = logging.getLogger('YearRangeFilter')
        self.logger.info("Plugin initialized")
    
    def initGui(self):
        """Initialize the plugin GUI"""
        from qgis.PyQt.QtWidgets import QAction
        self.action = QAction('Kaart Jaar Filter', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu('Kaart Jaar Filter', self.action)
        self.logger.debug("Plugin GUI initialized")
    
    def unload(self):
        """Clean up when plugin is unloaded"""
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginToMenu('Kaart Jaar Filter', self.action)
        self.logger.info("Plugin unloaded")
    
    def run(self):
        """Run the plugin"""
        self.logger.debug("Running plugin")
        try:
            dialog = YearRangeFilterDialog(self.iface.mainWindow(), self.iface)
            # Setup UI is called in constructor, show dialog if it was set up successfully
            if hasattr(dialog, 'from_year'):  # Check if UI was set up
                dialog.show()
                dialog.exec_()
            self.logger.debug("Dialog execution completed")
        except Exception as e:
            self.logger.error(f"Error running plugin: {str(e)}", exc_info=True)
            QMessageBox.critical(self.iface.mainWindow(), "Error", f"Error running plugin: {str(e)}") 