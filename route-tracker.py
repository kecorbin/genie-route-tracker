import argparse
from genie.conf import Genie
from ats.topology import loader
from ats.log.utils import banner
import ipyats.tasks as tasks


OSPF_PROCESS = "1"
EXPECTED_INTERFACE = "GigabitEthernet2"
OSPF_AREA = "0.0.0.0"


def check_for_neighbor(ospf_data,
                       expected_neighbor,
                       proc=OSPF_PROCESS,
                       area=OSPF_AREA,
                       intf=EXPECTED_INTERFACE,
                       vrf='default'):

    try:
        vrf_data = ospf_data["vrf"][vrf]
        instance = vrf_data['address_family']['ipv4']['instance'][str(proc)]
        area = instance['areas'][area]
        intf = area['interfaces'][intf]
        nbrs = intf['neighbors']
    except KeyError as e:
        print(banner("Could not retrieve neighbors: {}".format(e)))
        exit()


    if expected_neighbor in nbrs.keys():
        return nbrs[expected_neighbor]['state']
    else:
        return None


def main():

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument('--testbed', dest='testbed', type=loader.load)
    parser.add_argument('--neighbor', help="Expected neighbor RID")

    args, unknown = parser.parse_known_args()
    if not all([args.testbed, args.neighbor]):
        print(
            banner("Please specify a testbed file and expected neighbor")
            )

    else:

        # pyats testbed != genie testbed
        testbed = Genie.init(args.testbed)
        uut = testbed.devices['uut']
        ospf = tasks.learn('ospf', uut)
        nbr = args.neighbor
        state = check_for_neighbor(ospf, nbr)
        if state:
            print(
                banner("Successfully verified neighbor {} is {}".format(nbr,
                                                                        state))
            )
        else:
            print(banner("Failed to verify neighbor, now what?"))


if __name__ == '__main__':
    main()
