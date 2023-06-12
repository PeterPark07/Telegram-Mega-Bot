from mega import Mega
import os
email = os.getenv('email')
password = os.getenv('pass')
mega = Mega()
m = mega.login(email, password)