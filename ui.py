import sys
import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QFileDialog, QWidget, QSizePolicy, QHBoxLayout, \
    QVBoxLayout, QDateEdit, QComboBox, QAbstractSpinBox, QSpacerItem
from PyQt5.QtCore import pyqtSignal, Qt, QEvent, QThread, pyqtSlot, QDate
from PyQt5.QtGui import QColor, QPalette
from PyQt5.uic import loadUi
from main_v2 import start_automation, Logger, check_quarter

import pandas as pd
from openpyxl.utils import get_column_letter
from check_rules import check_rules_ar2, check_rules_ar1, AR2_TO_CHECK, AR1_TO_CHECK
from generate_ar1_xml import create_xml_ar1
from generate_ar2_xml import create_xml_ar2


class QuarterlyDateEdit(QWidget):
    def __init__(self, parent=None):
        super(QuarterlyDateEdit, self).__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.year_combo = QComboBox(self)
        self.year_combo.addItems([str(year) for year in range(2000, 2031)])
        current_year = QDate.currentDate().year()  # Get the current year
        self.year_combo.setCurrentIndex(self.year_combo.findText(str(current_year)))
        self.year_combo.currentIndexChanged.connect(self.update_date)
        self.year_combo.setEnabled(False)  # Initially disabled
        self.year_combo.setFixedWidth(100)

        self.quarter_combo = QComboBox(self)
        self.quarter_combo.addItems(["Q1", "Q2", "Q3", "Q4"])
        current_quarter = (QDate.currentDate().month() - 1) // 3 + 1  # Get the current quarter
        self.quarter_combo.setCurrentIndex(current_quarter - 2)
        self.quarter_combo.currentIndexChanged.connect(self.update_date)
        self.quarter_combo.setEnabled(False)  # Initially disabled
        self.quarter_combo.setFixedWidth(100)

        self.date_edit = QDateEdit(self)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setEnabled(False)  # Initially disabled
        self.date_edit.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.date_edit.setFixedWidth(100)

        # Add a spacer to push the button to the center
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer)
        layout.addWidget(self.year_combo, alignment=Qt.AlignCenter)
        layout.addWidget(self.quarter_combo, alignment=Qt.AlignCenter)
        layout.addWidget(self.date_edit, alignment=Qt.AlignCenter)
        # Add another spacer to balance the layout
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.update_date()

    def update_date(self):
        year = int(self.year_combo.currentText())
        quarter = self.quarter_combo.currentIndex() + 1
        last_day_of_quarter = self.last_day_of_quarter(year, quarter)
        self.date_edit.setDate(last_day_of_quarter)

    def last_day_of_quarter(self, year, quarter):
        month = (quarter - 1) * 3 + 3
        last_day = QDate(year, month, 1).addMonths(1).addDays(-1)
        return last_day


class CheckThread(QThread):
    # Define custom signals to communicate with the main thread
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    log_updated = pyqtSignal(str)  # Custom signal to send log messages
    progress_text_updated = pyqtSignal(str)  # Custom signal for updating PasswordText label

    def __init__(self):
        super(CheckThread, self).__init__()
        self.progress = 0
        self.total_steps = 100

    def run(self):
        # Run the start_automation function
        print('Checking')

        # Call the start_automation function with progress_callback
        def progress_callback(step):
            self.progress = (step * 100) // self.total_steps
            self.progress_updated.emit(self.progress)

        # Call the start_automation function with progress_callback_text
        def progress_callback_text(text):
            self.progress_text_updated.emit(text)  # Emit the signal to update the PasswordText label

        perform_tests(progress_callback_text, progress_callback)

        # Emit the finished signal to indicate the completion
        self.finished.emit()

        # Enable the toolButton
        dialog.toolButton.setEnabled(True)
        dialog.radioButton_check.setEnabled(True)
        dialog.radioButton_xml.setEnabled(True)
        dialog.radioButton_prepare.setEnabled(True)
        dialog.pushButton_openAR1.setEnabled(True)
        dialog.pushButton_openAR2.setEnabled(True)


class ConvertThread(QThread):
    # Define custom signals to communicate with the main thread
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    log_updated = pyqtSignal(str)  # Custom signal to send log messages
    progress_text_updated = pyqtSignal(str)  # Custom signal for updating PasswordText label

    def __init__(self, date):
        super(ConvertThread, self).__init__()
        self.date = date.split('-')
        self.progress = 0
        self.total_steps = 100

    def run(self):
        # Run the start_automation function
        print('Making xml files.')

        # Call the start_automation function with progress_callback
        def progress_callback(step):
            self.progress = (step * 100) // self.total_steps
            self.progress_updated.emit(self.progress)

        def progress_callback_text(text):
            self.progress_text_updated.emit(text)  # Emit the signal to update the PasswordText label

        if dialog.AR2 is None:
            path_2 = f'EXAMPLE\\Filled\\' + f'{check_quarter()[1]}_Q{check_quarter()[3]}___BSP_AR2_v.4.01.xlsx'
        else:
            path_2 = dialog.AR2

        if dialog.AR1 is None:
            path_1 = f'EXAMPLE\\Filled\\' + f'{check_quarter()[1]}_Q{check_quarter()[3]}___BSP_AR1_ST.w.8.7.5.xlsx'
        else:
            path_1 = dialog.AR1

        # Perform all the tests
        df_nbp_2 = pd.read_excel(path_2, sheet_name=AR2_TO_CHECK, header=None, keep_default_na=False)
        df_nbp_1 = pd.read_excel(path_1, sheet_name=AR1_TO_CHECK, header=None, keep_default_na=False)

        create_xml_ar1(df_nbp_1, self.date, path_1, progress_callback, progress_callback_text)
        create_xml_ar2(df_nbp_2, self.date, progress_callback, progress_callback_text)

        # Emit the finished signal to indicate the completion
        self.finished.emit()

        # Disable the toolButton
        dialog.pushButton_convert.setEnabled(True)
        dialog.radioButton_check.setEnabled(True)
        dialog.radioButton_xml.setEnabled(True)
        dialog.radioButton_prepare.setEnabled(True)
        dialog.pushButton_openAR1.setEnabled(True)
        dialog.pushButton_openAR2.setEnabled(True)

        print(
            f"Files (PayTel_fjk_{self.date[0] + self.date[1] + self.date[2]}_AR2.xml and PayTel_fjk_{self.date[0] + self.date[1] + self.date[2]}_AR2.xml) created successfully.")


class AutomationThread(QThread):
    # Define custom signals to communicate with the main thread
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    log_updated = pyqtSignal(str)  # Custom signal to send log messages
    progress_text_updated = pyqtSignal(str)  # Custom signal for updating PasswordText label

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

        # Call the start_automation function with progress_callback_text
        def progress_callback_text(text):
            self.progress_text_updated.emit(text)  # Emit the signal to update the PasswordText label

        start_automation(self.name, self.surname, self.phone, self.email, self.password, progress_callback,
                         progress_callback_text)

        # Emit the finished signal to indicate the completion
        self.finished.emit()

        # Enable the toolButton
        dialog.toolButton.setEnabled(True)


class MyDialog(QDialog):
    editing_finished = pyqtSignal()
    progress_updated = pyqtSignal(int)

    @pyqtSlot(str)
    def update_progress_text(self, text):
        self.progressLabel.setText(text)

    @pyqtSlot(str)
    def update_display(self, message):
        self.TDisplay.append(message)
        scrollbar = self.TDisplay.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_date(self):
        # Handle date updates here if needed
        pass

    def __init__(self):
        super(MyDialog, self).__init__()

        # Load the UI from the XML file
        ui = loadUi("./UI/nbp_ui.ui", self)
        self.window_height = 755
        self.window_width = 365
        # Get the system palette
        system_palette = QApplication.palette()

        # Adjust the color role based on the Windows dark theme
        if system_palette.color(QPalette.Window).value() < 200:
            # Light theme
            print("Light color theme", system_palette.color(QPalette.Window).value())
            # new_color = QColor(240, 240, 240)
        else:
            # Dark theme
            print("Dark color theme")
            # new_color = QColor(45, 45, 45)

        # Set the window background color
        # system_palette.setColor(QPalette.Window, new_color)
        # self.setPalette(system_palette)

        # Create an instance of QuarterlyDateEdit
        self.quarterly_date_edit = QuarterlyDateEdit(self)
        self.quarterly_date_edit.year_combo.currentIndexChanged.connect(self.update_date)
        self.quarterly_date_edit.quarter_combo.currentIndexChanged.connect(self.update_date)

        # Find the existing QVBoxLayout named verticallayout_convert
        existing_layout = ui.findChild(QVBoxLayout, "verticallayout_convert")

        # Check if the layout exists
        if existing_layout is not None:
            # Add QuarterlyDateEdit to the existing layout
            existing_layout.insertWidget(0, self.quarterly_date_edit)
        else:
            print("No verticallayout_convert found in the loaded UI.")

        # Add existing components and QuarterlyDateEdit to verticallayout_convert
        # self.verticallayout_convert.addWidget(self.TDisplay)
        # self.verticallayout_convert.addWidget(self.progressLabel)
        # self.verticallayout_convert.addWidget(self.quarterly_date_edit)

        self.automation_thread = None
        self.check_thread = None
        self.convert_thread = None
        self.AR1 = None
        self.AR2 = None

        self.setup_table()  # Call the method to set up the table
        self.name = ""
        self.surname = ""
        self.enlarged = False  # track window state
        self.current_tab = 0

        # Set the fixed size of the window
        self.setFixedSize(self.window_width, self.window_height)

        # Connect the "Apply" buttons click events to their functions
        self.BName.clicked.connect(self.on_name_apply_clicked)
        self.BSurname.clicked.connect(self.on_surname_apply_clicked)
        self.BPhone.clicked.connect(self.on_phone_apply_clicked)
        self.BEmail.clicked.connect(self.on_email_apply_clicked)
        self.Start.clicked.connect(self.on_start_clicked)
        self.pushButton_convert.clicked.connect(self.on_convert_button_clicked)

        # Connect radio buttons
        self.radioButton_check.clicked.connect(lambda button: self.radio_buttons(button='check'))
        self.radioButton_prepare.clicked.connect(lambda button: self.radio_buttons(button='prepare'))
        self.radioButton_xml.clicked.connect(lambda button: self.radio_buttons(button='xml'))

        self.pushButton_openAR1.clicked.connect(lambda source: self.open_file_dialog(source='AR1'))
        self.pushButton_openAR2.clicked.connect(lambda source: self.open_file_dialog(source='AR2'))

        # Connect tabs
        self.tabWidget.tabBarClicked.connect(lambda index: self.toggle_window_size(index, source='tabWidget'))

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
        self.toolButton.clicked.connect(lambda: self.toggle_window_size(self.current_tab, source='toolButton'))

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
    def change_cell_background(self, row, col, r, g, b, excel):
        if excel == 'AR2':
            item = self.tableWidget_AR2.item(row, col)
        elif excel == 'AR1-ST.01':
            item = self.tableWidget_AR1_1.item(row, col)
        elif excel == 'AR1-ST.02':
            item = self.tableWidget_AR1_2.item(row, col)
        elif excel == 'AR1-ST.03':
            item = self.tableWidget_AR1_3.item(row, col)
        elif excel == 'AR1-ST.04':
            item = self.tableWidget_AR1_4.item(row, col)
        elif excel == 'AR1-ST.05':
            item = self.tableWidget_AR1_5.item(row, col)
        elif excel == 'AR1-ST.06':
            item = self.tableWidget_AR1_6.item(row, col)
        elif excel == 'AR1-ST.07':
            item = self.tableWidget_AR1_7.item(row, col)

        if 'item' in locals():
            item.setBackground(QColor(r, g, b))
        else:
            print('Item not declared.')

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
        self.tableWidget_AR2.setFixedSize(1572, 700)  # Adjust the values as needed
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

        for i in range(1, 8):
            exec(f"""
# Set default alignment for wrapped text in header
for col in range(self.tableWidget_AR1_{i}.columnCount()):
    header_item = self.tableWidget_AR1_{i}.horizontalHeaderItem(col)
    if header_item:
        header_item.setTextAlignment(Qt.AlignHCenter | Qt.TextWordWrap)

# Enable word wrapping for all cells
for row in range(self.tableWidget_AR1_{i}.rowCount()):
    for col in range(self.tableWidget_AR2.columnCount()):
        item = self.tableWidget_AR1_{i}.item(row, col)
        if item:
            item.setTextAlignment(Qt.AlignVCenter | Qt.TextWordWrap)
            self.tableWidget_AR1_{i}.setItem(row, col, item)
            if col > 1:  # Adjust the column index where alignment should be set
                item.setTextAlignment(
                    Qt.AlignVCenter | Qt.AlignHCenter)  # Align center for columns 2 and onward
            
self.tableWidget_AR1_{i}.setFixedSize(1072, 700)  # Adjust the values as needed
self.tableWidget_AR1_{i}.setColumnWidth(0, 80)
self.tableWidget_AR1_{i}.setColumnWidth(1, 200)
self.tableWidget_AR1_{i}.setColumnWidth(1, 350)

# Connect cell content change signal to row height adjustment
self.tableWidget_AR1_{i}.cellChanged.connect(self.adjust_row_heights)
""")

    def adjust_row_heights(self, row, col):
        # Adjust the row height based on the contents of the specified cell
        self.tableWidget_AR2.resizeRowToContents(row)

    def toggle_window_size(self, index, source):
        if self.enlarged and source == "toolButton":
            self.setFixedSize(self.window_width, self.window_height)  # Set your original size
            self.enlarged = False
        else:
            if index == 0:  # tab_AR2
                self.setFixedSize(1975, self.window_height)  # Set the enlarged size
                self.current_tab = 0
                self.enlarged = True
            elif index == 1:  # tab_AR1
                self.setFixedSize(1075, self.window_height)  # Set the enlarged size
                self.enlarged = True
                self.current_tab = 1

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
        if self.Start.text() == 'Start':
            password = self.TPassword.text()  # Use text() method instead of toPlainText()

            self.Start.text() == 'Exit'

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

            # Connect the password_text_updated signal from the AutomationThread to the update_password_text slot
            self.automation_thread.progress_text_updated.connect(self.update_progress_text)
            self.automation_thread.progress_updated.connect(self.update_progress)
            self.automation_thread.finished.connect(self.on_automation_finished)

            # Connect the log_updated signal to the logger.log_updated signal
            self.automation_thread.log_updated.connect(self.logger.log_updated)

            self.pushButton_openAR1.setEnabled(False)
            self.pushButton_openAR2.setEnabled(False)
            self.radioButton_prepare.setEnabled(False)
            self.radioButton_check.setEnabled(False)
            self.radioButton_xml.setEnabled(False)

            # Start the automation thread
            self.automation_thread.start()

        elif self.Start.text() == 'Exit':
            QApplication.quit()

    def on_convert_button_clicked(self):
        check_or_convert = self.pushButton_convert.text()

        selected_date = self.quarterly_date_edit.date_edit.date()
        date_string = selected_date.toString(Qt.ISODate)
        print("Selected Date:", selected_date.toString(Qt.ISODate))
        self.pushButton_convert.setEnabled(False)
        self.pushButton_openAR1.setEnabled(False)
        self.pushButton_openAR2.setEnabled(False)

        if check_or_convert == "CONVERT":
            # Start the convert thread
            self.convert_thread = ConvertThread(date_string)

            # Connect the password_text_updated signal from the ConvertThread to the update_password_text slot
            self.convert_thread.progress_text_updated.connect(self.update_progress_text)
            self.convert_thread.progress_updated.connect(self.update_progress)

            # Start the check thread
            self.convert_thread.start()

        elif check_or_convert == "CHECK":
            # Create the AutomationThread and start it
            self.check_thread = CheckThread()

            # Connect the password_text_updated signal from the ConvertThread to the update_password_text slot
            self.check_thread.progress_text_updated.connect(self.update_progress_text)
            self.check_thread.progress_updated.connect(self.update_progress)

            # Start the check thread
            self.check_thread.start()

        self.progressBar.setEnabled(True)

    def update_progress(self, progress):
        # Update the progress bar
        self.progressBar.setValue(progress)

    def append_text_to_cell(self, row, col, text_to_append, excel):
        if excel == 'AR2':
            current_item = self.tableWidget_AR2.item(row, col)
        elif excel == 'AR1-ST.01':
            current_item = self.tableWidget_AR1_1.item(row, col)
        elif excel == 'AR1-ST.02':
            current_item = self.tableWidget_AR1_2.item(row, col)
        elif excel == 'AR1-ST.03':
            current_item = self.tableWidget_AR1_3.item(row, col)
        elif excel == 'AR1-ST.04':
            current_item = self.tableWidget_AR1_4.item(row, col)
        elif excel == 'AR1-ST.05':
            current_item = self.tableWidget_AR1_5.item(row, col)
        elif excel == 'AR1-ST.06':
            current_item = self.tableWidget_AR1_6.item(row, col)
        elif excel == 'AR1-ST.07':
            current_item = self.tableWidget_AR1_7.item(row, col)
        else:
            print(f'Not declared in append_text_to_cell {excel}.')

        if 'current_item' in locals():
            current_text = current_item.text()
            new_text = current_text + " " + text_to_append
            current_item.setText(new_text)
        else:
            print(f'Not declared in append_text_to_cell {excel}.')

    def on_automation_finished(self):

        # Update the PasswordText label with the provided email
        progress_text = f"Report finished. Checking border conditions..."
        self.progressLabel.setText(progress_text)

        self.pushButton_openAR1.setEnabled(False)
        self.pushButton_openAR2.setEnabled(False)
        self.radioButton_prepare.setEnabled(False)
        self.radioButton_check.setEnabled(False)
        self.radioButton_xml.setEnabled(False)

        # Enable the "Start" button when the automation is finished
        self.Start.setEnabled(True)
        self.Start.setText("Exit")
        # Save the logs to the log file
        self.save_logs()

    def radio_buttons(self, button):
        if button == 'prepare':
            self.pushButton_convert.setEnabled(False)

            self.quarterly_date_edit.quarter_combo.setEnabled(False)
            self.quarterly_date_edit.year_combo.setEnabled(False)
            self.quarterly_date_edit.date_edit.setEnabled(False)

            self.radioButton_check.setChecked(False)
            self.radioButton_xml.setChecked(False)
            self.TName.setEnabled(True)
            self.BName.setEnabled(True)
            self.pushButton_openAR1.setEnabled(False)
            self.pushButton_openAR2.setEnabled(False)
            self.AR1 = None
            self.AR2 = None
            self.toolButton.setEnabled(False)
            self.enlarged = True
            self.toggle_window_size(self.current_tab, source="toolButton")
            self.pushButton_convert.setText("-")

        if button == 'check':
            self.pushButton_convert.setEnabled(True)

            self.quarterly_date_edit.quarter_combo.setEnabled(False)
            self.quarterly_date_edit.year_combo.setEnabled(False)
            self.quarterly_date_edit.date_edit.setEnabled(False)

            self.radioButton_prepare.setChecked(False)
            self.radioButton_xml.setChecked(False)
            self.TName.setEnabled(False)
            self.BName.setEnabled(False)
            self.pushButton_openAR1.setEnabled(True)
            self.pushButton_openAR2.setEnabled(True)
            self.enlarged = True
            self.toggle_window_size(self.current_tab, source="toolButton")
            self.pushButton_convert.setText("CHECK")

        if button == 'xml':
            self.pushButton_convert.setEnabled(True)

            self.quarterly_date_edit.quarter_combo.setEnabled(True)
            self.quarterly_date_edit.year_combo.setEnabled(True)
            self.quarterly_date_edit.date_edit.setEnabled(True)

            self.radioButton_prepare.setChecked(False)
            self.radioButton_check.setChecked(False)
            self.TName.setEnabled(False)
            self.BName.setEnabled(False)
            self.pushButton_openAR1.setEnabled(True)
            self.pushButton_openAR2.setEnabled(True)
            self.enlarged = True
            self.toggle_window_size(self.current_tab, source="toolButton")
            self.pushButton_convert.setText("CONVERT")

    def open_file_dialog(self, source):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)

        if file_name:
            if source == 'AR1':
                self.AR1 = file_name
            if source == 'AR2':
                self.AR2 = file_name

        if self.AR1 is not None and self.AR2 is not None:
            self.pushButton_openAR1.setEnabled(False)
            self.pushButton_openAR2.setEnabled(False)
            self.radioButton_prepare.setEnabled(False)
            self.radioButton_check.setEnabled(False)
            self.radioButton_xml.setEnabled(False)


def run_rule(ar, df, progress_callback_text=None, progress_callback=None):
    if progress_callback:
        progress_callback(0)

    # [sheet, boolean, row, column]
    rules_2 = ["PCP_090", "PCP_091", "PCP_092", "PCP_093", "PCP_094", "PCP_096", "PCP_099", "PCP_006",
               "PCP_095", "PCP_102", "PCP_105", "PCP_007", "PCP_108", "PCP_120", "PCP_109", "PCP_121",
               "PCP_111", "PCP_123", "PCP_245_R", "DSDs_038_R", "DSDs_040_R", "PCP_110", "PCP_122"]
    rules_1 = [
        "RW_ST.01_01", "RW_ST.01_02", "RW_ST.01_03", "RW_ST.01_04", "RW_ST.01_05", "RW_ST.01_06",
        "RW_ST.01_07", "RW_ST.01_08", "RW_ST.01_09", "RW_ST.01_10", "RW_ST.01_11", "RW_ST.01_12",
        "RW_ST.01_13", "RW_ST.01_14", "RW_ST.01_15", "RW_ST.01_16", "RW_ST.01_17", "RW_ST.01_18",
        "RW_ST.01_19", "RW_ST.01_20", "RW_ST.01_21", "RW_ST.01_22", "RW_ST.01_23", "RW_ST.01_24",
        "RW_ST.01_25", "RW_ST.01_26", "RW_ST.01_27", "RW_ST.01_28", "RW_ST.01_29", "RW_ST.01_30",

        "RW_ST.02_01", "RW_ST.02_02", "RW_ST.02_03", "RW_ST.02_04", "RW_ST.02_05", "RW_ST.02_06",
        "RW_ST.02_07",

        "RW_ST.03_01", "RW_ST.03_02", "RW_ST.03_03", "RW_ST.03_04", "RW_ST.03_05", "RW_ST.03_06",

        "RW_ST.04_01", "RW_ST.04_02", "RW_ST.04_03", "RW_ST.04_04", "RW_ST.04_05",

        "RW_ST.05_01", "RW_ST.05_02", "RW_ST.05_03", "RW_ST.05_04", "RW_ST.05_05", "RW_ST.05_06",
        "RW_ST.05_07", "RW_ST.05_08", "RW_ST.05_09", "RW_ST.05_10", "RW_ST.05_11", "RW_ST.05_12",
        "RW_ST.05_13",

        "RW_ST.06_01",

        "RW_ST.07_01", "RW_ST.07_02", "RW_ST.07_03", "RW_ST.07_04", "RW_ST.07_05", "RW_ST.07_06",
        "RW_ST.07_07"
    ]

    rule: str
    if ar == 2:
        for r, rule in enumerate(rules_2):
            if progress_callback_text:
                progress_callback_text(f"AR{ar} - {rule}")

            results = check_rules_ar2(ar, df, rule, 6)

            if progress_callback:
                percent = 100 / len(rules_2) * (r + 1)
                progress_callback(int(percent))

            for result in results:
                row = result[2]
                n = result[0]
                if result[1]:
                    dialog.change_cell_background(row, n + 3, 50, 205, 50, 'AR2')
                else:
                    dialog.change_cell_background(row, n + 3, 255, 0, 0, 'AR2')
                    dialog.append_text_to_cell(row, n + 3, f'; Error in column: {get_column_letter(result[3] + 1)}; ',
                                               'AR2')
    elif ar == 1:
        for r, rule in enumerate(rules_1):
            if progress_callback_text:
                progress_callback_text(f"AR{ar} - {rule}")

            results = check_rules_ar1(ar, df, rule, 13)

            if progress_callback:
                percent = 100 / len(rules_1) * (r + 1)
                progress_callback(int(percent))

            if results is None:
                continue
            for result in results:
                row = result[2]
                col = 3
                sheet = result[0]

                if result[1]:
                    dialog.change_cell_background(row, col, 50, 205, 50, f'AR1-ST.0{sheet}')
                else:
                    dialog.change_cell_background(row, col, 255, 0, 0, f'AR1-ST.0{sheet}')
                    dialog.append_text_to_cell(row, col,
                                               f'; Error in column: {get_column_letter(result[3] + 1)} - Value difference = {result[3]}; ',
                                               f'AR1-ST.0{sheet}')


def perform_tests(progress_callback_text=None, progress_callback=None):
    if dialog.AR2 is None:
        path_2 = f'EXAMPLE\\Filled\\' + f'{check_quarter()[1]}_Q{check_quarter()[3]}___BSP_AR2_v.4.01.xlsx'
    else:
        path_2 = dialog.AR2

    if dialog.AR1 is None:
        path_1 = f'EXAMPLE\\Filled\\' + f'{check_quarter()[1]}_Q{check_quarter()[3]}___BSP_AR1_ST.w.8.7.5.xlsx'
    else:
        path_1 = dialog.AR1

    na_values_list = ['N/A']
    # Perform all the tests
    df_nbp_2 = pd.read_excel(path_2, sheet_name=AR2_TO_CHECK, header=None, keep_default_na=False,
                             na_values=na_values_list)
    df_nbp_1 = pd.read_excel(path_1, sheet_name=AR1_TO_CHECK, header=None, keep_default_na=False,
                             na_values=na_values_list)
    run_rule(2, df_nbp_2, progress_callback_text, progress_callback)
    run_rule(1, df_nbp_1, progress_callback_text, progress_callback)

    if progress_callback_text:
        progress_callback_text('Report checked - open review tab >>>')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
