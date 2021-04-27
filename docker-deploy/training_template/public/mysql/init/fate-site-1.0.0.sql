CREATE DATABASE fate_site DEFAULT CHARACTER SET utf8mb4;
use fate_site;

CREATE TABLE `fs_site` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(64) NOT NULL COMMENT '唯一编号',
  `name` varchar(256) NOT NULL COMMENT '站点名称',
  `web_ip` varchar(256) NOT NULL COMMENT '站点web服务ip',
  `algo_ip` varchar(256) NOT NULL COMMENT '站点算法服务ip',
  `web_port` varchar(32) NOT NULL COMMENT '站点web服务端口',
  `algo_port` varchar(32) NOT NULL COMMENT '站点算法服务端口',
  `party_id` varchar(128) NOT NULL COMMENT 'party_id',
  `role` varchar(256) NOT NULL COMMENT '角色(host，guest，master)',
  `status` tinyint(4) DEFAULT 1 COMMENT '状态（1：可使用，2:已删除，3：未激活）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='站点信息表';

CREATE TABLE `fs_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(64) NOT NULL COMMENT '唯一编号',
  `name` varchar(256) NOT NULL COMMENT '名称',
  `description` varchar(512) DEFAULT '' COMMENT '描述',
  `file_name` varchar(256) NOT NULL COMMENT '文件名称',
  `file_upload_name` varchar(256) NOT NULL COMMENT '文件上传名称',
  `local_url` varchar(512) NOT NULL COMMENT '本地上传路径',
  `field` varchar(512) DEFAULT '' COMMENT '字段',
  `party_id` varchar(256) NOT NULL COMMENT 'party_id',
  `site_id` varchar(256) NOT NULL COMMENT '站点id',
  `site_name` varchar(256) NOT NULL COMMENT '站点名称',
  `sample_num` bigint(20) DEFAULT 0  COMMENT '样本数量',
  `job_id` varchar(256) DEFAULT '' COMMENT 'jobId',
  `job_dsl_path` varchar(256) DEFAULT '' COMMENT 'jobDslPath',
  `conf_path` varchar(256) DEFAULT '' COMMENT 'confPath',
  `board_url` varchar(256) DEFAULT '' COMMENT 'boardUrl',
  `namespace` varchar(512) DEFAULT '' COMMENT '数据库名',
  `table_name` varchar(256) DEFAULT '' COMMENT '表名',
  `status` tinyint(4) DEFAULT 1 COMMENT '状态（1：已上传，2:未上传，3：已删除）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `udx_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='数据集信息表';

CREATE TABLE `fs_task` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `task_code` varchar(20) DEFAULT NULL COMMENT '任务编码',
  `task_name` varchar(50) NOT NULL COMMENT '任务名称',
  `task_desc` varchar(128) NOT NULL COMMENT '任务描述',
  `task_type` varchar(20) NOT NULL COMMENT '任务类型(INTERSECTION：联邦求交，MODELING：联邦建模，FORECAST:联邦预测)',
  `site_name` varchar(50) NOT NULL COMMENT '配置站点名称',
  `site_id` bigint(20) NOT NULL COMMENT '合作站点ID',
  `local_site_id` bigint(20) DEFAULT NULL COMMENT '本地站点ID',
  `local_site_name` varchar(50) DEFAULT NULL COMMENT '本地站点名称',
  `namespace` varchar(50) DEFAULT NULL COMMENT '合作方库名',
  `table_name` varchar(50) NOT NULL COMMENT '合作站点数据表名称',
  `local_namespace` varchar(50) DEFAULT NULL COMMENT '我方库名',
  `local_table_name` varchar(50) NOT NULL COMMENT '我方数据表名称',
  `config` text NOT NULL COMMENT '建模配置，JSON格式，根据不同的任务类型，配置分别不同',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `local_party_id` varchar(50) DEFAULT NULL COMMENT '本地站点partyID',
  `party_id` varchar(50) DEFAULT NULL COMMENT '合作站点partyID',
  `start_time` timestamp NULL DEFAULT NULL COMMENT '任务开始时间',
  `complete_time` timestamp NULL DEFAULT NULL COMMENT '任务完成时间',
  `state` varchar(20) DEFAULT 'CREATE' COMMENT '任务状态CREATE,SUBMIT,RUNNING,SUCCESS,FAIL，CANCELED',
  `result` text COMMENT '任务执行结果',
  `job_id` varchar(50) DEFAULT NULL COMMENT '算法的任务ID',
  `conf` text COMMENT 'conf参数',
  `dsl` text COMMENT 'dsl参数',
  `report_state` int(2) DEFAULT '0' COMMENT '是否上报管理端0，未上报，1上报中，2上报成功，3上报失败',
  `data_count` int(11) DEFAULT NULL COMMENT '合作方数据量',
  `local_data_count` int(11) DEFAULT NULL COMMENT '我放表数据量',
  `data_name` varchar(255) DEFAULT NULL COMMENT '合作方表名称',
  `local_data_name` varchar(255) DEFAULT NULL COMMENT '我方表名称',
  `submit_result` text COMMENT '任务提交到算法返回的结果',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='联邦任务信息';

CREATE TABLE `fs_model` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `code` varchar(50) DEFAULT NULL COMMENT '模型编码',
  `name` varchar(50) DEFAULT NULL COMMENT '模型名称',
  `evaluation_info` text COMMENT '模型评估指标',
  `task_id` varchar(20) DEFAULT NULL COMMENT '任务ID',
  `task_name` varchar(50) DEFAULT NULL COMMENT '任务名称',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_delete` tinyint(1) DEFAULT '0' COMMENT '0未删除，1删除',
  `model_id` varchar(255) DEFAULT NULL,
  `model_version` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='模型信息表';



