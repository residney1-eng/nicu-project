import sys
import socket
from datetime import datetime
from noise_sensor import get_average_noise #get_noise_level
from config import ALARM_THRESHOLD_DB, ALARM_RESET_DB, OUTSIDE_MIC_DEVICE, INSIDE_MIC_DEVICE

def get_anc_db():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 5005))
        sock.settimeout(1.0)
        data, addr = sock.recvfrom(1024)
        sock.close()
        return float(data.decode().strip())
    except:
        return 0.0

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtCore import QTimer, Qt

from alarm_logic import inside_db

alarm = inside_db (
    threshold_db=ALARM_THRESHOLD_DB,
    reset_db=ALARM_RESET_DB,
)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NICU Noise Monitor")
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: gray;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

    # Flashing Screen
        self.flash_on = False
        self.is_flashing = False
        self.anc_enabled = True

        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.toggle_flash)

	# Title
        self.title = QLabel("NICU Noise Monitoring System")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")

	# Alarm Status
        self.alarm_status = QLabel("ALARM: Safe")
        self.alarm_status.setAlignment(Qt.AlignCenter)
        self.alarm_status.setStyleSheet("color: green; font-size: 36px; font-weight: bold;")

	# Labels
        self.inside_label = QLabel("Inside Noise: --dB")
        self.outside_label= QLabel("Outside Noise: --dB")
        self.count_label = QLabel("Alarm Count Today: 0")
        self.anc_level_label = QLabel("Reduction Level: 0%")

        for label in [self.inside_label, self.outside_label, self.count_label, self.anc_level_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; font-size: 22px;")
        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.alarm_status)
        layout.addSpacing(20)
        layout.addWidget(self.inside_label)
        layout.addWidget(self.outside_label)
        layout.addWidget(self.count_label)
        layout.addSpacing(20)
        layout.addWidget(self.anc_level_label)
        self.setLayout(layout)

	# Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(500)

    def update_dashboard(self):
        try:
            inside_noise = get_average_noise(INSIDE_MIC_DEVICE)
            outside_noise = get_average_noise(OUTSIDE_MIC_DEVICE)
            noise_diff = max(0, outside_noise - inside_noise)

            self.inside_label.setText(f"Inside Noise: {inside_noise} dB")
            self.outside_label.setText(f"Outside Noise: {outside_noise} dB")
            self.count_label.setText(f"Alarm Count Today: {alarm.get_count()}")

            if self.anc_enabled and noise_diff > 3:
                print(f"DEBUG outside={outside_noise} inside={inside_noise} diff={outside_noise - inside_noise}")
                reduction = min(int(noise_diff * 3), 100)
                self.anc_level_label.setText(f"Reduction Level: {reduction}%")
            else:
                reduction = 0
                self.anc_level_label.setText("Reduction Level: 0%")
                # print(f"DEBUG inside={inside_noise} outside={outside_noise} alarm={alarm.is_active()}")
            noise_to_check = inside_noise if inside_noise > 0 else outside_noise
            alarm.process_noise(noise_to_check)

            if alarm.is_active():
                self.alarm_status.setText("ALARM: Loud")
                self.alarm_status.setStyleSheet("color: red; font-size: 36px; font-weight: bold;")

                if not self.is_flashing:
                    self.flash_timer.setSingleShot(False)
                    self.flash_timer.start(300)
                    self.is_flashing = True
                # print(f"DEBUG is_flashing={self.is_flashing} flash_on{self.flash_on} timer_active{self.flash_timer.isActive()}")

            else:
                self.alarm_status.setText("ALARM: Safe")
                self.alarm_status.setStyleSheet("color: lime; font-size: 36px; font-weight: bold;")

                if self.is_flashing:
                    self.flash_timer.stop()
                    self.setStyleSheet("background-color: gray;")
                    self.flash_on = False
                    self.is_flashing = False

        except Exception as e:
            print("Dashboard update error:", e)

    def toggle_flash(self):
        if self.flash_on:
           self.setStyleSheet("background-color: gray;")
           self.flash_on =  False
        else:
           self.setStyleSheet("background-color: red;")
           self.flash_on = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
