import sys
import json
import subprocess

# Check if required packages are installed, and install them if necessary
def check_dependencies():
    required_packages = ["PyQt5"]
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode("utf-8")
    missing_packages = [package for package in required_packages if package not in installed_packages]

    if missing_packages:
        for package in missing_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print("All required packages found.")

# Check dependencies before running the application
check_dependencies()


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QListView, QTextEdit
from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex

class Layer:
    def __init__(self, name, modules):
        self.name = name
        self.modules = modules

class LayerModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layers = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.layers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.layers)):
            return None

        layer = self.layers[index.row()]

        if role == Qt.DisplayRole:
            return f"Layer: {layer.name}"

        return None

    def set_layers(self, layers):
        self.beginResetModel()
        self.layers = layers
        self.endResetModel()

def preprocess_json_data(file_path):
    """Preprocess JSON data to organize modules by layer and sort layers by SNR."""
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            layer_snr_statistics = {}
            for module_name, module_info in json_data.items():
                layer_name = module_name.split('.')[2]
                snr = module_info['snr']
                if layer_name not in layer_snr_statistics:
                    layer_snr_statistics[layer_name] = {'modules': [(module_name, snr)], 'snr': snr}
                else:
                    layer_snr_statistics[layer_name]['modules'].append((module_name, snr))
                    layer_snr_statistics[layer_name]['snr'] += snr

            sorted_layers = sorted(layer_snr_statistics.items(), key=lambda x: x[1]['snr'], reverse=True)
            return sorted_layers
    except Exception as e:
        print("Error processing JSON file:", e)
        return []

class SNRAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neural Network SNR Analyzer")
        self.resize(800, 600)  # Adjusted initial size

        self.layer_model = LayerModel()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add some margins for better spacing

        # Information banner
        info_label = QLabel("""<b>Welcome to the Signal-to-Noise Ratio (SNR) Analyzer Tool!</b><br><br>This tool helps evaluate the performance of 
            different layers within a neural network model by comparing the strength of the useful signal to the level 
            of unwanted noise.<br><br>
            The SNR analysis is similar to adjusting the volume on your music player to hear the melody clearly amidst 
            background chatter. In this case, the 'signal' represents the melody (useful information), while the 'noise' 
            represents the chatter (unwanted interference).<br><br>
            The tool's core function, <b>calculate_snr_for_layer</b>, breaks down the layers' signal and noise components, 
            allowing you to identify which layers contribute the most to the model's performance.<br><br>
            By understanding the SNR of each layer, you can optimize your neural network model to focus on the most 
            important information, leading to better performance and efficiency.<br><br>
            For further information and usage instructions, please refer to the accompanying documentation or README file.""")
        info_label.setWordWrap(True)  # Wrap text to fit the window width
        info_label.setStyleSheet("font-size: 12px;")  # Adjust font size
        main_layout.addWidget(info_label)

        # File selection layout
        file_layout = QHBoxLayout()

        self.selected_file_label = QLabel("No file selected.")
        file_layout.addWidget(self.selected_file_label)

        self.select_file_button = QPushButton("Select JSON File")
        self.select_file_button.setToolTip("Click to choose a JSON file containing SNR data.")
        self.select_file_button.clicked.connect(self.select_json_file)
        file_layout.addWidget(self.select_file_button)

        main_layout.addLayout(file_layout)

        # Layer selection and display layout
        layer_layout = QHBoxLayout()
        layer_layout.setSpacing(20)  # Add spacing between widgets

        # Layer selection list
        layer_view_layout = QVBoxLayout()

        self.layer_view_label = QLabel("<b>Layers with SNR (Sorted by SNR)</b>")
        self.layer_view_label.setStyleSheet("font-size: 14px;")  # Adjust font size
        layer_view_layout.addWidget(self.layer_view_label)

        self.layer_view = QListView()
        self.layer_view.setModel(self.layer_model)
        self.layer_view.setToolTip("Click on a layer to view details.")
        self.layer_view.setStyleSheet("font-size: 12px;")  # Adjust font size
        self.layer_view.clicked.connect(self.show_layer_details)
        layer_view_layout.addWidget(self.layer_view)

        layer_layout.addLayout(layer_view_layout)

        # Display for selected item
        self.module_details_label = QTextEdit()
        self.module_details_label.setReadOnly(True)
        layer_layout.addWidget(self.module_details_label)

        main_layout.addLayout(layer_layout)

        self.setLayout(main_layout)

    def select_json_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
        if file_path:
            self.display_layers(file_path)

    def display_layers(self, file_path):
        self.sorted_layers = preprocess_json_data(file_path)
        layers = []
        for layer_name, layer_info in self.sorted_layers:
            modules = [{'name': module[0], 'snr': module[1]} for module in layer_info['modules']]
            layers.append(Layer(layer_name, modules))
        self.layer_model.set_layers(layers)
        self.selected_file_label.setText(f"<b>Selected file:</b> {file_path}")

    def show_layer_details(self, index):
        layer = self.layer_model.layers[index.row()]
        module_details_str = f"<h2>Layer: {layer.name}</h2>"
        module_details_str += "<ul>"
        for module in layer.modules:
            module_details_str += f"<li><b>Module:</b> {module['name']}<br><b>SNR:</b> {module['snr']:.2f}</li>"
        module_details_str += "</ul>"
        self.module_details_label.setHtml(module_details_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SNRAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
