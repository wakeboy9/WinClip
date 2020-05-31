# -*- coding: utf-8 -*-
import win32clipboard as win32
from PIL import Image, ImageGrab
from io import BytesIO
import struct
import os
import time

BMP_DATATYPE = win32.CF_DIB
MAX_MB = 7.9
MB = 1024 * 1024
file_name = "temp/temp.png"

# Set the clipboard to have the data of given type
def set_clipboard(type, data):
	win32.OpenClipboard()
	win32.EmptyClipboard()
	win32.SetClipboardData(type, data)
	win32.CloseClipboard()

def send_image_to_clipboard(img):
	with BytesIO() as output:
		img.convert("RGBA").save(output, "BMP")
		data = output.getvalue()[14:]

	win32.OpenClipboard()
	win32.EmptyClipboard()
	win32.SetClipboardData(BMP_DATATYPE, data)
	win32.CloseClipboard()

# Get PNG size in MB
def get_rgba_size(img):
	with BytesIO() as output:
		rgba = img.convert("RGBA")
		rgba.save(output, "BMP")
		data = output.getvalue()[14:]

	return get_size_saved(rgba)

def get_size_saved(img):
	img.save(file_name)
	if os.path.isfile(file_name):
		return round(os.stat(file_name).st_size / MB, 2)

def brute_clip():
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

def save_clip():
	img = ImageGrab.grabclipboard()
	if isinstance(img, Image.Image):
		# Resize the image to convert it into bytes so we can convert it to RGBA
		rgba = img.resize(img.size, resample=Image.NEAREST)
		size = get_rgba_size(rgba)

		if(size < MAX_MB):
			print("Under 8MB, {}MB".format(size))
		else:
			print("Original size: {}MB".format(size))

			rows, cols = img.size
			ratio = size / MAX_MB
			ratio = ((ratio - 1) / 2) + 1

			# Resize the output
			out_size = (int(rows / ratio), int(cols / ratio))
			out = img.resize(out_size, resample=Image.NEAREST)

			save_size = get_rgba_size(out)
			print("Saved image size: {}MB".format(save_size))

			send_image_to_clipboard(out)

# -------------------------------------------------

save_clip()