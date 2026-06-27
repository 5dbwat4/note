# 浙江大学**2025–2026** 学年春夏季学期

## 《数据库系统》课程课堂测试一

(Quiz 1 for Database Systems)

考生姓名：　　　　　学号：　　　　　专业：　　　　　得分：

## **Problems concerning the basic concepts of database systems**

**1. According to the levels of data abstraction, database systems have several schemas, which are as follows:**

**Physical schema**, **Logical schema**, and **View schema**.

**2. List the names of data model used in database systems, and explain briefly how or when to use it.**

(i) **E-R model:** It is used in the conceptual database design, which describes the real world objects with entities, and relationships among these objects.

(ii) **Relational model:** It is used in the logical database design. It is the basis of the most DBMS products in the database world for more than 30 years, and it uses tables to represent both data and the relationships among those data.

(iii) **Object-oriented model:** It is heavily influenced by object-oriented programming language and can be understood as an attempt to add DBMS functionality to a programming language environment. It can be regarded as extending the E-R model with notions of encapsulation, methods and object identity, and support complex data structure. The model can be used in logical database design in most cases, and can also be used in conceptual design step.

(iv) **Object-relational model:** It extends the relational model with features of object-oriented model.

(v) **Semistructured-data model:** It is used in the logical database design steps. In this model, XML is widely used to represent semistructured data.

(vi) **Network model:** Data are represented by collections of records, and relationships among data are represented by links, which can be viewed as pointers. The records in the database are organized as collections of arbitrary graphs. It was only used in old database systems.

(vii) **Hierarchical model:** It is similar to the network model in the sense that data and relationships among data are represented by records and links, respectively. But it differs from the network model in that the records are organized as collections of trees rather than arbitrary graphs. It was used only in old database systems.

**3. What are the physical data independence and logical data independence in database system?**

**Physical Data Independence:** the ability to modify the physical schema without changing the logical schema, as well as application programs, that is, the modification in the physical schema does not affect the logical schema, there application program need not be changed.

**Logical data independence:** Protect application programs from changes in *logical* structure of data, i.e., the modification in the logical schema does not affect the view schema, there application program need not be changed.
