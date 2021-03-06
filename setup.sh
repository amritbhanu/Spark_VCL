#from the source directory.
#~/hadoop/bin/hdfs namenode –format
cp AutoSpark/Spark_Jobs/lda.zip ~
cd ../
mv spark/spark_latest/conf/spark-env.sh.template spark/spark_latest/conf/spark-env.sh
touch spark/spark_latest/conf/slaves
unzip lda.zip
rm lda.zip
cd Spark_VCL

#if [ ! -d "ssh_keys" ]; then
  #ssh-keygen -t rsa
  #mkdir ssh_keys
  #cp ~/.ssh/id_rsa ssh_keys/id_rsa
  #cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub
  # Control will enter here if $DIRECTORY doesn't exist.
#fi

sudo python setup.py install
echo $1 > user.txt

export ANSIBLE_HOST_KEY_CHECKING=False

cd AutoSpark/driver

if [ ! -d "node_modules" ]; then
  npm install
  # Control will enter here if $DIRECTORY doesn't exist.
fi

node autospark-cluster-launcher.js
