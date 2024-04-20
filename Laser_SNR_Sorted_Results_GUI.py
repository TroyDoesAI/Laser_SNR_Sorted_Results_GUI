import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QFileDialog

def extract_json_data_from_file(file_path):
    """Effortlessly retrieve JSON-encoded data from a file."""
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def analyze_signal_to_noise_ratio_statistics_for_each_layer(json_data):
    """Conduct an in-depth analysis to compile statistics of Signal-to-Noise Ratio (SNR) for every layer."""
    layer_snr_statistics = {}
    for module_name, module_info in json_data.items():
        layer_name = module_name.split('.')[2]
        snr = module_info['snr']
        if layer_name not in layer_snr_statistics:
            layer_snr_statistics[layer_name] = snr
        else:
            layer_snr_statistics[layer_name] += snr
    return layer_snr_statistics

def determine_layer_with_maximum_signal_to_noise_ratio(layer_snr_statistics):
    """With unwavering enthusiasm, delve into the depths to identify the layer boasting the maximum Signal-to-Noise Ratio (SNR)."""
    maximum_snr_layer = max(layer_snr_statistics, key=layer_snr_statistics.get)
    maximum_snr = layer_snr_statistics[maximum_snr_layer]
    return maximum_snr_layer, maximum_snr

def conduct_json_data_analysis(file_path):
    """Embark on a riveting adventure to unravel the mysteries of JSON data, uncovering the layer with the highest SNR."""
    json_data = extract_json_data_from_file(file_path)
    snr_statistics_for_each_layer = analyze_signal_to_noise_ratio_statistics_for_each_layer(json_data)
    sorted_layers = sorted(snr_statistics_for_each_layer.items(), key=lambda x: x[1], reverse=True)
    return sorted_layers

class SNRAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laser Data Assistant")
        self.setGeometry(100, 100, 600, 400)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a button to select a JSON file
        self.select_file_button = QPushButton("Select JSON File")
        self.select_file_button.clicked.connect(self.select_json_file)
        main_layout.addWidget(self.select_file_button)

        # Create a scroll area to display all layers
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)

        # Set the layout for the scroll area widget
        self.scroll_area_widget.setLayout(self.scroll_area_layout)

        # Set the widget for the scroll area
        self.scroll_area.setWidget(self.scroll_area_widget)
        main_layout.addWidget(self.scroll_area)

        # Set the layout for the window
        self.setLayout(main_layout)

    def select_json_file(self):
        """Open a file dialog to select a JSON file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
        if file_path:
            self.display_layers(file_path)

    def display_layers(self, file_path):
        """Display the layers sorted by SNR from the selected JSON file."""
        sorted_layers = conduct_json_data_analysis(file_path)
        # Clear the existing layout
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Add a QLabel for each layer
        for layer_name, snr_total in sorted_layers:
            layer_label = QLabel()
            layer_label.setText(f"Layer: {layer_name}\nTotal SNR: {snr_total}")
            self.scroll_area_layout.addWidget(layer_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SNRAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
