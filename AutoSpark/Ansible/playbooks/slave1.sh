ansible-playbook -s --extra-vars 'MASTER_YES="false" USER="" SPARK_URL="spark://127.0.1.1:7077" MASTER_IP=""' sparkplaybook1.yml -i slave_inventory
ansible-playbook -s --extra-vars 'MASTER_YES="false" USER="" SPARK_URL="spark://127.0.1.1:7077" MASTER_IP=""' sparkplaybook1.yml -i master_inventory
