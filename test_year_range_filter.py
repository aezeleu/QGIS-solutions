import unittest
import os
from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QApplication
from year_range_filter import YearRangeFilterDialog

class TestYearRangeFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.app = QApplication([])
        cls.project = QgsProject.instance()
        
        # Path to test data
        test_data_path = "E:/Aezel/QGISMap-sample-for-testing"
        
        # Load actual test layer
        cls.test_layer = QgsVectorLayer(
            os.path.join(test_data_path, "Tekenlaag-percelen-Sittard_B.shp"),
            "test_percelen",
            "ogr"
        )
        
        # Verify layer is valid
        if not cls.test_layer.isValid():
            raise Exception("Test layer failed to load!")
        
        cls.project.addMapLayer(cls.test_layer)
    
    def setUp(self):
        """Set up before each test"""
        self.dialog = YearRangeFilterDialog()
    
    def test_filter_range(self):
        """Test filtering layers based on year range"""
        # Set filter range for historical data
        self.dialog.from_year.setValue(1842)
        self.dialog.to_year.setValue(1900)
        
        # Apply filter
        self.dialog.apply_filter()
        
        # Verify filter expression
        expected_expr = '"beginkaart" <= 1900 AND "eindkaart" >= 1842'
        self.assertEqual(self.test_layer.subsetString(), expected_expr)
        
        # Check if any features are visible
        feature_count = self.test_layer.featureCount()
        self.assertGreater(feature_count, 0)
    
    def test_custom_properties(self):
        """Test filtering with custom property names"""
        # Set custom property names
        self.dialog.from_property.setText("custom_begin")
        self.dialog.to_property.setText("custom_end")
        
        # Set filter range
        self.dialog.from_year.setValue(1842)
        self.dialog.to_year.setValue(1900)
        
        # Apply filter
        self.dialog.apply_filter()
        
        # Layer should be hidden as it doesn't have these custom fields
        self.assertEqual(self.test_layer.subsetString(), "FALSE")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.project.removeAllMapLayers()
        del cls.app

if __name__ == '__main__':
    unittest.main() 