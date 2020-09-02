import re
import unittest
import textract
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE

essay = textract.process("/home/grace/Downloads/essay.pdf")
essayDecoded = essay.decode()
essayDecoded = essayDecoded.replace('\u200b', '').replace('\n', '')
re.sub('“', '', essayDecoded)
httpOccurrences = [m.start() for m in re.finditer('http', essayDecoded)]
httpOccurrencesLen = len(httpOccurrences)

linksUnformatted = re.findall(r'(https?://[^\s]+[\.]?)', essayDecoded) #If the student has a period at the end of their links, remove the question mark.
links = [x[:-1] for x in linksUnformatted]
linksLen = len(links)

citations = set()
i = 0
while i < linksLen: 
    citations.add(links[i])
    i += 1

citations = list(citations)
quote = input("Enter a quote to search the student's citations for: ")

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList",2)
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", "/home/grace/Downloads")
        profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  
        self.driver = webdriver.Firefox(firefox_profile=profile)
    def test_search_in_python_org(self):
        driver = self.driver
        for citation in citations:
            try: 
                driver.get(citation)
                if 'pdf' in citation:
                    pdfText = textract.process('0029682-003-XIE.pdfpage27.pdf')
                    pdfTextDecoded = pdfText.decode()
                    if quote in pdfTextDecoded:
                        print("The quote was found in a PDF file downloaded from", citation)
                else:
                    assert quote in driver.page_source
                print("The quote was found on the web page", citation)
            except WDE:
                print("The web page at", citation, "did not load correctly. It may require logging in.")
            except AssertionError:
                print("The citation was not found on page", citation)
    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    unittest.main()
