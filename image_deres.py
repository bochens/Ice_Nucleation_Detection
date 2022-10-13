from PIL import Image, ImageStat, ImageEnhance
import os
from os import listdir
from os.path import isfile, join

file_dir = "/Users/bochen/TAMU/Ice nucleation detection/fucoxanthin 5mgml/DCIM/101EOS5D"

output_dir = "/Users/bochen/TAMU/Ice nucleation detection/fucoxanthin 5mgml/DCIM/deres_adjusted_brightness"


def brightness(im_file):
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

jpeg_files = []
for f in os.listdir(file_dir):
    if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
        jpeg_files.append(f)

base_width = 1200

# read brightness of the first file
a_path = join(file_dir, jpeg_files[0])
#target_brightness = brightness(a_path)
target_brightness = 108.49451985677084
print(target_brightness)

for a_file in jpeg_files:
    a_path = join(file_dir, a_file)
    image_file = Image.open(a_path)
    enhancer = ImageEnhance.Brightness(image_file)

    this_brightness = brightness(a_path)
    brightness_factor = target_brightness / this_brightness
    im_output = enhancer.enhance(brightness_factor)

    exif = image_file.info['exif']
    width, height = im_output.size

    wpercent = (base_width/width)
    hsize = int((height*float(wpercent)))

    img = im_output.resize((base_width,hsize), Image.ANTIALIAS)
    a_file = "1"+a_file
    img.save(join(output_dir, a_file), quality=80, exif=exif)
    print(a_file)