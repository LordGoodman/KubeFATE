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


class QueryCondition():
    """QueryCondition is context for job query"""

    def __init__(self, job_id):
        """ Init QueryCondition with job id

        :param job_id: The uuid of job
        :type job_id: string

        """
        self._job_id = job_id

    def get_job_id(self):
        """ Fetch the job id

        :rtype: dict

        """
        return {'job_id': self._job_id}

    def set_job_id(self, job_id):
        """ Set job id

        :param job_id: The uuid of job
        :type job_id: string

        """
        self._job_id = job_id

    def __str__(self):

        return self.get_job_id().__str__()


class Component():
    # TODO: add setter/getter
    """Component is used to describe steps in a pipline"""

    def __init__(self):
        """ Init an empty component
        """
        self._name = None
        self._module = None

        #: Need deploy of data io
        self._need_deploy = False

        #: The input part contains two sub structures, for more details please refer to `DSL definition <https://github.com/FederatedAI/FATE/blob/master/doc/dsl_conf_setting_guide.rst>`_
        #: They should be list type
        self._input_data = None
        self._input_train_data = None
        self._input_eval_data = None
        self._input_model = None
        self._input_isometric_model = None

        #: The output part also contains two sub structures, for more details please refer to `DSL definition <https://github.com/FederatedAI/FATE/blob/master/doc/dsl_conf_setting_guide.rst>`_
        #: They should be list type
        self._output_data = None
        self._output_model = None

    def to_dict(self):
        """ Convert Component to dictionary

        :rtype: dict

        """
        name = self._name
        body = {}
        module = {'module': self._module}
        inputs = {'input': {}}
        outputs = {'output': {}}
        need_deploy = {'need_deploy': self._need_deploy}

        # check all input
        if self._input_data != None:
            inputs['input']['data'] = {
                'data': self._input_data
            }
        elif self._input_train_data != None:
            inputs['input']['data'] = {
                'train_data': self._input_train_data
            }
        elif self._input_eval_data != None:
            inputs['input']['data'] = {
                'eval_data': self._input_eval_data
            }

        if self._input_model != None:
            inputs['input']['model'] = self._input_model
        elif self._input_isometric_model != None:
            inputs['input']['isometric_model'] = self._input_isometric_model

        if self._output_data != None:
            outputs['output']['data'] = self._output_data
        if self._output_model != None:
            outputs['output']['model'] = self._output_model

        body.update(module)
        body.update(inputs)
        body.update(outputs)
        body.update(need_deploy)

        return {name: body}


class ComponentBuilder():
    """ComponentBuilder is used to build Component instance"""

    def __init__(self):
        """ Init ComponentBuilder instance
        """

        self.reset()

    def reset(self):
        self._component = Component()

    def with_need_deploy(self, need_deploy):
        """ Set 'need_deploy' for DataIO module

        :param need_deploy: Value of need_deploy
        :type need_deploy: bool

        """
        self._component._need_deploy = need_deploy
        return self

    def with_name(self, name):
        """ Set component name

        :param name: name of the component
        :type name: string

        """
        self._component._name = name
        return self

    def with_module(self, module):
        """ Set component module

        :param module: The available module in FATE, for more details please refer to `Modules <https://github.com/FederatedAI/FATE/tree/master/federatedml>`
        :type module: string
        """
        self._component._module = module
        return self

    def with_input_data(self, *data):
        """ Set input data
        """
        self._component._input_data = [d for d in data]
        return self

    def with_input_train_data(self, *train_data):
        """ Set input data for training
        """
        self._component._input_train_data = [d for d in train_data]
        return self

    def with_input_eval_data(self, *eval_data):
        """ Set input data for evaluation
        """
        self._component._input_eval_data = [d for d in eval_data]
        return self

    def with_input_model(self, *model):
        """ Set input model
        """
        self._component._input_model = [d for d in module]
        return self

    def with_input_isometric_model(self, *isometric_model):
        """ Set input isometric model
        """
        self._component._input_isometric_model = [d for d in isometric_model]
        return self

    def with_output_data(self, *data):
        """ Set output data
        """
        self._component._output_data = [d for d in data]
        return self

    def with_output_model(self, *model):
        """ Set output model
        """

        self._component._output_model = [d for d in model]
        return self

    def build(self):
        component = self._component
        self.reset()
        return component


class Pipline():
    """Pipline is used to described pipline in FATE"""

    def __init__(self):
        self._name = 'components'
        self._components = {}

    def to_dict(self):
        return {self._name: self._components}


class PiplineBuilder():
    """PiplineBuilder is used to build pipline instance"""

    def __init__(self):
        self.reset()

    def reset(self):
        self._pipline = Pipline()

    def with_components(self, *components):
        for component in components:
            self._pipline._components.update(component.to_dict())
        return self

    def build(self):
        return self._pipline
