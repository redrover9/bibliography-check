from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import re
import unittest
import shutil
import requests
import textract
import os
import tkinter as tk
from tkinter import Frame
from tkinter import messagebox
from tkinter import filedialog
class App(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack()
		self.make_widgets()
		super().__init__()
	def make_widgets(self):
		self.winfo_toplevel().title("Bibliography Checker")
		tk.Label(self, text="Select a file to determine whether the bibliography is correct: ", name="essayLabel").grid(row=0, column=0)
		essayPath = filedialog.askopenfilename(initialdir = "/", title="Select an essay to check its bibliography", filetypes=[("PDF", '*.pdf')])
		essay = textract.process(essayPath)
		essayDecoded = essay.decode()
		essayDecoded = essayDecoded.replace('\u200b', '').replace('\n', '')
		re.sub('“', '', essayDecoded)
		linksUnformatted = re.findall(r'(https?://[^\s]+[\.]?)', essayDecoded) 
		links = [x[:-1] for x in linksUnformatted]
		linksLen = len(links)
		global citations
		citations = set()
		i = 0
		while i < linksLen: 
			citations.add(links[i])
			i += 1
		citations = list(citations)
		tk.Label(self, text="Enter a quote to check the bibliography for it: ", name="myLabel").grid(row=1, column=0)
		self.entry = tk.Entry(self)
		self.entry.grid(row=1, column=1)
		btn = tk.Button(self, text="Submit", command=self.on_submit)
		btn.grid(row=2, column=2, columnspan=2, sticky="ew")
	def on_submit(self):
		quote = self.entry.get()
		os.environ['MOZ_HEADLESS'] = '1'
		profile = webdriver.FirefoxProfile()
		profile.set_preference("browser.download.folderList",2)
		profile.set_preference("browser.helperApps.alwaysAsk.force", False)
		profile.set_preference("browser.download.manager.showWhenStarting",False)
		profile.set_preference("browser.download.dir", "/home/grace/Downloads")
		profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
		profile.set_preference("pdfjs.disabled", True)
		profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  
		self.driver = webdriver.Firefox(firefox_profile=profile)
		driver = self.driver
		for citation in citations:
			try: 
				if '.pdf' in citation:
					try:
						pdf = requests.get(citation, allow_redirects=True)
						open('pdf1.pdf', 'wb').write(pdf.content)
						pdfText = textract.process('pdf1.pdf')
						pdfTextDecoded = pdfText.decode()
						assert quote in pdfTextDecoded
						if quote in pdfTextDecoded:
							tk.messagebox.showinfo("Quote found", "The quote was found in a PDF file downloaded from" + citation)
					except AssertionError:
						pass
					except:
						tk.messagebox.showerror("Error", "The PDF could not be loaded.")
				else:
					driver.get(citation)
					assert quote in driver.page_source
					tk.messagebox.showinfo("Quote found", "The quote was found on the web page" + citation)
			except WDE:
				tk.messagebox.showerror("Error", "The web page at" + citation + "did not load correctly. It may require logging in.")
			except AssertionError:
				pass
	def tearDown(self):
		self.driver.close()
if __name__ == '__main__':
	App().mainloop()
