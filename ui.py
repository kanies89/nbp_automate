import sys
import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt, QEvent, QThread, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from main import start_automation, Logger, check_quarter
from check import AR2_TO_CHECK
import importlib
import pandas as pd
from openpyxl.utils import get_column_letter


class CheckThread(QThread):
    # Define custom signals to communicate with the main thread

    def __init__(self):
        super(CheckThread, self).__init__()

    def run(self):
        # Run the start_automation function
        print('Checking')

        # Call the start_automation function with progress_callback
        def progress_callback(step):
            self.progress = (step * 100) // self.total_steps
            self.progress_updated.emit(self.progress)

        perform_tests()

        # Emit the finished signal to indicate the completion
        self.finished.emit()


class AutomationThread(QThread):
    # Define custom signals to communicate with the main thread
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    log_updated = pyqtSignal(str)  # Custom signal to send log messages

    def __init__(self, name, surname, phone, email, password):
        super(AutomationThread, self).__init__()
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.password = password
        self.progress = 0
        self.total_steps = 100  # You can adjust this value based on the total steps in start_automation

    def run(self):
        # Run the start_automation function
        print('starting the function')

        # Call the start_automation function with progress_callback
        def progress_callback(step):
            self.progress = (step * 100) // self.total_steps
            self.progress_updated.emit(self.progress)

        start_automation(self.name, self.surname, self.phone, self.email, self.password, progress_callback)

        # Emit the finished signal to indicate the completion
        self.finished.emit()


class MyDialog(QDialog):
    editing_finished = pyqtSignal()
    # Custom signal for progress updates
    progress_updated = pyqtSignal(int)

    @pyqtSlot(str)
    def update_display(self, message):
        self.TDisplay.append(message)
        # Scroll to the last row
        scrollbar = self.TDisplay.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def __init__(self):
        super(MyDialog, self).__init__()
        # Load the UI from the XML file
        loadUi("./UI/nbp_ui.ui", self)

        self.automation_thread = None
        self.check_thread = None

        self.setup_table()  # Call the method to set up the table
        self.name = ""
        self.surname = ""
        self.enlarged = False  # track window state

        # Set the fixed size of the window
        self.setFixedSize(402, 528)

        # Connect the "Apply" buttons click events to their functions
        self.BName.clicked.connect(self.on_name_apply_clicked)
        self.BSurname.clicked.connect(self.on_surname_apply_clicked)
        self.BPhone.clicked.connect(self.on_phone_apply_clicked)
        self.BEmail.clicked.connect(self.on_email_apply_clicked)
        self.Start.clicked.connect(self.on_start_clicked)

        # Set the password field to display asterisks
        self.TPassword.setEchoMode(QLineEdit.Password)

        # Install the event filter for the QTextEdit widgets
        self.TName.installEventFilter(self)
        self.TSurname.installEventFilter(self)
        self.TPhone.installEventFilter(self)
        self.TEmail.installEventFilter(self)
        self.TPassword.installEventFilter(self)

        # Dictionary to map each widget with its corresponding button and the next widget in line
        self.widget_button_map = {
            self.TName: (self.BName, self.TSurname),
            self.TSurname: (self.BSurname, self.TPhone),
            self.TPhone: (self.BPhone, self.TEmail),
            self.TEmail: (self.BEmail, self.TPassword),
            self.TPassword: (self.Start, None),
        }

        # Connect the clicked signal of the toolbutton
        self.toolButton.clicked.connect(self.toggle_window_size)

        # Create the logger object
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name = f'Log/{report_date}_LOG.txt'
        log_file = open(log_file_name, "w")
        self.logger = Logger(log_file)

        # Connect the log_updated signal from the logger to the update_display slot
        self.logger.log_updated.connect(self.update_display)

        # Assign the logger as the new sys.stdout
        sys.stdout = self.logger

    def save_logs(self):
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name = f'Log/{report_date}_LOG.txt'
        with open(log_file_name, 'w') as log_file:
            log_file.write(self.TDisplay.toPlainText())

    # Method to change the background color of a cell
    def change_cell_background(self, row, col, r, g, b):
        item = self.tableWidget_AR2.item(row, col)
        if item:
            item.setBackground(QColor(r, g, b))

    def setup_table(self):
        # Set default alignment for wrapped text in header
        for col in range(self.tableWidget_AR2.columnCount()):
            header_item = self.tableWidget_AR2.horizontalHeaderItem(col)
            if header_item:
                header_item.setTextAlignment(Qt.AlignHCenter | Qt.TextWordWrap)

        # Enable word wrapping for all cells
        for row in range(self.tableWidget_AR2.rowCount()):
            for col in range(self.tableWidget_AR2.columnCount()):
                item = self.tableWidget_AR2.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.TextWordWrap)
                    self.tableWidget_AR2.setItem(row, col, item)
                    if col > 1:  # Adjust the column index where alignment should be set
                        item.setTextAlignment(
                            Qt.AlignVCenter | Qt.AlignHCenter)  # Align center for columns 2 and onward

        # Connect cell content change signal to row height adjustment
        self.tableWidget_AR2.cellChanged.connect(self.adjust_row_heights)

        # Set the width and height of the QtableWidget_AR2
        self.tableWidget_AR2.setFixedSize(1572, 500)  # Adjust the values as needed
        self.tableWidget_AR2.setColumnWidth(0, 80)
        self.tableWidget_AR2.setColumnWidth(1, 200)
        self.tableWidget_AR2.setColumnWidth(3, 50)
        self.tableWidget_AR2.setColumnWidth(4, 50)
        self.tableWidget_AR2.setColumnWidth(6, 95)
        self.tableWidget_AR2.setColumnWidth(10, 100)
        self.tableWidget_AR2.setColumnWidth(11, 105)
        self.tableWidget_AR2.setColumnWidth(12, 90)
        self.tableWidget_AR2.setColumnWidth(13, 50)
        self.tableWidget_AR2.setColumnWidth(14, 60)
        self.tableWidget_AR2.setColumnWidth(15, 70)
        self.tableWidget_AR2.setColumnWidth(16, 70)

    def adjust_row_heights(self, row, col):
        # Adjust the row height based on the contents of the specified cell
        self.tableWidget_AR2.resizeRowToContents(row)

    def toggle_window_size(self):
        if self.enlarged:
            self.setFixedSize(402, 528)  # Set your original size
            self.enlarged = False
        else:
            self.setFixedSize(1975, 528)  # Set the enlarged size
            self.enlarged = True

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj in [self.TName, self.TSurname, self.TPhone, self.TEmail,
                                                       self.TPassword]:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # Get the corresponding button and next widget
                button, next_widget = self.widget_button_map[obj]

                # Emit the editing_finished signal and click the appropriate button
                self.editing_finished.emit()
                button.click()

                # Move the focus to the next widget in line if available
                if next_widget:
                    next_widget.setFocus()

                return True

        return super().eventFilter(obj, event)

    def on_name_apply_clicked(self):
        name = self.TName.toPlainText()
        # Do something with the name input
        print("Name:", name)

        # Store the name
        self.name = name

        # Disable the current input field and enable the next one
        self.TName.setEnabled(False)
        self.BName.setEnabled(False)
        self.TSurname.setEnabled(True)
        self.BSurname.setEnabled(True)

        # Create the AutomationThread and start it
        self.check_thread = CheckThread()
        # self.automation_thread.progress_updated.connect(self.update_progress)
        # self.automation_thread.finished.connect(self.on_automation_finished)

        # Start the check thread
        self.check_thread.start()

    def on_surname_apply_clicked(self):
        surname = self.TSurname.toPlainText()
        # Do something with the surname input
        print("Surname:", surname)

        # Store the surname
        self.surname = surname

        # Disable the current input field and enable the next one
        self.TSurname.setEnabled(False)
        self.BSurname.setEnabled(False)
        self.TPhone.setEnabled(True)
        self.BPhone.setEnabled(True)

    def on_phone_apply_clicked(self):
        phone = self.TPhone.toPlainText()

        # Disable the current input field and enable the next one
        self.TPhone.setEnabled(False)
        self.BPhone.setEnabled(False)
        self.TEmail.setEnabled(True)
        self.BEmail.setEnabled(True)

    def on_email_apply_clicked(self):
        email = self.TEmail.toPlainText()

        # Disable the current input field and enable the next one
        self.TEmail.setEnabled(False)
        self.BEmail.setEnabled(False)
        self.TPassword.setEnabled(True)
        self.Start.setEnabled(True)

        # Update the PasswordText label with the provided email
        user_text = f"Provide password to your personal account for user: {self.name} {self.surname}"
        self.PasswordText.setText(user_text)

    def on_start_clicked(self):
        password = self.TPassword.text()  # Use text() method instead of toPlainText()

        # Disable the current input field and enable the "Start" button
        self.TPassword.setEnabled(False)
        self.Start.setEnabled(False)
        self.progressBar.setEnabled(True)

        # Get the input values from other fields
        name = self.TName.toPlainText()  # Use toPlainText() for QTextEdit
        surname = self.TSurname.toPlainText()  # Use toPlainText() for QTextEdit
        phone = self.TPhone.toPlainText()  # Use toPlainText() for QTextEdit
        email = self.TEmail.toPlainText()  # Use toPlainText() for QTextEdit

        # Create the AutomationThread and start it
        self.automation_thread = AutomationThread(name, surname, phone, email, password)
        self.automation_thread.progress_updated.connect(self.update_progress)
        self.automation_thread.finished.connect(self.on_automation_finished)

        # Connect the log_updated signal to the logger.log_updated signal
        self.automation_thread.log_updated.connect(self.logger.log_updated)

        # Start the automation thread
        self.automation_thread.start()

    def update_progress(self, progress):
        # Update the progress bar
        self.progressBar.setValue(progress)

    def append_text_to_cell(self, row, col, text_to_append):
        current_item = self.tableWidget_AR2.item(row, col)
        if current_item:
            current_text = current_item.text()
            new_text = current_text + " " + text_to_append
            current_item.setText(new_text)

    def on_automation_finished(self):
        # Enable the "Start" button when the automation is finished
        self.Start.setEnabled(True)
        # Save the logs to the log file
        self.save_logs()


def run_rule(col_from, col_to, dataframe, rule_number, row):
    rule_module = importlib.import_module('check')
    rule_function_name = f'rule_{rule_number}'
    rule_function = getattr(rule_module, rule_function_name, None)

    if rule_function is None or not callable(rule_function):
        raise ValueError(f"Rule {rule_function_name} not found or not callable")

    for n in range(col_from, col_to):
        bool = True
        results = rule_function(dataframe, n - 3)

        for result in results:
            if not result[1]:
                dialog.change_cell_background(row, n, 255, 0, 0)
                if rule_number != 24 and rule_number != 29:
                    dialog.append_text_to_cell(row, n, f'; Error in column: {get_column_letter(result[2] + 1)}; ')
                else:
                    dialog.append_text_to_cell(row, n, f'; Error in column: {result[2]}; ')
                bool = False

            if result[1] and bool:
                dialog.change_cell_background(row, n, 50, 205, 50)


def perform_tests():
    date = check_quarter()
    # path = f'EXAMPLE\\Filled\\' + f'BSP_AR2_v.4.0_Q{date[3]}{datetime.date.today().strftime("%Y")}_{datetime.date.today().strftime("%Y%m%d")}.xlsx'
    path = "C:\\Users\\Krzysztof kaniewski\\PycharmProjects\\pythonProject\\Example\\Filled\\BSP_AR2_v.4.0_Q12023_20230721-9RL-NO-ZEROS.xlsx"
    # Perform all the tests
    df_nbp = pd.read_excel(path, sheet_name=AR2_TO_CHECK, header=None, keep_default_na=False)
    # Call the function
    run_rule(5, 13, df_nbp, 1, 0)
    run_rule(5, 13, df_nbp, 2, 1)
    run_rule(5, 13, df_nbp, 3, 2)
    run_rule(5, 13, df_nbp, 4, 3)
    run_rule(5, 13, df_nbp, 5, 4)
    run_rule(5, 13, df_nbp, 6, 5)
    run_rule(5, 13, df_nbp, 7, 6)
    run_rule(5, 13, df_nbp, 8, 7)
    run_rule(5, 13, df_nbp, 9, 8)
    run_rule(5, 13, df_nbp, 10, 9)
    run_rule(5, 13, df_nbp, 11, 10)
    run_rule(5, 13, df_nbp, 12, 11)
    run_rule(9, 13, df_nbp, 13, 12)
    run_rule(9, 13, df_nbp, 14, 13)
    run_rule(9, 13, df_nbp, 15, 14)
    run_rule(9, 13, df_nbp, 16, 15)
    run_rule(9, 13, df_nbp, 17, 16)
    run_rule(9, 13, df_nbp, 18, 17)
    run_rule(9, 13, df_nbp, 19, 18)
    run_rule(9, 13, df_nbp, 20, 19)
    run_rule(15, 17, df_nbp, 21, 20)
    run_rule(15, 17, df_nbp, 22, 21)
    run_rule(15, 17, df_nbp, 23, 22)
    run_rule(15, 17, df_nbp, 24, 23)

    run_rule(15, 17, df_nbp, 26, 25)
    run_rule(15, 17, df_nbp, 27, 26)
    run_rule(15, 17, df_nbp, 29, 28)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
