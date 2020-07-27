# Copyright 2019-2020 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# you may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fml_manager import ClusterManager
from fml_manager import PartyBuilder, PartyType

if __name__ == "__main__":
    # init the cluster manager
    cluster_manager = ClusterManager("fate-10000", "fate")

    # get route table
    route_table = cluster_manager.get_route_table()

    # show all party
    print(route_table.get_party())

    # delete route table party
    route_table.remove_party('9999', '8888')
    print(route_table.get_party())

    # define normal party
    party = PartyBuilder().with_id(
        '9999').with_ip('192.168.2.2').with_port('30010').build()

    # append normal party to route table
    route_table.add_party(party)
    print(route_table.get_party())

    # define exchange
    party = PartyBuilder().with_id('any').with_ip(
        '192.168.1.2').with_port('30009').with_type(PartyType.EXCHANGE).build()

    # append exchange to route table
    route_table.add_party(party)
    print(route_table.get_party())

    # update route table of configmap
    cluster_manager.set_route_table(route_table)

    # get entrypoint
    print(cluster_manager.get_entry_point())
