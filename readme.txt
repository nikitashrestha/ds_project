# Get session token
aws sts get-session-token --duration-seconds 129600


# Format hadoop filesystem
bin/hdfs namenode -format

# Start namenode and datanode
start-dfs.sh

# Stop daemon
stop-dfs.sh

# start yarn
start-yarn.sh

NameNode - http://localhost:9870/

ResourceManager - http://localhost:8088/

# stop yarn
stop-yarn.sh


https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html

https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html