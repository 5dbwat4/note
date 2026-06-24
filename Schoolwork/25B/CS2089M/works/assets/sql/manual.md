# Lab 3 & Lab 4 录屏操作手册

## 整体流程

所有 SQL 文件在**同一个 MySQL 实例**中运行，数据在 cast 之间持久保留。
MySQL 容器已在 Docker 中运行，root 密码为 `root`。

**顺序**：先完成 Lab 3 全部 6 个 cast，再完成 Lab 4 全部 3 个 cast。
（Lab 4 的 l4ca1.sql 会 DROP DATABASE Banking 并重建，所以必须在 Lab 3 全部完成后运行。）

---

## Lab 3: SQL 数据完整性

### Cast 1 → assets/l3ca1.cast

**SQL 文件**：`assets/sql/l3ca1.sql`

**作用**：创建数据库 Banking，创建 customer、branch、account、depositor 四张表，查看建表语句。

```
asciinema rec assets/l3ca1.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca1.sql
exit
```

### Cast 2 → assets/l3ca2.cast

**SQL 文件**：`assets/sql/l3ca2.sql`

**作用**：插入初始数据，测试主键重复和主键为空。

**前置条件**：Cast 1 已运行（表已存在）。

```
asciinema rec assets/l3ca2.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca2.sql
exit
```

### Cast 3 → assets/l3ca3.cast

**SQL 文件**：`assets/sql/l3ca3.sql`

**作用**：测试 ON DELETE RESTRICT——删除被引用的 branch 行。

**前置条件**：Cast 2 已运行（数据已插入）。

```
asciinema rec assets/l3ca3.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca3.sql
exit
```

### Cast 4 → assets/l3ca4.cast

**SQL 文件**：`assets/sql/l3ca4.sql`

**作用**：测试 ON UPDATE RESTRICT——修改被引用的 branch 主键。

**前置条件**：Cast 3 已运行（数据仍在，ON DELETE RESTRICT 阻止了删除）。

```
asciinema rec assets/l3ca4.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca4.sql
exit
```

### Cast 5 → assets/l3ca5.cast

**SQL 文件**：`assets/sql/l3ca5.sql`

**作用**：测试 CHECK 约束（负余额插入和更新被拒绝）和外键引用检查。

**前置条件**：Cast 4 已运行。

```
asciinema rec assets/l3ca5.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca5.sql
exit
```

### Cast 6 → assets/l3ca6.cast

**SQL 文件**：`assets/sql/l3ca6.sql`

**作用**：创建审计日志表和触发器，通过 UPDATE 验证触发器自动记录功能。

**前置条件**：Cast 5 已运行。

```
asciinema rec assets/l3ca6.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l3ca6.sql
exit
```

---

## Lab 4: SQL 安全性

### Cast 1 → assets/l4ca1.cast

**SQL 文件**：`assets/sql/l4ca1.sql`

**作用**：重建 Banking 数据库，创建 employee 表并插入数据，查看表创建者 root 的权限。

```
asciinema rec assets/l4ca1.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l4ca1.sql
exit
```

### Cast 2 → assets/l4ca2.cast

**SQL 文件**：`assets/sql/l4ca2.sql`

**作用**：创建用户 user001，GRANT SELECT+INSERT，SHOW GRANTS，REVOKE INSERT，再次 SHOW GRANTS。

**前置条件**：Cast 1 已运行（employee 表存在）。

```
asciinema rec assets/l4ca2.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l4ca2.sql
exit
```

### Cast 3 → assets/l4ca3.cast

这个 cast 需要**两个终端**，或者在一个 asciinema 录屏中先后执行两个命令。

**Part A（root 终端）**：
```
asciinema rec assets/l4ca3.cast
docker exec -i infallible_swirles mysql -u root -proot -f < assets/sql/l4ca3_root.sql
```

**Part B（user002 终端，在同一录屏中操作）**：
先 Ctrl+D 退出 root 的 mysql，然后在同一 shell 中执行：
```
docker exec -i infallible_swirles mysql -u user002 -p123456 -f < assets/sql/l4ca3_user002.sql
exit
```

> 如果 user002 连接报错"Access denied for user 'user002'@'localhost'"，请尝试：
> ```
> docker exec -i infallible_swirles mysql -u user002 -p123456 -h 127.0.0.1 -f < assets/sql/l4ca3_user002.sql
> ```

---

## 重要说明

### `-f` 参数
所有命令都使用了 `mysql -f`（--force）：即使某个语句报错（如违反约束），mysql 也会继续执行后续语句。这让录屏能正确展示错误信息 + 后续验证查询。

### 如果中途录坏了
- Lab 3 任一 cast 重录：从 l3ca1.sql 重新跑起（因为数据会累积）
- Lab 4 任一 cast 重录：从 l4ca1.sql 重新跑起

### 容器名称
如果你的 MySQL 容器名不是 `infallible_swirles`，请用 `docker ps` 查看实际容器名并替换。
