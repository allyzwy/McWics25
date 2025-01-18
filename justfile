start:
	venv/bin/python3 App/app.py

install args:
	venv/bin/pip3 install {{args}}

fmt:
	venv/bin/black .
