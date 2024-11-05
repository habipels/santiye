import polib
from deep_translator import GoogleTranslator

# Load the .po file using polib
sorani = polib.pofile(r"C:\Users\habip\Documents\GitHub\santiye\sorani.po")
ingilizce = polib.pofile(r"C:\Users\habip\Documents\GitHub\santiye\ingilizce.po")
# Translator instance for Turkish to English
translator = GoogleTranslator(source='auto', target='tr')

for i in ingilizce:
    if i.msgstr:
        i.msgid = i.msgstr
        i.msgstr = ""

# Save the translated file
translated_po_file_path = r'C:\Users\habip\Documents\GitHub\santiye\donustu.po'
ingilizce.save(translated_po_file_path)

translated_po_file_path  # Return the path to the translated .po file
