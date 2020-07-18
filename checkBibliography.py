import re
import unittest
import textract
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

essay = textract.process("/home/grace/Downloads/essay.pdf")
essayDecoded = essay.decode()
essayDecoded = essayDecoded.replace('\u200b', '').replace('\n', '')
re.sub('“', '', essayDecoded)
httpOccurrences = [m.start() for m in re.finditer('http', essayDecoded)]
httpOccurrencesLen = len(httpOccurrences)

linksUnformatted = re.findall(r'(https?://[^\s]+[\.]?)', essayDecoded) #If the student has a period at the end of their links, remove the question mark.
links = [x[:-1] for x in linksUnformatted]
linksLen = len(links)
refRegex = r'"(.*?)"'
refs = re.findall(refRegex, essayDecoded)
print(essayDecoded)

citations = {}
i = 0
while i < linksLen: 
    citations["link{0}".format(i)] = links[i]
    i += 1

"""
quote = "Healthcare"

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        for key in citations.keys():
            driver.get(citations[key])
            assert quote in driver.page_source
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

"""