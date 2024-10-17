from PIL import Image
import cairosvg

def convert_image_to_svg(input_path, output_path):
    # Buka gambar dan konversi ke format PNG (untuk memastikan kompatibilitas)
    image = Image.open(input_path)
    image.save("temp.png", format="PNG")

    # Konversi dari PNG ke SVG
    cairosvg.png2svg(url="temp.png", write_to=output_path)

    print(f"Converted {input_path} to {output_path}")

# Contoh penggunaan
input_image_path = 'pengajuandana.jpg'  # Ganti dengan path gambar Anda
output_svg_path = 'output_image.svg'  # Ganti dengan path output yang diinginkan

convert_image_to_svg(input_image_path, output_svg_path)