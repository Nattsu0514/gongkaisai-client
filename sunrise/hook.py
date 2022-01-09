from sunrise.filter import proxy_startup_set, proxy_shutdown_set
from sunrise.mainwindow import MainWindow


def main_window_instantiate(func):
    MainWindow.start_set.add(func)


def main_window_shutdown(func):
    MainWindow.shutdown_set.add(func)


def proxy_startup(func):
    proxy_startup_set.add(func)


def proxy_shutdown(func):
    proxy_shutdown_set.add(func)
