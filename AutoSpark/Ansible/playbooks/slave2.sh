ansible-playbook -s --extra-vars 'MASTER_YES="false" USER="aagrawa8" SPARK_URL="spark://152.46.18.234:7077" MASTER_IP="152.46.18.234"' sparkplaybook2.yml -i slave_inventory
