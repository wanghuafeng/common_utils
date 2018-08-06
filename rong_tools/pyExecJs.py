from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage
import sys
import re
class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = r'E:\php_workspace\mail_qq_login\1430895072.html'
# url = r'E:\php_workspace\mail_qq_login\qq_login.php'
r = Render(url)
html = r.frame.toHtml().replace('&amp;', '&')
print html.toUtf8()
submitUrl = re.search(r'\<body\>(.*?)\<\/body\>', html, re.S).group(1)
print str(submitUrl).strip()
