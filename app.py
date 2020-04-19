
def get_app():

    from PyQt5.QtCore import QCoreApplication
    from PyQt5.QtWidgets import QApplication

    app = QCoreApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def show_splash_screen():

    from PyQt5.QtWidgets import QSplashScreen
    from PyQt5.QtGui import QPixmap, QColor
    from PyQt5.QtCore import Qt

    # create and display the splash screen
    splash_pix = QPixmap('assets/splash.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    splash.showMessage('Loading...',
                       alignment=Qt.AlignCenter | Qt.AlignBottom,
                       color=QColor(Qt.white))

    splash.show()

    return splash


if __name__ == '__main__':

    app = get_app()
    splash = show_splash_screen()

    from gui_template.gui import GUI
    GUI(app, splash)
