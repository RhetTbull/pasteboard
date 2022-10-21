"""Example usage for pasteboard.py"""

from pasteboard import Pasteboard, PNG, TIFF

pb = Pasteboard()

# set the current clipboard contents as text
pb.copy("Hello World")

# also
pb.set_text("Hello World")

# get the current clipboard contents as text
text = pb.paste()

# also
text = pb.get_text()

# append text to the current clipboard contents
pb.copy("Hello")
pb.append(" World")

# determine if the clipboard contains text
if pb.has_text():
    print("Clipboard contains text")

# set the clipboard contents as an image
pb.copy_image("test.png", PNG)

# also
pb.set_image("test.png", PNG)

# get the clipboard contents as an image as a PNG file
# overwrite optional and is False by default
# if overwrite is False and the file exists, a FileExistsError will be raised
image = pb.paste_image("contents.png", PNG, overwrite=True)

# also
image = pb.get_image("contents.png", PNG, overwrite=True)

# clipboard can be set to PNG or TIFF
pb.copy_image("test.tiff", TIFF)

# determine if the clipboard contains an image
if pb.has_image():
    print("Clipboard contains an image")
if pb.has_image(PNG):
    print("Clipboard contains a PNG image")
if pb.has_image(TIFF):
    print("Clipboard contains a TIFF image")

# monitor the clipboard for changes
# Note: changes made by the Pasteboard instance itself are ignored
# this is useful for monitoring changes made by other applications
if pb.has_changed():
    print("Clipboard has changed")
