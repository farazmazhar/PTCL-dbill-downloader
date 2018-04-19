import mechanicalsoup
"""This library is responsible for filling form at
      https://dbill.ptcl.net.pk/PTCLSearchInvoice.aspx."""

class PTCL_dbill:
    """This class is going make the magic happen."""

    def __init__(self):
        """Initializes required variables and stuff."""
        self._billing_month = None
        self.set_sub_info()

    def set_sub_info(self):
        """Reads `sub_info.txt` for PTCL subscriber information."""
        with open('sub_info.txt', 'r') as file:
            # Following list will be carrying PTCL subscriber information.
            sub_info = file.readlines()[0:2]
            try:
                self._phone = int(sub_info[0].split(':')[1].strip())
                self._account = int(sub_info[1].split(':')[1].strip())
            except TypeError:
                print("Invalid phone number/account id.")
                exit()

    def fill_dbill_form(self):
        """Filling form at search invoice link."""
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://dbill.ptcl.net.pk/PTCLSearchInvoice.aspx")

        browser.select_form("#aspnetForm")
        browser["ctl00$ContentPlaceHolder1$txtPhoneNo"] = self._phone
        browser["ctl00$ContentPlaceHolder1$txtAccountID"] = self._account
        browser.submit_selected()

        self._billing_month = browser.get_current_page().findAll('span', {"id":"ctl00_ContentPlaceHolder1_lblBillingMonth"})[0].text
        return browser.open_relative(browser.get_current_page().findAll('a', {"id":"ctl00_ContentPlaceHolder1_hplPrintBill"})[0]['href'])

    def save_dbill(self, path="./"):
        """Stores content of response i.e. PTCL dbill as a pdf file."""
        dbill_response = self.fill_dbill_form()
        with open(path + "dbill-" + str(self._phone) + "-" + self._billing_month + ".pdf", 'wb') as file:
            file.write(dbill_response.content)