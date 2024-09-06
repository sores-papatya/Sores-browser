import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class WebBrowser(QMainWindow):
    def __init__(self):
        super(WebBrowser, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  # Başlangıç sayfası
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navigasyon çubuğu
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        back_btn = QAction('geri.png', self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction('İleri', self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction('Yenile', self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        home_btn = QAction('Ana Sayfa', self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName("Şoreş browser")
window = WebBrowser()
app.exec_()


import tkinter as tk
from tkinter import ttk
import webview

class Browser:
    def __init__(self, root):
        self.root = root
        self.root.title("Basit Web Tarayıcısı")

        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill='both')

        # İlk sekmeyi oluştur
        self.create_new_tab()

        # Sekme ekleme butonu
        self.add_tab_button = ttk.Button(self.root, text="+", command=self.create_new_tab)
        self.add_tab_button.pack(side='right')

    def create_new_tab(self):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text="Yeni Sekme")

        # Webview oluşturma
        webview_frame = tk.Frame(tab)
        webview_frame.pack(expand=1, fill='both')

        # Webview içeriğini yükleme
        self.webview = webview.create_window("Web", width=800, height=600, parent=webview_frame)
        webview.load_url("https://www.example.com")  # Varsayılan URL

        # Sekme açıldığında bir URL yükleyin
        self.webview.evaluate("window.location.href = 'https://www.example.com'")

        # Webview penceresini göster
        webview.start()

# Uygulama başlatma
if __name__ == "__main__":
    root = tk.Tk()
    browser = Browser(root)
    root.mainloop()
