
# SQL

> SQL——基本SQL和扩展SQL。这部分比较适合出填空题和判断题，SQL语句嘛。所以主要考察大家像create table这样的语句，这里要注意数据类型——数字型还是什么，数据的类型；还有一直在强调的约束条件、完备性约束；还有key，比如主码、超码、候选码、外码，很关键，包括foreign key可能会有一些级联操作，像cascade等；还有授权、权限设置。这些知识点大家要注意。对于SQL语句，比较容易出判断和填空。判断题经常尤其涉及聚合函数，大家一定要注意，这里很容易出判断题。聚合函数包括count、max、min、average、sum，就是求平均、求和、求最大、求最小、求个数。这些里面有一些注意点。还有，比如假设给你一个查询请求以及一个写好的SQL语句，要你判断SQL语句中某部分写得对不对——相当于需求告诉你，SQL语句也写好，但里面有正确有错误。这些SQL语句包括from、where、group by（涉及聚合函数的分组）、order by排序等，你要判断这些关键字怎么用，要注意什么，实现什么功能，要学会判断。所以难度已经降了不少，不要求你写，只要求你看得懂，根据需求判断哪个对哪个错，包括聚合函数的也要会判断。OK，这就是SQL语句主要知识点。

第3章：SQL 介绍

本章主要讲授SQL的核心基础语法，涵盖数据定义、基本查询、集合运算、聚集以及子查询。

1. **数据定义语言（DDL）基础**
   - **基本类型**：`char(n)`, `varchar(n)`, `int`, `numeric(p,d)`, `real`, `double precision` 等。
   - **模式定义**：使用 `create table` 创建关系，定义属性及约束（`primary key` 主码、`foreign key...references` 外码、`not null` 非空约束）。
   - **表修改与删除**：`drop table` 删除表，`alter table...add/drop` 增加或删除属性。

2. **查询的基本结构**
   - **单表查询**：`select...from...where` 子句，使用 `distinct` 去重，`all` 保留重复。
   - **多表查询**：通过 `from` 子句生成笛卡尔积，并用 `where` 指定连接条件（如 `instructor.ID = teaches.ID`）。
   - **算术表达式**：在 `select` 中使用 `+ - * /`。

3. **附加基本运算**
   - **更名运算**：使用 `as` 为属性或关系重命名（表别名/元组变量）。
   - **字符串运算**：使用 `like` 进行模式匹配（`%` 匹配任意子串，`_` 匹配单个字符），转义字符 `escape`。
   - **排序**：`order by` 配合 `asc`/`desc` 对结果排序。
   - **谓词**：`between...and...` 范围比较，行构造器 `(v1, v2, ...)` 用于元组比较。

4. **集合运算**
   - 并（`union` / `union all`）、交（`intersect` / `intersect all`）、差（`except` / `except all`）。

5. **空值处理**
   - 使用 `is null` / `is not null` 测试空值。
   - 涉及空值的比较结果为 `unknown`，以及 `and`/`or`/`not` 对 `unknown` 的逻辑处理。

6. **聚集函数与分组**
   - 固有聚集函数：`avg`, `min`, `max`, `sum`, `count`。
   - 使用 `group by` 进行分组聚集。
   - 使用 `having` 对分组进行条件筛选（在分组后应用谓词）。

7. **嵌套子查询**
   - **集合成员资格**：`in` / `not in`。
   - **集合比较**：`> some` / `> all` 等（与子查询返回的集合比较）。
   - **空关系测试**：`exists` / `not exists`（相关子查询）。
   - **重复元组测试**：`unique` / `not unique`。
   - **from 子句中的子查询**：将子查询结果作为派生表，可使用 `lateral` 访问同层前面表的属性。
   - **with 子句**：定义临时视图，提高查询可读性和复用性。
   - **标量子查询**：返回单个值的子查询，可出现在 `select`、`where` 等期望单值的地方。

8. **数据库修改**
   - **删除**：`delete from...where`。
   - **插入**：`insert into...values` 或 `insert into...select`。
   - **更新**：`update...set...where`，以及使用 `case` 结构进行条件更新。

第4章：中级 SQL

本章在基础之上，重点讲授更复杂的查询表达（连接）、视图、事务、完整性约束、数据类型扩展、索引以及权限管理。

1. **连接表达式**
   - **自然连接**：`natural join`（自动在相同属性名上等值连接）。
   - **using 子句连接**：`join...using (属性列表)`，指定等值匹配的属性。
   - **on 子句连接**：`join...on <谓词>`，可指定任意连接条件。
   - **外连接**：左外连接（`left outer join`）、右外连接（`right outer join`）、全外连接（`full outer join`），保留未匹配元组并补空值。
   - **连接类型与条件组合**：内连接（`inner join`）与外连接，结合自然、using 或 on。

2. **视图**
   - **视图定义**：`create view...as <查询表达式>`，创建虚拟关系。
   - **视图使用**：在查询中直接使用视图名。
   - **物化视图**：存储视图结果并自动维护（`materialized view`）。
   - **视图更新**：可更新视图的条件，以及 `with check option` 确保插入/更新满足视图条件。

3. **事务**
   - 事务概念：`commit work`（提交）和 `rollback work`（回滚）。
   - 原子性：事务要么全部执行，要么全部撤销。

4. **完整性约束**
   - **单关系约束**：`not null`、`unique`、`check (<谓词>)`。
   - **引用完整性**：`foreign key...references`，并指定 `on delete cascade` / `on update cascade` 级联操作。
   - **约束命名**：使用 `constraint <名称>` 命名约束，便于 `alter table...drop constraint` 删除。
   - **延迟约束**：`initially deferred` 允许事务结束才检查约束。
   - **复杂 check 与断言**：`create assertion` 定义全局谓词约束（尽管多数系统未实现）。

5. **数据类型与模式**
   - **日期/时间类型**：`date`, `time`, `timestamp`，提取域（`extract`）和当前时间函数。
   - **类型转换与格式化**：`cast(e as t)` 转换类型，`coalesce` 返回第一个非空值。
   - **缺省值**：`default <值>`。
   - **大对象类型**：`clob`（字符大对象）和 `blob`（二进制大对象）。
   - **用户自定义类型**：`create type`（独特类型，强类型）和 `create domain`（域，可加约束）。
   - **自动生成唯一码**：`generated always as identity`（或 `serial`, `auto_increment`）及 `create sequence`。
   - **表创建扩展**：`create table...like`（复制模式）和 `create table...as`（复制查询结果）。
   - **模式与目录**：三层命名空间（目录.模式.关系）。

6. **索引定义**
   - 创建索引：`create index <索引名> on <关系名>(<属性列表>)`。
   - 唯一索引：`create unique index`。
   - 删除索引：`drop index <索引名>`。

7. **授权**
   - **权限类型**：`select`, `insert`, `update`, `delete`, `references`（引用权限），`all privileges`。
   - **授予权限**：`grant <权限> on <对象> to <用户/角色>`。
   - **收回权限**：`revoke <权限> on <对象> from <用户/角色>`。
   - **角色**：`create role`，将权限授予角色，再将角色授予用户（权限继承）。
   - **视图授权**：通过视图限制用户对底层数据的访问。
   - **权限转移**：`with grant option` 允许被授权者继续授权。
   - **级联收回**：收权时默认级联（`cascade`），可用 `restrict` 限制。
   - **行级授权**：通过虚拟私有数据库（VPD）添加行级谓词。

第5章：高级 SQL

本章主要讲授SQL与程序语言的交互、存储过程/函数、触发器、递归查询以及面向数据分析的高级聚集特性。

1. **使用程序设计语言访问 SQL**
   - **JDBC（Java）**：连接数据库（`DriverManager`）、执行语句（`Statement` / `PreparedStatement`）、处理结果集（`ResultSet`）、元数据（`DatabaseMetaData`）、事务控制（`setAutoCommit`, `commit`, `rollback`）、大对象处理（`getBlob`/`setBlob`）。
   - **Python 访问**：使用 `psycopg2` 等驱动程序，执行带参数查询，提交/回滚。
   - **ODBC（C/C++等）**：分配环境/连接句柄（`SQLAllocEnv`/`SQLAllocConnect`），执行 SQL（`SQLExecDirect`），绑定变量（`SQLBindCol`），获取结果（`SQLFetch`）。
   - **嵌入式 SQL**：使用预处理器（`EXEC SQL`）将 SQL 嵌入宿主语言（如C），使用游标遍历结果。

2. **函数和过程**
   - **SQL 函数**：`create function...returns...`，可返回标量值或表（表函数）。
   - **SQL 过程**：`create procedure...`，使用 `in`/`out` 参数。
   - **过程化语言结构（PSM）**：变量声明（`declare`）、赋值（`set`）、复合语句（`begin...end`）、循环（`while`, `repeat`, `for`）、条件判断（`if...then...else`, `case`）、异常处理（`declare handler`）。
   - **外部语言例程**：用 Java/C/C++ 等定义函数，在数据库沙盒中执行。

3. **触发器**
   - 触发时机：`before` / `after` 插入、删除、更新（可指定特定属性）。
   - 触发粒度：`for each row`（行级）或 `for each statement`（语句级）。
   - 过渡变量：`referencing new row as` / `old row as`，以及过渡表（`old table`/`new table`）。
   - 触发动作：使用 `when` 条件，执行 `begin...end` 中的操作（可回滚或修改数据）。
   - 触发器的禁用/启用与删除：`alter trigger...disable` / `drop trigger`。
   - 何时不用触发器：可以用级联删除、物化视图或存储过程替代的场景。

4. **递归查询**
   - **迭代方法**：使用临时表和循环（如 `repeat...until`）计算传递闭包。
   - **递归 SQL**：使用 `with recursive` 定义递归视图，包含基查询（非递归部分）和递归查询（使用自身），通过不动点迭代计算。
   - **单调性要求**：递归查询必须是单调的，禁止在递归视图上使用聚集、`not exists` 或 `except`。

5. **高级聚集特性**
   - **排名函数**：`rank()`、`dense_rank()`、`percent_rank()`、`cume_dist()`、`row_number()`，配合 `over (partition by... order by...)` 进行分区内排名。
   - **分窗（窗口函数）**：使用 `over` 子句定义窗口，支持 `rows` / `range` 指定前/后行范围（如 `rows between 3 preceding and 2 following`），计算移动平均等。
   - **旋转（Pivot）**：使用 `pivot` 子句将行属性值转换为列（交叉表/数据透视表）。
   - **上卷与立方体**：`group by rollup(...)` 生成分组层次（所有前缀组合），`group by cube(...)` 生成所有属性子集组合。配合 `grouping sets` 可自定义分组列表，并使用 `grouping()` 函数区分空值来源。



# ER模型
> 第二，ER模型。ER模型相对比较容易出选择题。ER模型里要了解实体与实体之间的关系——一对一、一对多、多对一、多对多。还有各种属性类型，尤其要注意派生属性,导出的属性和多值属性。这些属性类型需要注意。还有弱实体，对应的强实体。实体之间有关系，还有全参与和部分参与——全参与就是整个实体集合中的所有值都包含在关系里；部分参与则只有部分。比如把我们班所有同学都归到某一项任务，就是全参与；如果只有部分同学，就是部分参与。还有ER模型到关系模式的转换，有些关系不需要转成一张表，比如弱实体可以合并到它所对应的宿主实体那里去。这种题目，比如给定一个例子，要你选择属于哪种关系或实体，这些知识点不难，掌握了选择题很好选。


- 实体间关系
  - 一对一：实体集 A 中的一个实体至多与实体集 B 中的一个实体相关联，且 B 中的一个实体也至多与 A 中的一个实体相关联。
  - 一对多：实体集 A 中的一个实体可与 B 中任意数量的实体相关联，而 B 中的一个实体至多与 A 中的一个实体相关联。
  - 多对一：实体集 A 中的一个实体至多与 B 中的一个实体相关联，而 B 中的一个实体可与 A 中任意数量的实体相关联。
  - 多对多：实体集 A 中的一个实体可与 B 中任意数量的实体相关联，且 B 中的一个实体也可与 A 中任意数量的实体相关联。
  - many就是不唯一的那个；ER图中箭头朝向many的那一个

- 属性类型：
  - **简单属性（Simple Attribute）：不能进一步划分为子部分的属性。** 例如，性别（sex）、课程号（course_id）。
  - **复合属性（Composite Attribute）：可以被划分为若干子部分（即其他属性）的属性。** 例如，姓名（name）可划分为名（first_name）、中间名首字母（middle_initial）和姓（last_name）；地址（address）可细分为街道（street）、城市（city）、州（state）、邮政编码（postal_code），其中街道还可继续细分为街道号、街道名和公寓号。
  
  - **单值属性（Single-valued Attribute）：对某个特定实体而言，该属性只对应单独的一个值。** 例如，学生ID（student_ID）对于一个学生实体只有一个值。
  - **多值属性（Multivalued Attribute）：对某个特定实体而言，该属性可以对应一组值（零个、一个或多个）。** 例如，教师的电话号码（phone_number），一位教师可能有多个电话号码。
  - **派生属性（Derived Attribute）：该属性的值可以从其他相关属性或实体的值计算得出，通常不存储在数据库中，而是在需要时动态计算出来。** 例如，年龄（age）可以从出生日期（date_of_birth）计算得出。
  
- 弱实体与强实体
  - **强实体集（Strong Entity Set）：拥有足够的属性来构成主码（Primary Key），从而能够唯一标识每一个实体的实体集。** 例如，课程（course）实体集具有主码 course_id，可以独立标识每一门课程；贷款（loan）实体集具有主码 loan_number，可以独立标识每一笔贷款。
  - **弱实体集（Weak Entity Set）：不具有足够属性来形成主码的实体集，其存在必须依赖于另一个实体集（称为标识性实体集或属主实体集）。** 例如，课程段（section）实体集仅凭 sec_id、semester、year 无法在全库范围唯一标识，因为不同课程可能拥有相同的课程段编号，必须依赖于课程（course）实体集才能唯一区分；又如还款记录（payment）依赖于贷款（loan），仅凭 payment_number 无法在全库唯一标识。
  
  - **分辨符（Discriminator / Partial Key）：弱实体集中用于区分依赖于同一个强实体集的不同实体的属性集合。** 例如，section 的分辨符是 {sec_id, semester, year}；payment 的分辨符是 payment_number。
  
  - **主码构成：弱实体集的主码由标识性实体集的主码加上该弱实体集的分辨符共同组成。** 例如，section 的主码为 (course_id, sec_id, semester, year)；payment 的主码为 (loan_number, payment_number)。
  
  - **标识性联系（Identifying Relationship）：连接弱实体集与其标识性实体集的多对一联系，且弱实体集在该联系中的参与必须是全部的（即每个弱实体都必须与一个强实体相关联）。** 例如，sec_course 联系将 section 与 course 关联；loan-payment 联系将 payment 与 loan 关联。
  
  - **E-R图表示：弱实体集用双边框矩形表示，分辨符属性加虚下划线，标识性联系用双边框菱形表示。**

  - 参与约束
    - 如果实体集 E 中的每个实体都必须参与到联系集 R 中的至少一个联系中，那么实体集 E 在联系集 R 中的参与就被称为是全部的。如果 E 中一些实体可能不参与到 R 的联系中，那么实体集 E 在联系集 R 中的参与就被称为是部分的。
    - 全参与：每个实体都有人连着
    - “映射基数”：1:M, 1:1, M:N这种

  - ER模型到关系模式的转换
  - 


# 