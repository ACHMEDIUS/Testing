# Create a virtual environment called openai-env
venv:
	python3 -m venv openai-env

# Activate the virtual environment
activate:
	source openai-env/Scripts/activate

# Install required Python packages
install:
	pip install -r requirements.txt
