
class DuniterError(Exception):
    """
    duniter error
    """
    def __init__(self, data):
        super().__init__("Error code {0} - {1}".format(data["ucode"], data["message"]))
        self.ucode = data["ucode"]
        self.message = data["message"]

UNKNOWN                              = 1001
UNHANDLED                            = 1002
SIGNATURE_DOES_NOT_MATCH             = 1003
ALREADY_UP_TO_DATE                   = 1004
WRONG_DOCUMENT                       = 1005
HTTP_LIMITATION                      = 1006

HTTP_PARAM_PUBKEY_REQUIRED           = 1101
HTTP_PARAM_IDENTITY_REQUIRED         = 1102
HTTP_PARAM_PEER_REQUIRED             = 1103
HTTP_PARAM_BLOCK_REQUIRED            = 1104
HTTP_PARAM_MEMBERSHIP_REQUIRED       = 1105
HTTP_PARAM_TX_REQUIRED               = 1106
HTTP_PARAM_SIG_REQUIRED              = 1107
HTTP_PARAM_CERT_REQUIRED             = 1108
HTTP_PARAM_REVOCATION_REQUIRED       = 1109
HTTP_PARAM_CONF_REQUIRED             = 1110

NO_MATCHING_IDENTITY                 = 2001
UID_ALREADY_USED                     = 2002
PUBKEY_ALREADY_USED                  = 2003
NO_MEMBER_MATCHING_PUB_OR_UID        = 2004
SELF_PEER_NOT_FOUND                  = 2005
WRONG_SIGNATURE_MEMBERSHIP           = 2006
ALREADY_RECEIVED_MEMBERSHIP          = 2007
MEMBERSHIP_A_NON_MEMBER_CANNOT_LEAVE = 2008
NOT_A_MEMBER                         = 2009
NO_CURRENT_BLOCK                     = 2010
BLOCK_NOT_FOUND                      = 2011
PEER_NOT_FOUND                       = 2012
WRONG_UNLOCKER                       = 2013
LOCKTIME_PREVENT                     = 2014
SOURCE_ALREADY_CONSUMED              = 2015
WRONG_AMOUNTS                        = 2016
WRONG_OUTPUT_BASE                    = 2017
CANNOT_ROOT_BLOCK_NO_MEMBERS         = 2018