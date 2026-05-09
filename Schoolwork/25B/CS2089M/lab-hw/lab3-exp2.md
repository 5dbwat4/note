数据库系统实验三：SQL 数据完整性
一、实验目的
1. 熟悉通过 SQL 进行数据完整性控制的方法。
二、实验平台
1. 操作系统： Windows
2. 数据库管理系统：MySQL
三、实验内容
1. 主键、外键和 check 的定义
(1) 定义表 city_area(id, city_name, city_id)，其中 id 为主键。
(2) 在表中加入 city_area 字段（类型为 float）。
(3) 将 city_area 表中 city_id 设为 city_district 表中 city_id 的外键。
一个表可以设置多个外键。
(4) 查看 city_area 表的创建语句
我们可以看到下表
其中第二列的内容如下：
可以看到外键 c_id 被成功定义。
(5) 在表中加入 check 语句
2. 主键控制
进入 city_district 表，我们可以看到表中已经存在 17 条内容。
其中最左侧的 city_id 是表的主键。
(1) 主键重复
我们继续插入一条新的内容：
可以看到，新的内容中的主键为“17”，但是表中已经有名为“17”的主键了，
所以若按照此类插入则应该返回错误信息。我们来运行一下观察结果。
可以看到，MySQL 返回了一个报错，内容是主键“17”被重复定义。
(2) 主键为空
我们再来插入一条内容：
可以看到在这条内容中，主键 city_id 未定义，为空值。但是主键的内容一定
是非空的。这条语句同样会产生报错。
可以看到，MySQL 返回了一个报错，内容是 city_id 关键字没有默认值。
(3) 正确插入
最后，我们正确插入一条内容：
可以看到这条内容被成功插入。
3. on delete 语句
在创建了新表之后，city_area 表中的 city_id 字段被设为外键，引用自 city_district
表中的 city_id 字段。
现在在 city_area 中有如下的字段：
我们在引用表 city_district 中删除 city_id = 18 的行。
然而，city_area 中已经存在 city_id = 18 的行了，而 MySQL 在 ON DELETE 语句中
默认执行的是 RESTRICT 行为，即限制删除，所以此次删除是无法成功的。
可以看到，因为外键冲突，删除语句返回了报错。
4. on update 语句
同上，我们在引用表 city_district 中更新 city_id = 18 的行，将 city_id 改为 19。
同样地，MySQL 的 ON UPDATE 语句也会触发 RESTRICT 行为，即限制更新，所
以此次更新是无法成功的。
可以看到，因为外键冲突，更新语句返回了报错。
5. check 语句
我们在 city_area 表中插入这么一条数据：
可以看到，city_area 一栏的数据为 2，不满足 check 语句中要求 city_area ≥ 5 的
要求。所以这条指令将会报错。
可以看到，指令返回了错误信息。
6. trigger 的定义
定义一个触发器，当删除 city_district 中的数据后，同步删除 dis_name 中与
city_district 中 city_name 相同的记录。
这是原来的 dis_name 表。
现在我们将 city_district 中的第 5 行删除。第 5 行的 city_name 为“温州市”，有了
trigger 之后，这意味着 dis_name 中的第 16 行也应该被删除。
执行语句后，可以看到第 16 行被同步执行了删除命令。