from building_rec_module import process_image
# from container_rec_module import detect_containers

# Usage
image_path = 'pics/test3.jpeg'
output_folder = 'pics/output'

# Print label using default color set
# process_image(image_path)

# Print label using a specific color set
process_image(image_path, color_set='set1', output_folder=output_folder)

