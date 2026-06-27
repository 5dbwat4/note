# 浙江大学2025–2026 学年春夏季学期
## 《数据库系统》课程课堂测试二
### Quiz 2 for Database Systems
考生姓名：
学号：
得分：

Consider the following relation schemas and then answer the subsequent problems. Note that the key attributes in the relation schemas are underlined.

$$
\begin{align*}
&\text{Movie}(\underline{\text{title}}, \text{type}, \text{director}) \\
&\text{Comment}(\underline{\text{title}, \text{user\_name}}, \text{grade})
\end{align*}
$$

## Problem 1. Relational algebra
### (1) Find all the movie titles that are directed by “Yimou Zhang” and exist the comment grade of greater than or equal to 4. (16 points)
$$
\prod_{title }\left(\sigma_{director="Yimou Zhang"}(\text{Movie}) \bowtie \sigma_{grade \ge 4}(\text{Comment})\right)
$$

### (2) Find the titles of movies which are commented by “San Zhang”. (17 points)
$$
\Pi_{title}\left(\sigma_{user\_name="San Zhang"}(\text{Comment})\right)
$$

### (3) Find the lowest grade in Comment Table. (17 points)
Method 1:
$$
\Pi_{grade}(\text{Comment}) - \Pi_{grade}\left(\sigma_{\text{Comment}.grade > cmt2.grade}\big(\text{Comment} \times \rho_{cmt2}(\text{Comment})\big)\right)
$$
Method 2:
$$
\mathcal{G}_{min(grade)}(\text{Comment})
$$
(Different answer is OK if it is correct.)

## Problem 2. Write SQL statement for the following queries.
### (1) Find all the movie titles and types with their average grade. (16 points)
(Different answer is OK if it is correct.)
```sql
SELECT title, type, avg(grade)
FROM Movie M, Comment C
WHERE M.title=C.title
GROUP BY title
```

### (2) Find the directors of the movies that have the lowest average grade. (17 points)
(Different answer is OK if it is correct.)
```sql
SELECT director 
FROM Movie M, Comment C 
WHERE M.title=C.title 
GROUP BY title 
HAVING avg(grade)<=all (
    SELECT avg(grade) 
    FROM Movie, Comment 
    WHERE Movie.title=Comment.title
    GROUP BY title
)
```

### (3) Find all the movie titles where every user gives higher grade than movie “the avenger”. (17 points)
(Different answer is OK if it is correct.)
```sql
SELECT title from Movie
EXCEPT
SELECT title from movie
WHERE EXISTS (
    SELECT *
    FROM Comment A, Comment B 
    WHERE A.title=movie.title 
      and A.user_name = B.user_name 
      AND B.title='the avenger' 
      AND A.grade <=B.grade
)
```

$$
\begin{align*}
&\text{Student}(\underline{\text{SID}}, \text{name}) \\
&\text{Course}(\underline{\text{CID}},\text{name},\text{Teacher}) \\
&\text{SC}(\underline{\text{SID},\text{CID}})
\end{align*}
$$
检索学过高老师主讲的所有课程的同学姓名。
```sql
SELECT name FROM Student 
WHERE NOT EXISTS (
    SELECT * FROM course 
    WHERE course.Teacher='高云君' 
      AND NOT EXISTS (
          SELECT * FROM SC 
          WHERE Student.SID=SC.SID 
            AND Course.CID=SC.CID
      )
)
```