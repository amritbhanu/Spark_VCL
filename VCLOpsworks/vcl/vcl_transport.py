import xmlrpclib
import sys


class VCLTransport(xmlrpclib.SafeTransport):
    ##
    # Send a complete request, and parse the response.
    #
    # @param host Target host.
    # @param handler Target PRC handler.
    # @param request_body XML-RPC request body.
    # @param verbose Debugging flag.
    # @return Parsed response.

    def request(self, host, userid, passwd, handler, request_body, verbose=0):
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        h.putheader('X-APIVERSION', '2')
        h.putheader('X-User', userid)
        h.putheader('X-Pass', passwd)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        response = h.getresponse()
        errcode, errmsg, headers = response.status, response.msg, response.getheaders()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
            )
        self.verbose = verbose
        resp = response.read()
        try:
            resp = xmlrpclib.loads(resp)[0]
        except xmlrpclib.Fault, err:
            if err.faultCode == 3:
                print "ERROR: Received '%s' error. " \
                      "The credentials you supplied to log in to the VCL site were not accepted." % err.faultString
            elif err.faultCode == 4:
                print "ERROR: %s" % err.faultString
            elif err.faultCode == 5:
                print "ERROR: Received '%s' error. " \
                      "The VCL site could not establish a connection with your authentication server." % err.faultString
            elif err.faultCode == 6:
                print "ERROR: Received '%s' error. " \
                      "The VCL site could not determine a method to use to authenticate the supplied user." \
                      % err.faultString
            else:
                print "ERROR: Received '%s' error from VCL site." % err.faultString

        return resp
