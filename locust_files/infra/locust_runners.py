import multiprocessing
import time

import allure
import invokust
from datetime import datetime
import yaml

from automation_infra.support_utils import kubernetes_support as kub_sup
from automation_infra.support_utils.gcp_support import wait_cluster_status

yaml.Dumper.ignore_aliases = lambda *args: True

from automation_infra.support_utils import SupportUtils as sup
from locust.env import Environment
import gevent
from locust_files.infra import locust_constants as const

from automation_infra.support_utils import FileUtil as f


class LocustRunner:

    def __init__(self):
        self.unique_log_name = sup.createUnigueName(const.locust_logs)
        self.unique_statistics_name = sup.createUnigueName(const.locust_results)

    def invoker_run(self, user_classes, host, num_of_users, spawn_rate, run_time, app_key):
        f.create_text_file(const.app_key_path, app_key)
        settings = invokust.create_settings(
            classes=user_classes,
            host=host,
            num_users=num_of_users,
            spawn_rate=spawn_rate,
            run_time=run_time
        )
        load_test = invokust.LocustLoadTest(settings)
        load_test.run()
        return load_test.stats()

    def cmd_run(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time, app_key):
        try:
            sup.runCmd(
                str.format(const.locust_run_command, locust_file, self.unique_statistics_name, host, num_of_users,
                           spawn_rate, run_time, stop_time, const.locust_statistics_local_run_path))
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust distributed mode locally")
    def cm_mode_locally_run_distributed(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time,
                                        app_key):
        f.create_text_file(const.app_key_path, app_key)
        num_of_workers = multiprocessing.cpu_count() - 1
        cmd = str.format(const.locust_master_command, locust_file, self.unique_statistics_name, num_of_workers, host,
                         num_of_users, spawn_rate, run_time, stop_time, const.locust_statistics_local_run_path)
        for cpu_num in range(num_of_workers):
            cmd += str.format(";" + const.locust_worker_command, locust_file)
        try:
            sup.runMultipleCmdsAsync(cmd)
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust with env tool locally")
    def env_run(self, user_classes, host, num_of_users, spawn_rate, run_time, app_key):
        env = Environment(user_classes=user_classes)
        env.create_local_runner()
        f.create_text_file(const.app_key_path, app_key)
        env.runner.start(num_of_users, spawn_rate=spawn_rate)
        env.host = host
        gevent.spawn_later(run_time, lambda: env.runner.quit())
        result = env.runner.greenlet.join()
        print(result)

    @allure.step("Run locust distributed mode with docker locally")
    def run_with_docker(self, locust_file_path, worker_num, host, user_num, spawn_rate, run_time, app_key):
        f.create_text_file(const.app_key_path, app_key)
        docker_master = const.docker_master.copy()
        docker_worker = const.docker_worker.copy()
        docker_services = const.docker_services.copy()
        docker_master["command"] = str.format(docker_master["command"], locust_file_path, worker_num, host,
                                              user_num, spawn_rate, run_time, self.unique_statistics_name,
                                              const.locust_statistics_local_run_path)
        docker_worker["command"] = str.format(docker_worker["command"], locust_file_path)
        docker_services["services"]["master-distributed"] = docker_master
        for num_of_workers in range(worker_num):
            dict_helper = docker_worker.copy()
            dict_helper.update({"container_name": "Distributed-Worker" + str(num_of_workers)})
            dict_helper["container_name"] = dict_helper["container_name"] + str(num_of_workers)
            docker_services["services"]["worker-distributed" + str(num_of_workers)] = dict_helper
        yml_path = f.getFullPath("")
        f.create_yml_file(yml_path + const.docker_compose_file, docker_services)
        sup.runCmd(f"cd {yml_path};{const.docker_compose_up_cmd}")

    @allure.step("Run locust distributed mode on GCP cloud")
    def run_distributed_mode_on_gcp(self, host, expected_workers_num, num_of_users, spawn_rate, run_time, app_key,
                                    locust_file_to_run):
        image = str.format(const.image_path, self.project_id, create_global_unique_name('latest', 5))
        f.create_text_file(const.app_key_path, app_key)
        f.replace_master_yaml_value(const.master_deployment_file_path, self.host, image)
        # worker deployment yaml file values replacement
        f.replace_worker_yaml_value(const.worker_deployment_file_path, self.host, self.expected_workers_num, image)
        docker_file_text = str.format(const.docker_file_text, self.locust_file_to_run, const.locust_templates,
                                      const.locust_files_dir, const.locust_tasks_dir, const.docker_image_dir,
                                      app_key_file, locust_support)
        run_sh_text = str.format(const.run_sh_text, const.locust_statistic_dir,
                                 expected_workers_num, host, num_of_users, spawn_rate, run_time, locust_file_to_run,
                                 self.unique_log_name)
        rename_sh_script = str.format(const.rename_sh_script, self.unique_statistics_name)
        f.create_text_file(const.run_sh_path, run_sh_text)
        f.create_text_file(const.rename_sh_path, rename_sh_script)
        f.create_text_file(const.docker_file_path, docker_file_text)
        f.create_text_file(const.requirements_txt_path, const.requirments_text)
        master_pod = ''
        try:
            sup.runCmd(const.load_test_cluster_connection_str)
            sup.runCmd(const.create_pvc_clime)
            pods = kub_sup.getRunningKubernetesPods(1, 180)
            for pod_name in pods:
                print(pod_name)

            log.info("Push image to GCP cloud")
            sup.run_cmd_by_terminal(f"cd {const.locust_files_path};{str.format(const.push_image_cmd, image)}")
            sup.runCmd(const.create_master_pod_cmd)
            sup.runCmd(const.create_master_service_pod_cmd)
            sup.runCmd(const.create_worker_pod_cmd)
            pods = kub_sup.getRunningKubernetesPods(1, 180)
            for pod_name in pods:
                if "master" in pod_name:
                    master_pod = pod_name
                    break
            print(f"Starting to run load {str(datetime.now())}")
            sup.runCmd(str.format(const.get_kubectl_logs, master_pod))
            print(f"Load was finished {str(datetime.now())}")
        except Exception as e:
            raise Exception(str.format("Fail to run load test on GCP cloud cause of error: {0}"), e)
        finally:
            sup.runCmd(const.delete_master_deployment_cmd)
            sup.runCmd(const.delete_worker_deployment_cmd)
            sup.runCmd(const.delete_service)
            sup.runCmd(const.create_pvc_access_pod)
            kub_sup.getRunningKubernetesPods(1, 60)
            time.sleep(5)
            sup.runCmd(const.copy_locust_statistics_cmd)
            sup.runCmd(str.format(const.delete_pod_cmd, const.persistence_pod_name))
            sup.run_cmd_by_terminal(str.format(const.delete_image_cmd, image))
