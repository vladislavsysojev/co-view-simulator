import time

import allure
import invokust
# try:
#     from gevent.monkey import patch_all
#
#     patch_all()
# except ImportError:
#     pass
import yaml

from automation_infra.support_utils import kubernetes_support as kub_sup

yaml.Dumper.ignore_aliases = lambda *args: True

from automation_infra.support_utils import SupportUtils as sup
from locust.env import Environment
import gevent
import multiprocessing

from automation_infra.support_utils import FileUtil as f


class LocustRunner:
    # def __init__(self):
    #     self.unique_statistics_name = sup.createUnigueName("locust_results")

    def invoker_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        settings = invokust.create_settings(
            classes=user_classes,
            host=host,
            num_users=num_of_users,
            spawn_rate=spawn_rate,
            run_time=run_time
            # loglevel="DEBUG"
        )
        load_test = invokust.LocustLoadTest(settings)
        load_test.run()
        return load_test.stats()

    def cmd_run(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        try:
            sup.runCmd(
                f"locust -f {locust_file} --csv=locust_files/locust_statistic/{self.unique_statistics_name} --headless --host {host}"
                f" -u {num_of_users} -r {spawn_rate} --run-time {run_time} --stop-time {stop_time}")
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust distributed mode locally")
    def cmd_run_distributed_mode_locally(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        num_of_workers = multiprocessing.cpu_count() - 1
        cmd = f"locust -f {locust_file} --csv=locust_files/locust_statistic/{self.unique_statistics_name} --master --headless " \
              f"--expect-workers={num_of_workers} --host {host} -u {num_of_users} -r {spawn_rate} --run" \
              f"-time {run_time} --stop-time {stop_time} "
        for cpu_num in range(num_of_workers):
            cmd += f";locust -f {locust_file} --worker"
        try:
            sup.runMultipleCmdsAsync(cmd)
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust with env tool locally")
    def env_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        env = Environment(user_classes=user_classes)
        env.create_local_runner()
        env.runner.start(num_of_users, spawn_rate=spawn_rate)
        env.host = host
        # env.stop_timeout = "1m"
        gevent.spawn_later(run_time, lambda: env.runner.quit())
        result = env.runner.greenlet.join()
        print(result)

    docker_services = {
        "version": "3",
        "services": {}}
    docker_worker = {'container_name': 'Distributed-Worker', 'image': 'locustio/locust',
                     'depends_on': ['master-distributed'], 'volumes': ['./:/mnt/locust'],
                     'command': '-f /mnt/locust/{0} --worker --master-host master-distributed'}
    docker_master = {'container_name': 'Distributed-Master', 'image': 'locustio/locust', 'ports': ['8089:8089'],
                     'volumes': ['./:/mnt/locust'],
                     'command': '-f /mnt/locust/{0} --csv=/mnt/locust/locust_files/locust_statistic/{6} --master '
                                '--expect-workers={1} --headless -H {2} -u {3} -r {4} --run-time {5} --stop-time 99'}

    @allure.step("Run locust distributed mode with docker locally")
    def run_with_docker(self, locust_file_path, worker_num, host, user_num, spawn_rate, run_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        # yml_path = f.getFullPath("locust_files/docker-compose.yml")
        # with open(yml_path) as file:
        #     # The FullLoader parameter handles the conversion from YAML
        #     # scalar values to Python the dictionary format
        #     docker_compose_list = yaml.load(file, Loader=yaml.FullLoader)
        self.docker_master["command"] = str.format(self.docker_master["command"], locust_file_path, worker_num, host,
                                                   user_num, spawn_rate, run_time, self.unique_statistics_name)
        self.docker_worker["command"] = str.format(self.docker_worker["command"], locust_file_path)
        self.docker_services["services"]["master-distributed"] = self.docker_master
        for num_of_workers in range(worker_num):
            dict_helper = self.docker_worker.copy()
            dict_helper.update({"container_name": "Distributed-Worker" + str(num_of_workers)})
            dict_helper["container_name"] = dict_helper["container_name"] + str(num_of_workers)
            self.docker_services["services"]["worker-distributed" + str(num_of_workers)] = dict_helper

        dict_file = [self.docker_master, self.docker_worker]
        # f.createLocalFileOrDir("locust_files/docker-compose.yml")
        yml_path = f.getFullPath("")
        with open(yml_path + "docker-compose.yml", 'w') as file:
            documents = yaml.dump(self.docker_services, file)
        sup.runCmd(f"cd {yml_path};docker-compose up")

    @allure.step("Run locust distributed mode on GCP cloud")
    def run_distributed_mode_on_gcp(self, host, expected_workers_num, num_of_users, spawn_rate, run_time,
                                    locust_file_to_run):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        kub_config_path = str.format("{}/locust_files/kubernetes-config/", f.getFullPath(""))
        f.replace_master_yaml_value(str.format("{0}/locust-master-controller.yaml", kub_config_path), host)
        f.replace_worker_yaml_value(str.format("{0}/locust-worker-controller.yaml", kub_config_path), host,
                                    expected_workers_num)
        locust_files_path = str.format("{}/locust_files", f.getFullPath(""))
        docker_image_path = str.format("{}/locust_files/docker-image", f.getFullPath(""))
        locust_tasks_path = str.format("{}/locust_files/docker-image/locust-tasks", f.getFullPath(""))
        run_sh_text = str.format('''#!/bin/bash\nLOCUST="/usr/local/bin/locust" \nLOCUS_OPTS="-f {0}" \nsleep 30 
        \nLOCUST_MODE=${{LOCUST_MODE:-standalone}} \n \nif [[ "$LOCUST_MODE" = "master" ]]; then \nls -ltrh /locust_statistic 
        \nrm -rf /locust_statistic/* \nLOCUS_OPTS="$LOCUS_OPTS --csv=/locust_statistic/ --master --expect-workers={1} 
        --headless -H {2} -u {3} -r {4} --run-time {5} --stop-time 99" \nelif [[ "$LOCUST_MODE" = "worker" ]]; then 
        \n LOCUS_OPTS="$LOCUS_OPTS --worker --master-host=$LOCUST_MASTER" \nfi \necho "$LOCUST $LOCUS_OPTS" \n 
        \n$LOCUST $LOCUS_OPTS \nchmod +x /locust_statistic \nchmod +x /locust_statistic/*\nsleep 30
        \nchmod +x /locust-tasks/rename.sh;mv /locust-tasks/rename.sh /locust_statistic/;cd /locust_statistic/;./rename.sh
        \nls -ltrh /locust_statistic/*''',
                                 locust_file_to_run, expected_workers_num, host, num_of_users,
                                 spawn_rate, run_time)
        rename_sh_script = str.format("""rename_name_path='{0}' \nfor f in *.csv \ndo\n       mv "$f" "$rename_name_path$f"\ndone""", self.unique_statistics_name)
        file = open(str.format("{0}/run.sh", locust_tasks_path), "w")
        file.write(run_sh_text)
        file.close()
        file = open(str.format("{0}/rename.sh", locust_tasks_path), "w")
        file.write(rename_sh_script)
        file.close()
        master_pod = ""
        try:
            sup.runCmd(
                "gcloud container clusters get-credentials texel-load-tests-cluster --zone europe-west2-a --project charged-mind-247422")
            sup.runCmd(
                f"cd {locust_files_path};gcloud builds submit --tag gcr.io/charged-mind-247422/loadtest:latest .")
            # kub_sup.create_deployment(kub_config_path, "locust-master-controller.yaml")
            # kub_sup.create_deployment(kub_config_path, "locust-worker-controller.yaml")
            sup.runCmd(str.format("kubectl apply -f {0}locust-master-controller.yaml", kub_config_path))
            sup.runCmd(str.format("kubectl apply -f {0}locust-worker-controller.yaml", kub_config_path))
            pods = kub_sup.getRunningKubernetesPods(1, 180)
            for pod_name in pods:
                if "master" in pod_name:
                    master_pod = pod_name
                    break
            sup.runCmd(str.format("kubectl logs -f {0}", master_pod))
        except Exception as e:
            raise Exception(str.format("Fail to run load test on GCP cloud cause of error: {0}"), e)
        finally:
            sup.runCmd(f"kubectl delete pods {master_pod} --grace-period=0 --force")
            sup.runCmd("kubectl delete deployment locust-master")
            sup.runCmd("kubectl delete deployment locust-worker")
            sup.runCmd(f"kubectl apply -f {kub_config_path}locust-persistency.yaml")
            kub_sup.getRunningKubernetesPods(1, 60)
            time.sleep(5)
            sup.runCmd(str.format("kubectl cp dataaccess:/locust_statistic {0}/locust_statistic/ ", locust_files_path))
            sup.runCmd("kubectl delete pod dataaccess")
            print("exit")
