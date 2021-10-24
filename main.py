'''
Hey! This is my first project on GitHub.
I want to share this code. This is web-browser for my school.
But you can change other settings.
And I compliled this file to .exe for look how it is working.
Just look.. 
'''


'''
Import PyQt5 and other modules
'''
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtWebEngineWidgets import * 

# Import os and sys for opening and saving files.
import os
import sys

'''
Create class MainWindow for imagine the window for PyQt5.
And write here other settings.
'''
class MainWindow(QMainWindow):
	# Main function. There are main buttons for each browser.
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		'''
		Creating blanks system (Opening, Closing).
		'''
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		self.setCentralWidget(self.tabs)

		self.status = QStatusBar()
		self.setStatusBar(self.status)

		'''
		Create browser navigation
		(Open other pages, Back and forward to pages)
		with buttons.
		'''
		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(16,16))
		self.addToolBar(navtb)

		back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "reload", self)
		reload_btn.setStatusTip("Reload the page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
		home_btn.setStatusTip("Back to home page")
		home_btn.triggered.connect(lambda: self.navigate_home)
		navtb.addAction(home_btn)


		# Special 'Stop' button is stop reloading the page.
		navtb.addSeparator()
		self.httpsicon = QLabel()
		self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
		navtb.addWidget(self.httpsicon)

		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)

		stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		'''
		Create file menu 
		(Open HTM / HTML / TXT files).
		'''
		file_menu = self.menuBar().addMenu('&File')

		open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file", self)
		open_file_action.setStatusTip("Open from file")
		open_file_action.triggered.connect(self.open_file)
		file_menu.addAction(open_file_action)

		save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save file", self)
		save_file_action.setStatusTip("Save file")
		save_file_action.triggered.connect(self.save_file)
		file_menu.addAction(save_file_action)

		
		# All the same, but its help menu.
	
		help_menu = self.menuBar().addMenu('&Help')

		about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About PoPc Browser", self)
		about_action.setStatusTip("Find out more information about at localhost (Port: 9818)")
		about_action.triggered.connect(self.about)
		help_menu.addAction(about_action)

		# The same, but its blank menu.

		tab_menu = self.menuBar().addMenu('&Blanks')

		new_tab_action = QAction(QIcon(os.path.join('images', 'url-tab--plus.png')), "Open new tab", self)
		new_tab_action.setStatusTip("Create and open new tab")
		new_tab_action.triggered.connect(lambda _: self.add_new_tab())
		tab_menu.addAction(new_tab_action)

		# Homepage.

		self.add_new_tab(QUrl('http://gymnasium540.ru'), 'Homepage')

		self.show()

		self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

		# Creating new blank func with new page https: '//google.com/'.
	def add_new_tab(self, qurl=None, label="New blank"):
		if qurl is None:
			qurl = QUrl('')

		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)
		
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser:
									self.update_urlbar(qurl, browser))

		browser.loadFinished.connect(lambda _, i=i, browser=browser:
									self.tabs.setTabText(i, browser.page().title()))
		if self.tabs.count() > 1:
			browser.setUrl(QUrl("https://google.com"))
	'''
	This func can be able to open
	new blank by double click.
	'''
	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title(self.tabs.currentWidget())

	'''
	This func can close the current tab.
	'''
	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			return 

		self.tabs.removeTab(i)

	'''
	This func update the title
	of blank and the window like the title of site
	of the current blank.
	'''

	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
			return

		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle('%s - GyBrowse' % title)
	
	# Its 'about' func, you can write here, what you can write here about your browser.
	def about(self):
		pass
	# Open file
	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
		                                                "*.htm *.html"
														"All files (*.*)")
		if filename:
			with open(filename, 'r') as f:
				html = f.read()

			self.tabs.currentWidget().setHtml(html)
			self.urlbar.setText(filename)

	# Save opened file
	def save_file(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save file as", "",
		                                                "*.htm *.html"
														"All files (*.*)")
		if filename:
			html = self.tabs.currentWidget().page().toHtml()
			with open(filename, 'w') as f:
				f.write(html)

	# Go to homepage by button
	def navigate_home(self):
		self.browser.setUrl(QUrl("https://google.com"))

	# Go to writed in url bar url adress
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)

	# Update url bar like domain of the site
	def update_urlbar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return


		if q.scheme() == 'https':
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
		else:
			self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

# Configure the window
app = QApplication(sys.argv)
app.setApplicationName("GyBrowse")
app.setOrganizationName("GyBrowse")
app.setOrganizationDomain("gymnasium540.ru")

# And run the browser
window = MainWindow()
app.exec_()

'''
This is a small code of this browser, which writed on Python.
For what?
For PC or laptops with low perfomance.
Example: You're need to surf the internet, but your computer is 'very low'.
This browser can help you.
And you can use it how you'll want.
'''

'''
We love coding!))
		- Someone
'''