# fate-site version 0.4
use fate_site;
CREATE TABLE `fs_task_arbiter_site` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_code` varchar(50) DEFAULT NULL COMMENT '项目编号',
  `task_code` varchar(50) DEFAULT NULL COMMENT '任务编号',
  `party_id` varchar(32) DEFAULT NULL COMMENT 'partyId',
  `site_code` varchar(50) DEFAULT NULL COMMENT '站点编号',
  `table_name` varchar(225) DEFAULT NULL COMMENT '表名称',
  `namespace` varchar(225) DEFAULT NULL COMMENT 'namespace',
  `data_code` varchar(100) DEFAULT NULL COMMENT '数据编号',
  `data_name` varchar(100) DEFAULT NULL COMMENT '数据名称',
  `site_name` varchar(100) DEFAULT NULL COMMENT '站点名称',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务验证数据集信息';




CREATE TABLE `fs_data_access` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `site_id` bigint NOT NULL COMMENT '站点id',
  `name` varchar(200) NOT NULL COMMENT '名称',
  `description` varchar(200) NOT NULL COMMENT '描述',
  `address` varchar(50) NOT NULL COMMENT 'dataaccess的ip:port',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='在线数据的数据访问';

alter table fs_data add column id_type int;
alter table fs_data add column id_encrypt_type int;


alter table fs_task add column deploy_model_id varchar(255) comment '任务deploy后的模型id';
alter table fs_task add column deploy_model_version varchar(255) comment '任务deploy后的模型version';
