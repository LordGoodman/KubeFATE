import json
from enum import Enum

"""Module to Build Complex Data Structural in FATE"""


class PartyType(Enum):

    """PartyType is used to identified the type of party"""

    #: For normal party
    NORMAL = 1

    #: For exchange
    EXCHANGE = 2


class Party():
    """Party is used to define route table record"""

    def __init__(self) -> None:
        """ Return default party instance"""

        #: ID of the party
        self._id = None

        #: IP address of the party
        self._ip = None

        #: Service port of the party
        self._port = None

        #: Type of the party
        self._type = PartyType.NORMAL

    def set_id(self, party_id) -> None:
        """ Set party ID

        :param party_id: The ID of party
        :type party_id: string

        """

        self._id = party_id

    def set_ip(self, party_ip) -> None:
        """ Set IP address of party

        :param party_ip: The IP address of party
        :type party_ip: string

        """

        self._ip = party_ip

    def set_port(self, party_port) -> None:
        """ Set service port of the party

        :param party_port: The service port of party
        :type party_port: int

        """

        self._port = party_port

    def set_type(self, party_type) -> None:
        """ Set party type

        :param party_id: The type of party
        :type party_type: PartyType

        """

        self._type = party_type

    def get_id(self) -> str:
        """ Get party ID

        :rtype: string

        """

        return self._id

    def to_entry_point(self) -> dict:
        """ Get entrypoint of party

        :rtype: dict

        """
        return {'default': [{'ip': self._ip, 'port': self._port}]}


class PartyBuilder():
    """PartyBuilder is used to construct party instance"""

    def __init__(self) -> None:
        """ Get default party instance
        """

        self.reset()

    def reset(self) -> None:
        """ Reset the previous instance
        """

        self._party = Party()

    def with_id(self, party_id):
        """ Update ID
        :param party_id: The ID of party
        :type party_id: string
        """

        self._party.set_id(party_id)
        return self

    def with_ip(self, party_ip):
        """ Update IP
        :param party_ip: The IP of party
        :type party_ip: string
        """

        self._party.set_ip(party_ip)
        return self

    def with_port(self, party_port):
        """ Update port
        :param party_port: The port of party
        :type party_port: int
        """

        self._party.set_port(party_port)
        return self

    def with_type(self, party_type):
        """ Update type
        :param party_type: The type of party
        :type party_type: PartyType
        """

        self._party.set_type(party_type)
        return self

    def build(self):
        """ Return party instance with config
        :rtype: Party
        """
        party = self._party
        self.reset()

        # reset id to 'default' if party is exchange
        if party._type == PartyType.EXCHANGE:
            party._id = 'default'

        return party


class RouteTable():
    """RouteTable is used to communicate with other parties"""

    def __init__(self) -> None:
        """ Return instance with empty route table
        """

        #: The underlying route table config file
        self._route_table = None

    def add_party(self, *parties) -> None:
        """ Append parties to route table
        :param parties: A list of party instance
        :type parties: list
        """

        for party in parties:
            self._route_table['route_table'][party.get_id()] = party.to_entry_point(
            )

    def update_party(self, *parties) -> None:
        """ Update parties of route table
        :param parties: A list of party instance
        :type parties: list
        """

        for party in parties:
            self._route_table['route_table'][party.get_id()] = party.to_entry_point(
            )

    def remove_party(self, *party_ids) -> None:
        """ Remove parties from route table
        :param parties: A list of party ID
        :type parties: list
        """

        for party_id in party_ids:
            if(self._route_table['route_table'].get(party_id) != None):
                self._route_table['route_table'].pop(party_id)

    def get_party(self) -> dict:
        """ List all parties
        :rtype: dict
        """
        return self._route_table['route_table']

    def from_dict(self, route_table):
        """ Load route table config from dict
        :param route_table: The underlying route table
        :type route_table: dict
        :rtype: RouteTable
        """
        self._route_table = route_table
        return self

    def to_dict(self) -> dict:
        """ Return underlying route table
        :rtype: dict
        """
        return self._route_table