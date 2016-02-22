import xmlrpclib
import urllib

import vcl_transport


class VCLServerProxy(xmlrpclib.ServerProxy):
    __userid = ''
    __passwd = ''

    def __init__(self, uri, userid, passwd, transport=None, encoding=None,
                 verbose=0, allow_none=0, use_datetime=0):
        self.__userid = userid
        self.__passwd = passwd
        # establish a "logical" server connection

        # get the url
        type, uri = urllib.splittype(uri)
        if type not in ("http", "https"):
            raise IOError, "unsupported XML-RPC protocol"
        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = "/RPC2"
        if transport is None:
            transport = vcl_transport.VCLTransport()
        self.__transport = transport
        self.__encoding = encoding
        self.__verbose = verbose
        self.__allow_none = allow_none

    def __request(self, method_name, params):
        request = xmlrpclib.dumps(params, method_name, encoding=self.__encoding,
                                  allow_none=self.__allow_none)
        response = self.__transport.request(
            self.__host,
            self.__userid,
            self.__passwd,
            self.__handler,
            request,
            verbose=self.__verbose
        )
        if len(response) == 1:
            response = response[0]
        return response

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)
