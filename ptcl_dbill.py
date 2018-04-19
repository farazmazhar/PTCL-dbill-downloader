from bs4 import BeautifulSoup
""" This library is responsible for parsing and figuring out the PTCL dbill pdf file link."""
import mechanicalsoup
"""This library is responsible for filling form at  https://dbill.ptcl.net.pk/PTCLSearchInvoice.aspx."""
import urllib
"""This library is responsible for downloading retreving the PTCL dbill pdf file."""

class PTCL_dbill:
    """This class is going make the magic happen."""

    def __init__(self):
        """Initializes required variables."""
        self.set_sub_info()
    
    def set_sub_info(self):
        """Reads `sub_info.txt` for PTCL subscriber information."""
        with open('sub_info.txt', 'r') as file:
            sub_info = file.readlines()[0:2] # This list will be carrying PTCL subscriber information.
            try:
                self._phone = int(sub_info[0].split(':')[1].strip())
                self._account = int(sub_info[1].split(':')[1].strip())
            except(TypeError):
                print("Invalid phone number/account id.")
                exit()
    
    def get_sub_info():
        """If `sub_info.txt` doesn't exist, this function will be called
         and user will be prompted to enter details"""
        pass

    def fill_dbill_form(self):
        """Filling form at search invoice link."""
        self._browser = mechanicalsoup.StatefulBrowser()
        self._browser.open("https://dbill.ptcl.net.pk/PTCLSearchInvoice.aspx")

        self._browser.select_form("#aspnetForm")
        self._browser["ctl00$ContentPlaceHolder1$txtPhoneNo"] = self._phone
        self._browser["ctl00$ContentPlaceHolder1$txtAccountID"] = self._account
        self._browser.submit_selected()

        self._billing_month = self._browser.get_current_page().findAll('span', {"id":"ctl00_ContentPlaceHolder1_lblBillingMonth"})[0].text
        self._dbill_html = self._browser.open_relative(self._browser.get_current_page().findAll('a', {"id":"ctl00_ContentPlaceHolder1_hplPrintBill"})[0]['href'])

    def save_dbill(self, path="./"):
        """Stores content of response i.e. PTCL dbill as a pdf file."""
        with open(path + "dbill-" + str(self._phone) + "-" + self._billing_month + ".pdf", 'wb') as f:
            f.write(self._dbill_html.content)