#python environment
python3 -m venv myenv
source myenv/bin/activate

#initiating airflow
export AIRFLOW_HOME=~/airflow

#airflow straight-up
#airflow db init
#airflow scheduler
#airflow webserver --port 8080 

#airflow-docker
mkdir -p ./airflow/dags ./airflow/logs ./airflow/plugins ./airflow/config
cd airflow
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.1/docker-compose.yaml'
docker compose up airflow-init
docker compose up
