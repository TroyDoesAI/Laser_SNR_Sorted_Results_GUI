import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea

def extract_json_data_from_string(json_string):
    """Effortlessly retrieve JSON-encoded data from a string."""
    return json.loads(json_string)

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

def conduct_json_data_analysis(json_string):
    """Embark on a riveting adventure to unravel the mysteries of JSON data, uncovering the layer with the highest SNR."""
    json_data = extract_json_data_from_string(json_string)
    snr_statistics_for_each_layer = analyze_signal_to_noise_ratio_statistics_for_each_layer(json_data)
    sorted_layers = sorted(snr_statistics_for_each_layer.items(), key=lambda x: x[1], reverse=True)
    return sorted_layers

class SNRAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laser Data Assistant")
        self.setGeometry(100, 100, 600, 400)

        # Call the function to get SNR data
        json_data_string = '''
        {
            "model.layers.0.self_attn.q_proj": {
                "snr": 0.11516067286550018,
                "module": "model.layers.0.self_attn.q_proj"
            },
            "model.layers.0.self_attn.k_proj": {
                "snr": 0.16747126786955624,
                "module": "model.layers.0.self_attn.k_proj"
            },
            "model.layers.0.self_attn.v_proj": {
                "snr": 4.084768846522904,
                "module": "model.layers.0.self_attn.v_proj"
            },
            "model.layers.0.self_attn.o_proj": {
                "snr": 0.18308002598560322,
                "module": "model.layers.0.self_attn.o_proj"
            },
            "model.layers.0.mlp.gate_proj": {
                "snr": 2.2305537838781295,
                "module": "model.layers.0.mlp.gate_proj"
            }
        }
        '''

        sorted_layers = conduct_json_data_analysis(json_data_string)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a scroll area to display all layers
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)

        # Add a QLabel for each layer
        for layer_name, snr_total in sorted_layers:
            layer_label = QLabel()
            layer_label.setText(f"Layer: {layer_name}\nTotal SNR: {snr_total}")
            scroll_area_layout.addWidget(layer_label)

        # Set the layout for the scroll area widget
        scroll_area_widget.setLayout(scroll_area_layout)

        # Set the widget for the scroll area
        scroll_area.setWidget(scroll_area_widget)
        main_layout.addWidget(scroll_area)

        # Set the layout for the window
        self.setLayout(main_layout)

        # Display the window
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SNRAnalyzerApp()
    sys.exit(app.exec_())
