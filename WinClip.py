`# -*- coding: utf-8 -*-
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
		elif large >= 2500:
			ratio = large / 2500
		elif large >= 2000:
			ratio = large / 1500
		else:
			return

		img.save("out.bmp")

		# Resize the output
		out_size = (int(rows / ratio), int(cols / ratio))
		out = img.resize(out_size, resample=Image.LANCZOS)

		# Convert the image to bitmap
		output = BytesIO()
		out.convert("RGB").save(output, "BMP")
		out.save("outp.png")
		data = output.getvalue()[14:]
		head = output.getvalue()[2:6]
		output.close()
		
		# Get size of bmp
		intb = int.from_bytes(head, byteorder="little")
		megaB = 1024 * 1024
		print(str(intb/ megaB))

		# Set the image to the clipboard
		set_clipboard(win32.CF_DIB, data)

# -------------------------------------------------

clip()