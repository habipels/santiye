import polib
from deep_translator import GoogleTranslator

# Load the .po file using polib
po = polib.pofile(r"C:\Users\habip\Documents\GitHub\santiye\django_translated.po")

# Translator instance for Turkish to English
translator = GoogleTranslator(source='auto', target='tr')

# Translate each entry
for entry in po:
    if entry.msgid:  # Only translate if there's a msgstr (i.e., a Turkish translation exists)
        translated_text = translator.translate(entry.msgid)
        entry.msgstr = entry.msgid
# Save the translated file
translated_po_file_path = r'C:\Users\habip\Documents\GitHub\santiye\dsjango_translated.po'
po.save(translated_po_file_path)

translated_po_file_path  # Return the path to the translated .po file
translated = GoogleTranslator(source='auto', target='ckb', ).translate("Eline")
print(translated)