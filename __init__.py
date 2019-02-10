#
# Bulk Reading Generator Plus
#
# An attempt to improve the buld reading generation
# interface.
#
# Author: Francisco Miamoto
# GitHub: /fsmiamoto
#

# Dependencies
from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw
import sys

# Append path to use the Japanese Suport provided method
# The number corresponds to the addon ID
sys.path.append("../3918629684")

# Because the name of the module is invalid, a number in this case,
# imports japanese module with alternative syntax.
japanese = __import__("3918629684")


def generateReadings(select_cards, src, dst):
    """
        generateReadings - Generates the readings for
        cards selected with 'select_cards' and then getting the source text from 'src' and
        outputs to 'dst'
    """
    # Get cards from collection
    cards_id = mw.col.findNotes(select_cards)
    # Counter for changed cards
    changed_cards = 0

    # Multifield option
    if( ';' in dst and ';' in src):
        dst_fields = dst.strip().split(';')
        src_fields = src.strip().split(';')
    else:
        # Creates list with the only pair
        dst_fields = [ dst ]
        src_fields = [ src ]

    # For every card ID in cards_id
    for card_id in cards_id:
        # Get the note
        card = mw.col.getNote(card_id)
        try:
            # If any field is changed, it will be set to true
            changed_any_field = False
            # For every pair of filds in dst and src
            for dst,src in zip(dst_fields, src_fields): 
                # If the note doesn't have the fields, skip it.
                # This is useful for decks that have multiple note types
                if(dst not in card.keys() or src not in card.keys()):
                    continue

                # If dst field not set...
                if not card[dst]:
                    # Get source text
                    srcTxt = mw.col.media.strip(card[src])
                    # Generate reading of srcText and output to dst
                    card[dst] = japanese.reading.mecab.reading(srcTxt)
                    # 'Save' card
                    card.flush()
                    changed_any_field = True

            # Increment if any field of this note was changed
            if changed_any_field:
                changed_cards += 1
        except:
            raise

    # Show how many cards were changed
    if(changed_cards > 0):
        showInfo(str(changed_cards) + ' cards changed!')
    else:
        showInfo("No cards were changed!")

# Generates the dialog window.
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

        # Default values for textboxes
        self.src_sel.setText("Expression")
        self.dst_sel.setText("Reading")

        # Add the decks names to the combo box
        deck_names = [dk['name'] for dk in decks.values()]
        # Sort names
        deck_names.sort()
        # Insert deck names in ComboBox
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
        """
            Handler for Ok button, calling the generateReadings method
        """
        # Get the source field name
        src_field = self.src_sel.text()
        # Get the destination field name
        dst_field = self.dst_sel.text()
        # String to query for the cards on the selected deck
        deck_field = "deck:'" + self.deck_sel.currentText() + "'"
        # Generate readings with the obtained info
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
