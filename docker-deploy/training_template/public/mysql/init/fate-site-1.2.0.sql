# fate-site version 0.3
use fate_site;

ALTER TABLE fs_project ADD COLUMN audit_state TINYINT(1) DEFAULT 0 COMMENT '0未启用，1启用';

ALTER TABLE fs_task ADD COLUMN audit_state TINYINT(1) DEFAULT 0 COMMENT '是否开启审计,0未开启，1开启';
ALTER TABLE fs_task ADD COLUMN user_name VARCHAR(20) COMMENT "用户名";
ALTER TABLE fs_task ADD COLUMN user_id BIGINT(20) COMMENT "用户ID";

ALTER TABLE `fs_task` MODIFY task_name VARCHAR(128) NULL COMMENT '任务名称';
ALTER TABLE `fs_task` MODIFY task_desc VARCHAR(256) NULL COMMENT '任务描述';
ALTER TABLE fs_task MODIFY site_name VARCHAR(50) NULL COMMENT '合作方站点名称';
ALTER TABLE fs_task MODIFY table_name VARCHAR(50) NULL COMMENT '合作方数据表';
ALTER TABLE fs_task MODIFY task_desc VARCHAR(128)  NULL COMMENT '任务描述';
ALTER TABLE fs_task MODIFY task_type VARCHAR(20) NULL COMMENT '任务类型(INTERSECTION：联邦求交，MODELING：联邦建模，FORECAST:联邦预测)';
ALTER TABLE fs_task MODIFY site_id BIGINT(20) NULL COMMENT '合作站点ID';

ALTER TABLE fs_data ADD COLUMN total_count INT(11) COMMENT "数据总条数";
ALTER TABLE fs_data ADD COLUMN content TEXT COMMENT"部分数据内容（默认前十行）";
ALTER TABLE fs_data ADD COLUMN tag VARCHAR(20) DEFAULT 'y' COMMENT "标签页";
ALTER TABLE fs_data ADD COLUMN `column` VARCHAR(225) COMMENT "纬度";

ALTER TABLE fs_project_data ADD total_count INT(11) COMMENT "数据总条数";
ALTER TABLE fs_project_data ADD content TEXT COMMENT"部分数据内容（默认前十行）";
ALTER TABLE fs_project_data ADD  tag VARCHAR(20) DEFAULT 'y' COMMENT "标签页";
ALTER TABLE fs_project_data ADD  `column` VARCHAR(225) COMMENT "维度";

CREATE TABLE `fs_task_component` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_code` varchar(100) DEFAULT NULL COMMENT '项目名称',
  `task_code` varchar(100) DEFAULT NULL COMMENT '任务编号',
  `component_name` varchar(50) DEFAULT NULL COMMENT '模块名称',
  `state` varchar(30) DEFAULT NULL COMMENT '任务状态',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '开始时间',
  `end_time` timestamp  COMMENT '结束时间',
  `is_delete` tinyint(1) DEFAULT '0' COMMENT '0未删除，1删除',
  `order` int(11) DEFAULT NULL COMMENT 'conponent顺序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;




CREATE TABLE `fs_task_audit` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_code` varchar(50) DEFAULT NULL COMMENT '项目编号',
  `task_code` varchar(50) DEFAULT NULL COMMENT '任务编号',
  `site_code` VARCHAR(50) DEFAULT NULL COMMENT '站点编号',
  `audit_state` tinyint(4) DEFAULT NULL COMMENT '审计状态',
  `audit_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '审计时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(30) DEFAULT NULL COMMENT '审计人',
  `user_id` bigint(20) DEFAULT NULL COMMENT 'userId',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目任务审计详情';

CREATE UNIQUE  INDEX idx_pcode_tcode_scode ON fs_task_audit(project_code,task_code,site_code);



CREATE TABLE `fs_task_host_site` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务配合站点信息';

ALTER TABLE fs_project_data MODIFY content MEDIUMTEXT COMMENT '部分数据内容(默认前十行)';
ALTER TABLE fs_project_data MODIFY `column` MEDIUMTEXT COMMENT '部分数据内容(默认前十行)';
ALTER TABLE fs_data MODIFY content MEDIUMTEXT COMMENT '部分数据内容(默认前十行)';
ALTER TABLE fs_data MODIFY `column` MEDIUMTEXT COMMENT '部分数据内容(默认前十行)';
ALTER TABLE fs_task MODIFY `result` MEDIUMTEXT COMMENT '任务执行结果';