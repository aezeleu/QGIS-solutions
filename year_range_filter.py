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
            # Parent the QMessageBox to self for proper display if iface is None (e.g. during tests)
            QMessageBox.warning(self, "Warning", "Please select a layer first!")
            # We need to ensure that the object is fully initialized before returning
            # otherwise it can lead to issues, especially in testing environments.
            # One way is to set a flag and check it before showing.
            self._ui_initialized = False
            return

        # Check if selected layer has required fields
        if not self.check_layer_fields():
            self.logger.warning(f"Layer {self.selected_layer.name()} missing required fields")
            QMessageBox.warning(
                self,
                "Warning",
                f"Layer '{self.selected_layer.name()}' does not have the required fields (beginjaar, eindjaar)!"
            )
            self._ui_initialized = False
            return

        self.setup_ui()
        self._ui_initialized = True # Flag to indicate UI is ready

    def get_selected_layer(self):
        """Get the currently selected layer"""
        if self.iface:
            layer = self.iface.activeLayer()
            if layer:
                self.logger.debug(f"Active layer: {layer.name()}")
            else:
                self.logger.debug("No active layer found.")
            return layer
        # Fallback for testing when iface might not be available
        self.logger.debug("No iface available to get selected layer (e.g., during testing).")
        return None


    def check_layer_fields(self):
        """Check if the selected layer has the required fields"""
        if not self.selected_layer: # Ensure selected_layer is not None
            self.logger.warning("No layer available to check fields.")
            return False
        if not isinstance(self.selected_layer, QgsVectorLayer):
            self.logger.warning(f"Selected item '{self.selected_layer.name()}' is not a vector layer.")
            return False

        fields = self.selected_layer.fields()
        field_names = [field.name() for field in fields]
        required_fields = ["beginjaar", "eindjaar"] # Hardcoded as per current UI

        has_fields = all(field in field_names for field in required_fields)
        self.logger.debug(f"Layer fields: {field_names}")
        self.logger.debug(f"Required fields: {required_fields}")
        self.logger.debug(f"Has required fields: {has_fields}")
        return has_fields

    def setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger('YearRangeFilter')
        # Check if handlers are already present to avoid duplication if class is instantiated multiple times
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            # Create logs directory if it doesn't exist
            # __file__ is the path to the current script (year_range_filter.py)
            plugin_dir = os.path.dirname(__file__)
            log_dir = os.path.join(plugin_dir, 'logs')
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except OSError as e:
                    # This can happen if the plugin is in a read-only location
                    # or due to permission issues.
                    # Fallback or notify user. For now, log to console.
                    print(f"Could not create log directory: {log_dir}. Error: {e}")
                    # Add a console handler as a fallback if file handler fails
                    console_handler = logging.StreamHandler()
                    console_handler.setLevel(logging.DEBUG)
                    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    console_handler.setFormatter(console_formatter)
                    self.logger.addHandler(console_handler)
                    self.logger.warning("Logging to console as log file setup failed.")
                    return


            # File handler
            log_file = os.path.join(log_dir, 'year_range_filter.log')
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            except IOError as e:
                print(f"Could not set up log file: {log_file}. Error: {e}")
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                console_handler.setFormatter(console_formatter)
                self.logger.addHandler(console_handler)
                self.logger.warning("Logging to console as log file setup failed.")


    def setup_ui(self):
        """Setup the user interface components"""
        self.logger.debug("Setting up UI components")
        layout = QVBoxLayout()

        # Add selected layer information
        if self.selected_layer: # Check if a layer is selected
            layer_name = self.selected_layer.name()
        else: # Should not happen if checks in __init__ are effective, but as a fallback
            layer_name = "None (Error: UI setup with no layer)"
            self.logger.error("setup_ui called but self.selected_layer is None.")

        layer_info = QLabel(f"Selected Layer: {layer_name}")
        layer_info.setStyleSheet("font-weight: bold; color: #0066cc;")
        layout.addWidget(layer_info)

        # Create property name inputs
        property_group = QGroupBox("Veld Namen")
        property_layout = QVBoxLayout()

        # From property
        from_prop_layout = QHBoxLayout()
        from_prop_label = QLabel("Begin Jaar Veld:")
        self.from_property = QLineEdit()
        self.from_property.setText("beginjaar") # Hardcoded field name
        self.from_property.setEnabled(False)  # Make read-only as per current behavior
        from_prop_layout.addWidget(from_prop_label)
        from_prop_layout.addWidget(self.from_property)

        # To property
        to_prop_layout = QHBoxLayout()
        to_prop_label = QLabel("Eind Jaar Veld:")
        self.to_property = QLineEdit()
        self.to_property.setText("eindjaar") # Hardcoded field name
        self.to_property.setEnabled(False)  # Make read-only as per current behavior
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
        self.from_year.setRange(1000, 3000) # Expanded range for flexibility
        self.from_year.setValue(1842)  # Default historical start year
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.from_year)

        # To year
        to_layout = QHBoxLayout()
        to_label = QLabel("Tot Jaar:")
        self.to_year = QSpinBox()
        self.to_year.setRange(1000, 3000) # Expanded range for flexibility
        self.to_year.setValue(1900)  # Default historical end year
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_year)

        year_layout.addLayout(from_layout)
        year_layout.addLayout(to_layout)
        year_group.setLayout(year_layout)
        layout.addWidget(year_group)

        # Create +/- buttons for adjusting both years simultaneously
        year_adjust_layout = QHBoxLayout()
        year_adjust_label = QLabel("Pas Jaar Bereik Aan:")
        
        self.decrease_year_range_btn = QPushButton("-")
        self.decrease_year_range_btn.setToolTip("Verlaag 'Van Jaar' en 'Tot Jaar' met 1")
        self.decrease_year_range_btn.clicked.connect(self.decrease_year_range)
        
        self.increase_year_range_btn = QPushButton("+")
        self.increase_year_range_btn.setToolTip("Verhoog 'Van Jaar' en 'Tot Jaar' met 1")
        self.increase_year_range_btn.clicked.connect(self.increase_year_range)
        
        year_adjust_layout.addWidget(year_adjust_label)
        year_adjust_layout.addStretch() # Add stretch to push buttons to the right or center them
        year_adjust_layout.addWidget(self.decrease_year_range_btn)
        year_adjust_layout.addWidget(self.increase_year_range_btn)
        layout.addLayout(year_adjust_layout)


        # Create main action buttons
        action_buttons_layout = QHBoxLayout()

        reset_btn = QPushButton("Reset Filter")
        reset_btn.setToolTip("Verwijder het huidige jaarfilter van de laag")
        reset_btn.clicked.connect(self.reset_filter)

        apply_btn = QPushButton("Toepassen")
        apply_btn.setToolTip("Pas het gespecificeerde jaarfilter toe op de laag")
        apply_btn.setDefault(True) # Make Apply the default button
        apply_btn.clicked.connect(self.apply_filter)

        cancel_btn = QPushButton("Annuleren")
        cancel_btn.setToolTip("Sluit het dialoogvenster zonder wijzigingen toe te passen")
        cancel_btn.clicked.connect(self.reject) # QDialog's reject() slot

        action_buttons_layout.addWidget(reset_btn)
        action_buttons_layout.addStretch(1) # Add stretch to space out buttons
        action_buttons_layout.addWidget(apply_btn)
        action_buttons_layout.addWidget(cancel_btn)
        layout.addLayout(action_buttons_layout)

        self.setLayout(layout)
        self.logger.debug("UI setup completed")

    def increase_year_range(self):
        """Increases both 'From Year' and 'To Year' by 1."""
        self.logger.debug("Increasing year range by 1.")
        current_from = self.from_year.value()
        current_to = self.to_year.value()
        
        # Ensure we don't exceed max range of spinboxes
        if current_from < self.from_year.maximum():
            self.from_year.setValue(current_from + 1)
        if current_to < self.to_year.maximum():
            self.to_year.setValue(current_to + 1)
        self.logger.debug(f"New range: {self.from_year.value()}-{self.to_year.value()}")

    def decrease_year_range(self):
        """Decreases both 'From Year' and 'To Year' by 1."""
        self.logger.debug("Decreasing year range by 1.")
        current_from = self.from_year.value()
        current_to = self.to_year.value()

        # Ensure we don't go below min range of spinboxes
        if current_from > self.from_year.minimum():
            self.from_year.setValue(current_from - 1)
        if current_to > self.to_year.minimum():
            self.to_year.setValue(current_to - 1)
        self.logger.debug(f"New range: {self.from_year.value()}-{self.to_year.value()}")


    def reset_filter(self):
        """Reset the filter on the selected layer"""
        self.logger.debug("Reset filter called.")
        if not self.selected_layer:
            self.logger.warning("Reset filter called but no layer selected.")
            if self.iface:
                self.iface.messageBar().pushMessage("Error", "No layer selected to reset filter.", level=Qgis.Critical, duration=3)
            else:
                QMessageBox.critical(self, "Error", "No layer selected to reset filter.")
            return
        try:
            self.selected_layer.setSubsetString("") # Empty string removes the subset filter
            # Force a refresh of the map canvas if an interface is available
            if self.iface and self.iface.mapCanvas():
                self.iface.mapCanvas().refresh()
            # Also refresh layer's feature count if displayed in legend
            if self.iface and self.iface.layerTreeView():
                self.iface.layerTreeView().refreshLayerSymbology(self.selected_layer.id())


            message = f"Filter reset for layer: {self.selected_layer.name()}"
            self.logger.info(message)
            if self.iface:
                self.iface.messageBar().pushMessage("Success", message, level=Qgis.Success, duration=3)
            else: # For testing or standalone dialog
                QMessageBox.information(self, "Success", message)

        except Exception as e:
            error_msg = f"Error resetting filter for layer {self.selected_layer.name()}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            if self.iface:
                self.iface.messageBar().pushMessage("Error", error_msg, level=Qgis.Critical, duration=5)
            else:
                QMessageBox.critical(self, "Error", error_msg)

    def apply_filter(self):
        """Apply the year range filter to the selected layer"""
        self.logger.debug("Apply filter called.")
        if not self.selected_layer:
            self.logger.warning("Apply filter called but no layer selected.")
            if self.iface:
                self.iface.messageBar().pushMessage("Error", "No layer selected to apply filter.", level=Qgis.Critical, duration=3)
            else:
                QMessageBox.critical(self, "Error", "No layer selected to apply filter.")
            return

        try:
            from_year_val = self.from_year.value()
            to_year_val = self.to_year.value()
            
            # It's good practice to ensure 'from_year_val' is not greater than 'to_year_val'
            if from_year_val > to_year_val:
                self.logger.warning(f"From Year ({from_year_val}) is greater than To Year ({to_year_val}). Swapping them for filter logic.")
                QMessageBox.warning(self,"Input Warning", f"'Van Jaar' ({from_year_val}) is groter dan 'Tot Jaar' ({to_year_val}). De waarden worden mogelijk intern omgewisseld voor de filterlogica, of u kunt ze handmatig corrigeren.")
                # Optionally, swap them or just warn. For now, we'll proceed, QGIS filter might handle it or result in no features.
                # For robust behavior, consider swapping: from_year_val, to_year_val = to_year_val, from_year_val

            from_property_name = self.from_property.text() # Should be "beginjaar"
            to_property_name = self.to_property.text()     # Should be "eindjaar"

            self.logger.info(f"Applying filter to {self.selected_layer.name()} - "
                             f"Properties: '{from_property_name}', '{to_property_name}'. "
                             f"Year range: {from_year_val}-{to_year_val}")

            # Construct the filter expression
            # Ensure property names are correctly quoted if they contain spaces or special characters.
            # QGIS usually requires double quotes for field names.
            expr = f'"{from_property_name}" <= {to_year_val} AND "{to_property_name}" >= {from_year_val}'
            self.logger.debug(f"Filter expression: {expr}")

            self.selected_layer.setSubsetString(expr)
            
            # Force a refresh of the map canvas and legend
            if self.iface and self.iface.mapCanvas():
                self.iface.mapCanvas().refresh()
            if self.iface and self.iface.layerTreeView():
                 self.iface.layerTreeView().refreshLayerSymbology(self.selected_layer.id())


            # featureCount() on a filtered layer gives the count of matching features
            filtered_count = self.selected_layer.featureCount()

            message = f"Filter toegepast op laag '{self.selected_layer.name()}': {filtered_count} objecten komen overeen."
            self.logger.info(message)
            if self.iface:
                self.iface.messageBar().pushMessage("Success", message, level=Qgis.Success, duration=4)
            else:
                QMessageBox.information(self, "Success", message)
            
            self.accept() # Close the dialog after applying

        except Exception as e:
            error_msg = f"Error applying filter to layer {self.selected_layer.name()}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            if self.iface:
                self.iface.messageBar().pushMessage("Error", error_msg, level=Qgis.Critical, duration=5)
            else:
                QMessageBox.critical(self, "Error", error_msg)


class YearRangeFilterPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None # Keep track of the dialog instance

        # Setup logging for the plugin itself
        self.logger = logging.getLogger('YearRangeFilter')
        # Basic configuration if not already configured by the dialog's logger setup
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO) # Default to INFO for plugin level
            # Attempt to set up file logging similar to dialog if needed, or console
            plugin_dir = os.path.dirname(__file__)
            log_dir = os.path.join(plugin_dir, 'logs')
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except OSError:
                    pass # Silently fail if log dir cannot be created by plugin main class

            log_file = os.path.join(log_dir, 'year_range_filter_plugin.log') # Different log file for plugin class
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(file_handler)
            except IOError: # Fallback to console if file logging fails
                ch = logging.StreamHandler()
                ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(ch)
                self.logger.warning("Plugin file logging failed, using console.")
        
        self.logger.info("YearRangeFilterPlugin initialized")

    def initGui(self):
        """Initialize the plugin GUI components (action, menu, toolbar)"""
        from qgis.PyQt.QtWidgets import QAction
        from qgis.PyQt.QtGui import QIcon # For icon (optional)

        # Optionally, add an icon to your plugin
        # Ensure you have an 'icon.png' in the same directory as this script,
        # or update the path accordingly.
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png') 
        
        self.action = QAction('Kaart Jaar Filter', self.iface.mainWindow())
        if os.path.exists(icon_path): # Check if icon exists before trying to set it
             self.action.setIcon(QIcon(icon_path))
        else:
            self.logger.warning(f"Plugin icon not found at: {icon_path}")

        self.action.setToolTip("Filter lagen op jaarbereik") # Tooltip for the action
        self.action.triggered.connect(self.run)

        # Add to toolbar and menu
        self.iface.addToolBarIcon(self.action)
        # This adds a new top-level menu named "Kaart Jaar Filter"
        self.iface.addPluginToMenu('&Kaart Jaar Filter', self.action) 
        self.logger.debug("Plugin GUI initialized (action, toolbar, menu)")

    def unload(self):
        """Clean up when plugin is unloaded"""
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            # Correctly remove the plugin menu item using its text and the action
            self.iface.removePluginMenu('&Kaart Jaar Filter', self.action) 
            del self.action # Explicitly delete to help with garbage collection
            self.action = None
        self.logger.info("YearRangeFilterPlugin unloaded")

    def run(self):
        """Run the plugin: show the YearRangeFilterDialog"""
        self.logger.debug("Plugin run method called.")
        try:
            # Create a new dialog instance each time, or reuse if self.dialog is managed
            # For modal dialogs, creating a new instance is often simpler.
            # Pass the QGIS interface (iface) to the dialog
            dialog = YearRangeFilterDialog(self.iface.mainWindow(), self.iface)

            # The dialog's __init__ now handles checks and might return early if conditions not met.
            # It sets _ui_initialized flag.
            if hasattr(dialog, '_ui_initialized') and dialog._ui_initialized:
                dialog.show()
                # exec_() is for modal dialogs, it blocks until the dialog is closed.
                result = dialog.exec_() 
                self.logger.debug(f"Dialog execution completed with result: {result} (Accepted: {QDialog.Accepted}, Rejected: {QDialog.Rejected})")
            else:
                self.logger.warning("Dialog UI was not initialized, not showing. Check logs for reasons (e.g., no layer selected, missing fields).")
                # No need to show a message here, as the dialog's __init__ should have already shown one.

        except Exception as e:
            self.logger.error(f"Error running plugin: {str(e)}", exc_info=True)
            QMessageBox.critical(self.iface.mainWindow(), "Plugin Error", f"An unexpected error occurred while running the plugin: {str(e)}")
