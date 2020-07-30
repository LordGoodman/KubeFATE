import pprint

from fml_manager import *

# Pipline
data_io = ComponentBuilder().with_name('dataio_0').with_module(
    'DataIO').with_input_data('arg.train_data').with_output_data('train').with_output_model(
    'dataio').with_need_deploy(True).build()

hetero_feature_selection = ComponentBuilder().with_name('hetero_feature_selection_0').with_module(
    'HeteroFeatureSelection').with_input_data('hetero_feature_binning_0.train').with_output_data(
    'eval').with_output_model('selected').with_input_isometric_model('hetero_feature_binning_0.hetero_feature_binning').build()

hetero_feature_binning = ComponentBuilder().with_name('hetero_feature_binning_0').with_module(
    'HeteroFeatureBinning').with_input_data('hetero_feature_selection_0.eval').with_output_data(
    'train').with_output_model("hetero_feature_binning").build()

evaluation = ComponentBuilder().with_name('evaluation_0').with_module(
    'Evaluation').with_input_data('hetero_feature_selection_0.eval').with_output_data('evaluate').build()

pipline = PiplineBuilder().with_components(
    data_io, hetero_feature_selection, hetero_feature_binning, evaluation).build()

pprint.pprint(pipline.to_dict())

# Configuration
initiator = InitiatorBuilder().with_role("guest").with_party_id(1000).build()
job_parameters = JobParametersBuilder().with_work_mode(1).with_job_type(
    "predict").with_model_id("123").with_model_version("sss").build()
role = RoleBuilder().with_guest(10000).with_host(
    10001, 100002).with_arbiter(10001).build()

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

role_parameters = RoleParametersBuilder().with_guest_train_data(namespaces=['breast_b'], names=['brest_b']).with_guest_module_config(modules=['dataio_0'], configs=[
    guest_data_io_config]).with_host_train_data(namespaces=['abc', 'efg'], names=['abc', 'efg']).with_host_module_config(modules=['dataio_0'], configs=[host_data_io_config]).build()

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

pprint.pprint(config.to_dict())
