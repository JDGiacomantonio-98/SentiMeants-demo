from app import burner


def powderize(psw):
	return burner.generate_password_hash(psw)


def reidrate_hash(pswHash, psw):
	return burner.check_password_hash(pswHash, psw)
