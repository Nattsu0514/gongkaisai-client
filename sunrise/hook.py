from sunrise.mainwindow import MainWindow


def main_window_instantiate(func):
    MainWindow.start_set.add(func)


def main_window_close(func):
    MainWindow.shutdown_set.add(func)


