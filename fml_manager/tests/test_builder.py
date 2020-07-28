import pprint

from fml_manager import ComponentBuilder, PiplineBuilder

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
