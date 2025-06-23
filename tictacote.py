


from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QLabel,
    QWidget, QFileDialog, 
)
import sys

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Τρίλιζα")
        
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setStyleSheet("""
            QLabel {
                background-image: url('ff.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)
        self.bg_label.lower()  #  background πίσω απ' όλα τα κουμπιά
        
        
        self.board_buttons = []      # κουμπιά τρίλιζας
        self.button_states = []      # καταστάσεις 0, 1, 2 ("" / X / O), αντι να γράφει κάποιος
        
    
            
        # Δημιουργία 3x3 κουμπιών για τρίλιζα. Το έκανα χειροκίνητα αρχικά, έψαξα μετά αυτοματοποιημένο τρόπο
        start_x = 90
        start_y = 60
        width = 60
        height = 30

        for row in range(3):
            for col in range(3):
                button = QPushButton("", self)
                x = start_x + col * width
                y = start_y + row * height 
                button.setGeometry(x, y, width, height)
                button.setStyleSheet("font-size: 16px;")
                button.clicked.connect(self.handle_click)
                
                self.board_buttons.append(button)
                self.button_states.append(0)

        # QLineEdit για μηνύματα ("Παίξε!", "Κλείδωσε!" "Νικητής ο ...".)
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(90, 20, 200, 25)
        
        # Κουμπί Check
        self.check_button = QPushButton("Check", self)
        self.check_button.setGeometry(200, 180, 80, 30)
        self.check_button.clicked.connect(self.Check)

        # Κουμπί Clear
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(290, 180, 80, 30)
        self.clear_button.clicked.connect(self.clear)

        

        # Κουμπί αλλαγής background
        self.bg_button = QPushButton("Change Background", self)
        self.bg_button.setGeometry(380, 260, 150, 30)
        self.bg_button.clicked.connect(self.change_background)
        self.bg_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)

        # Στυλ για Check, Clear, Play
        for btn in [self.check_button, self.clear_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 8px 14px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)

        # Widget για εικόνα background
        self.output_container = QWidget(self)
        self.output_container.setGeometry(400, 50, 150, 150)
        self.output_container.setStyleSheet("""
            QWidget {
                background-image: url('west_mani.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
                border-radius: 8px;
            }
        """)

    # Πάτημα κουμπιού στο ταμπλό
    def handle_click(self):
        button = self.sender() # αυτό ήταν αρκετά μυστήρια λειτουργία.
        index = self.board_buttons.index(button)
        self.button_states[index] = (self.button_states[index] + 1) % 3
        state = self.button_states[index]

        if state == 1:
            button.setText("X")
        elif state == 2:
            button.setText("O")
        else:
            button.setText("")

    # Check: κλείδωμα κουμπιών που έχουν τιμή
    def Check(self):
        for button in self.board_buttons:
            if button.text() == "X" or button.text() == "O":
                button.setEnabled(False)
        self.text_input.setText("Κλείδωσε!")
        self.check_winner()

    

    # Clear: επαναφορά κουμπιών και κατάστασης
    def clear(self):
        for button in self.board_buttons:
            button.setText("")
            button.setEnabled(True)
        self.button_states = [0] * 9
        self.text_input.setText("")

    # Αλλαγή εικόνας φόντου
    def change_background(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        dialog.setViewMode(QFileDialog.Detail)
        
        if dialog.exec_():
            file_path = dialog.selectedFiles()[0]
            css_path = file_path.replace("\\", "/")
            
            self.bg_label.setStyleSheet(f"""
            QLabel {{
                background-image: url('{css_path}');
                background-repeat: no-repeat;
                background-position: center center;
                background-size: cover;
            }}
        """)
    def resizeEvent(self, event):
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            super().resizeEvent(event)     
        
    def check_winner(self):
        winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Οριζόντια
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Κάθετα
        [0, 4, 8], [2, 4, 6] ]             # Διαγώνια
  
        for combo in winning_combinations:
            values = [self.board_buttons[i].text() for i in combo]
            if values[0] != "" and values.count(values[0]) == 3:
                winner = values[0]
                self.text_input.setText(f"Νικητής: {winner}")
                for btn in self.board_buttons:
                    btn.setEnabled(False)
                return

        # Αν όλα τα κουμπιά έχουν συμπληρωθεί χωρίς νικητή
        if all(btn.text() != "" for btn in self.board_buttons):
            self.text_input.setText("Ισοπαλία!")

app = QApplication(sys.argv)
app.setFont(QFont("Calibri", 11))
window = MainWindow()
window.show()
sys.exit(app.exec_())
