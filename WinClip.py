# -*- coding: utf-8 -*-
import win32clipboard as win32
from PIL import Image, ImageGrab
from io import BytesIO
import struct
import os
import time

MAX_MB = 7.7
MB = 1024 * 1024
file_name = "temp/out.png"

# Set the clipboard to have the data of given type
def set_clipboard(type, data):
	win32.OpenClipboard()
	win32.EmptyClipboard()
	win32.SetClipboardData(type, data)
	win32.CloseClipboard()


# Get PNG size in MB
def get_size(img):
	with BytesIO() as out:
		img = img.convert("RBGA")
		img.save(out, 'png')
		size = out.tell()

	return round(size / MB, 2)

def get_size_saved(img):
	img.save(file_name)
	if os.path.isfile(file_name):
		return round(os.stat(file_name).st_size / MB, 2)

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

		# Stop if under 8MB
		# >8MB get the ratio of input file size to max size, then half it's distance to 1. 
		# This is to try and fix bug where image would be shrunk too far. Still edge cases 
		# exist where image is too big for discord, but registers as less than 8MB in memory 5/14/2020
		if(size < MAX_MB):
			print("Under 8MB, {}MB".format(size))
		else:
			ratio = size / MAX_MB
			ratio = ((ratio - 1) / 3) + 1

			# Resize the output
			out_size = (int(rows / ratio), int(cols / ratio))
			out = img.resize(out_size, resample=Image.LANCZOS)

			# TODO: Remove this after testing
			print("In size: {}, Out size: {}".format(size, get_size(out)))

			with BytesIO() as output:
				out.convert("RGB").save(output, "BMP")
				data = output.getvalue()[14:]

			# Set the image to the clipboard
			set_clipboard(win32.CF_DIB, data)

def save_clip():
	img = ImageGrab.grabclipboard()
	if isinstance(img, Image.Image):
		size = get_size_saved(img)

		if(size < MAX_MB):
			print("Under 8MB, {}MB".format(size))
		else:
			rows, cols = img.size
			ratio = size / MAX_MB
			ratio = ((ratio - 1) / 2.5) + 1

			print(ratio)

			# Resize the output
			out_size = (int(rows / ratio), int(cols / ratio))
			# near = img.resize(out_size, resample=Image.NEAREST)
			# box = img.resize(out_size, resample=Image.BOX)
			# bilinear = img.resize(out_size, resample=Image.BILINEAR)
			# hamming = img.resize(out_size, resample=Image.HAMMING)
			# bicubic = img.resize(out_size, resample=Image.BICUBIC)
			out = img.resize(out_size, resample=Image.NEAREST)

			t0 = time.time()
			save_size = get_size_saved(out)
			t1 = time.time()
			print("Saved image time: {} \
				\nSaved image size: {}".format((t1-t0), save_size))

			with BytesIO() as output:
				png = out.convert("RGBA")
				png.save(output, "BMP")
				data = output.getvalue()[14:]

			size = get_size_saved(png)
			print("PNG: {}".format(size))

			rows, cols = png.size

			ratio = size / MAX_MB
			ratio = ((ratio - 1) / 2) + 1
			out_size = (int(rows / ratio), int(cols / ratio))

			out = png.resize(out_size, resample=Image.NEAREST)
			save_size = get_size_saved(out)

			print("Saved image size: {}".format(save_size))

			with BytesIO() as output:
				out.convert("RGBA").save(output, "BMP")
				data = output.getvalue()[14:]

			# Set the image to the clipboard
			set_clipboard(win32.CF_DIB, data)

# -------------------------------------------------

save_clip()