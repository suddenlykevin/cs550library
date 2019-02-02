"""
KIVY DEMO: PIL VISUALIZER
Kevin Xie CS550 Healey

This PIL visualizer is built with Kivy's flexible UI widgets. It is not
necessary to understand all of the python, but here is the gist: 
MainUI is the home to all the behaviors (functions) that the widgets
in the UI can trigger. This includes image filters, operations, etc.
FilterApp creates an app window for MainUI to function and stores
MainUI in its default state. Please open the .kv file for a more
indepth explanation on UI structure.

Sources:
Reference - https://kivy.org/doc/stable/
Browsing and Displaying images - https://stackoverflow.com/questions/43452697/browse-an-image-file-and-display-it-in-a-kivy-window
Reloading images - https://stackoverflow.com/questions/42328063/how-can-i-reload-a-image-in-kivy-python

On my honor, I have neither given nor received unauthorized aid.
Kevin Xie '19

"""
# CORE FRAMEWORK AND BEHAVIOR
import kivy 
from kivy.app import App # for creating and opening "App" window cluster of widgets
from kivy.core.window import Window # for altering window color
# enter your Kivy version to ensure compatibility
kivy.require('1.10.1') 
# WIDGET MODULES (mostly self explanatory)
from kivy.uix.button import Button
from kivy.uix.image import Image as Ima # not to be confused with PIL Image
from kivy.uix.boxlayout import BoxLayout # Layout type
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooser
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.accordion import Accordion # Separates two different spaces on a UI
from kivy.uix.spinner import Spinner # Drop-down menu

from PIL import Image, ImageDraw, ImageStat, ImageFilter, ImageOps, ImageEnhance # For python functionality

# BEHAVIOR (python code) -- if you are only interested in learning Kivy, it is not necessary to understand all of this.
class MainUI(BoxLayout):
	# Checks if any modificatoins are already selected -- i.e. self.ids.solarize.active is whether or not solarization is selected.
	# Generally, use self.ids.[widget id].[property] to evaluate widget properties
	def checkIn(self): 
		if self.ids.solarize.active == True:
			self.solarize(True)
		if self.ids.bw.active == True:
			self.bwConvert(True)
		if self.ids.halftone.active == True:
			self.halftone(True)
	# Default condition so that there is always an image to manipulate
	def default(self):
		self.ids.image.source = "colors.png"
		self.im = Image.open("colors.png").convert("RGB") # Always convert to RGB for compatibility with other modifications
		self.image = Ima(source="colors.png")
		self.route = "colors.png"
	# The behavior if the "Open" button is pressed - loads a new image as the source for result tab and applies existing manipulations.
	def load(self, path, filename):
		self.ids.image.source = filename[0]
		self.im = Image.open(filename[0]).convert("RGB")
		self.image = Ima(source=filename[0])
		self.route = filename[0] # self.route is used when user wants to return to original image.
		self.image.reload()
		self.checkIn()
	# Checks if user wants to see original or result by evaluating the state of the Toggle Buttons
	def show(self):
		if self.ids.result.state == 'down':
			self.ids.image.source = self.route
			self.image = Ima(source="result.jpg")
			# it is necessary to reload an image after its modification because Kivy keeps a local cache of the image
			self.image.reload()
			self.ids.image.source = "result.jpg"
		else:
			self.ids.image.source = self.route
	# all-purpose saving function for saving the results of each modification
	def saver(self, result):
		result.convert("RGB").save("result.jpg")
		self.im = Image.open("result.jpg")
		self.ids.image.source = self.route
		self.image = Ima(source="result.jpg")
		self.image.reload()
		self.ids.image.source = "result.jpg"
		self.show()
	# Halftoning function -- no need to understand or read unless interested. 
	def halftone(self, value):
		if value:
			sample = 30 
			channel = self.im.split()[2]
			# New, single 8-bit channel image for halftoning
			halftoned = Image.new('L', (channel.width,channel.height)) 
			# sets the draw command
			draw = ImageDraw.Draw(halftoned) 
			# goes from 0 to width of image with step size of 30 (sample size -- basically in a grid of width/30)
			for x in range(0, channel.width, sample): 
			    for y in range(0, channel.height, sample): 
			    	# makes a new box that takes a sample sized (30x30) square of the original image's B channel
			        box = channel.crop((x, y, x + sample, y + sample)) 
			        # sets the stat command
			        stat = ImageStat.Stat(box) 
			        # Scales diameter of the halftoning circle (0-sample=30) based on the 0-255 value of the L (only) channel which indicates pixel brightness out of 255 to make it a value from 0-1
			        diameter = stat.mean[0]*sample / 255 
			        # draws a new halftoned circle with size based on the diameter of the halftoning circle
			        draw.ellipse((x, y, x + diameter, y + diameter), fill=255) 
			# saves new halftoned image using saver function
			self.saver(halftoned)
		# IF Halftoning is DESELECTED: return to original state
		else: 
			self.ids.image.source = self.route
			self.im = Image.open(self.route)
			self.image = Ima(source=self.route)
			self.checkIn()
	# Solarizing function -- uses PIL's native solarizing capabilities.
	def solarize(self,value):
		if value:
			self.saver(ImageOps.solarize(self.im, 95))
		else:
			self.ids.image.source = self.route
			self.im = Image.open(self.route)
			self.image = Ima(source=self.route)
			self.checkIn()
	# Black and white conversion using PIL
	def bwConvert(self,value):
		if value:
			self.saver(self.im.convert("LA"))
		else:
			self.ids.image.source = self.route
			self.im = Image.open(self.route)
			self.image = Ima(source=self.route)
			self.checkIn()
	# re-assigns RGB values for funky effect based on spinner
	def rgbroll(self,text):
		if text == "RGB":
			result = Image.open(self.route)
		elif text == "BGR":
			b,g,r = self.im.split()
			result = Image.merge("RGB", (r,g,b))
		elif text == "GBR":
			g, b, r = self.im.split()
			result = Image.merge("RGB", (r,g,b))
		else:
			result = Image.open(self.route)
		self.saver(result)
	# rotates image based on button
	def rotate(self):
		self.saver(self.im.rotate(90))

	# changes the "fidelity/brightness" of R,G,B channels based on sliders.
	def rmod(self,value):
		r,g,b=self.im.split()
		r = ImageEnhance.Brightness(r).enhance(value/255)
		self.saver(Image.merge("RGB",(r,g,b)))
	def gmod(self,value):
		r,g,b=self.im.split()
		g = ImageEnhance.Brightness(g).enhance(value/255)
		self.saver(Image.merge("RGB",(r,g,b)))
	def bmod(self,value):
		print(value)
		r,g,b=self.im.split()
		b = ImageEnhance.Brightness(b).enhance(value/255)
		self.saver(Image.merge("RGB",(r,g,b)))

	# Uses PIL's native mirroring function
	def mirror(self,value):
		if value:
			self.saver(ImageOps.mirror(self.im))
		else:
			image = Image.open(self.route)
			self.saver(image)

# Creates app window and calls on MainUI class.
class FilterApp(App):
	def build(self):
		self.load_kv('my.kv') # links kv file
		Window.clearcolor = (0.1,0.1,0.2,1) # changes window color
		UI = MainUI() 
		UI.default() # stores UI in default state
		return UI

# runs FilterApp and opens app.
if __name__ == '__main__':
	FilterApp().run()