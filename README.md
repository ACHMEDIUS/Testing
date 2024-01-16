# Testing image recognition models
# Run make 
<h4>Usage of building recognition and container detection:</h4>

```python
# import
from building_rec_module import process_dot, process_middle

# image paths
image_path = "pics/test.jpeg"
output_folder = 'pics/output'
color_set = 'set1'

# example usage
process_dot(image_path, color_set, output_folder)
# or
process_middle(image_path, color_set, output_folder)
```
