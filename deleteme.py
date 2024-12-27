import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
import pyaudio
import numpy as np
import crepe

# Audio settings
SAMPLE_RATE = 16000
BUFFER_SIZE = 1024

class GuitarString:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency

class PitchEstimationThread(QThread):
    pitch_estimated = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=BUFFER_SIZE)

        while self.is_running:
            data = stream.read(BUFFER_SIZE)
            audio = np.frombuffer(data, dtype=np.float32)
            time, frequency, confidence, activation = crepe.predict(audio, SAMPLE_RATE, viterbi=True)
            self.pitch_estimated.emit(frequency[-1])

        stream.stop_stream()
        stream.close()
        p.terminate()

class PitchEstimationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.string_dropdown = QComboBox()
        self.string_dropdown.addItems([f"{guitar_string.name} - {guitar_string.frequency:.2f} Hz" for guitar_string in reversed(guitar_strings)])
        self.string_dropdown.currentIndexChanged.connect(self.update_target_pitch)
        layout.addWidget(self.string_dropdown)

        self.target_pitch_label = QLabel('Target Pitch: -')
        layout.addWidget(self.target_pitch_label)

        self.estimated_pitch_label = QLabel('Estimated Pitch: -')
        layout.addWidget(self.estimated_pitch_label)

        self.pitch_difference_label = QLabel('Pitch Difference: -')
        layout.addWidget(self.pitch_difference_label)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_estimation)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_estimation)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.setWindowTitle('Guitar Tuner')

        self.estimation_thread = PitchEstimationThread()
        self.estimation_thread.pitch_estimated.connect(self.update_pitch)

    def update_target_pitch(self, index):
        self.target_pitch = guitar_strings[len(guitar_strings) - index - 1].frequency
        self.target_pitch_label.setText(f'Target Pitch: {self.target_pitch:.2f} Hz')

    def start_estimation(self):
        self.estimation_thread.is_running = True
        self.estimation_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_estimation(self):
        self.estimation_thread.is_running = False
        self.estimation_thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_pitch(self, estimated_pitch):
        self.estimated_pitch_label.setText(f'Estimated Pitch: {estimated_pitch:.2f} Hz')
        pitch_difference = estimated_pitch - self.target_pitch
        self.pitch_difference_label.setText(f'Pitch Difference: {pitch_difference:.2f} Hz')

if __name__ == '__main__':
    guitar_strings = [
        GuitarString('E', 82.41),
        GuitarString('A', 110.00),
        GuitarString('D', 146.83),
        GuitarString('G', 196.00),
        GuitarString('B', 246.94),
        GuitarString('E', 329.63)
    ]

    app = QApplication(sys.argv)
    gui = PitchEstimationGUI()
    gui.show()
    sys.exit(app.exec_())