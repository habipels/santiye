from bip38 import BIP38
from ecdsa import SECP256k1

# BIP38 şifreli anahtar
encrypted_key = "6PnPwpoLg5ZVtNx4jWbnfkQLn8L9xnsgEXVU3u5g3D52ELrshdPD3FXmmH"

# Parolayı manuel olarak belirle
password = 'A1 821_'

# BIP38 şifreli anahtarı çözme
bip38 = BIP38()
private_key = bip38.decrypt(encrypted_key, password)

print("Özel Anahtar:", private_key)
