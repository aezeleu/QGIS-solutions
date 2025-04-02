# Year Range Filter Plugin for QGIS

This plugin allows you to filter QGIS layers based on their year properties. It provides a simple interface to set a year range and automatically shows/hides layers based on whether their year properties fall within the specified range.

## Requirements

- QGIS 3.22 or higher
- Python 3.x

## Installation

1. Download the plugin files:
   - `year_range_filter.py`
   - `metadata.txt`
   - `README.md`

2. Create a new directory in your QGIS plugins folder:
   - Windows: `C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\year_range_filter`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter`

3. Copy the downloaded files into this directory

4. Restart QGIS

5. Enable the plugin in QGIS:
   - Go to Plugins → Manage and Install Plugins
   - Find "Year Range Filter" in the list
   - Check the box to enable it

## Usage

1. Load your layers into QGIS
2. Set the year properties for your layers (if not already set)
3. Click the "Year Range Filter" button in the toolbar or menu
4. In the dialog that appears:
   - Set the property names for "From" and "To" years (default: "year_from" and "year_to")
   - Set the "From Year" value
   - Set the "To Year" value
   - Use the "+" buttons to increment the year values
   - Click "Apply" to filter the layers
   - Click "Cancel" to close without applying changes

The plugin will automatically:
- Show layers whose year range overlaps with the specified range
- Hide layers that don't have the required year properties
- Allow customization of property names for flexible layer filtering

## Layer Properties

To use this plugin, your layers should have two properties:
- A "From" year property (default name: "year_from")
- A "To" year property (default name: "year_to")

You can customize these property names in the plugin dialog to match your layer properties.

## Uninstallation

1. In QGIS, go to Plugins → Manage and Install Plugins
2. Find "Year Range Filter" in the list
3. Uncheck the box to disable it
4. Delete the plugin directory:
   - Windows: `C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\year_range_filter`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter`
5. Restart QGIS

## Troubleshooting

If the plugin doesn't appear in QGIS:
1. Make sure all files are in the correct directory
2. Check that the file permissions are correct
3. Restart QGIS
4. Check the QGIS log for any error messages

## Support

For issues or questions, please create an issue in the plugin's repository or contact the plugin author. 