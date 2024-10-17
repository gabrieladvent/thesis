from PIL import Image
import os

# Path folder dengan file JPEG
input_folder = 'temp'

# Path folder untuk menyimpan file JPG
output_folder = 'resultRename'

# Pastikan output folder sudah ada
os.makedirs(output_folder, exist_ok=True)

# Loop untuk mengubah setiap file JPEG ke format JPG
for filename in os.listdir(input_folder):
    if filename.endswith(".jpeg") or filename.endswith(".JPEG"):
        # Baca file JPEG
        with Image.open(os.path.join(input_folder, filename)) as img:
            # Simpan sebagai file JPG
            new_filename = os.path.splitext(filename)[0] + '.jpg'
            img.save(os.path.join(output_folder, new_filename), 'JPEG')
