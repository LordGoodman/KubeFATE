#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: fmt_obj.py
@time: 2020-07-24 14:26

To make the modeling task more flexible, currently, FATE use its own domain-specific language(DSL) to describe modeling task. With usage of this DSL, modeling components such as data-io, feature-engineering and classification/regression module etc. can be combined as a Directed Acyclic Graph(DAG). Therefore, user can take and combine the algorithm components flexibly according to their needs.

In addition, each component has their own parameters to be configured. Also, the configuration may differ from party to party. For convenience, FATE configure all parameters for all parties and all components in one file. This guide will show you how to create such a configure file.

DSL Configure File
We use json file which is actually a dict as a dsl config file. The first level of the dict is always "components," which indicates content in the dict are components in your modeling task.

{
  "components" : {
          ...
      }
  }
Then each component should be defined on the second level. Here is an example of setting a component:

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
  }
As the example shows, user define the component name as key of this module. Note this module name should end up with a "_num" where the num should start with 0.

Field Specification
module:
Specify which component to use. This field should strictly match the file name in federatedml/conf/setting_conf except the .json suffix.

input:
There are two types of input, data and model.

Data: There are three possible data_input type:

data: typically used in data_io, feature_engineering modules and evaluation.
train_data: Used in homo_lr, hetero_lr and secure_boost. If this field is provided, the task will be parse as a fit task
eval_data: If train_data is provided, this field is optional. In this case, this data will be used as validation set. If train_data is not provided, this task will be parsed as a predict or transform task.
Model: There are two possible model-input types:

model: This is a model input by the same type of component. For example, hetero_binning_0 run as a fit component, and hetero_binning_1 take model output of hetero_binning_0 as input so that can be used to transform or predict.
Here's an example showing this logic:

"hetero_feature_binning_1": {
  "module": "HeteroFeatureBinning",
  "input": {
      "data": {
          "data": [
              "dataio_1.eval_data"
          ]
      },
      "model": [
          "hetero_feature_binning_0.fit_model"
      ]
  },
  "output": {
      "data": ["eval_data"],
      "model": ["eval_model"]
  }
}
isometric_model: This is used to specify the model input from upstream components.
For example, feature selection will take feature binning as upstream model, since it will use information value as feature importance. Here's an example of feature selection component:

"hetero_feature_selection_0": {
    "module": "HeteroFeatureSelection",
    "input": {
        "data": {
            "data": [
                "hetero_feature_binning_0.train"
            ]
        },
        "isometric_model": [
            "hetero_feature_binning_0.output_model"
        ]
    },
    "output": {
        "data": ["train"],
        "model": ["output_model"]
    }
}
output: Same as input, two types of output may occur which are data and model.

Data: Specify the output data name
Model: Specify the output model name
You can take the above case as an example.

Submit Runtime Conf
Besides the dsl conf, user also need to prepare a submit runtime conf to set the parameters of each component.

initiator:
To begin with, the initiator should be specified in this runtime conf. Here is an exmaple of setting initiator:

"initiator": {
    "role": "guest",
    "party_id": 10000
}
role:
All the roles involved in this modeling task should be specified. Each element in the role should contain role name and their party ids. The reason for ids are with form of list is that there may exist multiple parties in one role.

"role": {
    "guest": [
      10000
    ],
    "host": [
      10000
    ],
    "arbiter": [
      10000
    ]
}
role_parameters:
Those parameters that are differ from party to party, should be indicated here. Please note that each parameters should has the form of list. Inside the role_parameters, party names are used as key and parameters of these parties are values. Take the following structure as an example:

"guest": {
  "args": {
    "data": {
      "train_data": [
        {
          "name": "1ca0d9eea77e11e9a84f5254005e961b",
          "namespace": "arbiter-10000#guest-10000#host-10000#train_input#guest#10000"
        }
      ]
    }
  },
  "dataio_0": {
    "with_label": [
      true
    ],
    ...
  }
},
"host": {
  "args": {
    "data": {
      "train_data": [
        {
          "name": "3de22bdaa77e11e99c5d5254005e961b",
          "namespace": "arbiter-10000#guest-10000#host-10000#train_input#host#10000"
        }
      ]
    }
  },
  "dataio_0": {
     ...
  }
  ...
}
As this example shows, for each party, the input parameters such as train_data, eval_data and so on should be list in args. The name and namespace above are table indicators for uploaded data.

Then, user can config parameters for each components. The component names should match names defined in the dsl config file. The content of each component parameters are defined in Param class located in federatedml/param.

algorithm_parameters:
If some parameters are the same among all parties, they can be set in algorithm_parameters. Here is an example showing how to do that.

"hetero_feature_binning_0": {
    ...
},
"hetero_feature_selection_0": {
    ...
},
"hetero_lr_0": {
  "penalty": "L2",
  "optimizer": "rmsprop",
  "eps": 1e-5,
  "alpha": 0.01,
  "max_iter": 10,
  "converge_func": "diff",
  "batch_size": 320,
  "learning_rate": 0.15,
  "init_param": {
    "init_method": "random_uniform"
  },
  "cv_param": {
    "n_splits": 5,
    "shuffle": false,
    "random_seed": 103,
    "need_cv": false,

  }
}
Same with the form in role parameters, each key of the parameters are names of components that are defined in dsl config file.

After setting config files and submitting the task, fate-flow will combine the parameter list in role-parameters and algorithm parameters. If there are still some undefined fields, values in default runtime conf will be used. Then fate-flow will send these config files to their corresponding parties and start the federated modeling task.

Multi-host configuration
For multi-host modeling case, all the host's party ids should be list in the role field.

"role": {
  "guest": [
    10000
  ],
  "host": [
    10000, 10001, 10002
  ],
  "arbiter": [
    10000
  ]
}
Each parameter set for host should also be list in a list. The number of elements should match the number of hosts.

"host": {
    "args": {
      "data": {
        "train_data": [
          {
            "name": "hetero_breast_host_1",
            "namespace": "hetero_breast_host"
          },
          {
            "name": "hetero_breast_host_2",
            "namespace": "hetero_breast_host"
          },
          {
            "name": "hetero_breast_host_3",
            "namespace": "hetero_breast_host"
          }

        ]
      }
    },
    "dataio_0": {
      "with_label": [false, false, false],
      "output_format": ["dense", "dense", "dense"],
      "outlier_replace": [true, true, true]
    }
The parameters set in algorithm parameters need not be copied into host role parameters. Algorithm parameters will be copied for every party.
"""

__mtime__ = '2020-07-24'

import json

pipline = '''
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
                "data": ["eval"],
                "model": ["selected"]
            }
        },
        "evaluation_0": {
            "module": "Evaluation",
            "input": {
                "data": {
                    "data": ["hetero_feature_selection_0.eval"]
                }
            },
            "output": {
                "data": ["evaluate"]
            }
        }
    }
}
'''


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Builder(Dict):
    __root__ = None

    def __init__(self, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        if self.__root__ is None:
            pass
        else:
            self[self.__root__] = Builder()

    def __getattr__(self, *args, **kwargs):
        name = args[0]
        return self.__setvalue(name)

    def __setvalue(self, name):
        self = self

        def foo(*args):
            if len(args) == 1:
                value = args[0]
                if self.__root__ is None:
                    self[name] = value
                else:
                    self[self.__root__][name] = value
            return self

        return foo


class Metadata(object):
    def withInput(self):
        if self.get("input") is None:
            self["input"] = Builder()

        return self

    def withInputData(self, value):
        self.withInput()
        if self["input"].get("data") is None:
            self["input"].data(Builder())
        if self["input"]["data"].get("data") is None:
            self["input"]["data"]["data"] = []
        self["input"]["data"]["data"].append(value)
        return self

    def withOutput(self):
        if self.get("output") is None:
            self["output"] = Builder()
        return self

    def withOutputData(self, value):
        self.withOutput()
        if self["output"].get("data") is None:
            self["output"]["data"] = []
        self["output"]["data"].append(value)
        return self

    def withOutputModel(self, value):
        self.withOutput()
        if self["output"].get("model") is None:
            self["output"]["model"] = []
        self["output"]["model"].append(value)
        return self


class DataIoBuilder(Builder, Metadata):
    pass


class HeteroFeatureBinninBuilder(Builder, Metadata):
    pass


class EvaluationBinninBuilder(Builder, Metadata):
    pass


class HeteroFeatureSelectionBuilder(Builder, Metadata):
    def withInputIsometricModel(self, value):
        self.withInput()
        if self["input"].get("isometric_model") is None:
            self["input"]["isometric_model"] = []
        self["input"]["isometric_model"].append(value)
        return self


class ComponentBuilder(Builder):
    __root__ = "components"


config = '''
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


class InitiatorBuilder(Builder):

    def __init__(self, *args, **kwargs):
        super(InitiatorBuilder, self).__init__(*args, **kwargs)
        self["role"] = None
        self["party_id"] = None


class JobParameterBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(JobParameterBuilder, self).__init__(*args, **kwargs)
        self["work_mode"] = None


class AlgorithmParameterBuilder(Builder):
    pass


class RoleParameterBuilder(Builder):
    pass


class HostBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(HostBuilder, self).__init__(*args, **kwargs)
        self["args"] = Builder()
        self["args"]["data"] = Builder()
        self["args"]["data"]["train_data"] = []

        self["dataio_0"] = Builder()
        self["dataio_0"]["with_label"] = []
        self["dataio_0"]["output_format"] = []

    def train_data(self, value):
        self["args"]["data"]["train_data"].append(value)
        return self

    def with_label(self, value):
        self["dataio_0"]["with_label"].append(value)
        return self

    def output_format(self, value):
        self["dataio_0"]["output_format"].append(value)
        return self


class GuestBuilder(HostBuilder):
    def __init__(self, *args, **kwargs):
        super(GuestBuilder, self).__init__(*args, **kwargs)
        self["dataio_0"]["label_name"] = []
        self["dataio_0"]["label_type"] = []

    def label_name(self, value):
        self["dataio_0"]["label_name"].append(value)
        return self

    def label_type(self, value):
        self["dataio_0"]["label_type"].append(value)
        return self


class RoleBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(RoleBuilder, self).__init__(*args, **kwargs)
        self["guest"] = []
        self["host"] = []
        self["arbiter"] = []

    def guest(self, value):
        self["guest"].append(value)
        return self

    def host(self, value):
        self["host"].append(value)
        return self

    def arbiter(self, value):
        self["arbiter"].append(value)
        return self


class HeteroLrBuilder(Builder):

    def __init__(self, *args, **kwargs):
        super(HeteroLrBuilder, self).__init__(*args, **kwargs)
        self["penalty"] = None
        self["optimizer"] = None
        self["eps"] = None
        self["alpha"] = None
        self["max_iter"] = None
        self["converge_func"] = None
        self["batch_size"] = None
        self["learning_rate"] = None
        self["init_param"] = Builder()
        self["init_param"]["init_method"] = None

    def init_method(self, value):
        self["init_param"]["init_method"] = value
        return self


if __name__ == '__main__':
    configObj = Builder(). \
        initiator(
        InitiatorBuilder()
            .role("guest")
            .party_id(10000)
    ). \
        job_parameters(
        JobParameterBuilder()
            .work_mode(1)
    ). \
        role(
        RoleBuilder()
            .guest(10000)
            .host(9999)
            .arbiter(9999)
    ). \
        role_parameters(
        RoleParameterBuilder()
            .guest(
            GuestBuilder()
                .args()
                .data()
                .train_data(
                Builder()
                    .name("breast_b")
                    .namespace("fate_flow_test_breast")
            ).dataio_0()
                .with_label(True)
                .label_name("y")
                .label_type("int")
                .output_format("dense")
        ).host(
            HostBuilder().args()
                .data()
                .train_data(
                Builder()
                    .name("breast_a")
                    .namespace("fate_flow_test_breast")
            ).dataio_0()
                .with_label(False)
                .output_format("dense")
        )
    ). \
        algorithm_parameters(
        AlgorithmParameterBuilder()
            .hetero_lr_0(
            HeteroLrBuilder()
                .penalty("L2")
                .optimizer("rmsprop")
                .eps(1e-5)
                .alpha(0.01)
                .max_iter(3)
                .converge_func("diff")
                .batch_size(320)
                .learning_rate(0.15)
                .init_param().init_method("random_uniform")
        )
    )

    print(json.dumps(configObj, default=lambda o: o.__dict__, indent=2, ensure_ascii=False))
    fmtObj = ComponentBuilder().dataio_0(
        DataIoBuilder()
            .module("DataIO")
            .withInputData("args.train_data")
            .withOutputData("train")
            .withOutputModel("dataio")
            .need_deploy(True)
    ).hetero_feature_binning_0(
        HeteroFeatureBinninBuilder()
            .module("HeteroFeatureBinning")
            .withInputData("hetero_feature_selection_0.eval")
            .withOutputData("train")
            .withOutputModel("hetero_feature_binning")
    ).hetero_feature_selection_0(
        HeteroFeatureSelectionBuilder()
            .module("HeteroFeatureSelection")
            .withInputData("hetero_feature_binning_0.train")
            .withInputIsometricModel("hetero_feature_binning_0.hetero_feature_binning")
            .withOutputData("eval")
            .withOutputModel("selected")
    ).evaluation_0(
        EvaluationBinninBuilder().module("Evaluation")
            .withInputData("hetero_feature_selection_0.eval")
            .withOutputData("evaluate")
    )
    print(json.dumps(fmtObj, default=lambda o: o.__dict__, indent=2, ensure_ascii=False))
