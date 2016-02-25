## Steps for Spinning AutoSpark on Ubuntu VCL nodes

### For setting up master nodes
- On your local machine, git clone this repository, come to this directory and run **./user_package.sh**. Care to read the comments in the shell script.

- Open the id_rsa.pub file using **vi ~/.ssh/id_rsa.pub** and copy the keys. Paste the keys into [https://vcl.ncsu.edu/scheduling/] -> log in using your unity id -> goto **User Preferences** -> General Preferences -> Public keys -> Paste the copied keys.


- Now from the Spark_VCL directory, you might want to edit the **local.sh** at line 38, 39 specifying the full path of data file on which you want to run spark jobs. After that, run **./local.sh unity-id minutes**. Replace "unity-id" with the one provided to you by NC State and replace the minutes with integer value for which you want to reserve the master node for (Multiples of 60). It will ask for unity-id password.

- In the Spark_VCL directory, open main.yml file and edit at line 4 "unity-id" with your unity-id.

### For setting up the slave nodes
- Your Master node is setup. Now run **ssh unity-id@ip_address**. Replace "unity-id" with your unity-id and replace "ip_address" with the ip_address generated at the above step.

- You will see a directory automatically generated as "Spark_VCL". Change to this directory, and  open the main1.yml file and edit at line 3 "unity-id" with your unity-id.

- On the master node, come to this directory and run **./Master_package.sh**. Care to read the comments in the shell script.

- Now from the Spark_VCL directory, Run **./setup.sh unity-id**. It will ask for unity-id password.

- The above script will start a Prompt asking for different inputs like:
```
provider - vcl	#fixed input
name - 		# any arbitrary strings
count -		# No of slaves to be in the cluster or no. of VCL VMs you want to request.
duration -	# Duration for each node reservation
```

- After the successful completion of the above setup, you will have to run these commands from the **home directory**.
```
source ~/.bashrc
hadoop namenode -format
start-all.sh
hadoop fs -mkdir -p In
hadoop fs -put <data_file_full_path> /user/<unity-id>/In/<file_name_at_destination>
	- <data_file_full_path> the data file which you want to load (generally ~/filename).
	- <unity-id> - unity-id
	- <file_name_at_destination> - filename

ssh <unity-id>@<master-ip> 'sudo ~/spark/spark_latest/bin/spark-submit --driver-memory 1 --executor-memory 2 --class 3 4 --master 5 6 7 8'
	- <unity-id> - unity-id
	- <master-ip> - current nodes ip address
	- 1 - Ram like (2G, 3G)
	- 2 - Ram like (2G, 3G)
	- 3 - Class of scala file - In our example, I have provided you with the lda.jar scala example. (lda.lda)
	- 4 - Jar target path - In our example, I have provided you with the lda.jar scala example. (lda/target/lda-0.0.1.jar)
	- 5 - Spark Url - Which is of the form spark://<master-ip>:7077
	- 6 - Data filename which you put on hdfs. (filename)
	- 7 - <master-ip>
	- 8 - <unity-id>
	- NOTE: You can use your own examples but then you will have to transfer the data file and the scala code or jar files accordingly. Argument 3, 4 and 6 will change accordingly.
```

- I packaged the lda example using maven and then zipped it. Zipped file can be found under Spark_VCL/AutoSpark/Spark_Jobs. And you can transfer the zipped file on master node using scp.
