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

## Development Environment Setup

### Prerequisites

1. Install QGIS 3.22 or higher
2. Install Python 3.x (same version as used by QGIS)
3. Install Git (for version control)

### Setting Up the Development Environment

1. **Create a Development Directory**
   ```bash
   mkdir qgis_plugins_dev
   cd qgis_plugins_dev
   ```

2. **Clone the Repository**
   ```bash
   git clone [your-repository-url] year_range_filter
   cd year_range_filter
   ```

3. **Create a Symbolic Link to QGIS Plugins Directory**
   - Windows (Run as Administrator):
     ```bash
     mklink /D "C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\year_range_filter" "D:\path\to\your\development\year_range_filter"
     ```
   - Linux:
     ```bash
     ln -s /path/to/your/development/year_range_filter ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter
     ```
   - macOS:
     ```bash
     ln -s /path/to/your/development/year_range_filter ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/year_range_filter
     ```

4. **Set Up Python Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

5. **Install Development Dependencies**
   ```bash
   pip install pytest pytest-qt
   ```

### Testing the Plugin

1. **Enable Plugin Reloading**
   - Open QGIS
   - Go to Settings → Options → Python
   - Check "Enable plugin reloading"
   - Click OK and restart QGIS

2. **Load the Plugin**
   - Go to Plugins → Manage and Install Plugins
   - Find "Year Range Filter" in the list
   - Check the box to enable it

3. **Test the Plugin**
   - Create test layers with year properties
   - Use the plugin to filter layers
   - Verify the filtering behavior

### Development Workflow

1. **Make Changes**
   - Edit the plugin files in your development directory
   - Changes will be automatically reflected in QGIS if plugin reloading is enabled

2. **Test Changes**
   - Restart QGIS if needed
   - Test the modified functionality
   - Check for any errors in the QGIS Python console

3. **Debugging**
   - Open the QGIS Python console (Plugins → Python Console)
   - Use print statements in your code for debugging
   - Check the QGIS log for error messages

4. **Version Control**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

### Common Issues and Solutions

1. **Plugin Not Loading**
   - Check the QGIS Python console for error messages
   - Verify the symbolic link is correctly set up
   - Ensure all required files are present

2. **Changes Not Reflecting**
   - Make sure plugin reloading is enabled
   - Try restarting QGIS
   - Check file permissions

3. **Python Version Mismatch**
   - Ensure you're using the same Python version as QGIS
   - Check QGIS Python version in the Python console:
     ```python
     import sys
     print(sys.version)
     ```

### Recommended Development Tools

1. **Code Editor**
   - VS Code with Python extension
   - PyCharm
   - Any Python IDE of your choice

2. **Version Control**
   - Git
   - GitHub/GitLab for remote repository

3. **Testing**
   - pytest for unit testing
   - QGIS Python console for debugging 