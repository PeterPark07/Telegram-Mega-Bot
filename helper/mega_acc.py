from mega import Mega

email = os.getenv('email')
password = os.getenv('pass')
mega = Mega()
m = mega.login(email, password)