##Quick Field Editor=name
##Vector Tools=group

from qgis.PyQt.QtCore import QVariant, QDate
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QProgressBar, QDateTimeEdit
)
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField, QgsDistanceArea,
    QgsProcessingException, QgsMessageLog
)
import re
import datetime

# ------------------ GUI Dialog ------------------
class QuickFieldEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quick Field Editor")
        self.setMinimumWidth(640)
        self.build_ui()

    def build_ui(self):
        main = QVBoxLayout()

        lyr_row = QHBoxLayout()
        lyr_row.addWidget(QLabel("Input Layer:"))
        self.layer_combo = QComboBox()
        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr, QgsVectorLayer):
                self.layer_combo.addItem(lyr.name(), lyr.id())
        lyr_row.addWidget(self.layer_combo)
        main.addLayout(lyr_row)

        grp = QGroupBox("Field Update")
        grid = QGridLayout()
        self._row = 0

        def add(label, widget, extras=()):
            grid.addWidget(QLabel(label), self._row, 0)
            grid.addWidget(widget, self._row, 1)
            for i, w in enumerate(extras, start=2):
                grid.addWidget(w, self._row, i)
            self._row += 1

        self.serial_combo = QComboBox()
        self.area_combo, self.area_unit = QComboBox(), QComboBox()
        self.length_combo, self.length_unit = QComboBox(), QComboBox()
        self.perimeter_combo, self.perimeter_unit = QComboBox(), QComboBox()
        self.lat_combo, self.lon_combo = QComboBox(), QComboBox()
        self.date_combo, self.date_edit, self.date_button = QComboBox(), QLineEdit(), QPushButton("Pick Date")
        self.time_combo, self.time_edit = QComboBox(), QLineEdit()
        self.time_format = QComboBox()
        self.replace_combo, self.search_edit, self.replace_edit = QComboBox(), QLineEdit(), QLineEdit()
        self.concat_out_combo = QComboBox()
        self.concat1_combo, self.concat_text, self.concat2_combo = QComboBox(), QLineEdit(), QComboBox()

        self.area_unit.addItems(['Square Feet', 'Square Meters', 'Square Kilometers', 'Square Miles', 'Square Centimeters', 'Square Millimeters'])
        self.length_unit.addItems(['Meters', 'Kilometers', 'Feet', 'Miles', 'Centimeters'])
        self.perimeter_unit.addItems(['Meters', 'Kilometers', 'Feet', 'Miles', 'Centimeters'])
        self.time_format.addItems(['HH:MM:SS', 'HH:MM:SS AM/PM'])

        add("Serial No:", self.serial_combo)
        add("Area:", self.area_combo, [self.area_unit])
        add("Length:", self.length_combo, [self.length_unit])
        add("Perimeter:", self.perimeter_combo, [self.perimeter_unit])
        add("Latitude:", self.lat_combo)
        add("Longitude:", self.lon_combo)
        add("Date:", self.date_combo, [self.date_edit, self.date_button])
        add("Time:", self.time_combo, [self.time_edit, self.time_format])
        add("Replace:", self.replace_combo, [self.search_edit, self.replace_edit])
        add("Concatenate:", self.concat_out_combo, [self.concat1_combo, self.concat_text, self.concat2_combo])

        grp.setLayout(grid)
        main.addWidget(grp)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        main.addWidget(self.progress_bar)

        btn_row = QHBoxLayout()
        ok_btn, cancel_btn = QPushButton("OK"), QPushButton("Cancel")
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        main.addLayout(btn_row)
        self.setLayout(main)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.run_updates)
        self.date_button.clicked.connect(self.show_date_picker)
        self.layer_combo.currentIndexChanged.connect(self.populate_fields)
        self.populate_fields()

    def show_date_picker(self):
        date_picker = QDateTimeEdit(self)
        date_picker.setCalendarPopup(True)
        date_picker.setDate(QDate.currentDate())
        date_picker.dateChanged.connect(lambda d: self.date_edit.setText(d.toString("yyyy-MM-dd")))
        date_picker.show()

    def populate_fields(self):
        layer = QgsProject.instance().mapLayer(self.layer_combo.currentData())
        combos = [
            self.serial_combo, self.area_combo, self.length_combo, self.perimeter_combo,
            self.lat_combo, self.lon_combo, self.date_combo, self.time_combo,
            self.replace_combo, self.concat_out_combo, self.concat1_combo, self.concat2_combo
        ]
        for cb in combos:
            cb.clear()
            cb.addItem("", "")
            if layer:
                for f in layer.fields():
                    cb.addItem(f.name(), f.name())

    def reset_fields(self):
        """Reset all input fields to their default state."""
        # Clear QComboBox selections
        combos = [
            self.serial_combo, self.area_combo, self.length_combo, self.perimeter_combo,
            self.lat_combo, self.lon_combo, self.date_combo, self.time_combo,
            self.replace_combo, self.concat_out_combo, self.concat1_combo, self.concat2_combo
        ]
        for cb in combos:
            cb.setCurrentIndex(0)  # Set to the empty item ("")
        
        # Reset unit and format dropdowns
        self.area_unit.setCurrentIndex(0)  # Default to 'Square Feet'
        self.length_unit.setCurrentIndex(0)  # Default to 'Meters'
        self.perimeter_unit.setCurrentIndex(0)  # Default to 'Meters'
        self.time_format.setCurrentIndex(0)  # Default to 'HH:MM:SS'
        
        # Clear text inputs
        self.date_edit.clear()
        self.time_edit.clear()
        self.search_edit.clear()
        self.replace_edit.clear()
        self.concat_text.clear()

        # Reset progress bar
        self.progress_bar.setValue(0)

    def run_updates(self):
        layer = QgsProject.instance().mapLayer(self.layer_combo.currentData())
        if not layer or not layer.isValid():
            QgsMessageLog.logMessage("Quick Field Editor: Invalid layer selected.", "Quick Field Editor", 2)
            self.reject()
            return

        if not layer.isEditable():
            layer.startEditing()

        # Get all inputs
        def val(cb): return cb.currentData() or None
        def text(te): return te.text()

        p = dict(
            serial=val(self.serial_combo),
            area=val(self.area_combo), area_u=self.area_unit.currentText(),
            length=val(self.length_combo), length_u=self.length_unit.currentText(),
            peri=val(self.perimeter_combo), peri_u=self.perimeter_unit.currentText(),
            lat=val(self.lat_combo), lon=val(self.lon_combo),
            date_f=val(self.date_combo), date_v=text(self.date_edit),
            time_f=val(self.time_combo), time_v=text(self.time_edit),
            time_fmt=self.time_format.currentText(),
            repl_f=val(self.replace_combo), search=text(self.search_edit), replto=text(self.replace_edit),
            concat_out=val(self.concat_out_combo),
            concat1=val(self.concat1_combo), glue=text(self.concat_text), concat2=val(self.concat2_combo)
        )

        # Validate date format
        if p['date_f'] and p['date_v']:
            try:
                datetime.datetime.strptime(p['date_v'], '%Y-%m-%d')
            except ValueError:
                QgsMessageLog.logMessage("Quick Field Editor: Invalid date format. Use yyyy-MM-dd.", "Quick Field Editor", 2)
                self.reject()
                return

        def ensure(field_name, qtype):
            if field_name and field_name not in layer.fields().names():
                layer.addAttribute(QgsField(field_name, qtype))
                QgsMessageLog.logMessage(f"Added new field: {field_name}", "Quick Field Editor", 0)

        # Ensure fields exist
        ensure(p['serial'], QVariant.Int)
        ensure(p['area'], QVariant.Double)
        ensure(p['length'], QVariant.Double)
        ensure(p['peri'], QVariant.Double)
        ensure(p['lat'], QVariant.Double)
        ensure(p['lon'], QVariant.Double)
        ensure(p['date_f'], QVariant.String)
        ensure(p['time_f'], QVariant.String)
        ensure(p['repl_f'], QVariant.String)
        ensure(p['concat_out'], QVariant.String)
        layer.updateFields()

        fidx = lambda x: layer.fields().indexFromName(x) if x else -1
        serial_i = fidx(p['serial'])
        area_i = fidx(p['area'])
        len_i = fidx(p['length'])
        peri_i = fidx(p['peri'])
        lat_i = fidx(p['lat'])
        lon_i = fidx(p['lon'])
        date_i = fidx(p['date_f'])
        time_i = fidx(p['time_f'])
        repl_i = fidx(p['repl_f'])
        concat_i = fidx(p['concat_out'])
        concat1_i = fidx(p['concat1'])
        concat2_i = fidx(p['concat2'])

        area_f = {
            'Square Feet': 10.7639104, 'Square Meters': 1, 'Square Kilometers': 1e-6,
            'Square Miles': 3.861e-7, 'Square Centimeters': 10000, 'Square Millimeters': 1_000_000
        }
        len_f = {
            'Meters': 1, 'Kilometers': 0.001, 'Feet': 3.28084, 'Miles': 0.000621371, 'Centimeters': 100
        }
        time_formats_dict = {
            'HH:MM:SS': '%H:%M:%S',
            'HH:MM:SS AM/PM': '%I:%M:%S %p'
        }

        d = QgsDistanceArea()
        d.setSourceCrs(layer.crs(), QgsProject.instance().transformContext())
        d.setEllipsoid(QgsProject.instance().ellipsoid())

        total_features = layer.featureCount()
        self.progress_bar.setMaximum(total_features)
        current_feature_num = 0

        QgsMessageLog.logMessage(f"Processing {total_features} features...", "Quick Field Editor", 0)

        for i, f in enumerate(layer.getFeatures(), start=1):
            current_feature_num += 1
            self.progress_bar.setValue(current_feature_num)
            fid = f.id()
            geom = f.geometry()
            attrs_to_change = {}

            if serial_i >= 0:
                attrs_to_change[serial_i] = i

            if geom and geom.isGeosValid():
                if area_i >= 0:
                    attrs_to_change[area_i] = d.measureArea(geom) * area_f[p['area_u']]
                if len_i >= 0:
                    attrs_to_change[len_i] = d.measureLength(geom) * len_f[p['length_u']]
                if peri_i >= 0:
                    attrs_to_change[peri_i] = d.measurePerimeter(geom) * len_f[p['peri_u']]
                if lat_i >= 0 or lon_i >= 0:
                    centroid_geom = geom.centroid()
                    if centroid_geom and centroid_geom.isGeosValid():
                        pt = centroid_geom.asPoint()
                        if lat_i >= 0:
                            attrs_to_change[lat_i] = pt.y()
                        if lon_i >= 0:
                            attrs_to_change[lon_i] = pt.x()
                    else:
                        QgsMessageLog.logMessage(f"Could not calculate centroid for feature ID {fid}.", "Quick Field Editor", 1)

            if date_i >= 0 and p['date_f']:
                date_val = p['date_v'] if p['date_v'] else datetime.date.today().strftime('%Y-%m-%d')
                attrs_to_change[date_i] = date_val

            if time_i >= 0 and p['time_f']:
                time_val_str = p['time_v']
                if not time_val_str:
                    time_val_str = datetime.datetime.now().strftime(time_formats_dict[p['time_fmt']])
                else:
                    parsed_success = False
                    for fmt in time_formats_dict.values():
                        try:
                            parsed_time = datetime.datetime.strptime(time_val_str, fmt).time()
                            time_val_str = parsed_time.strftime(time_formats_dict[p['time_fmt']])
                            parsed_success = True
                            break
                        except ValueError:
                            pass
                    if not parsed_success:
                        QgsMessageLog.logMessage(
                            f"Warning: Could not parse time '{time_val_str}' for feature ID {fid}. Expected format: {p['time_fmt']}. Using as-is or current time.",
                            "Quick Field Editor", 1)
                        time_val_str = p['time_v'] if p['time_v'] else datetime.datetime.now().strftime(time_formats_dict.get(p['time_fmt'], '%H:%M:%S'))
                attrs_to_change[time_i] = time_val_str

            if repl_i >= 0 and p['repl_f'] and p['search']:
                orig = str(f[p['repl_f']] or "")
                QgsMessageLog.logMessage(f"DEBUG (Replace): Feature ID: {fid}, Original: '{orig}', Search: '{p['search']}', Replace: '{p['replto']}'", "Quick Field Editor", 0)
                new_val = re.sub(re.escape(p['search']), p['replto'], orig)
                attrs_to_change[repl_i] = new_val
                QgsMessageLog.logMessage(f"DEBUG (Replace): New value: '{new_val}'", "Quick Field Editor", 0)

            if concat_i >= 0 and concat1_i >= 0 and concat2_i >= 0 and p['concat_out'] and p['concat1'] and p['concat2']:
                v1 = str(f[p['concat1']] or "")
                v2 = str(f[p['concat2']] or "")
                attrs_to_change[concat_i] = f"{v1}{p['glue']}{v2}"

            if attrs_to_change:
                layer.changeAttributeValues(fid, attrs_to_change)

        layer.commitChanges()
        QgsMessageLog.logMessage("Quick Field Editor updates complete.", "Quick Field Editor", 0)
        self.accept()
        self.reset_fields()  # Reset all fields after successful execution