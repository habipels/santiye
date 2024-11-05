
import polib
from deep_translator import GoogleTranslator

# Load the .po file using polib
po = polib.pofile(r"C:\Users\habip\Documents\GitHub\santiye\sorani.po")
po2 = polib.pofile(r"C:\Users\habip\Documents\GitHub\santiye\ingilizce.po")

# Translator instance for Turkish to English
translator = GoogleTranslator(ource='auto', target='ckb')

# Translate each entry
for entry in po:
    if entry.msgid:  # Only translate if there's a msgstr (i.e., a Turkish translation exists)
        for i in po2:
            if i.msgstr and i.msgstr == entry.msgid:
                entry.msgid = i.msgid
                print(i.msgid)
        
# Save the translated file
translated_po_file_path = r'C:\Users\habip\Documents\GitHub\santiye\dsjango_translated.po'
po.save(translated_po_file_path)