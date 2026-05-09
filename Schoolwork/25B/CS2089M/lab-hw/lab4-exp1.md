数据库系统原理实验报告
课程名称:数据库系统原理
专业:竺可桢学院工科平台
学号:3080030049 
姓名:王可宇
实验 4 SQL 安全性
实验目的：
1. 熟悉通过 SQL 进行数据完整性控制的方法。
实验平台：
1. 数据库管理系统：SQL Server 2000 或 MySQL 
实验内容和要求：
1. 建立表，考察表的生成者拥有该表的哪些权限。
2. 使用 SQL 的 grant 和 revoke 命令对其他用户进行授权和权力回收，考察相应的作
用。
3. 建立视图，并把该视图的查询权限授予其他用户，考察通过视图进行权限控制的作
用。
实验过程: 
建立表，考察表的生成者拥有该表的哪些权限
使用 SQL 的 grant 和 revoke 命令对其他用户进行授权和权力回收，考察相应的作用
GRANT SELECT on works to user001 
 REVOKE SELECT ON works FROM user001 
建立视图，并把该视图的查询权限授予其他用户，考察通过视图进行权限控制的作用
CREATE VIEW member 
AS 
 SELECT person_name,street 
 FROM employee 
 WHERE city='Hangzhou' 
GRANT SELECT ON member TO user001 