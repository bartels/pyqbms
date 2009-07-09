"""
QuickBooks Merchant Services API Signon Requests

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.requests.qbms import QBMSRequest
from pyqbms.datatypes.signon import SignonAppCertRq, SignonAppCertRs
from pyqbms.datatypes.signon import SignonDesktopRq, SignonDesktopRs


class SignonAppCertRequest(QBMSRequest):
    rq_aggregate_type = SignonAppCertRq
    rs_aggregate_type = SignonAppCertRs

    def build_element_tree(self):
        tree =  super(SignonAppCertRequest, self).build_element_tree()
        self.signon_msgs_rq_el.append(self.rq_aggregate.element)
        return tree
        

class SignonDesktopRequest(QBMSRequest):
    rq_aggregate_type = SignonDesktopRq
    rs_aggregate_type = SignonDesktopRs

    def build_element_tree(self):
        tree =  super(SignonDesktopRequest, self).build_element_tree()
        self.signon_msgs_rq_el.append(self.rq_aggregate.element)
        return tree
        

