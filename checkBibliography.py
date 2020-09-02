import re
import unittest
import textract
import os
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE

essayPath = input("Enter the file path of the essay: ")
essay = textract.process(essayPath)
essayDecoded = essay.decode()
essayDecoded = essayDecoded.replace('\u200b', '').replace('\n', '')
re.sub('“', '', essayDecoded)
# httpOccurrences = [m.start() for m in re.finditer('http', essayDecoded)]
# httpOccurrencesLen = len(httpOccurrences)


linksUnformatted = re.findall(r'(https?://[^\s]+[\.]?)', essayDecoded) 
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
                if '.pdf' in citation:
                    try:
                        pdf = requests.get(citation, allow_redirects=True)
                        open('pdf1.pdf', 'wb').write(pdf.content)
                        pdfText = textract.process('pdf1.pdf')
                        pdfTextDecoded = pdfText.decode()
                        assert quote in pdfTextDecoded
                        if quote in pdfTextDecoded:
                            print("\n")
                            print("\n")
                            print("The quote was found in a PDF file downloaded from", citation)
                            print("\n")
                            print("\n")
                    except AssertionError:
                        pass
                    except:
                        print("The PDF could not be loaded.")
                else:
                    driver.get(citation)
                    assert quote in driver.page_source
                print("The quote was found on the web page", citation)
            except WDE:
                print("The web page at", citation, "did not load correctly. It may require logging in.")
            except AssertionError:
                pass
                # print("The citation was not found on page", citation)
    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    unittest.main()
