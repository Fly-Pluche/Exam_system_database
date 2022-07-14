DROP TABLE IF EXISTS `account_profile`;
CREATE TABLE `account_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `uid` varchar(22) DEFAULT NULL,
  `user_src` int(11) NOT NULL,
  `user_status` int(11) NOT NULL,
  `unionid` varchar(32) DEFAULT NULL,
  `openid` varchar(32) DEFAULT NULL,
  `wxid` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `sex` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `nickname` varchar(32) DEFAULT NULL,
  `avatar` varchar(60) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `country` varchar(32) DEFAULT NULL,
  `province` varchar(32) DEFAULT NULL,
  `city` varchar(32) DEFAULT NULL,
  `location` varchar(60) DEFAULT NULL,
  `is_upgrade` int(11) NOT NULL,
  `upgrade_time` datetime(6) DEFAULT NULL,
  `expire_time` datetime(6) DEFAULT NULL,
  `upgrade_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  UNIQUE KEY `account_profile_name_email_52e79ff2_uniq` (`name`,`email`),
  KEY `account_profile_status_cef42cf5` (`status`),
  KEY `account_profile_user_src_28c2847b` (`user_src`),
  KEY `account_profile_unionid_1021e9fa` (`unionid`),
  KEY `account_profile_openid_06478752` (`openid`),
  KEY `account_profile_name_13db32ec` (`name`),
  KEY `account_profile_email_df723ccb` (`email`),
  KEY `account_profile_phone_923990b3` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `account_userinfo`;
CREATE TABLE `account_userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `kind_id` varchar(32) DEFAULT NULL,
  `uid` varchar(32) DEFAULT NULL,
  `name` varchar(24) DEFAULT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `wxid` varchar(24) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `pid` varchar(18) DEFAULT NULL,
  `graduated_from` varchar(60) DEFAULT NULL,
  `address` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_userinfo_kind_id_uid_5acd2411_uniq` (`kind_id`,`uid`),
  KEY `account_userinfo_status_5adcd90c` (`status`),
  KEY `account_userinfo_kind_id_e4d2497b` (`kind_id`),
  KEY `account_userinfo_uid_c2ca5208` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `business_appconfiginfo`;
CREATE TABLE `business_appconfiginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `app_id` varchar(32) NOT NULL,
  `app_name` varchar(40) DEFAULT NULL,
  `rule_text` longtext,
  `is_show_userinfo` tinyint(1) NOT NULL,
  `userinfo_fields` varchar(128) DEFAULT NULL,
  `option_fields` varchar(128) DEFAULT NULL,
  `userinfo_field_names` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `business_appconfiginfo_status_23f940ab` (`status`),
  KEY `business_appconfiginfo_app_id_2366db42` (`app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `business_businessaccountinfo`;
CREATE TABLE `business_businessaccountinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `account_id` varchar(22) NOT NULL,
  `email` varchar(40) DEFAULT NULL,
  `company_name` varchar(60) DEFAULT NULL,
  `company_description` longtext,
  `company_username` varchar(32) DEFAULT NULL,
  `company_phone` varchar(16) DEFAULT NULL,
  `company_location` longtext,
  `company_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `business_businessaccountinfo_status_09dd4294` (`status`),
  KEY `business_businessaccountinfo_account_id_00a2690c` (`account_id`),
  KEY `business_businessaccountinfo_company_phone_01c42098` (`company_phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `business_businessappinfo`;
CREATE TABLE `business_businessappinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `account_id` varchar(32) NOT NULL,
  `app_id` varchar(22) NOT NULL,
  `app_name` varchar(40) DEFAULT NULL,
  `app_description` longtext,
  PRIMARY KEY (`id`),
  KEY `business_businessappinfo_status_c6858221` (`status`),
  KEY `business_businessappinfo_account_id_15798b98` (`account_id`),
  KEY `business_businessappinfo_app_id_7385168b` (`app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `business_userinfoimage`;
CREATE TABLE `business_userinfoimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `uii_name` varchar(32) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `sex` varchar(60) DEFAULT NULL,
  `age` varchar(60) DEFAULT NULL,
  `phone` varchar(60) DEFAULT NULL,
  `wxid` varchar(60) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `pid` varchar(60) DEFAULT NULL,
  `graduated_from` varchar(60) DEFAULT NULL,
  `address` varchar(60) DEFAULT NULL,
  `resume` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `business_userinfoimage_status_7072fef4` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `business_userinforegex`;
CREATE TABLE `business_userinforegex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `field_name` varchar(16) DEFAULT NULL,
  `regex` varchar(40) DEFAULT NULL,
  `description` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_userinforegex_status_a2e28d05` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `competition_bankinfo`;
CREATE TABLE `competition_bankinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `bank_id` varchar(22) DEFAULT NULL,
  `choice_num` int(11) NOT NULL,
  `fillinblank_num` int(11) NOT NULL,
  `bank_type` int(11) NOT NULL,
  `kind_num` int(11) NOT NULL,
  `partin_num` int(11) NOT NULL,
  `bank_name` varchar(40) DEFAULT NULL,
  `uid` varchar(32) DEFAULT NULL,
  `account_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_bankinfo_status_528ddf4a` (`status`),
  KEY `competition_bankinfo_bank_id_87352246` (`bank_id`),
  KEY `competition_bankinfo_uid_b0d74e2a` (`uid`),
  KEY `competition_bankinfo_account_id_939bd8f3` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `competition_choiceinfo`;
CREATE TABLE `competition_choiceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `audio_url` varchar(255) DEFAULT NULL,
  `audio_time` int(11) NOT NULL,
  `bank_id` varchar(32) DEFAULT NULL,
  `ctype` int(11) NOT NULL,
  `question` varchar(255) DEFAULT NULL,
  `answer` varchar(255) DEFAULT NULL,
  `item1` varchar(255) DEFAULT NULL,
  `item2` varchar(255) DEFAULT NULL,
  `item3` varchar(255) DEFAULT NULL,
  `item4` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_choiceinfo_status_dd6aa9e9` (`status`),
  KEY `competition_choiceinfo_bank_id_019a8691` (`bank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=268 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `competition_competitionkindinfo`;
CREATE TABLE `competition_competitionkindinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `kind_id` varchar(22) DEFAULT NULL,
  `account_id` varchar(32) DEFAULT NULL,
  `app_id` varchar(32) DEFAULT NULL,
  `bank_id` varchar(32) DEFAULT NULL,
  `kind_type` int(11) NOT NULL,
  `kind_name` varchar(32) DEFAULT NULL,
  `sponsor_name` varchar(60) DEFAULT NULL,
  `total_score` int(11) NOT NULL,
  `question_num` int(11) NOT NULL,
  `cop_startat` datetime(6) NOT NULL,
  `period_time` int(11) NOT NULL,
  `cop_finishat` datetime(6) DEFAULT NULL,
  `total_partin_num` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_competitionkindinfo_status_481c1948` (`status`),
  KEY `competition_competitionkindinfo_kind_id_6389e9c2` (`kind_id`),
  KEY `competition_competitionkindinfo_account_id_efc0a359` (`account_id`),
  KEY `competition_competitionkindinfo_app_id_78c25478` (`app_id`),
  KEY `competition_competitionkindinfo_bank_id_f8a0ba8c` (`bank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `competition_competitionqainfo`;
CREATE TABLE `competition_competitionqainfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `kind_id` varchar(32) DEFAULT NULL,
  `qa_id` varchar(22) DEFAULT NULL,
  `uid` varchar(32) DEFAULT NULL,
  `qsrecord` longtext,
  `asrecord` longtext,
  `aslogrecord` longtext,
  `started_stamp` bigint(20) NOT NULL,
  `finished_stamp` bigint(20) NOT NULL,
  `expend_time` int(11) NOT NULL,
  `started` tinyint(1) NOT NULL,
  `finished` tinyint(1) NOT NULL,
  `correct_num` int(11) NOT NULL,
  `incorrect_num` int(11) NOT NULL,
  `total_num` int(11) NOT NULL,
  `score` double NOT NULL,
  `correct_list` varchar(10000) DEFAULT NULL,
  `wrong_list` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_competitionqainfo_kind_id_10b82c49` (`kind_id`),
  KEY `competition_competitionqainfo_qa_id_3e2673ba` (`qa_id`),
  KEY `competition_competitionqainfo_uid_d8905edc` (`uid`),
  KEY `competition_competitionqainfo_started_f1ffb449` (`started`),
  KEY `competition_competitionqainfo_finished_b77ac7ad` (`finished`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `competition_fillinblankinfo`;
CREATE TABLE `competition_fillinblankinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `audio_url` varchar(255) DEFAULT NULL,
  `audio_time` int(11) NOT NULL,
  `bank_id` varchar(32) DEFAULT NULL,
  `ctype` int(11) NOT NULL,
  `question` varchar(255) DEFAULT NULL,
  `answer` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_fillinblankinfo_status_903a1b01` (`status`),
  KEY `competition_fillinblankinfo_bank_id_c7404b1d` (`bank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

