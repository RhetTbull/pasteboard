"""Example usage for pasteboard.py"""

from pasteboard import Pasteboard

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
# clipboard will be set as PNG but it's likely any image format supported by macOS will work
pb.copy_image("test.png")

# also
pb.set_image("test.png")

# get the clipboard contents as an image as a PNG file
# overwrite optional and is False by default
# if overwrite is False and the file exists, a FileExistsError will be raised
image = pb.paste_image("contents.png", overwrite=True)

# also
image = pb.get_image("contents.png", overwrite=True)

# determine if the clipboard contains an image
if pb.has_image():
    print("Clipboard contains an image")

# monitor the clipboard for changes
# Note: changes made by the Pasteboard instance itself are ignored
# this is useful for monitoring changes made by other applications
if pb.has_changed():
    print("Clipboard has changed")
