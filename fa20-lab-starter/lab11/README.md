We still can run this lab locally.

Here is some steps

1. Download and install anaconda3
```sh
# Go to Home dir(Choose any dir you want)
cd ~
# Download conda
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
# install conda
bash Anaconda-latest-Linux-x86_64.sh
```

2. Install Java 1.8
```sh
# Install java 1.8, command may vary due to different systems, Ubuntu as example:
sudo apt-get update
sudo apt-get install openjdk-8-jdk
# Check if java 1.8 is installed
ls /usr/lib/jvm/
# Set java1.8 as java version
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

3. Install Hadoop 
```sh
# Go to Home dir(Choose any dir you want)
cd ~
# Download Hadoop
wget https://archive.apache.org/dist/hadoop/core/hadoop-2.7.3/hadoop-2.7.3.tar.gz
# Extract Hadoop
tar -xvf hadoop-2.7.3.tar.gz
# Set up Hadoop Path
# open your shell config file, such as .zshrc or .bashrc depends on your shell
# check shell type
echo "$SHELL"
# open config
vim ~/.zshrc
# Add following PATH to the end of file
export HADOOP_INSTALL=$HOME/hadoop-2.7.3
export PATH=$PATH:$HADOOP_INSTALL/bin
export PATH=$PATH:$HADOOP_INSTALL/sbin
export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
export HADOOP_COMMON_HOME=$HADOOP_INSTALL
export HADOOP_HDFS_HOME=$HADOOP_INSTALL
export YARN_HOME=$HADOOP_INSTALL
# source the config
source ~/.zshrc
```

4. Go to lab directory, and start virtual env
```sh
# activate anaconda3 in the lab folder, this should be your anaconda path
source ~/anaconda3/bin/activate
# Create a virtual environment using the correct version of Python
conda create --name lab11env python=2.7
# Activate the virtual environment
source activate lab11env
```