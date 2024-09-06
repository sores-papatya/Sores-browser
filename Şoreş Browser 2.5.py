import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *

class WebBrowser(QMainWindow):
    def __init__(self):
        super(WebBrowser, self).__init__()

        self.history_list = []  # Geçmişi kaydetmek için bir liste

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        # İlk sekmeyi aç
        self.add_new_tab(QUrl('https://www.google.com'), 'Yeni Sekme')

        self.showMaximized()

        # Navigasyon çubuğu
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Geri butonu
        back_btn = QAction(QIcon('geri.png'), 'Geri', self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_bar.addAction(back_btn)

        # İleri butonu
        forward_btn = QAction(QIcon('ileri.png'), 'İleri', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav_bar.addAction(forward_btn)

        # Yenile butonu
        reload_btn = QAction(QIcon('yenileme.png'), 'Yenile', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        nav_bar.addAction(reload_btn)

        # Ana sayfa butonu
        home_btn = QAction(QIcon('ana_sayfa.png'), 'Ana Sayfa', self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        # Geçmiş butonu
        history_btn = QAction(QIcon('geçmiş.png'), 'Geçmiş', self)
        history_btn.triggered.connect(self.show_history)
        nav_bar.addAction(history_btn)  # Ana sayfa butonunun yanına ekleniyor

        # Yeni sekme butonu
        new_tab_btn = QAction(QIcon('yeni_sekme.png'), 'Yeni Sekme', self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('https://www.google.com'), 'Yeni Sekme'))
        nav_bar.addAction(new_tab_btn)

        # URL çubuğu
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.open_new_tab_with_url)
        nav_bar.addWidget(self.url_bar)

        self.tabs.currentWidget().urlChanged.connect(self.update_urlbar)

    def add_new_tab(self, qurl=None, label="Yeni Sekme"):
        if qurl is None:
            qurl = QUrl('https://www.google.com')

        browser = QWebEngineView()

        # Kamera, mikrofon ve ses erişimi için izin isteme
        browser.page().featurePermissionRequested.connect(self.on_feature_permission_requested)

        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Yeni sekmedeki sayfayı geçmişe kaydet
        browser.urlChanged.connect(lambda qurl, browser=browser: self.add_to_history(qurl))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser))

    def on_feature_permission_requested(self, url, feature):
        # Kullanıcıdan ses, kamera veya mikrofon izni isteme
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("İzin İsteği")
        if feature == QWebEnginePage.MediaAudioCapture:
            msg_box.setText(f"{url.toString()} ses erişimi istiyor. İzin verilsin mi?")
        elif feature == QWebEnginePage.MediaVideoCapture:
            msg_box.setText(f"{url.toString()} kamera erişimi istiyor. İzin verilsin mi?")
        elif feature == QWebEnginePage.MediaAudioVideoCapture:
            msg_box.setText(f"{url.toString()} hem ses hem de kamera erişimi istiyor. İzin verilsin mi?")
        else:
            return

        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            self.tabs.currentWidget().page().setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.tabs.currentWidget().page().setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))

    def open_new_tab_with_url(self):
        url = self.url_bar.text()
        self.add_new_tab(QUrl(url), label=url)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())

    def add_to_history(self, qurl):
        if qurl.toString() not in self.history_list:
            self.history_list.append(qurl.toString())

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle('Gezinme Geçmişi')
        layout = QVBoxLayout()

        history_list_widget = QListWidget()
        for url in self.history_list:
            history_list_widget.addItem(url)
        
        history_list_widget.itemClicked.connect(lambda item: self.tabs.currentWidget().setUrl(QUrl(item.text())))

        layout.addWidget(history_list_widget)
        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, browser.title())

app = QApplication(sys.argv)
QApplication.setApplicationName("Gelişmiş Web Tarayıcı")
window = WebBrowser()
app.exec_()
