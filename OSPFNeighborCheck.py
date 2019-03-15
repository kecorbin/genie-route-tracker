import logging
from pyats import aetest
from genie.conf import Genie

try:
    from genie.ops.utils import get_ops
except ModuleNotFoundError:
    from genie.ops.base import get_ops

from ats.log.utils import banner

log = logging.getLogger(__name__)


class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):

        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        uut = genie_testbed.devices['uut']
        uut.connect()


class NeighborTest(aetest.Testcase):
    """Check for the existence of a route, perform recovery action if route
    is not present"""

    @aetest.test
    def collect_ospf_info(self, testbed):
        uut = testbed.devices['uut']

        nbr_details = uut.custom['expected_ospf_neighbor']
        ospf_process = nbr_details['ospf_process']
        expected_interface = nbr_details['expected_interface']
        ospf_area = nbr_details['ospf_area']
        # Retrieve Ospf Class for this device
        ospf_cls = get_ops('ospf', uut)
        # Instantiate the class, and provides some attributes
        # Attributes limit the # of clis to use;
        # It will only learn the neighbors,  nothing else.
        attributes = ['info[vrf][(.*)][address_family][ipv4]'
                      '[instance][{OSPF_PROCESS}]'
                      '[areas][{OSPF_AREA}]'
                      '[interfaces][{EXPECTED_INTERFACE}]'
                      '[neighbors][(.*)]'
                      .format(OSPF_PROCESS=ospf_process,
                              OSPF_AREA=ospf_area,
                              EXPECTED_INTERFACE=expected_interface)]

        ospf = ospf_cls(uut, attributes=attributes)

        ospf.learn()

        if ospf.info:
            self.parent.parameters['ospf_ops'] = ospf
            log.info(ospf.info)
            self.passed("Collected OSPF Information")
        else:
            self.failed("Could not collect OSPF information")

    @aetest.test
    def check_for_neighbor(self, testbed):
        uut = testbed.devices['uut']
        nbr_details = uut.custom['expected_ospf_neighbor']
        ospf_process = nbr_details['ospf_process']
        expected_interface = nbr_details['expected_interface']
        expected_neighbor = nbr_details['expected_neighbor']
        vrf = nbr_details['vrf']
        ospf_area = nbr_details['ospf_area']

        try:
            ospf_data = self.parent.parameters['ospf_ops']
            vrf_data = ospf_data.info["vrf"][vrf]
            instance = vrf_data['address_family']['ipv4']['instance'][str(ospf_process)] # noqa
            area = instance['areas'][ospf_area]
            intf = area['interfaces'][expected_interface]
            nbrs = intf['neighbors']
            log.info("Parsed OSPF ops data and found neighbors")
        except KeyError as e:
            log.error(banner("Could not parse ospf neighbors: {}".format(e)))
            exit()

        if expected_neighbor in nbrs.keys():
            # we do not need to perform any recovery action
            aetest.skip.affix(section=Recovery.perform_recovery_action,
                              reason="Recovery Action Not Required")
            self.passed('yay!')

        else:
            # recovery action needs to be performed
            self.failed('ruh roh')


class Recovery(aetest.Testcase):
    """Recover from failure scenario, this testcase is skipped if
    NeighborTest suceeds"""

    @aetest.test
    def perform_recovery_action(self):
        log.info('Starting Recovery Procedure')

        recovered = False
        # your recovery code here

        if recovered:
            self.passed('Looks like we saved the day')
        else:
            self.failed("Oops - didn't recover")
