# Testing image recognition models
# Run make 
<h3>Usage of building recognition model</h3>
<h4>Function is called "process_image" and can be used as followed:</h4>

```python
# example usage
from building_rec_module import process_image

# define input
image_path = 'pics/test.jpeg'

# detect and label location
process_image(image_path, color_set='default')

# detect data containers
detect_containers(image_path)
```

# To use the container detection function run:

```bash
python container_rec_module.py  
```
