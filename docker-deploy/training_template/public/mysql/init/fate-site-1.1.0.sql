use fate_site;

ALTER TABLE fs_task ADD `ascription_type` VARCHAR(20) DEFAULT 'ENTERPRISE' COMMENT '归属类型 ENTERPRISE(企业), PROJECT(项目)';
ALTER TABLE fs_task ADD `is_delete` tinyint(1) DEFAULT '0' COMMENT '0未删除，1删除';
ALTER TABLE fs_task ADD `project_code` VARCHAR(32)  COMMENT '项目编号';
ALTER TABLE fs_task MODIFY `task_code` VARCHAR(32) COMMENT '任务编号';
ALTER TABLE fs_task ADD site_code VARCHAR(32)  COMMENT '配合站点编号';
ALTER TABLE fs_task ADD local_site_code VARCHAR(32) COMMENT '本地站点编号';

ALTER TABLE fs_model ADD task_code VARCHAR(32) COMMENT '任务编号';
ALTER TABLE fs_model ADD `ascription_type` VARCHAR(20) DEFAULT 'ENTERPRISE' COMMENT '归属类型 ENTERPRISE(企业), PROJECT(项目)';
ALTER TABLE fs_model ADD `project_code` VARCHAR(32)  COMMENT '项目编号';
ALTER TABLE fs_model ADD `algorithm_type` VARCHAR(255) COMMENT '算法类型';
ALTER TABLE fs_model ADD `last_use_time` TIMESTAMP  NULL COMMENT '最后一次调用时间';

CREATE UNIQUE INDEX idx_model_code ON fs_model(`project_code`,`code`);

CREATE UNIQUE INDEX idx_task_code ON fs_task(`project_code`,task_code);

CREATE TABLE `fs_project` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `code` varchar(32) NOT NULL COMMENT '项目编号',
  `name` varchar(255) DEFAULT NULL COMMENT '项目名称',
  `description` varchar(255) DEFAULT NULL COMMENT '项目简介',
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户id',
  `ip` varchar(20) DEFAULT NULL COMMENT '创建项目站点的ip',
  `user_name` varchar(20) DEFAULT NULL COMMENT '创建项目的用户名',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '项目创建时间',
  `role` varchar(20) DEFAULT 'MASTER' COMMENT 'MASTER 创建着 SLAVE参与着',
  `state` varchar(20) DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_delete` tinyint(1) DEFAULT '0' COMMENT '0未删除，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  COMMENT='项目信息表';

CREATE UNIQUE INDEX idx_project_code ON fs_project(code);

CREATE TABLE `fs_sync_data_queue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `request_id` varchar(32) DEFAULT NULL COMMENT '每次请求唯一的id',
  `create_time` timestamp  NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `method` varchar(20) DEFAULT 'POST' COMMENT 'POST,GET',
  `sync_type` varchar(255) DEFAULT NULL COMMENT '代表同步那种类型的数据',
  `url` varchar(255) DEFAULT NULL COMMENT 'url',
  `content` text COMMENT '同步的内容',
  `state` varchar(10) DEFAULT NULL COMMENT 'SUCCESS,FAIL,IN_SYNC,WAIT',
  `last_retry_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次重试时间',
  `retry` int(11) DEFAULT '0' COMMENT '重试失败的次数',
  `ip` varchar(20) DEFAULT NULL COMMENT 'ip',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

CREATE UNIQUE INDEX idx_request_id ON fs_sync_data_queue(request_id);

CREATE TABLE `fs_project_site` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(64) NOT NULL COMMENT '唯一编号',
  `pcode` varchar(64) NOT NULL COMMENT '项目唯一编号',
  `name` varchar(256) NOT NULL COMMENT '站点名称',
  `web_ip` varchar(256) NOT NULL COMMENT '站点web服务ip',
  `algo_ip` varchar(256) NOT NULL COMMENT '站点算法服务ip',
  `web_port` varchar(32) NOT NULL COMMENT '站点web服务端口',
  `algo_port` varchar(32) NOT NULL COMMENT '站点算法服务端口',
  `party_id` varchar(128) NOT NULL COMMENT 'party_id',
  `role` varchar(256) NOT NULL COMMENT '角色(host，guest)',
  `master` tinyint(4) NOT NULL COMMENT '是否项目创建者(1:项目创建者，2：非项目创建者)',
  `status` tinyint(4) DEFAULT 1 COMMENT '状态（1：可使用，2:已删除，3：未激活）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='项目成员信息表';


CREATE TABLE `fs_project_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(64) NOT NULL COMMENT '唯一编号',
  `pcode` varchar(64) NOT NULL COMMENT '项目唯一编号',
  `dcode` varchar(64) NOT NULL COMMENT '数据编号',
  `dname` varchar(256) DEFAULT '' COMMENT '数据名称',
  `pmcode` varchar(64) NOT NULL COMMENT '成员编号',
  `pmname` varchar(256) DEFAULT '' COMMENT '成员名称',
  `provider` varchar(256) NOT NULL COMMENT '数据提供方ip',
  `party_id` varchar(256) NOT NULL COMMENT '数据提供方partyId',
  `status` tinyint(4) DEFAULT 1 COMMENT '状态（1：已加入合作，2:已退出合作）',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `udx_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='项目合作数据表';

CREATE TABLE `fs_authentication` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'PK，验证码记录表和扫码登录表的ticket',
  `type` tinyint NOT NULL COMMENT '认证类型',
  `user_id` bigint DEFAULT NULL COMMENT '认证的用户ID',
  `created_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间',
  `expired_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '认证过期时间',
  `status` tinyint NOT NULL COMMENT '认证状态：0-未认证，1-已认证，2-已使用',
  `salt` bigint NOT NULL COMMENT '盐值，随机数，防止认证伪造，非实际验证码',
  `authentication_info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '验证的信息，根据type存储电话号码或邮箱',
  `code` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '验证码',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_type_authinfo_expire` (`type`,`authentication_info`,`expired_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='认证ticket表';

CREATE TABLE `fs_login_fail_count` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `failed_count` tinyint DEFAULT '1',
  `max_allowed_count` tinyint DEFAULT '5',
  `modified_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `expire_seconds` int DEFAULT '1800',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  KEY `modified_time_idx` (`modified_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `fs_sso_jwt` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'PK',
  `jwt` varchar(2048) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'jwt信息',
  `user_id` bigint NOT NULL COMMENT '登录的用户ID',
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '对应的用户昵称',
  `created_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间',
  `expired_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '认证过期时间',
  `status` tinyint NOT NULL COMMENT '状态(备用)：0-已登录',
  `authentication_level` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户认证登记',
  `login_ip` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '登录IP',
  `digest` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'md5(jwt)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `fs_user_account` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'PK（10位，从1000000000开始递增）',
  `nickname` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户昵称',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '密码(MD5)',
  `status` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'enable' COMMENT '用户状态：正常、注销、禁用等',
  `created_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间',
  `modified_time` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '修改时间',
  `password_modified_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '密码修改时间',
  `deregistration_mark` tinyint DEFAULT NULL,
  `parent_id` bigint DEFAULT '0' COMMENT '父节点ID',
  `last_login_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上次登陆时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nick_name` (`nickname`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=1000000001 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='用户基础信息表';

INSERT INTO `fs_user_account` (`nickname`, `password`) VALUES ('admin', '0::962B168E58E6166C3700A1F8EEF6D5FF::74D085542B25EDAD68639E5000273638');