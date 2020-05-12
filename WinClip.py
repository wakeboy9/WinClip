# -*- coding: utf-8 -*-
import win32clipboard as win32
from PIL import Image, ImageGrab
from io import BytesIO
import struct

MAX_MB = 8
MB = 1024 * 1024

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

		return round(size / MB, 2)

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

		# Make BytesIO bitmap
		with BytesIO() as output:
			out.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]

		# Set the image to the clipboard
		set_clipboard(win32.CF_DIB, data)


# Working on new method to get as close to 8MB rather than cutting to a specific number
# As of 5/11/2020 it is working but shrinking too much. Ie ~15MB input -> ~3MB output
def new_clip():
	img = ImageGrab.grabclipboard()
	if isinstance(img, Image.Image):
		rows, cols = img.size
		size = get_size(img)
		ratio = 1

		if(size < MAX_MB):
			out = img
		else:
			ratio = size / MAX_MB

			# Resize the output
			out_size = (int(rows / ratio), int(cols / ratio))
			out = img.resize(out_size, resample=Image.LANCZOS)

		print("In size: {}, Out size: {}".format(size, get_size(out)))

		with BytesIO() as output:
			out.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]

		# Set the image to the clipboard
		set_clipboard(win32.CF_DIB, data)

# -------------------------------------------------

new_clip()