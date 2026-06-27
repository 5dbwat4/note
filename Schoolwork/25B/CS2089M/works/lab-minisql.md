# MiniSQL 模块详细报告

## Interpreter 模块

Interpreter 模块是 MiniSQL 的前端，负责与用户直接交互。它实现了程序的主控流程和命令的解析、执行与结果显示。

### 整体架构

Interpreter 由 `main.cpp` 中的 `main()` 函数和 `executor/execute_engine.cpp` 中的 `ExecuteEngine` 类共同构成。`main()` 负责启动与循环控制，`ExecuteEngine` 负责 SQL 语句的分派与执行。

### 程序启动与循环控制

在 `main.cpp` 中，我们实现了典型的 REPL（Read-Eval-Print Loop）流程：读取命令 → 解析命令 → 执行命令 → 显示结果 → 循环直到退出。

```cpp
int main(int argc, char **argv) {
  InitGoogleLog(argv[0]);
  const int buf_size = 1024;
  char cmd[buf_size];
  ExecuteEngine engine;
  // ...

  while (1) {
    // Step 1: 读取用户输入
    InputCommand(cmd, buf_size);

    // Step 2: 调用 lex/yacc 进行词法语法分析
    YY_BUFFER_STATE bp = yy_scan_string(cmd);
    yy_switch_to_buffer(bp);
    MinisqlParserInit();
    yyparse();

    // Step 3: 检查语法错误
    if (MinisqlParserGetError()) {
      printf("%s\n", MinisqlParserGetErrorMessage());
    }
    else {
      // Step 3: 执行解析得到的语法树
      auto result = engine.Execute(MinisqlGetParserRootNode());
      engine.ExecuteInformation(result);
    }

    MinisqlParserFinish();
    yy_delete_buffer(bp);
    yylex_destroy();

    // Step 4: 检查退出条件
    if (result == DB_QUIT) break;
  }
}
```

**工作流程说明：**

1. **启动初始化**：`InitGoogleLog()` 初始化日志系统；`ExecuteEngine` 构造函数确保 `./databases` 目录存在。

2. **命令读取**：`InputCommand()` 函数逐字符读取用户输入，以分号 `;` 作为命令终止符，以换行符结束输入：

```cpp
void InputCommand(char *input, const int len) {
  memset(input, 0, len);
  printf("minisql > ");
  int i = 0;
  char ch;
  while ((ch = getchar()) != ';') {
    input[i++] = ch;
  }
  input[i] = ch;      // 保留分号
  getchar();          // 丢弃换行符
}
```

3. **语法解析**：使用 Flex/Bison 配合 `yy_scan_string` 和 `yyparse` 对输入字符串进行词法分析和语法分析，生成抽象语法树（AST）。`MinisqlParserGetError()` 用于检查解析阶段是否出错，如有错误则打印错误信息。

4. **命令执行与结果显示**：将 AST 传递给 `ExecuteEngine::Execute()` 执行，根据返回的 `dberr_t` 状态码通过 `ExecuteInformation()` 显示相应的结果信息。

5. **退出条件**：当 `Execute()` 返回 `DB_QUIT` 时，跳出循环，程序结束。

### 命令行界面的结果显示

`ExecuteInformation()` 函数根据不同的错误码提供用户友好的提示信息：

```cpp
void ExecuteEngine::ExecuteInformation(dberr_t result) {
  switch (result) {
    case DB_ALREADY_EXIST:   cout << "Database already exists." << endl; break;
    case DB_NOT_EXIST:       cout << "Database not exists." << endl; break;
    case DB_TABLE_ALREADY_EXIST: cout << "Table already exists." << endl; break;
    case DB_TABLE_NOT_EXIST: cout << "Table not exists." << endl; break;
    case DB_INDEX_ALREADY_EXIST: cout << "Index already exists." << endl; break;
    case DB_INDEX_NOT_FOUND: cout << "Index not exists." << endl; break;
    case DB_COLUMN_NAME_NOT_EXIST: cout << "Column not exists." << endl; break;
    case DB_KEY_NOT_FOUND:   cout << "Key not exists." << endl; break;
    case DB_QUIT:            cout << "Bye." << endl; break;
    default: break;
  }
}
```

`ExecuteShowDatabases()` 和 `ExecuteShowTables()` 还实现了表格形式的结果输出，使用 `setw` 和 `setfill` 控制对齐和表格边框。

---

## API 模块

API 模块是系统的核心，其入口为 `ExecuteEngine::Execute()` 函数。它接收 Interpreter 层传入的语法树节点，根据节点类型分派到对应的 DDL 处理函数或进入 DML 查询计划流程。

### DDL 命令分派

`Execute()` 函数首先根据 AST 节点类型，将 `CREATE TABLE`、`DROP TABLE`、`CREATE INDEX`、`DROP INDEX`、`SHOW INDEXES` 等 DDL 命令分派到相应的处理函数：

```cpp
dberr_t ExecuteEngine::Execute(pSyntaxNode ast) {
  if (ast == nullptr) return DB_FAILED;
  unique_ptr<ExecuteContext> context(nullptr);
  if (!current_db_.empty())
    context = dbs_[current_db_]->MakeExecuteContext(nullptr);
  switch (ast->type_) {
    case kNodeCreateDB:    return ExecuteCreateDatabase(ast, context.get());
    case kNodeDropDB:      return ExecuteDropDatabase(ast, context.get());
    case kNodeShowDB:      return ExecuteShowDatabases(ast, context.get());
    case kNodeUseDB:       return ExecuteUseDatabase(ast, context.get());
    case kNodeShowTables:  return ExecuteShowTables(ast, context.get());
    case kNodeShowIndexes: return ExecuteShowIndexes(ast, context.get());
    case kNodeCreateTable: return ExecuteCreateTable(ast, context.get());
    case kNodeDropTable:   return ExecuteDropTable(ast, context.get());
    case kNodeCreateIndex: return ExecuteCreateIndex(ast, context.get());
    case kNodeDropIndex:   return ExecuteDropIndex(ast, context.get());
    case kNodeExecFile:    return ExecuteExecfile(ast, context.get());
    case kNodeQuit:        return ExecuteQuit(ast, context.get());
    // ...
    default: break;
  }
  // DML 语句进查询计划
  // ...
}
```

### DDL 实现详解

**CREATE TABLE** — `ExecuteCreateTable()` 解析语法树中的列定义节点，提取列名、类型、是否 unique 以及主键信息，构造 `Column` 对象和 `Schema`，调用 Catalog Manager 创建表；若指定了主键约束，自动创建 B+ 树主键索引：

```cpp
dberr_t ExecuteEngine::ExecuteCreateTable(pSyntaxNode ast, ExecuteContext *context) {
  if (current_db_.empty()) {
    cout << "No database selected" << endl;
    return DB_FAILED;
  }
  auto table_node = ast->child_;               // 表名
  auto column_list_node = table_node->next_;    // 列定义列表
  std::set<std::string> primary_keys;
  // 提取 primary keys 声明
  for (auto node = column_list_node->child_; node != nullptr; node = node->next_) {
    if (node->type_ == kNodeColumnList && node->val_ != nullptr
        && std::string(node->val_) == "primary keys") {
      for (auto key = node->child_; key != nullptr; key = key->next_) {
        primary_keys.insert(key->val_);
      }
    }
  }
  // 构造 Column 对象
  std::vector<Column *> columns;
  uint32_t column_index = 0;
  for (auto node = column_list_node->child_; node != nullptr; node = node->next_) {
    if (node->type_ != kNodeColumnDefinition) continue;
    auto name_node = node->child_;
    auto type_node = name_node->next_;
    bool unique = node->val_ != nullptr
        || primary_keys.find(column_name) != primary_keys.end();
    if (type == "int")
      columns.emplace_back(new Column(column_name, kTypeInt, column_index, false, unique));
    else if (type == "float")
      columns.emplace_back(new Column(column_name, kTypeFloat, column_index, false, unique));
    else if (type == "char") {
      uint32_t len = std::stoul(type_node->child_->val_);
      columns.emplace_back(new Column(column_name, kTypeChar, len, column_index, false, unique));
    }
    column_index++;
  }
  auto schema = std::make_shared<Schema>(columns);
  TableInfo *table_info = nullptr;
  auto result = context->GetCatalog()->CreateTable(table_node->val_, schema.get(), nullptr, table_info);
  // 自动创建主键索引
  if (result == DB_SUCCESS && !primary_keys.empty()) {
    vector<string> keys(primary_keys.begin(), primary_keys.end());
    IndexInfo *index_info = nullptr;
    context->GetCatalog()->CreateIndex(table_node->val_,
        string(table_node->val_) + "_primary", keys, nullptr, index_info, "bptree");
  }
  return result;
}
```

**EXECFILE** — `ExecuteExecfile()` 实现从外部 SQL 文件批量执行命令。逐行读取文件并按分号切分命令，对每条 SQL 语句独立进行词法语法分析和执行：

```cpp
dberr_t ExecuteEngine::ExecuteExecfile(pSyntaxNode ast, ExecuteContext *context) {
  std::ifstream input(ast->child_->val_);
  if (!input.is_open()) return DB_FAILED;
  std::string sql, line;
  while (std::getline(input, line)) {
    sql += line + '\n';
    size_t pos;
    while ((pos = sql.find(';')) != std::string::npos) {
      std::string command = sql.substr(0, pos + 1);
      sql.erase(0, pos + 1);
      YY_BUFFER_STATE bp = yy_scan_string(command.c_str());
      yy_switch_to_buffer(bp);
      MinisqlParserInit(); yyparse();
      if (!MinisqlParserGetError()) {
        auto result = Execute(MinisqlGetParserRootNode());
        ExecuteInformation(result);
        if (result == DB_QUIT) { /* cleanup & return */ }
      }
      MinisqlParserFinish();
      yy_delete_buffer(bp); yylex_destroy();
    }
  }
  return DB_SUCCESS;
}
```

### DML 查询计划

对于 SELECT、INSERT、DELETE、UPDATE 等 DML 语句，`Execute()` 调用 `Planner` 模块将语法树转换为执行计划树：

```cpp
// Execute() 后半部分 — DML 处理
Planner planner(context.get());
vector<Row> result_set{};
planner.PlanQuery(ast);                    // 语法树 → 执行计划
ExecutePlan(planner.plan_, &result_set, nullptr, context.get()); // 执行计划

// 格式化输出结果集
ResultWriter writer(ss);
if (planner.plan_->GetType() == PlanType::SeqScan
    || planner.plan_->GetType() == PlanType::IndexScan) {
  auto schema = planner.plan_->OutputSchema();
  // 输出表头、分隔线、数据行
  // ...
}
cout << writer.stream_.rdbuf();
```

**Planner 查询计划流程** (`planner/planner.cpp:8-37`)：

```cpp
void Planner::PlanQuery(pSyntaxNode ast) {
  switch (ast->type_) {
    case kNodeSelect: {
      auto statement = make_shared<SelectStatement>(ast, context_);
      statement->SyntaxTree2Statement(ast->child_);
      plan_ = PlanSelect(statement);  return;
    }
    case kNodeInsert: {
      auto statement = make_shared<InsertStatement>(ast, context_);
      statement->SyntaxTree2Statement(ast->child_);
      plan_ = PlanInsert(statement);  return;
    }
    case kNodeDelete: {
      auto statement = make_shared<DeleteStatement>(ast, context_);
      statement->SyntaxTree2Statement(ast->child_);
      plan_ = PlanDelete(statement);  return;
    }
    case kNodeUpdate: {
      auto statement = make_shared<UpdateStatement>(ast, context_);
      statement->SyntaxTree2Statement(ast->child_);
      plan_ = PlanUpdate(statement);  return;
    }
    // ...
  }
}
```

**SELECT 的索引选择策略** — `PlanSelect()` 检查 WHERE 条件中涉及的列是否有可用的 B+ 树索引，优先采用 IndexScan：

```cpp
AbstractPlanNodeRef Planner::PlanSelect(shared_ptr<SelectStatement> statement) {
  auto out_schema = MakeOutputSchema(statement->column_list_);
  vector<IndexInfo *> indexes;
  vector<IndexInfo *> available_index;
  context_->GetCatalog()->GetTableIndexes(statement->table_name_, indexes);
  for (auto index : indexes) {
    if (index->GetIndexKeySchema()->GetColumns().size() == 1) {
      auto col_id = index->GetIndexKeySchema()->GetColumn(0)->GetTableInd();
      if (find(statement->column_in_condition_.begin(),
               statement->column_in_condition_.end(), col_id)
          != statement->column_in_condition_.end()) {
        available_index.push_back(index);
      }
    }
  }
  if (available_index.empty() || statement->has_or)
    return make_shared<SeqScanPlanNode>(out_schema, statement->table_name_, statement->where_);
  return make_shared<IndexScanPlanNode>(out_schema, statement->table_name_,
      available_index,
      available_index.size() != statement->column_in_condition_.size(),
      statement->where_);
}
```

### 执行器创建与计划执行

`CreateExecutor()` 根据计划节点类型构造对应的执行器（SeqScan、IndexScan、Insert、Update、Delete、Values）。`ExecutePlan()` 初始化执行器后通过 `executor->Next()` 循环获取每行结果，填充到 `result_set` 中：

```cpp
dberr_t ExecuteEngine::ExecutePlan(const AbstractPlanNodeRef &plan,
    vector<Row> *result_set, Txn *txn, ExecuteContext *exec_ctx) {
  auto executor = CreateExecutor(exec_ctx, plan);
  executor->Init();
  RowId rid{}; Row row{};
  while (executor->Next(&row, &rid)) {
    if (result_set != nullptr) result_set->push_back(row);
  }
  return DB_SUCCESS;
}

unique_ptr<AbstractExecutor> ExecuteEngine::CreateExecutor(
    ExecuteContext *exec_ctx, const AbstractPlanNodeRef &plan) {
  switch (plan->GetType()) {
    case PlanType::SeqScan:
      return make_unique<SeqScanExecutor>(exec_ctx, ...);
    case PlanType::IndexScan:
      return make_unique<IndexScanExecutor>(exec_ctx, ...);
    case PlanType::Insert:
      return make_unique<InsertExecutor>(exec_ctx, ...);
    case PlanType::Update:
      return make_unique<UpdateExecutor>(exec_ctx, ...);
    case PlanType::Delete:
      return make_unique<DeleteExecutor>(exec_ctx, ...);
    case PlanType::Values:
      return make_unique<ValuesExecutor>(exec_ctx, ...);
    // ...
  }
}
```

---

## Record Manager

Record Manager 是 MiniSQL 的存储层核心，负责管理数据表记录的物理存储。本实现基于页式存储，每页大小与缓冲区块大小相同（4KB，即 `PAGE_SIZE`），每个数据页存储若干条定长记录，不支持跨页存储。

### 模块层次结构

Record Manager 由以下层次组成（从低到高）：

```
Column (列定义)  →  Schema (表模式)  →  Field (字段值)
Row (行，含序列化/反序列化)          →  TablePage (页内记录管理)
TableHeap (表级记录管理)            →  TableIterator (记录迭代器)
```

### 列定义 — Column 的序列化与反序列化

`Column::SerializeTo()` 将列元数据序列化为字节流，写入格式为：魔数(4B) + 列名长度(4B) + 列名字符串 + 类型(4B) + 长度(4B) + 表索引(4B) + nullable(1B) + unique(1B)：

```cpp
uint32_t Column::SerializeTo(char *buf) const {
  uint32_t ofs = 0;
  MACH_WRITE_UINT32(buf + ofs, COLUMN_MAGIC_NUM);
  ofs += sizeof(uint32_t);
  MACH_WRITE_UINT32(buf + ofs, name_.length());
  ofs += sizeof(uint32_t);
  memcpy(buf + ofs, name_.c_str(), name_.length());
  ofs += name_.length();
  MACH_WRITE_TO(TypeId, buf + ofs, type_);
  ofs += sizeof(TypeId);
  MACH_WRITE_UINT32(buf + ofs, len_);
  ofs += sizeof(uint32_t);
  MACH_WRITE_UINT32(buf + ofs, table_ind_);
  ofs += sizeof(uint32_t);
  MACH_WRITE_TO(bool, buf + ofs, nullable_);
  ofs += sizeof(bool);
  MACH_WRITE_TO(bool, buf + ofs, unique_);
  ofs += sizeof(bool);
  return ofs;
}
```

对应的 `Column::DeserializeFrom()` 按相同顺序还原字段，根据类型区分 CHAR 和其他类型的构造方式：

```cpp
uint32_t Column::DeserializeFrom(char *buf, Column *&column) {
  uint32_t ofs = 0;
  uint32_t magic_num = MACH_READ_UINT32(buf + ofs);
  ASSERT(magic_num == COLUMN_MAGIC_NUM, "Failed to deserialize column.");
  ofs += sizeof(uint32_t);
  uint32_t name_len = MACH_READ_UINT32(buf + ofs);
  ofs += sizeof(uint32_t);
  string name(buf + ofs, name_len);
  ofs += name_len;
  TypeId type = MACH_READ_FROM(TypeId, buf + ofs);
  ofs += sizeof(TypeId);
  uint32_t len = MACH_READ_UINT32(buf + ofs);
  ofs += sizeof(uint32_t);
  uint32_t table_ind = MACH_READ_UINT32(buf + ofs);
  ofs += sizeof(uint32_t);
  bool nullable = MACH_READ_FROM(bool, buf + ofs);
  ofs += sizeof(bool);
  bool unique   = MACH_READ_FROM(bool, buf + ofs);
  ofs += sizeof(bool);
  if (type == TypeId::kTypeChar)
    column = new Column(name, type, len, table_ind, nullable, unique);
  else
    column = new Column(name, type, table_ind, nullable, unique);
  return ofs;
}
```

### Schema 的序列化

`Schema::SerializeTo()` 将整个表模式序列化：先写魔数和列数，然后依次序列化每个 `Column`。`Schema::DeserializeFrom()` 反向操作，构建出 `Schema` 对象。

### 记录（Row）的序列化

`Row::SerializeTo()` 实现行数据的二进制序列化。格式为：

```
| field_count (4B) | null_bitmap (ceil(N/8) B) | field_0 | field_1 | ... | field_{N-1} |
```

其中 null bitmap 的每个 bit 表示对应字段是否为 NULL。

```cpp
uint32_t Row::SerializeTo(char *buf, Schema *schema) const {
  uint32_t ofs = 0;
  uint32_t field_count = static_cast<uint32_t>(fields_.size());
  uint32_t null_bitmap_size = (field_count + 7) / 8;
  MACH_WRITE_UINT32(buf + ofs, field_count);
  ofs += sizeof(uint32_t);
  memset(buf + ofs, 0, null_bitmap_size);
  for (uint32_t i = 0; i < field_count; i++) {
    if (fields_[i]->IsNull())
      buf[ofs + i / 8] |= static_cast<char>(1U << (i % 8));
  }
  ofs += null_bitmap_size;
  for (uint32_t i = 0; i < field_count; i++)
    ofs += fields_[i]->SerializeTo(buf + ofs);
  return ofs;
}
```

反序列化 `Row::DeserializeFrom()` 先读取列数验证与 schema 一致性，然后解析 null bitmap，最后逐个还原 Field 对象：

```cpp
uint32_t Row::DeserializeFrom(char *buf, Schema *schema) {
  uint32_t ofs = 0;
  uint32_t field_count = MACH_READ_UINT32(buf + ofs);
  ASSERT(field_count == schema->GetColumnCount(), "Fields count mismatch.");
  ofs += sizeof(uint32_t);
  uint32_t null_bitmap_size = (field_count + 7) / 8;
  char *null_bitmap = buf + ofs;
  ofs += null_bitmap_size;
  for (uint32_t i = 0; i < field_count; i++) {
    bool is_null = (null_bitmap[i / 8] & (1U << (i % 8))) != 0;
    Field *field = nullptr;
    ofs += Field::DeserializeFrom(buf + ofs, schema->GetColumn(i)->GetType(), &field, is_null);
    fields_.push_back(field);
  }
  return ofs;
}
```

### TableHeap — 表级记录管理

`TableHeap` 管理整个表的记录集合，对外提供记录的插入、更新、删除和查找接口。表的存储结构是一个单向链表的数据页，每个数据页通过 `next_page_id` 指针链接。

**插入记录 `InsertTuple()`**：从第一页起遍历每个 TablePage 尝试插入；若所有页已满，则创建新页并插入。插入成功后，`Row` 对象中的 `RowId` 被更新为实际的页面和槽位。

```cpp
bool TableHeap::InsertTuple(Row &row, Txn *txn) {
  if (row.GetSerializedSize(schema_) > TablePage::SIZE_MAX_ROW)
    return false;                         // 记录过大拒绝插入

  page_id_t page_id = first_page_id_;
  while (page_id != INVALID_PAGE_ID) {
    auto page = reinterpret_cast<TablePage *>(
        buffer_pool_manager_->FetchPage(page_id));
    if (page == nullptr) return false;
    page->WLatch();
    if (page->InsertTuple(row, schema_, txn, lock_manager_, log_manager_)) {
      page->WUnlatch();
      buffer_pool_manager_->UnpinPage(page_id, true);
      return true;
    }
    page_id_t next_page_id = page->GetNextPageId();
    if (next_page_id == INVALID_PAGE_ID) {
      // 所有页已满，创建新页
      page_id_t new_page_id;
      auto new_page = reinterpret_cast<TablePage *>(
          buffer_pool_manager_->NewPage(new_page_id));
      new_page->Init(new_page_id, page_id, log_manager_, txn);
      page->SetNextPageId(new_page_id);
      page->WUnlatch();
      buffer_pool_manager_->UnpinPage(page_id, true);

      new_page->WLatch();
      bool inserted = new_page->InsertTuple(row, schema_, txn, lock_manager_, log_manager_);
      new_page->WUnlatch();
      buffer_pool_manager_->UnpinPage(new_page_id, true);
      return inserted;
    }
    page->WUnlatch();
    buffer_pool_manager_->UnpinPage(page_id, false);
    page_id = next_page_id;
  }
  return false;
}
```

**更新记录 `UpdateTuple()`**：根据 `RowId` 定位到所在页面，调用 TablePage 的 `UpdateTuple` 方法进行原地更新。

```cpp
bool TableHeap::UpdateTuple(Row &row, const RowId &rid, Txn *txn) {
  auto page = reinterpret_cast<TablePage *>(
      buffer_pool_manager_->FetchPage(rid.GetPageId()));
  if (page == nullptr) return false;
  Row old_row(rid);
  page->WLatch();
  bool updated = page->UpdateTuple(row, &old_row, schema_, txn, lock_manager_, log_manager_);
  if (updated) row.SetRowId(rid);
  page->WUnlatch();
  buffer_pool_manager_->UnpinPage(page->GetTablePageId(), updated);
  return updated;
}
```

**查找记录 `GetTuple()`**：根据 Row 中已携带的 RowId 定位页面并读取。

```cpp
bool TableHeap::GetTuple(Row *row, Txn *txn) {
  auto page = reinterpret_cast<TablePage *>(
      buffer_pool_manager_->FetchPage(row->GetRowId().GetPageId()));
  if (page == nullptr) return false;
  page->RLatch();
  bool found = page->GetTuple(row, schema_, txn, lock_manager_);
  page->RUnlatch();
  buffer_pool_manager_->UnpinPage(page->GetTablePageId(), false);
  return found;
}
```

**删除记录 `ApplyDelete()`**：定位页面后直接调用 TablePage 的删除方法。MiniSQL 采用删除标记机制：`MarkDelete` 先打标记，`ApplyDelete` 在事务提交时真正删除。

```cpp
void TableHeap::ApplyDelete(const RowId &rid, Txn *txn) {
  auto page = reinterpret_cast<TablePage *>(
      buffer_pool_manager_->FetchPage(rid.GetPageId()));
  assert(page != nullptr);
  page->WLatch();
  page->ApplyDelete(rid, txn, log_manager_);
  page->WUnlatch();
  buffer_pool_manager_->UnpinPage(page->GetTablePageId(), true);
}
```

### TableIterator — 记录迭代器

`TableIterator` 提供对表记录的顺序遍历能力，用于支持不带条件的全表扫描和带条件的扫描。

**构造函数**：保存 TableHeap 引用和当前记录。如果构造的是有效记录（非 end 迭代器），立即从存储中读出该记录的数据。

```cpp
TableIterator::TableIterator(TableHeap *table_heap, RowId rid, Txn *txn)
    : table_heap_(table_heap), row_(rid), txn_(txn),
      is_end_(rid == INVALID_ROWID) {
  if (!is_end_ && table_heap_ != nullptr)
    table_heap_->GetTuple(&row_, txn_);
}
```

**前向迭代 `operator++()`**：在当前页内查找下一个有效记录（通过 `GetNextTupleRid`），如果当前页已遍历完，则跳转到下一个数据页，直到找到有效记录或到达表尾。

```cpp
TableIterator &TableIterator::operator++() {
  if (is_end_ || table_heap_ == nullptr) return *this;
  RowId cur_rid = row_.GetRowId();
  auto page = reinterpret_cast<TablePage *>(
      table_heap_->buffer_pool_manager_->FetchPage(cur_rid.GetPageId()));
  if (page == nullptr) { is_end_ = true; return *this; }

  RowId next_rid;
  bool found = page->GetNextTupleRid(cur_rid, &next_rid);
  page_id_t next_page_id = page->GetNextPageId();
  table_heap_->buffer_pool_manager_->UnpinPage(page->GetTablePageId(), false);

  // 跨页查找
  while (!found && next_page_id != INVALID_PAGE_ID) {
    page = reinterpret_cast<TablePage *>(
        table_heap_->buffer_pool_manager_->FetchPage(next_page_id));
    found = page->GetFirstTupleRid(&next_rid);
    next_page_id = page->GetNextPageId();
    table_heap_->buffer_pool_manager_->UnpinPage(old_page_id, false);
  }
  if (found) {
    row_ = Row(next_rid);
    table_heap_->GetTuple(&row_, txn_);
    is_end_ = false;
  } else {
    row_ = Row(INVALID_ROWID);
    is_end_ = true;
  }
  return *this;
}
```

**Begin/End 迭代器**：`TableHeap::Begin()` 从第一页开始查找第一个有效记录，`TableHeap::End()` 返回标记为结束的无效迭代器。

```cpp
TableIterator TableHeap::Begin(Txn *txn) {
  page_id_t page_id = first_page_id_;
  while (page_id != INVALID_PAGE_ID) {
    auto page = reinterpret_cast<TablePage *>(
        buffer_pool_manager_->FetchPage(page_id));
    RowId first_rid;
    bool found = page->GetFirstTupleRid(&first_rid);
    page_id_t next_page_id = page->GetNextPageId();
    buffer_pool_manager_->UnpinPage(page_id, false);
    if (found) return TableIterator(this, first_rid, txn);
    page_id = next_page_id;
  }
  return End();
}

TableIterator TableHeap::End() {
  return TableIterator(nullptr, INVALID_ROWID, nullptr);
}
```
