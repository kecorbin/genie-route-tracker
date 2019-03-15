from pyats.easypy import run


# main() function must be defined in each job file
#   - it should have a runtime argument
#   - and contains one or more tasks
def main(runtime):

    run(testscript='OSPFNeighborCheck.py',
        runtime=runtime,
        ospf_process='1',
        vrf='default',
        expected_interface='GigabitEthernet0/1',
        expected_neighbor='192.168.0.2',
        ospf_area='0.0.0.0')
