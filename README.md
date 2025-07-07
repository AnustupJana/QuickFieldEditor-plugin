# Quick Field Editor QGIS Plugin
![Quick Field Editor Icon](https://github.com/yourusername/quick_field_editor/blob/main/icon.png?raw=true)

## Overview

The **Quick Field Editor** plugin for QGIS is a powerful tool designed to simplify attribute table updates for vector layers. It offers an intuitive interface to perform a variety of tasks, including generating serial numbers, calculating geometry-based values (area, length, perimeter), extracting coordinates, setting date and time values, performing text replacements, and concatenating fields—all without the need for manual expressions.

## Features
- Generate sequential serial numbers for features.
- Calculate area, length, and perimeter with customizable units (e.g., square meters, feet).
- Extract latitude and longitude from geometry centroids.
- Set and format date and time values with a calendar picker.
- Perform search-and-replace operations on text fields.
- Concatenate multiple fields with an optional separator.
- Dynamic field selection and progress feedback during processing.
- Automatically resets fields after each run for a fresh start.
- Robust error handling with log messages.

## Requirements
- **QGIS Version**: 3.0 or later (up to 3.99).
- **Operating System**: Windows, macOS, or Linux (compatible with QGIS installations).
- **Dependencies**: No additional Python libraries required; uses QGIS core and PyQt modules.

## Installation

1. **From QGIS Plugin Repository**:
   - In QGIS, go to `Plugins > Manage and Install Plugins`.
   - Search for "Quick Field Editor" in the `All` tab.
     ![Search for Plugin](https://github.com/yourusername/quick_field_editor/blob/main/doc/search_plugin.png?raw=true)
   - Click `Install Plugin`.

2. **From ZIP File**:
   - Download the plugin ZIP file from the [GitHub Releases](https://github.com/yourusername/quick_field_editor/releases) page.
   - In QGIS, go to `Plugins > Manage and Install Plugins > Install from ZIP`.
   - Select the downloaded ZIP file and click `Install Plugin`.

3. **From Source (for developers)**:
   - Clone or download this repository:
     ```bash
     git clone https://github.com/yourusername/quick_field_editor.git
     ```
   - Copy the `quick_field_editor` folder to your QGIS plugins directory:
     - Windows: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
     - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
     - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`

4. **Enable the Plugin**:
   - In the QGIS Plugin Manager, search for **Quick Field Editor**.
   - Check the box to enable the plugin.

5. **Verify Installation**:
   - Look for the **Quick Field Editor** icon in the QGIS toolbar or find it in the **Vector** menu.
   - Open the Processing Toolbox (`Ctrl+Alt+T`) and locate **Quick Field Editor** under **Vector Tools**.

## Usage

1. **Launch the Plugin**:
   - Click the **Quick Field Editor** toolbar icon or select **Quick Field Editor** from the **Vector** menu.
   - Alternatively, open the Processing Toolbox (`Ctrl+Alt+T`), navigate to **Vector Tools**, and double-click **Quick Field Editor**.
     ![Launch Plugin](https://github.com/yourusername/quick_field_editor/blob/main/doc/launch_plugin.png?raw=true)

2. **Configure Parameters**:
   - **Select Layer**: Choose an input vector layer from the dropdown.
   - **Field Updates**:
     - **Serial No**: Select a field to populate with sequential numbers.
     - **Area**: Select a field and unit (e.g., Square Meters, Square Feet).
     - **Length/Perimeter**: Select fields and units (e.g., Meters, Feet).
     - **Latitude/Longitude**: Select fields to extract coordinates from centroids.
     - **Date**: Enter a date (yyyy-MM-dd) or use the "Pick Date" button.
     - **Time**: Enter a time (e.g., HH:MM:SS or HH:MM:SS AM/PM) and choose a format.
     - **Replace**: Specify a search string and replacement text.
     - **Concatenate**: Select two fields and an optional separator.
     ![Configure Fields](https://github.com/yourusername/quick_field_editor/blob/main/doc/configure_fields.png?raw=true)

3. **Run the Tool**:
   - Click **OK** to process the updates. A progress bar will show the operation’s status.
   - Check the QGIS Log Messages panel (View > Panels > Log Messages) for success messages or warnings.
     ![Run Tool](https://github.com/yourusername/quick_field_editor/blob/main/doc/run_tool.png?raw=true)

4. **View Results**:
   - Updated fields are applied to the selected layer.
   - The tool resets all fields automatically for the next use.
     ![Results](https://github.com/yourusername/quick_field_editor/blob/main/doc/results.png?raw=true)

## Development
- **Author**: Anustup Jana
- **Email**: anustupjana21@gmail.com
- **Version**: 1.0
- **Started**: July 06, 2025
- **License**: GNU General Public License v2.0 or later

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Issues and Support
- Report bugs or suggest features via the [issue tracker](https://github.com/yourusername/quick_field_editor/issues).
- For questions, contact the author at anustupjana21@gmail.com.

## Acknowledgments
- Built using the QGIS Python API and Plugin Builder.
- Thanks to the QGIS community for their support and resources.

## License
This plugin is licensed under the **GNU General Public License v2.0 or later**. See the [LICENSE](https://github.com/yourusername/quick_field_editor/blob/main/LICENSE) file for details.
