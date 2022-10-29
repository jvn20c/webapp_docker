CREATE DATABASE vsearchlogDB;
use vsearchlogDB;

CREATE TABLE `log` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `ts` timestamp default current_timestamp,
  `phrase` varchar(128) NOT NULL,
  `letters` varchar(32) NOT NULL,
  `ip` varchar(16) NOT NULL,
  `browser_string` varchar(256),
  `results` varchar(64) NOT NULL );

--  TIREI O NÃO NULO DO browser_string para fazer a parada funcionar kkkj
--   `browser_string` varchar(256) NOT NULL,

-- insert  into `log`(`phrase`,`letters`,`ip`,`browser_string`,`results`) values ('galaxy','xyz', '127.0.0.1', 'Opera', "{'x', 'y'}");