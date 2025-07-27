from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
							 QStackedWidget, QTextEdit, QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import sys
import os
import json

class DoubleClicking(QListWidget):
	doubleClicked = pyqtSignal(QListWidgetItem)

	def mouseDoubleClickEvent(self, event):
		item = self.itemAt(event.pos())
		if item:
			self.doubleClicked.emit(item)
		super().mouseDoubleClickEvent(event)

class Notepad(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Notepad")
		self.setFixedSize(550, 550)

		self.setStyleSheet("""
			QMainWindow {
				background-color: #333;
			}

			QTextEdit {
				background-color: #444;
				color: white;
				font-size: 24px;
				border-radius: 5px;
			}

			QListWidget {
				background-color: #444;
				color: white;
				font-size: 24px;
				border: 1px solid #666;
				border-radius: 5px;
			}

			QInputDialog {
				background-color: #333;
				color: white
			}
			
			QMessageBox {
				background-color: #333;
				color: white
			}

			QLabel {
				color: white;
			}

			QPushButton {
				background-color: #555;
				color: white;
				border: 1px solid #666;
				padding: 5px;
				width: 65px;
				border-radius: 5px;
			}

			QPushButton:hover {
				border: 3px solid #666;
				border-radius: 7px;
			}
			"""
			)

		self.generalLayout = QVBoxLayout()
		centralWidget = QWidget(self)
		centralWidget.setLayout(self.generalLayout)
		self.setCentralWidget(centralWidget)

		self.stacked = QStackedWidget()
		self.generalLayout.addWidget(self.stacked)


		self.listNotes = QWidget()
		self.listNotesLayout = QVBoxLayout(self.listNotes)
		self.stacked.addWidget(self.listNotes)

		self.createDisplay()
		self.createButtons()

		self.notesScreen = QWidget()
		self.notesScreenLayout = QVBoxLayout(self.notesScreen)

		self.backBtnLayout = QHBoxLayout()
		self.backToMainBtn = QPushButton("⟵")
		self.backToMainBtn.clicked.connect(self.backToMain)
		self.backBtnLayout.addWidget(self.backToMainBtn)
		self.backBtnLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.notesScreenLayout.addLayout(self.backBtnLayout)

		self.notesEdit = QTextEdit()
		self.notesScreenLayout.addWidget(self.notesEdit)

		self.stacked.addWidget(self.notesScreen)

		self.dir = "notes"
		self.notesEdit.textChanged.connect(self.autoSave)
		self.loadNotes()

	def createDisplay(self):
		self.display = DoubleClicking()
		self.display.doubleClicked.connect(self.openNote)
		self.display.setFixedHeight(475)
		
	def createButtons(self):
		self.buttonsLayout = QHBoxLayout()

		createNoteBtn = QPushButton("+")
		removeNoteBtn = QPushButton("-")
		self.changeThemeBtn = QPushButton("☀")	
		createNoteBtn.clicked.connect(self.addNote)
		removeNoteBtn.clicked.connect(self.removeNote)
		self.changeThemeBtn.clicked.connect(self.changeTheme)

		self.buttonsLayout.addWidget(createNoteBtn)
		self.buttonsLayout.addWidget(removeNoteBtn)
		self.buttonsLayout.addWidget(self.changeThemeBtn)
		self.buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
		self.listNotesLayout.addLayout(self.buttonsLayout)
		self.listNotesLayout.addWidget(self.display)

	def addNote(self):
		title, ok = QInputDialog.getText(self, "Creating new note", "Enter the title for new note:", )
		if ok and title:
			item = QListWidgetItem(title)
			item.setData(Qt.ItemDataRole.UserRole, "")
			self.display.addItem(item)
			QMessageBox.information(
				self,
				"Done!",
				"Created the note",
			)

	def openNote(self, item):
		content = item.data(Qt.ItemDataRole.UserRole)
		self.notesEdit.setText(content)
		self.stacked.setCurrentIndex(1)

	def backToMain(self):
		current_item = self.display.currentItem()
		if current_item:
			current_item.setData(Qt.ItemDataRole.UserRole, self.notesEdit.toPlainText())
		self.stacked.setCurrentIndex(0)

	def removeNote(self):
		selected = self.display.currentRow()
		if selected != -1:
			self.display.takeItem(selected)
			QMessageBox.information(
				self,
				"Done!",
				"Note has been removed"
			)
		else:
			QMessageBox.critical(
				self,
				"Failed!",
				"Please, select the note!",
				QMessageBox.StandardButton.Ok
			)

	def changeTheme(self):
		if self.changeThemeBtn.text() == "☀":
			self.setStyleSheet("""
			QMainWindow {
				background-color: white;
			}

			QTextEdit {
				background-color: white;
				color: black;
				font-size: 24px;
				border: 1px solid #ccc;
				border-radius: 5px;
			}

			QListWidget {
				background-color: white;
				color: black;
				font-size: 24px;
				border: 1px solid #ccc;
				border-radius: 5px;
			}

			QInputDialog {
				background-color: white;
				color: black;
			}
			
			QMessageBox {
				background-color: white;
				color: black
			}

			QLabel {
				color: black;
			}

			QPushButton {
				background-color: #f0f0f0;
				color: black;
				border: 1px solid #ccc;
				padding: 5px;
				width: 65px;
				border-radius: 5px;
			}

			QPushButton:hover {
				border: 3px solid #ccc;
				border-radius: 7px;
			}
			"""
			)
			self.changeThemeBtn.setText("☾")
		else:
			self.setStyleSheet("""
			QMainWindow {
				background-color: #333;
			}

			QTextEdit {
				background-color: #444;
				color: white;
				border: 1px solid #666;
				border-radius: 5px;
				font-size: 24px;
			}

			QListWidget {
				background-color: #444;
				color: white;
				font-size: 24px;
				border: 1px solid #666;
				border-radius: 5px;
			}

			QInputDialog {
				background-color: #333;
				color: white
			}
			
			QMessageBox {
				background-color: #333;
				color: white
			}

			QLabel {
				color: white;
			}

			QPushButton {
				background-color: #555;
				color: white;
				border: 1px solid #666;
				border-radius: 5px;
				padding: 5px;
				width: 65px;
			}

			QPushButton:hover {
				border: 3px solid #666;
				border-radius: 7px;
			}
			"""
			)
			self.changeThemeBtn.setText("☀")


	def closeEvent(self, event):
		self.saveNotes()
		event.accept()

	def saveNotes(self):
		if not os.path.exists(self.dir):
			os.makedirs(self.dir)
            
		notes_data = {}
		for i in range(self.display.count()):
			item = self.display.item(i)
			title = item.text()
			content = item.data(Qt.ItemDataRole.UserRole)
            
			filename = os.path.join(self.dir, f"{title}.txt")
			try:
				with open(filename, "w", encoding="utf-8") as f:
					f.write(content)
				notes_data[title] = filename
			except Exception as e:
				print(f"Save error {title}: {e}")
                
		with open(os.path.join(self.dir, "_meta.json"), "w") as f:
			json.dump({
				"notes_order": [self.display.item(i).text() for i in range(self.display.count())]
			}, f)

	def loadNotes(self):
		if not os.path.exists(self.dir):
			return
            
		order = []
		meta_path = os.path.join(self.dir, "_meta.json")
		if os.path.exists(meta_path):
			with open(meta_path, "r") as f:
				try:
					order = json.load(f).get("notes_order", [])
				except:
					order = []
                    
		loaded_titles = set()
		for title in order:
			filename = os.path.join(self.dir, f"{title}.txt")
			if os.path.exists(filename):
				try:
					with open(filename, "r", encoding="utf-8") as f:
						content = f.read()
					item = QListWidgetItem(title)
					item.setData(Qt.ItemDataRole.UserRole, content)
					self.display.addItem(item)
					loaded_titles.add(title)
				except:
					continue
                    
		for filename in os.listdir(self.dir):
			if filename.endswith(".txt") and filename != "_meta.json":
				title = os.path.splitext(filename)[0]
				if title not in loaded_titles:
					try:
						with open(os.path.join(self.dir, filename), "r", encoding="utf-8") as f:
							content = f.read()
						item = QListWidgetItem(title)
						item.setData(Qt.ItemDataRole.UserRole, content)
						self.display.addItem(item)
					except:
						continue

    
	def autoSave(self):
		if self.display.currentItem():
			self.saveNotes()

def main():
	app = QApplication(sys.argv)
	notepad = Notepad()
	notepad.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()