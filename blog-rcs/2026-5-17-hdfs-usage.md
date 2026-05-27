# List files in HDFS
/opt/hadoop/bin/hdfs dfs -ls /

# Create a directory
/opt/hadoop/bin/hdfs dfs -mkdir /user/testHDFS

# Upload a file from local to HDFS
/opt/hadoop/bin/hdfs dfs -put localfile.txt /user/testHDFS/

# View file contents
/opt/hadoop/bin/hdfs dfs -cat /user/testHDFS/localfile.txt

# Move a file within HDFS
/opt/hadoop/bin/hdfs dfs -mv /user/testHDFS/localfile.txt /user/testHDFS/newname.txt

# Download from HDFS to local
/opt/hadoop/bin/hdfs dfs -get /user/testHDFS/newname.txt ./localcopy.txt

# Remove a file or directory
/opt/hadoop/bin/hdfs dfs -rm -r /user/testHDFS