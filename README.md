# Zabbix-Graph-Download


run

```
source .venv/bin/activate
pip3 install -r requirements.txt
for host in $(cat hosts);do python3 ./graph.py $host;done
cd widgets
while IFS=',' read -r col1 col2;do mv $col2 $col1;done < ../srv.csv
```