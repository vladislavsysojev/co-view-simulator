from automation_infra.support_utils import FileUtil as f
from automation_infra.support_utils import SupportUtils as sup

locust_templates = "locust_templates.py"
locust_files_dir = "locust_files"
locust_statistic_dir = "locust_statistic"
locust_tasks_dir = "locust-tasks"
docker_image_dir = "docker-image"
locust_statistics_local_run_path = str.format("{1}/{0}", locust_statistic_dir, locust_files_dir)
docker_file_text = '''FROM python:3.9.1\n# Add the licenses for third party software and libraries
        \nADD /{4}/licenses /licenses\n# Add the external tasks directory into /tasks
        \nADD /{4}/{3} /{3}
        \nCOPY {0} .
        \nRUN mkdir {2}
        \nCOPY {1} /{2}
        \nCOPY {5} /{2}
        \n# Install the required dependencies via pip
        \nRUN pip install -r /{3}/requirements.txt
        \n# Expose the required Locust ports
        \nEXPOSE 5557 5558 8089
        \n# Set script to be executable
        \nRUN chmod 755 /{3}/run.sh
        \n# Start Locust using LOCUS_OPTS environment variable
        \nENTRYPOINT ["/{3}/run.sh"]'''

run_sh_text = '''#!/bin/bash\nLOCUST="/usr/local/bin/locust" \nLOCUS_OPTS="-f {6}" \nsleep 60 
        \nLOCUST_MODE=${{LOCUST_MODE:-standalone}} 
        \n \nif [[ "$LOCUST_MODE" = "master" ]]; then \nls -ltrh /{0} \nls
        \nrm -rf /{0}/* \nLOCUS_OPTS="$LOCUS_OPTS --csv=/{0}/ --logfile=/{0}/{7}.log --master --expect-workers={1} --headless -H {2} -u {3} -r {4} --run-time {5} --stop-time 99" \nelif [[ "$LOCUST_MODE" = "worker" ]]; then 
        \n LOCUS_OPTS="$LOCUS_OPTS --worker --master-host=$LOCUST_MASTER" \nfi \necho "$LOCUST $LOCUS_OPTS" \n 
        \n$LOCUST $LOCUS_OPTS \nchmod +x /{0} \nchmod +x /{0}/*\nsleep 30 \nls -ltrh /{0}/*
        \nchmod +x /locust-tasks/rename.sh;mv /locust-tasks/rename.sh /{0}/;cd /{0}/;./rename.sh
        \nls -ltrh /{0}/*'''

rename_sh_script = """rename_name_path='{0}' \nfor f in *.csv \ndo\n       mv "$f" "$rename_name_path$f"\ndone"""

requirments_text = '''certifi==2020.12.5 
\nchardet==3.0.4 
\nclick==7.1.2 
\nFlask==1.1.2 
\ngevent==21.1.2 
\ngreenlet==1.0.0 
\nidna==2.10 
\nitsdangerous==1.1.0 
\nJinja2==2.11.3 
\nlocust==1.4.3 
\nMarkupSafe==1.1.1 
\nmsgpack==1.0.2 
\npyzmq==22.0.3 
\nrequests==2.25.1 
\nsix==1.15.0 
\nurllib3==1.26.3 
\nWerkzeug==1.0.1
\nlocust-plugins==1.1.7'''

docker_services = {
    "version": "3",
    "services": {}}
docker_worker = {'container_name': 'Distributed-Worker', 'image': 'locustio/locust',
                 'depends_on': ['master-distributed'], 'volumes': ['./:/mnt/locust'],
                 'command': '-f /mnt/locust/{0} --worker --master-host master-distributed'}

docker_master = {'container_name': 'Distributed-Master', 'image': 'locustio/locust', 'ports': ['8089:8089'],
                 'volumes': ['./:/mnt/locust'],
                 'command': '-f /mnt/locust/{0} --csv=/mnt/locust/{7}/{6} --master '
                            '--expect-workers={1} --headless -H {2} -u {3} -r {4} --run-time {5} --stop-time 99'}

docker_compose_file = "docker-compose.yml"
locust_results = "locust_results"
locust_logs = "locust_logs"
master_deployment_file = "locust-master-controller.yaml"
worker_deployment_file = "locust-worker-controller.yaml"
master_deployment_service_file = "locust-master-service.yaml"
gcloud_project_id = "charged-mind-247422"
persistence_deployment_file = "locust-persistency.yaml"
persistence_volume_deployment_file = "persistent-volume-load-test.yaml"
master_deployment_name = "locust-master"
worker_deployment_name = "locust-worker"
persistence_pod_name = "dataaccess"
kub_config_path = str.format("{}/locust_files/kubernetes-config/", f.getFullPath(""))
persistence_file_path = kub_config_path + persistence_deployment_file
persistence_clime_file_path = kub_config_path + persistence_volume_deployment_file
locust_files_path = str.format("{}/locust_files", f.getFullPath(""))
docker_file_path = str.format("{0}/Dockerfile", locust_files_path)
app_key_file = "app_key.txt"
app_key_path = str.format("{0}/{1}", locust_files_path, app_key_file)
locust_tasks_path = str.format("{}/locust_files/docker-image/locust-tasks", f.getFullPath(""))
requirements_txt_path = str.format("{0}/requirements.txt", locust_tasks_path)
rename_sh_path = str.format("{0}/rename.sh", locust_tasks_path)
run_sh_path = str.format("{0}/run.sh", locust_tasks_path)
master_deployment_file_path = str.format("{0}/{1}", kub_config_path, master_deployment_file)
worker_deployment_file_path = str.format("{0}/{1}", kub_config_path, worker_deployment_file)
master_service_deployment_file_path = str.format("{0}/{1}", kub_config_path, master_deployment_service_file)
image_path = "gcr.io/{0}/loadtest:{1}"
push_image_cmd = "gcloud builds submit --tag {} ."

delete_image_cmd = "gcloud container images delete {} --quiet"

create_pod_cmd = "kubectl apply -f {0}"

create_pvc_clime = str.format(create_pod_cmd, persistence_clime_file_path)

create_pvc_access_pod = str.format(create_pod_cmd, persistence_file_path)

create_master_pod_cmd = str.format(create_pod_cmd + master_deployment_file, kub_config_path)

create_worker_pod_cmd = str.format(create_pod_cmd + worker_deployment_file, kub_config_path)

create_master_service_pod_cmd = str.format(create_pod_cmd + master_deployment_service_file, kub_config_path)

get_kubectl_logs = "kubectl logs -f {0}"

delete_pod_cmd_force = "kubectl delete pods {0} --grace-period=0 --force"

delete_pod_cmd = "kubectl delete pods {0}"

delete_deployment_cmd = "kubectl delete deployment {0}"

delete_master_deployment_cmd = str.format(delete_deployment_cmd, master_deployment_name)

delete_worker_deployment_cmd = str.format(delete_deployment_cmd, worker_deployment_name)

copy_locust_statistics_cmd = str.format("kubectl cp {1}:/{2} {0}/{2}/ ", locust_files_path, persistence_pod_name,
                                        locust_statistic_dir)

delete_service = f"kubectl delete svc {master_deployment_name}"

docker_compose_up_cmd = "docker-compose up"
gcp_load_cluster = "load-test-simulator-cluster-demo-"


def init_cluster_name(name=gcp_load_cluster):
    global gcp_load_cluster
    if name == gcp_load_cluster:
        name = sup.create_global_unique_name_once(name, 2)
    else:
        sup.names_diff.append(name)
        global load_test_cluster_connection_str
        load_test_cluster_connection_str = f"gcloud container clusters get-credentials {name}" \
                                           f" --zone {gcp_zone} --project {gcloud_project_id}"
        global create_cluster_cmg
        create_cluster_cmg = f"gcloud container clusters create {name} --zone {gcp_zone}" \
                             " --scopes 'https://www.googleapis.com/auth/cloud-platform' --machine-type 'c2-standard-8'" \
                             " --enable-autoscaling --min-nodes '0' --max-nodes '10' --scopes=logging-write,storage-ro" \
                             " --addons HorizontalPodAutoscaling,HttpLoadBalancing"
        global gcp_cluster_status
        gcp_cluster_status = str.format("""gcloud container clusters list --zone {} | awk '/{}/{}'""", gcp_zone,
                                        name, "{print $8}")
        global upgrade_cluster_cmd
        upgrade_cluster_cmd = f"gcloud container clusters upgrade {name} --zone {gcp_zone} --quiet"
        global gcloud_cluster_delete
        gcloud_cluster_delete = f"gcloud container clusters delete {name} --zone {gcp_zone} --quiet"
    return name



gcp_zone = "us-central1-a"
# gcloud container clusters upgrade NAME
load_test_cluster_connection_str = f"gcloud container clusters get-credentials {init_cluster_name()} " \
                                   f"--zone {gcp_zone} --project {gcloud_project_id}"

create_cluster_cmg = "gcloud container clusters create {} --zone {}" \
                     " --scopes 'https://www.googleapis.com/auth/cloud-platform' --machine-type 'c2-standard-8'" \
                     " --num-nodes {} --enable-autoscaling --min-nodes '0' --max-nodes {} --scopes=logging-write,storage-ro" \
                     " --addons HorizontalPodAutoscaling,HttpLoadBalancing"

gcp_cluster_status = str.format("""gcloud container clusters list --zone {} | awk '/{}/{}'""", gcp_zone,
                                init_cluster_name(), "{print $8}")

locust_run_command = "locust -f {0} --csv={7}/{1} --headless --host {2} -u {3} -r {4} " \
                     "--run-time {5} --stop-time {6} "

locust_master_command = "locust -f {0} --csv={8}/{1} --master --headless --expect-workers={" \
                        "2} --host {3} -u {4} -r {5} --run-time {6} --stop-time {7} "

locust_worker_command = "locust -f {0} --worker"

gcloud_set_project_cmd = str.format("gcloud config set project {0}", gcloud_project_id)

upgrade_cluster_cmd = f"gcloud container clusters upgrade {init_cluster_name()} --zone {gcp_zone} --quiet"

gcloud_cluster_delete = f"gcloud container clusters delete {init_cluster_name()} --zone {gcp_zone} --quiet"
