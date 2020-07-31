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
from fml_manager import Party, PartyType

if __name__ == "__main__":
    # init the cluster manager
    cluster_manager = ClusterManager("fate-10000", "fate")

    # get route table
    route_table = cluster_manager.get_route_table()

    # show all party
    print(route_table.get_party())

    # delete route table party
    party_id_1 = '9999'
    party_id_2 = '8888'
    route_table.remove_party(party_id_1, party_id_2)
    print(route_table.get_party())

    # define normal party
    party = Party(p_id='9999', ip='192.168.2.2', port=30010)

    # append normal party to route table
    route_table.add_party(party)
    print(route_table.get_party())

    # define exchange
    party = Party(ip='192.168.2.2', port=30009, p_type=PartyType.EXCHANGE)

    # append exchange to route table
    route_table.add_party(party)
    print(route_table.get_party())

    # update route table of configmap
    cluster_manager.set_route_table(route_table)

    # get entrypoint
    print(cluster_manager.get_entry_point())
