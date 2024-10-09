#init python environment
python3 -m venv myenv
source myenv/bin/activate

#airflow docker
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'
AIRFLOW_UID=50000
mkdir -p ./dags ./logs ./plugins ./config
docker compose up airflow-init
docker compose up -d

#turn on server
airflow webserver -p 8080

#compose down
docker compose down