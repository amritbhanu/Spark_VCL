#Step 1: Predefined Packages
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
