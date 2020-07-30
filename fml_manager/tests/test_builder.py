import pprint

from fml_manager import *

# hetero lr
pipline_str = '''
{
    "components" : {
        "dataio_0": {
            "module": "DataIO",
            "input": {
                "data": {
                    "data": [
                        "args.train_data"
                    ]
                }
            },
            "output": {
                "data": ["train"],
                "model": ["dataio"]
            },
                        "need_deploy": true
         },
        "hetero_feature_binning_0": {
            "module": "HeteroFeatureBinning",
            "input": {
                "data": {
                    "data": [
                        "dataio_0.train"
                    ]
                }
            },
            "output": {
                "data": ["train"],
                "model": ["hetero_feature_binning"]
            }
        },
        "hetero_feature_selection_0": {
            "module": "HeteroFeatureSelection",
            "input": {
                "data": {"data": [
                        "hetero_feature_binning_0.train"
                    ]
                },
                "isometric_model": [
                    "hetero_feature_binning_0.hetero_feature_binning"
                ]
            },
            "output": {
                "data": ["train"],
                "model": ["selected"]
            }
        },
        "hetero_lr_0": {
            "module": "HeteroLR",
            "input": {
                "data": {
                    "train_data": ["hetero_feature_selection_0.train"]
                }
            },
            "output": {
                "data": ["train"],
                "model": ["hetero_lr"]
            }
        },
        "evaluation_0": {
            "module": "Evaluation",
            "input": {
                "data": {
                    "data": ["hetero_lr_0.train"]
                }
            },
            "output": {
                "data": ["evaluate"]
            }
        }
    }
}
'''


# Pipline
data_io = ComponentBuilder().with_name('dataio_0').with_module(
    'DataIO').with_input_data('arg.train_data').with_output_data('train').with_output_model(
    'dataio').with_need_deploy(True).build()

hetero_feature_selection = ComponentBuilder().with_name('hetero_feature_selection_0').with_module(
    'HeteroFeatureSelection').with_input_data('hetero_feature_binning_0.train').with_output_data(
    'train').with_output_model('selected').with_input_isometric_model('hetero_feature_binning_0.hetero_feature_binning').build()

hetero_feature_binning = ComponentBuilder().with_name('hetero_feature_binning_0').with_module(
    'HeteroFeatureBinning').with_input_data('dataio_0.train').with_output_data(
    'train').with_output_model("hetero_feature_binning").build()

hetero_lr = ComponentBuilder().with_name('hetero_lr_0').with_module('HeteroLR').with_input_train_data(
    'hetero_feature_selection_0.train').with_output_data('train').with_output_model('hetero_lr').build()

evaluation = ComponentBuilder().with_name('evaluation_0').with_module(
    'Evaluation').with_input_data('hetero_lr_0.train').with_output_data('evaluate').build()

pipline = PiplineBuilder().with_components(
    data_io, hetero_feature_selection, hetero_feature_binning, hetero_lr, evaluation).build()

lho = pipline.to_dict()
rho = json.loads(pipline_str)

pprint.pprint(lho)
print('------')
pprint.pprint(rho)

# config
config_str = '''
{
    "initiator": {
        "role": "guest",
        "party_id": 10000
    },
    "job_parameters": {
        "work_mode": 1
    },
    "role": {
        "guest": [10000],
        "host": [9999],
        "arbiter": [9999]
    },
    "role_parameters": {
        "guest": {
            "args": {
                "data": {
                    "train_data": [{"name": "breast_b", "namespace": "fate_flow_test_breast"}]
                }
            },
            "dataio_0":{
                "with_label": [true],
                "label_name": ["y"],
                "label_type": ["int"],
                "output_format": ["dense"]
            }
        },
        "host": {
            "args": {
                "data": {
                    "train_data": [{"name": "breast_a", "namespace": "fate_flow_test_breast"}]
                }
            },
             "dataio_0":{
                "with_label": [false],
                "output_format": ["dense"]
            }
        }
    },
    "algorithm_parameters": {
        "hetero_lr_0": {
            "penalty": "L2",
            "optimizer": "rmsprop",
            "eps": 1e-5,
            "alpha": 0.01,
            "max_iter": 3,
            "converge_func": "diff",
            "batch_size": 320,
            "learning_rate": 0.15,
            "init_param": {
                                "init_method": "random_uniform"
            }
        }
    }
}
'''

# Configuration
initiator = InitiatorBuilder().with_role("guest").with_party_id(1000).build()
job_parameters = JobParametersBuilder().with_work_mode(1).build()
role = RoleBuilder().with_guest(10000).with_host(9999).with_arbiter(9999).build()

guest_data_io_config = {
    "with_label": [True],
    "label_name": ["y"],
    "label_type": ["int"],
    "output_format": ["dense"]
}

host_data_io_config = {
    "with_label": [False],
    "output_format": ["dense"]
}

role_parameters = RoleParametersBuilder().with_guest_train_data(namespaces=['fate_flow_test_breast'], names=['brest_b']).with_guest_module_config(modules=['dataio_0'], configs=[
    guest_data_io_config]).with_host_train_data(namespaces=['breast_a'], names=['fate_flow_test_breast']).with_host_module_config(modules=['dataio_0'], configs=[host_data_io_config]).build()

hetero_lr_params = {
    "penalty": "L2",
    "optimizer": "rmsprop",
    "eps": 1e-5,
    "alpha": 0.01,
    "max_iter": 3,
    "converge_func": "diff",
    "batch_size": 320,
    "learning_rate": 0.15,
    "init_param": {
        "init_method": "random_uniform"
    }
}

algorithm_parameters = AlgorithmParametersBuilder().with_module_config(
    modules=['hetero_lr_0'], configs=[hetero_lr_params]).build()

config = ConfigBuilder().with_initiator(initiator).with_job_parameters(job_parameters).with_role(
    role).with_role_parameters(role_parameters).with_algorithm_parameters(algorithm_parameters).build()

lho = config.to_dict()
rho = json.loads(config_str)

pprint.pprint(lho)
print('------')
pprint.pprint(rho)