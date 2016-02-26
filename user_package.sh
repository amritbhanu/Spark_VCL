#Step 1: Predefined Packages
sudo apt-get update -y
sudo apt-get install python-pip -y
sudo apt-get install python-dev -y
sudo apt-get install libgmp3-dev -y
pip install pycrypto

#Step 2: Instaling ansible
wget https://pypi.python.org/packages/source/a/ansible/ansible-1.9.4.tar.gz
tar -xvf ansible-1.9.4.tar.gz
cd ansible-1.9.4
sudo python setup.py install
cd ..
rm ansible-1.9.4.tar.gz
sudo rm -rf ansible-1.9.4
#Check if ansible is properly installed by going to terminal, write "python". The python interpereter will start and then type "from ansible.playbook import PlayBook". If there is no error then it is properly installed, else run the above step #2 manually.

#Step 3: Generating ssh-keys. # It will prompt for couple of options, just keep pressing "enter", you don't need to write anything.
ssh-keygen -t rsa
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub
#Copying id_rsa.pub key on the user preferences, ssh-key authentication
