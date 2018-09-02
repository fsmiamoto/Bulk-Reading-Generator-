# Bulk Reading Generatoe

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from japanese.reading import mecab

def generateReadings(select_cards, src, dst):
    cards = mw.col.findNotes(select_cards)
    changed_cards = 0
    for card_id in cards:
        card = mw.col.getNote(card_id)
        try:
            # If dst field not set...
            if not card[dst]:
                srcTxt = mw.col.media.strip(card[src])
                card[dst]= mecab.reading(srcTxt)
                card.flush()
                changed_cards += 1
        except:
            raise
    showInfo(str(changed_cards) + ' cards changed!')

class ReadingGenerator(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, parent=mw)
        self.readingsMenu()

    def readingsMenu(self):
        # Get collection decks
        decks = mw.col.decks.decks

        # Labels
        deck_lbl = QLabel("Deck Name")     
        src_lbl = QLabel("Source field")     
        dst_lbl = QLabel("Destination field")     

        # ComboBox for showing deck's names
        self.deck_sel = QComboBox()

        # Textbox's
        self.src_sel = QLineEdit()
        self.dst_sel = QLineEdit()

        # Add the decks names to the combo box
        deck_names = [dk['name'] for dk in decks.values()]
        # Sort names
        deck_names.sort()
        for name in deck_names:
            self.deck_sel.addItem(name)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(deck_lbl, 1, 0, 1, 1)
        grid.addWidget(self.deck_sel, 1, 1, 1, 2)
        grid.addWidget(src_lbl, 2, 0, 1, 1)
        grid.addWidget(self.src_sel, 2, 1, 1, 2)
        grid.addWidget(dst_lbl, 3, 0, 1, 1)
        grid.addWidget(self.dst_sel, 3, 1, 1, 2)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok
                            | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.on_accept)  
        button_box.rejected.connect(self.on_reject)  
        l_main = QVBoxLayout()
        l_main.addLayout(grid)
        l_main.addWidget(button_box) 
        self.setLayout(l_main)
        self.setMinimumWidth(200)  
        self.setWindowTitle('Generate Japanese Readings')

    def on_accept(self):
        src_field = self.src_sel.text()
        dst_field = self.dst_sel.text()
        deck_field = "deck:'"+ self.deck_sel.currentText() +"'"
        generateReadings(deck_field, src_field, dst_field)

    def on_reject(self):
        self.close()

def menu_call():
    dialog = ReadingGenerator(mw)
    dialog.exec_()

# Action that will be added to the menu
action = QAction("Reading Generator", mw)
# Set it to call generateReadings when it's clicked
action.triggered.connect(menu_call)
# Add action to the tools menu
mw.form.menuTools.addAction(action)

