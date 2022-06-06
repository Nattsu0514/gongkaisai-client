import re
import sys

import clr

from sunrise import pid
from sunrise.filter import MetaFilter
from sunrise.util import get_file_as_byte

sys.path.append(r"./dll/")
clr.FindAssembly("FiddlerCore4")
clr.AddReference("FiddlerCore4")

import Fiddler


def _before_response_session(session):
    for r in Filter.Rules.values():
        if re.search(r.pattern, session.fullUrl, re.I) is not None:
            session.ResponseBody = get_file_as_byte(r.respond)


def _before_request_session(session):
    if session.LocalProcessID == pid:
        session.bBufferResponse = True


class Filter(MetaFilter):
    def __init__(self):
        Fiddler.CONFIG.IgnoreServerCertErrors = True
        Fiddler.FiddlerApplication.BeforeRequest += _before_request_session
        Fiddler.FiddlerApplication.BeforeResponse += _before_response_session

        if not Fiddler.CertMaker.rootCertIsTrusted():
            Fiddler.CertMaker.createRootCert()
            Fiddler.CertMaker.trustRootCert()

    def startup(self):
        Fiddler.FiddlerApplication.Startup(self.port, Fiddler.FiddlerCoreStartupFlags.Default)

    def shutdown(self):
        Fiddler.FiddlerApplication.Shutdown()
