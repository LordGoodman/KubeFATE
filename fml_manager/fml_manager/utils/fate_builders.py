import json
from enum import Enum


class PartyType(Enum):
    NORMAL = 1
    EXCHANGE = 2


class Party():
    def __init__(self) -> None:
        self._id = None
        self._ip = None
        self._port = None
        self._type = PartyType.NORMAL

    def set_id(self, party_id) -> None:
        self._id = party_id

    def set_ip(self, party_ip) -> None:
        self._ip = party_ip

    def set_port(self, party_port) -> None:
        self._port = party_port

    def set_type(self, party_type) -> None:
        self._type = party_type

    def get_id(self) -> str:
        return self._id

    def to_entry_point(self) -> dict:
        return {'default': [{'ip': self._ip, 'port': self._port}]}


class PartyBuilder():
    def __init__(self) -> None:
        self.reset()
        self

    def reset(self) -> None:
        self._party = Party()

    def with_id(self, party_id):
        self._party.set_id(party_id)
        return self

    def with_ip(self, ip):
        self._party.set_ip(ip)
        return self

    def with_port(self, port):
        self._party.set_port(port)
        return self

    def with_type(self, party_type):
        self._party.set_type(party_type)
        return self

    def build(self):
        party = self._party
        self.reset()

        # reset id to 'default' if party is exchange
        if party._type == PartyType.EXCHANGE:
            party._id = 'default'

        return party


class RouteTable():
    def __init__(self) -> None:
        self._route_table = None

    def add_party(self, party) -> None:
        self._route_table['route_table'][party.get_id()] = party.to_entry_point(
        )

    def update_party(self, party) -> None:
        self._route_table['route_table'][party.get_id()] = party.to_entry_point(
        )

    def remove_party(self, *party_ids) -> None:
        for party_id in party_ids:
            if(self._route_table['route_table'].get(party_id) != None):
                self._route_table['route_table'].pop(party_id)

    def get_party(self) -> dict:
        return self._route_table['route_table']

    def from_dict(self, route_table):
        self._route_table = route_table
        return self

    def to_dict(self) -> dict:
        return self._route_table
