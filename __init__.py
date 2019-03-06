#
# Bulk Reading Generator Plus - Anki 2.0 Version
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
from japanese.reading import mecab


def generateReadings(selectNotes, source, destination, allowOverwriting):
    """
        generateReadings - Generates the readings for
        notes selected with 'selectNotes' and then getting the source text from 'source' and
        outputs to 'destination'

        selectNotes - String that query's for the wanted notes
        Example: "deck:Sentences"

        source - Name of the source field. It can have more than one field separeted with ;
        Example: "Expression", "Expression;Word"

        destination - Destination fields
        Example: "Reading", "Expression Reading;Word Reading"

        allowOverwriting - Boolean value that determines if fields that are already populated 
        can be overwriten.
    """
    # Get the ID's of notes selected with the selectNotes string
    # e.g selectNotes = "deck:Sentences"
    noteIds = mw.col.findNotes(selectNotes)

    # Counter for changed notes
    changedNotes = 0

    # Multi field
    if(';' in destination and ';' in source):
        # Splits in ';' and removes extra whitespace
        destinationFields = [dest.strip() for dest in destination.split(';')]
        sourceFields = [src.strip() for src in source.split(';')]
    # Single field
    else:
        # Creates list with the only pair
        destinationFields = [destination.strip()]
        sourceFields = [source.strip()]

    for noteId in noteIds:

        note = mw.col.getNote(noteId)

        try:
            changedAnyField = False
            for destination, source in zip(destinationFields, sourceFields):
                # If the note doesn't have both of the fields, skip it.
                if(destination not in note.keys() or source not in note.keys()):
                    continue  # This is useful for decks that have multiple note types

                # If destination field not set...
                if allowOverwriting or not note[destination]:
                    # Get text from source field
                    sourceTxt = mw.col.media.strip(note[source])
                    # Generate reading of sourceText and output to destination
                    note[destination] = mecab.reading(sourceTxt)
                    # 'Save' note
                    note.flush()
                    changedAnyField = True

            if changedAnyField:
                changedNotes += 1
        except:
            raise

    # Show how many notes were changed
    if(changedNotes > 0):
        showInfo(str(changedNotes) + ' note(s) changed!')
    else:
        showInfo("No notes were changed!")

# Generates the dialog window.


class ReadingGenerator(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, parent=mw)
        self.readingsMenu()

    def readingsMenu(self):
        # Get collection decks
        decks = mw.col.decks.decks

        # Labels
        deckLbl = QLabel("Deck Name")
        sourceLbl = QLabel("Source field")
        destinationLbl = QLabel("Destination field")
        overwriteLbl = QLabel("Allow overwriting?")

        # ComboBox for showing deck's names
        self.deckSel = QComboBox()

        # Textbox's
        self.sourceSel = QLineEdit()
        self.destinationSel = QLineEdit()

        # CheckBox
        self.overwriteCheckBox = QCheckBox()

        # Default values for textboxes
        self.sourceSel.setText("Expression")
        self.destinationSel.setText("Reading")

        # Add the decks names to the combo box
        deckNames = [dk['name'] for dk in decks.values()]
        # Sort names
        deckNames.sort()
        # Insert deck names in ComboBox
        for name in deckNames:
            self.deckSel.addItem(name)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(deckLbl, 1, 0, 1, 1)
        grid.addWidget(self.deckSel, 1, 1, 1, 2)
        grid.addWidget(sourceLbl, 2, 0, 1, 1)
        grid.addWidget(self.sourceSel, 2, 1, 1, 2)
        grid.addWidget(destinationLbl, 3, 0, 1, 1)
        grid.addWidget(self.destinationSel, 3, 1, 1, 2)
        grid.addWidget(overwriteLbl, 4, 0, 1, 1)
        grid.addWidget(self.overwriteCheckBox, 4, 1, 1, 2)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.onAccept)
        buttonBox.rejected.connect(self.onReject)
        lMain = QVBoxLayout()
        lMain.addLayout(grid)
        lMain.addWidget(buttonBox)
        self.setLayout(lMain)
        self.setMinimumWidth(200)
        self.setWindowTitle('Generate Japanese Readings')

    def onAccept(self):
        """
            Handler for Ok button, calling the generateReadings method
        """
        # Get the source field name
        sourceField = self.sourceSel.text()
        # Get the destination field name
        destinationField = self.destinationSel.text()
        # String to query for the notes on the selected deck
        deckField = "deck:'" + self.deckSel.currentText() + "'"
        # CheckBox Value Boolean Value
        checkBoxValue = bool(self.overwriteCheckBox.checkState())
        # Generate readings with the obtained info
        generateReadings(deckField, sourceField,
                         destinationField, checkBoxValue)

    def onReject(self):
        self.close()


def menuCall():
    dialog = ReadingGenerator(mw)
    dialog.exec_()


# Action that will be added to the menu
action = QAction("Bulk Reading Generator Plus", mw)
# Set it to call generateReadings when it's clicked
action.triggered.connect(menuCall)
# Add action to the tools menu
mw.form.menuTools.addAction(action)
