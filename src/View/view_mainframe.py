from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import Qt

from src.View.view_canvas import ViewCanvas
from src.View.widgets.view_board import ViewTeacherDeskLabel


class CentralWidget(QWidget):
    def __init__(self, config):
        """
        Application's central widget, contains all the app's widgets.

        :param config: application's parsed configuration
        """
        QWidget.__init__(self)

        self.config = config

        self.v_canvas = ViewCanvas(config)  # Central canvas

        self.btn = QPushButton("** Magic Button **")  # Debug btn
        self.btn.clicked.connect(self.do_magic)

        self.btn_perspective = QPushButton("Switch perspective")  # Perspective view button
        self.btn_perspective.clicked.connect(self.on_perspective_changed)

        self.view_students = ViewTeacherDeskLabel("Vue élève", config.get('colors', 'board_bg'))
        self.view_teacher = ViewTeacherDeskLabel("Vue prof", config.get('colors', 'board_bg'))
        self.is_view_students = None  # Current view

        self.sig_add_tile = None

        self.__set_layout()
        self.on_perspective_changed()  # This will switch the is_view_student flag and display the students' view

    def __set_layout(self):
        """
        Initializes the layout of this widget
        """
        layout = QVBoxLayout()

        # Widgets
        layout.addWidget(self.view_students)
        layout.addWidget(self.v_canvas)
        layout.addWidget(self.view_teacher)
        layout.addWidget(self.btn)
        layout.addWidget(self.btn_perspective)

        # Alignments
        layout.setAlignment(self.view_students, Qt.AlignCenter)
        layout.setAlignment(self.view_teacher, Qt.AlignCenter)

        self.setLayout(layout)

    def on_perspective_changed(self):
        """
        Switches the current view perspective and updates boards display and canvas
        """
        if self.is_view_students is None:  # To prevent updating the canvas for the initialization
            self.is_view_students = True
        else:
            self.is_view_students = not self.is_view_students
            self.v_canvas.perspective_changed()

        self.view_students.activate(self.is_view_students)
        self.view_teacher.activate(not self.is_view_students)

    def do_magic(self):
        self.sig_add_tile.emit()


class ViewMainFrame(QMainWindow):

    def __init__(self, sig_quit, config):
        """
        Main application's frame

        :param sig_quit: signal to trigger when the application closes
        :param config: application's parsed configuration
        """
        QMainWindow.__init__(self)
        self.central_widget = CentralWidget(config)
        self.setCentralWidget(self.central_widget)

        self.sig_quit = sig_quit

        self.setStyleSheet("QMainWindow {" + f"background-color: {config.get('colors', 'main_bg')};" + "}")

    def closeEvent(self, event):
        """
        Triggered on a close operation. Signals to the controller the event
        """
        self.sig_quit.emit()
        event.accept()
