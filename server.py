import functools
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from PyQt5.QtCore import QThread
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyServer, ProxyConfig
from mitmproxy.tools.dump import DumpMaster

import browser_proxy_setting


class Http(QThread):
    def __init__(self, host: str, port: int, path: str = 'file'):
        super().__init__()
        self.host: str = host
        self.port: int = port
        self.handler = functools.partial(SimpleHTTPRequestHandler, directory=os.path.relpath(path, os.getcwd()))

        self.httpd = HTTPServer((self.host, self.port), self.handler)

    def run(self) -> None:
        self.httpd.serve_forever()


class Proxy:
    addons: set = set()

    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port

        options: Options = Options(listen_host=self.host, listen_port=self.port, ignore_hosts=[".*443$"])
        config: ProxyConfig = ProxyConfig(options)
        self.master: DumpMaster = DumpMaster(options, with_termlog=False, with_dumper=False)

        self.master.server = ProxyServer(config)
        self.master.addons.add(*self.addons)

    @classmethod
    def add_addon(cls, rule):
        cls.addons.add(rule)

    def run(self) -> None:
        browser_proxy_setting.set_proxy_settings(self.host, self.port)
        self.master.run()

    def terminate(self) -> None:
        self.master.shutdown()
        browser_proxy_setting.set_proxy_settings(self.host, self.port, on=False)
