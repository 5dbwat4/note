
27017.
In hashig with open addressing method，rehashing is definitely necessary when __.


A. an insertion fails
B. the hash table is half full
C. primary clustering occurs
D. the hash function is not uniform

answer：A

27018.
Given a hash table of size 13 (indexed from 0 to 12) with the hash function $H(Key)=Key$%11， Quadratic probing $H_ i (key)=(H(key)+i^{2}$ )%13 is used to resolve collisions when the $i$-th($i$>0) collision occurs. Then after inserting {10, 21, 32, 33, 65, 12 } one by one into the hash table, which one of the following statements is false?


A. the loading density is less than 0.5
B. the key 65 is at position 6
C. the key 12 is at position 1
D. the average search time is greater than 2

answer：C

27019.
Given a hash table of size 13 (indexed from 0 to 12) with the hash function $H(Key)=Key$%11.  Quadratic probing $H_ i (key)=(H(key)+i^{2}$ )%13 is used to resolve collisions when the $i$-th($i$>0) collision occurs. Then after inserting { 9, 21, 20, 33, 31, 5 } one by one into the initially empty hash table, which one of the following statements is false?


A. the loading density is less than 0.5
B. the key 5 is at position 6
C. the key 20 is at position 0
D. the average search time is less than 2

answer：D

27459.
Let the hash table be 14 in length, the hash function be h (key) = key% 11, and there are four keywords of existing data in the table: 15, 38, 61, 84. Now, if you want to add the node with the keyword 49 to the table and solve the conflict with the second detection and hashing method, the position to put in is（     )   

A. 8
B. 3
C. 5
D. 9

answer：D

27460.
Hash function has a common property, that is, the value of function should be（     ) Take each value of its range


A. Maximum probability
B. Minimum probability
C. Average probability
D. Equal probability
answer：D

27481.
The method which not only hopes to find quickly but also facilitates the dynamic change of linear table is  (    )    

A. Sequential search
B.   Half search
C.   Index order lookup
D. Hash search

answer：C

27484.
The key words of a group of records are {19, 14, 23, 1, 68, 20, 84, 27, 55, 11, 10, 79}. The hash table is constructed by the chain address method. The hash function is h (key) = key mod 13, and the hash address is 1（     ） A record

A. 1
B. 2
C. 3
D. 4

answer：D

27485.
The following statement about hash search is correct（     )   

A. The more complex the hash function is, the better, because it has good randomness and little conflict
B. The remainder method is the best of all hash functions
C. There are no particularly good or bad hash functions, depending on the situation
D. If you need to delete an element in the hash table, no matter what method is used to solve the conflict, you just need to simply delete the element

answer：C

27486.
There are several incorrect statements about hash search（     )
（ 1) When the chain address method is used to solve the conflict, the time to find an element is the same
(2) When the chain address method is used to solve the conflict, if the insertion rule is always at the beginning of the chain, the time of inserting any element is the same
(3) Using chain address method to solve conflicts is easy to cause aggregation phenomenon
(4) Rehashifa is not easy to produce aggregation @ [b] (2)
A. 1
B. 2
C. 3
D. 4

answer：B

27487.
In hash search, K keywords have the same hash value. If linear detection method is used to store the records corresponding to the K keywords in the hash table, at least the following steps should be taken（     ) This is a probe


A.k
B.k+1
C.k(k+1)/2
D.1+k(k+1)/2
answer：C

27488.
Hash 10 elements into a hash table of 100000 units, then（     ） Conflict


A. Certainly
B. Certainly not
C. It's still possible
answer：C

27509.
Suppose that there are k keywords which are synonymous with each other, how many times do we need to detect at least if we use the linear detection method to store the K keywords in the hash table（     )    

A. K-1 times
B. K times
C. K + 1 times
D. K (K + 1) / 2 times

answer：D

27687.
Hash files are also called ()


A. Sequential file
B. Index file
C. Direct access file
D. Indirect access to files

answer：C

27688.
It is assumed that linear detection is used to resolve conflicts when constructing hash table. If n consecutive keywords are synonymous
Words, the number of comparisons needed to find the last inserted keyword is ()


A. n-1
B. n
C. n+l
D. n+2

answer：B



28658.
Given a hash table of size 13 and the hash function $$h(x)=x \% 13$$. Assume that quadratic probing is used to solve collisions. After filling in the hash table one by one with input sequence { 10, 23, 1, 36, 19, 5 }, which number is placed in the position of index 0?


A. 23
B. 36
C. 10
D. none

answer：D

28674.
Given a hash table of size 13 and the hash function $$h(x)=x \% 13$$. Assume that quadratic probing is used to solve collisions. After filling in the hash table one by one with input sequence { 10, 23, 1, 36, 19, 5 }, which number is placed in the position of index 6?


A. 5
B. 19
C. 36
D. none

answer：C

28781.
The following terms that have nothing to do with the storage structure of data are ()

A. Circular queue
B. Linked list
C. Hash table
D. Stack

answer：D

28873.
The hash function H (key) = key mod 7 is selected to solve the conflict with the chain address method. Try to construct hash table for keyword sequence {31,23,17,27,19,11,13,91,61,41} in hash address space of 0-6, and calculate the average length of successful search under equal probability

A. 15/10
B. 15/8
C. 17/10
D. 15/6

answer：A

28878.
A set of key words {9,01,23,14,55,20,84,27} is set up. Hash function: H (key) = key mod 7, table length is 10, and the conflict is solved by open address method's second detection re hashing method hi = (H (key) + DI) mod 10 (DI = 12,22,32,...). The average length of successful search is calculated as()

A. 13/6
B. 15/8
C. 17/8
D. 17/6

answer：B

28879.
In hash storage, the loading factor α The greater the value of, the greater the value of

A. The more likely there is to be a conflict when accessing an element
B. The less likely there are conflicts when accessing elements
C. There is no possibility of conflict when accessing elements
D. No impact

answer：A

28881.
In hash storage, the loading factor α The smaller the value of, the smaller the value of

A. The more likely there is to be a conflict when accessing an element
B. The less likely there are conflicts when accessing elements
C. There is no possibility of conflict when accessing elements
D. No impact

answer：B

28882.
Suppose K keywords are synonymous with each other. If the K keywords are stored in the hash table by linear detection and hashing method, at least () times of detection are needed

A. (k-1)/2
B. k/2
C. k(k+1)/2
D. k(k-1)/2

answer：D

28885.
In the hash function H (key) = key% P, the best value of P is ()

A. Can only be equal to table length
B. Can only be less than table length
C. The largest prime less than or equal to the length of the table
D. Arbitrary value

answer：C

28888.
Hash 10 elements into a hash table of 100000 units, then () conflicts

A. Certainly
B. Certainly not
C. Maybe

answer：C

28890.
Let the hash table be 14 in length, the hash function be h (key) = key% 11, and there are four keywords of existing data in the table: 15, 38, 61, 84. Now we want to add the node with the keyword 49 to the table, and use the second detection and hashing method to solve the conflict, then the position to put is () @ [D] (2)
A. 8
B. 3
C. 5
D. 9

answer：D

28892.
There are several incorrect statements about hash search
(1) When the chain address method is used to solve the conflict, the time to find an element is the same
(2) When the chain address method is used to solve the conflict, if the insertion rule is always at the beginning of the chain, the time of inserting any element is the same
(3) Using chain address method to solve conflicts is easy to cause aggregation phenomenon
(4) Re hashifa is not easy to produce aggregation


A. 1
B. 2
C. 3
D. 4

answer：B

28893.
Average lookup length of hash table()

A. It is related to the conflict handling method and not to the length of the table
B. It has nothing to do with the conflict handling method, but with the length of the table
C. It is related to the conflict handling method and the length of the table
D. It is independent of the conflict handling method and the length of the table

answer：A

28896.
The key words of a group of records are {19, 14, 23, 1, 68, 20, 84, 27, 55, 11, 10, 79}. Hash table is constructed by chain address method. Hash function is h (key) = key mod 13. There are () records in the chain with hash address 1

A. 1
B. 2
C. 3
D. 4

answer：D

28921.
The sequential search method is suitable for linear tables with () storage structure

A. Hash storage
B. Sequential storage or chain storage
C. Compressed storage
D. Index storage

answer：B

29153.
If a linear table is required to be able to search quickly and adapt to the requirements of dynamic changes, it is better to use () search method.


A. Sequential search
B. Half search
C. Block search
D. Hash lookup

answer：C

29177.
Suppose that the range of a hash table is [0, 16], and the hash function is H(Key)=Key%13. If linear probing is used to resolve collisions, then after inserting { 24, 12, 13, 49, 23 } one by one into the hash table, the index of 23 is:   

A. 13
B. 0
C. 10
D. 1

answer：A

29178.
Suppose that the range of a hash table is [0, 18], and the hash function is H(Key)=Key%17. If linear probing is used to resolve collisions, then after inserting { 16, 32, 14, 34, 48 } one by one into the hash table, the index of 48 is:   

A. 14
B. 0
C. 17
D. 1

answer：C

29179.
Insert {20, 25, 13, 22, 4, 9, 29, 35, 14, 17} one by one into an initially empty hash table of size 13 with the hash function H(Key)=Key%13, and quadratic probing is used to resolve collisions. How many numbers can be inserted without collisions?   

A. 5
B. 6
C. 7
D. 8

answer：C

29181.
Insert {18, 23, 11, 20, 2, 7, 27, 33, 42, 15} one by one into an initially empty hash table of size 11 with the hash function H(Key)=Key%11, and quadratic probing is used to resolve collisions. How many numbers can be inserted without collisions?   

A. 5
B. 6
C. 7
D. 8

answer：B