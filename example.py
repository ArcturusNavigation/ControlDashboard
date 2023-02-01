from PySide2.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide2.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage

import rospy
from sensor_msgs.msg import Image

import sys
import time


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")

        layout.addWidget(self.l)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_ros_callbacks)
        self.timer.start()

        rospy.Subscriber("/zed/zed_node/rgb/image_rect_color",
                         Image, self.zed_img_callback)

    def check_ros_callbacks(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)
        rospy.spinOnce()

    def zed_img_callback(self, msg):
        im = QImage(
            msg.data, 100, 100, QImage.Format_RGB32)
        self.l.setPixmap(QPixmap.fromImage(im))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    rospy.init_node('qt_test')
    app.exec_()
