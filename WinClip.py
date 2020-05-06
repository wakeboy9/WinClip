# -*- coding: utf-8 -*-
import win32clipboard as win32
from PIL import Image, ImageGrab
from io import BytesIO
import struct

# Set the clipboard to have the data of given type
def set_clipboard(type, data):
	win32.OpenClipboard()
	win32.EmptyClipboard()
	win32.SetClipboardData(type, data)
	win32.CloseClipboard()


# Get PNG size in MB
def get_size(img):
		with BytesIO() as out:
			img.save(out, 'png')
			size = out.tell()

		mb = 1024 * 1024

		return round(size / mb, 2)

def clip():
	# Grab the clipboard and do stuff if it's an image
	img = ImageGrab.grabclipboard()
	if isinstance(img, Image.Image):
		rows, cols = img.size
		large = max(rows, cols)
		
		# Find the ratio to resize the image by, first to _x3000, then _x2500, _x1500
		ratio = 1.0
		if large > 3000:
			ratio = large / 3000
		elif large > 2500:
			ratio = large / 2500
		elif large >= 2000:
			ratio = large / 1500
		else:
			print('small')
			return

		# Resize the output
		out_size = (int(rows / ratio), int(cols / ratio))
		out = img.resize(out_size, resample=Image.LANCZOS)

		# Convert the image to bitmap
		with BytesIO() as output:
			out.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]
			head = output.getvalue()[2:6]

		# Set the image to the clipboard
		set_clipboard(win32.CF_DIB, data)

# -------------------------------------------------

clip()