from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import os

# in_file, out_file, text = sys.argv[1:]

print(sys.argv[1:])

print((os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'max_hp_table.csv'))))
