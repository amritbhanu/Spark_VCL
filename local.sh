#from the source directory.
#1st parameter unity id, 2nd parameter length of reservation in mins.
python setup.py install

export ANSIBLE_HOST_KEY_CHECKING=False

echo $1 > user.txt
if [ ! -d "~/.ssh/id_rsa.pub" ]; then
  ssh-keygen -t rsa
  mkdir ssh_keys
  cp ~/.ssh/id_rsa ssh_keys/id_rsa
  cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub
  # Control will enter here if $DIRECTORY doesn't exist.
fi
#this will create 1 instance and we will install the packages and whatever is needed for that.
#apache spark 4065
#ubuntu - 3630
#centos - 3685
vcl-opsworks request add --image-id 4065 --node-type master -c 1 -l $2 --playbook main.yml "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall" "$1@NCSU"
#it will return a connecting ip address, use that to do ssh.

dir=$(pwd)
val=1
while read line           
do           
     val=$"$line"           
done < $dir/AutoSpark/Ansible/playbooks/master_file

cat ~/.ssh/id_rsa.pub | ssh $1@$val "chmod 700 ~/.ssh; cat >> ~/.ssh/id_rsa.pub; chmod 600 ~/.ssh/id_rsa.pub; chmod 600 ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa | ssh $1@$val "cat >> ~/.ssh/id_rsa; chmod 600 ~/.ssh/id_rsa"

#ssh to 1 of the ips
#ssh -X $1@$val

#distributed file system

#Sending file to master node.
scp /home/amrit/GITHUB/Enron/Datasets/SE/jones.txt $1@$val:/home/$1/jones.txt
scp /home/amrit/GITHUB/Enron/Datasets/SE/cs.txt $1@$val:/home/$1/cs.txt
