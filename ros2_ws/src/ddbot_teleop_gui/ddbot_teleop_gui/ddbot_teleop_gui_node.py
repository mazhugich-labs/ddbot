#!/usr/bin/env python3

import sys
import math

from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class JoystickWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(300, 300)

        self.knob_pos = QPointF(0, 0)
        self.dragging = False

        # Normalized joystick values: -1.0 ... +1.0
        self.x = 0.0
        self.y = 0.0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.update_joystick(event.pos())

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.update_joystick(event.pos())

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.x = 0.0
        self.y = 0.0
        self.knob_pos = QPointF(0, 0)
        self.update()

    def update_joystick(self, mouse_pos):
        center = QPointF(self.width() / 2, self.height() / 2)

        dx = mouse_pos.x() - center.x()
        dy = mouse_pos.y() - center.y()

        radius = min(self.width(), self.height()) / 2 - 30

        distance = math.sqrt(dx * dx + dy * dy)

        if distance > radius:
            scale = radius / distance
            dx *= scale
            dy *= scale

        self.knob_pos = QPointF(dx, dy)

        self.x = dx / radius
        self.y = -dy / radius  # screen Y is inverted

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 30

        # Joystick background
        painter.setPen(QPen(Qt.black, 3))
        painter.setBrush(QBrush(Qt.lightGray))
        painter.drawEllipse(center, radius, radius)

        # Crosshair
        painter.setPen(QPen(Qt.gray, 1))
        painter.drawLine(
            int(center.x() - radius),
            int(center.y()),
            int(center.x() + radius),
            int(center.y()),
        )
        painter.drawLine(
            int(center.x()),
            int(center.y() - radius),
            int(center.x()),
            int(center.y() + radius),
        )

        # Joystick knob
        knob_center = center + self.knob_pos
        knob_radius = 30

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.darkGray))
        painter.drawEllipse(knob_center, knob_radius, knob_radius)


class JoystickROSNode(Node):
    def __init__(self):
        super().__init__("pyqt_joystick")

        self.declare_parameter("cmd_vel_topic", "/ddbot/cmd_vel")
        self.declare_parameter("max_lin_vel", 3.0)
        self.declare_parameter("ang_vel", 1.5)

        self.publisher = self.create_publisher(
            Twist,
            self.get_parameter("cmd_vel_topic").value,
            10,
        )

    def publish_velocity(self, linear, angular):
        msg = Twist()

        msg.linear.x = float(linear)
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = float(angular)

        self.publisher.publish(msg)

    @property
    def max_lin_vel(self) -> float:
        return self.get_parameter("max_lin_vel").value

    @property
    def max_ang_vel(self) -> float:
        return self.get_parameter("max_ang_vel").value

    def stop_robot(self):
        self.publish_velocity(0.0, 0.0)


class MainWindow(QWidget):
    def __init__(self, ros_node):
        super().__init__()

        self.ros_node = ros_node

        # Maximum robot velocities
        self.max_linear = ros_node.max_lin_vel
        self.max_angular = ros_node.max_lin_vel

        self.setWindowTitle("ROS 2 Diff Drive Joystick")

        self.joystick = JoystickWidget()

        self.velocity_label = QLabel()
        self.velocity_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.joystick)
        layout.addWidget(self.velocity_label)

        self.setLayout(layout)

        # Publish at 20 Hz
        self.timer = QTimer()
        self.timer.timeout.connect(self.publish_cmd_vel)
        self.timer.start(50)

    def publish_cmd_vel(self):
        linear = self.joystick.y * self.max_linear

        # ROS convention:
        # angular.z > 0 = turn left
        # angular.z < 0 = turn right
        angular = -self.joystick.x * self.max_angular

        self.ros_node.publish_velocity(linear, angular)

        self.velocity_label.setText(
            f"Linear X: {linear:+.2f} m/s    " f"Angular Z: {angular:+.2f} rad/s"
        )

    def closeEvent(self, event):
        # Send stop command before closing
        self.ros_node.stop_robot()
        event.accept()


def main(args=None):
    rclpy.init(args=args)

    ros_node = JoystickROSNode()

    app = QApplication(sys.argv)

    window = MainWindow(ros_node)
    window.resize(400, 450)
    window.show()

    exit_code = app.exec_()

    ros_node.stop_robot()
    ros_node.destroy_node()
    rclpy.shutdown()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
