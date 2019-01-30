"""
Kivy Example 1: Hello World!
Kevin Xie CS550 

This example files gives a short introduction to programming
Kivy widgets in Python. It uses a number of widgets from popups
to sldiers to buttons to Codeinputs. However, it may seem messy!
This is because Kivy works best when typed in kv, where widget
trees and behavior are easier to follow and edit. Here's a short
flow chart:

Execute Code > Opens MyFirstButton > builds button and slider widgets in
a horizontal Boxlayout (stack) 
1. If button > bind behavior (popup) > on_press > opens popup > builds
label (text), exit button, and codeinput in GridLayout and BoxLayout
	a. If exit button > dismiss popup > return to MyFirstButton
2. If slider > bind behavior (recolor) > when value changes > recolors 
window background color

More comments can be found in the code.

Sources (applies to all example files):
Reference - https://kivy.org/doc/stable/

On my honor, I have neither given nor received unauthorized aid.
Kevin Xie '19

"""
# core framework and behavior
import kivy 
from kivy.app import App # for creating and opening "App" window cluster of widgets
from kivy.core.window import Window # for altering window color
# enter your Kivy version to ensure compatibility
kivy.require('1.10.1') 
# import ux elements (widgets -- most titles are self explanatory)
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput # a text box formatted for code
from kivy.uix.popup import Popup
from pygments.lexers import CythonLexer # used to format the syntax of python text
from kivy.uix.boxlayout import BoxLayout # formats the available space as "boxes" stacking either horizontally or vertically
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout # formats available space as a "grid" with rows and columns of widgets
from kivy.uix.slider import Slider

# content of the popup
content = BoxLayout(orientation="vertical") # in vertical stack
topbar = GridLayout(cols=2,size_hint=(1,0.2)) # create a grid layout (with 2 columns) topbar/menu bar for dismissing popup etc.
btn2 = Button(text='Close Me!',size_hint_x=0.2) # dismiss button with custom text and spacing (size_hint is the fraction of the x axis the widget occupies)
topbar.add_widget(Label(text="How does a button and slider work?")) # adds label (text) for title
topbar.add_widget(btn2) # adds dismiss button (order matters in boxlayout and gridlayout -- typically left to right, top down) 
content.add_widget(topbar) # adds topbar to popup
# code input widget to explain the code of slider and button
content.add_widget(CodeInput(lexer=CythonLexer(),text="""# Button and Slider
# 
# This simple button and slider was built entirely in Python using no Kv. 
# It uses a box layout to arrange the two separate widgets and just two of Kivy's 
# many offered widgets. 
# Take a look at the code. Does it seem tedious or hard to follow?


# opens the core functionality of the Kivy framework
import kivy 
# set this to the version of Kivy you are running to ensure compatibility
kivy.require('1.10.1') 
# imports the ability to create "Apps" or groups of widgets to be executed
from kivy.app import App
# imports the abilities to create Buttons, Sliders, manipulate the window properties (color), and arrange widgets
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# executes this popup
# instance is input name (self.btn)
def popup(instance):
	print("Popup opened!") # check the console!
	code.open() # opens this popup

# recolors the background every time the slider is moved
# instance2 is the value of the slider
def recolor(instance,instance2):
	val = float(instance2)/100.0 # retrieves a fraction out of 1 (rgba values from 0-1)
	Window.clearcolor = (val,val,val,1) # sets window color

# the "App" or group of widgets that can all be run in one window
class MyFirstButton(App):
	# the widgets to build into the app
	def build(self):
		self.content=BoxLayout(orientation="horizontal") # sets the layout of the window -- in this case, box layout indicates that widgets are "stacked" based on the orientation
		self.slider = Slider(orientation='vertical', min=0, max=100, value = 0) # vertical slider from 0-100 with default 0
		self.slider.bind(value=recolor) # binds the "recolor" function to every time the value of the slider changes
		self.btn = Button(text='Hello World! (this is a button)', font_size = 25) # new button with text property "Hello World!" and font size 25
		self.btn.bind(on_press=popup) # sets button behavior (calls function "popup")
		self.content.add_widget(self.btn) # adds button to box layout (horizontal "stack")
		self.content.add_widget(self.slider) # adds slider to box layout
		return self.content # returns the arranged content of the app

# if still in original file
if __name__ == '__main__':
    MyFirstButton().run() # runs the "app" in a new window

# Open the hellowworld.py file in Sublime to learn more about how this Popup was 
# created!""",size_hint=(1,0.8))) # size_hint dictates the fraction of the screen across (1) and from top to bottom (0.8) the code should occupy
code = Popup(content=content, title="Popup!", auto_dismiss = False) # creates a popup with the aforemmentioned content
btn2.bind(on_press=code.dismiss) # binds behavior that dismisses code on_press of dismiss button

# function to open popup, first argument is always input name (btn in this case)
def popup(instance):
	print("Popup opened!") # check your console!
	code.open() # opens popup

# function to recolor the background, argument 2 is value of slider
def recolor(instance,instance2):
	val = float(instance2)/100.0 # makes slider value a float between 0 and 1
	Window.clearcolor = (val,val,val,1) # sets color in rgba from 0-1

# main cluster in the form of an "App" window that opens on run()
class MyFirstButton(App):
	# sets widgets to build
	def build(self):
		self.content=BoxLayout(orientation="horizontal", padding=20) # widgets arranged horizontally, padded with 20% for each widget for visual reasons
		self.slider = Slider(orientation='vertical', min=0, max=100, value = 0) # vertical slider from 0-100 with default 0
		self.btn = Button(text='Hello World! (click me!)',font_size = 25) # button with text and font size 25
		self.btn.bind(on_release=popup) # binds popup summoning behavior to button
		# adds widgets to the arrangement of self.content
		self.content.add_widget(self.btn)
		self.content.add_widget(self.slider)
		self.slider.bind(value=recolor) # binds recoloring behavior to slider
		return self.content # returns the arranged content to the App

if __name__ == '__main__':
    MyFirstButton().run() # runs widget in an "app" window!
