# Create a virtual environment called openai-env
venv:
	python3 -m venv venv

# Activate the virtual environment
activate:
	source venv/bin/activate

# Install required Python packages
install:
	pip install -r requirements.txt
