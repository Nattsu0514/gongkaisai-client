import os
import re
from abc import ABC
from typing import Union, Pattern, AnyStr, Type, Any

import mitmproxy.http
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig, ProxyServer
from mitmproxy.tools.dump import DumpMaster

from sunrise.filter import MetaFilter, MetaRuleManager
from sunrise.filter import proxy_startup_set, proxy_shutdown_set
from sunrise.util import Singleton, get_file_as_byte


def _instance_method(self, flow: mitmproxy.http.HTTPFlow):
    if re.search(self.pattern, flow.request.url, re.I):

        if isinstance(self.respond, str):
            flow.response.content = get_file_as_byte(self.respond)
        elif isinstance(self.respond, int):
            flow.response = mitmproxy.http.HTTPResponse.make(self.respond)
        else:
            raise


@Singleton
class Filter(MetaFilter, ABC):
    def __init__(self):
        options: Options = Options(listen_host="127.0.0.1", listen_port=8099, allow_hosts=[".*61.com:443"])
        config: ProxyConfig = ProxyConfig(options)
        self.master = DumpMaster(options, with_termlog=True, with_dumper=True)
        self.master.server = ProxyServer(config)
        os.system(f"certutil -addstore root C:{os.getenv('HOMEPATH')}/.mitmproxy/mitmproxy-ca-cert.cer")


    def run(self):
        [func() for func in proxy_startup_set]
        self.master.run()

    def shutdown(self):
        self.master.shutdown()
        [func() for func in proxy_shutdown_set]
        os.system("certutil -delstore root mitmproxy")


@Singleton
class FilterRuleManager(MetaRuleManager, ABC):
    def __init__(self):
        self.manager = Filter().master.addons
        self.exclude = dict()
        self.exclude.update(self.manager.lookup)

    def new_rule(self, name: str, pattern: Union[str, Pattern[AnyStr]], respond: Union[str, int]):
        rule = type(name, (), {"response": _instance_method, "pattern": pattern, "respond": respond})
        self.add_rule(name, rule())

    def add_rule(self, name: str, rule: Type[Any]):
        rule.name = name
        print(rule)

        self.manager.add(rule() if callable(rule) else rule)

    def get(self, name: str):
        return self.manager.get(name)

    def remove(self, name: str):
        if rule := self.get(name):
            self.manager.remove(rule)
        else:
            raise

    def copy(self):
        return dict().fromkeys(self.manager.lookup.items() - self.exclude.items())
