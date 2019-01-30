"""
Kivy Example 1 (KV Edition): Hello World!
Kevin Xie CS550 

This example files gives a short introduction to programming
Kivy widgets in Python. It uses a number of widgets from popups
to sldiers to buttons to Codeinputs. This time, it is written in
Python as well as Kv. This means that the majority of the 
widgets are written in Kv (check helloworld.kv). Unfortunately,
popups were not functioning in kv, so they were done in py.

Here is another flow chart:

Execute Code > Opens MyFirstButton > builds button and slider widgets in
a horizontal Boxlayout (stack) based on helloworld.kv
1. If button > bind behavior (popup) > on_press > opens popup > builds
label (text), exit button, and codeinput in GridLayout and BoxLayout
	a. If exit button > dismiss popup > return to MyFirstButton
2. If slider > when value changes > recolors window background color

More comments can be found in the code.

Sources (applies to all example files):
Reference - https://kivy.org/doc/stable/

On my honor, I have neither given nor received unauthorized aid.
Kevin Xie '19
"""

import kivy
kivy.require('1.10.1')

import kivy 
from kivy.app import App # for creating and opening "App" window cluster of widgets
from kivy.core.window import Window # for altering window color
from kivy.lang import Builder
# enter your Kivy version to ensure compatibility
kivy.require('1.10.1') 
# import ux elements (widgets -- most titles are self explanatory)
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput # a text box formatted for code
from kivy.uix.popup import Popup
from kivy.extras.highlight import KivyLexer # used to format the syntax of kv text
from kivy.uix.boxlayout import BoxLayout # formats the available space as "boxes" stacking either horizontally or vertically
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout # formats available space as a "grid" with rows and columns of widgets
from kivy.uix.slider import Slider

# Content of popup -- for one reason or another popups were broken in kv as I was programming this.
content = BoxLayout(orientation="vertical") # in vertical stack
topbar = GridLayout(cols=2,size_hint=(1,0.2)) # create a grid layout (with 2 columns) topbar/menu bar for dismissing popup etc.
btn2 = Button(text='Close Me!',size_hint_x=0.2) # dismiss button with custom text and spacing (size_hint is the fraction of the x axis the widget occupies)
topbar.add_widget(Label(text="How does a button and slider work?")) # adds label (text) for title
topbar.add_widget(btn2) # adds dismiss button (order matters in boxlayout and gridlayout -- typically left to right, top down) 
content.add_widget(topbar) # adds topbar to popup
# code input widget to explain the code of slider and button
content.add_widget(CodeInput(lexer=KivyLexer(),text="""# kivy 1.10.1
# Using kv language, it's easy to read what's going on
# in the code. The layout is clear and legible.
# The behavior (root.command()) associated with
# actions calls on functions in the Python code.

# Full arrangement
<Layout>
	orientation: 'horizontal' # is horizontally stacked
	padding: 20 # padded 20% per widget for aesthetic reasons

	# the "Hello World" button and its properties and behavior
	Button:
		id: hw
		text: 'Hello World! (click me!)'
		font_size: 25
		on_release: root.popup() #opens popup on release

	# the slider and its properties and behavior
	Slider:
		id: bgcolor
		orientation: 'vertical'
		min: 0
		max: 100
		value: 0
		on_value: root.recolor(bgcolor.value) # when value changes, background is 
		# recolored""",size_hint=(1,0.8))) # size_hint dictates the fraction of the screen across (1) and from top to bottom (0.8) the code should occupy
code = Popup(content=content, title="Popup!", auto_dismiss = False) # creates a popup with the aforemmentioned content
btn2.bind(on_press=code.dismiss) # binds behavior that dismisses code on_press of dismiss button

# opens the <Layout> class in the root kv file
class Layout(BoxLayout):
	# functions that dictate the behavior of the GUI
	def popup(self):
		print("Popup opened!") # check your console!
		code.open() # opens popup
	def recolor(self, val):
		val = float(val)/100.0
		Window.clearcolor = (val,val,val,1) # changes background color

# opens app window
class MyFirstButton(App):
	def build(self):
		self.load_kv('helloworld.kv') # links to kv file
		return Layout()

if __name__ == '__main__':
	MyFirstButton().run()