import multiprocessing
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
from locust_files.infra import locust_constants as const

from automation_infra.support_utils import FileUtil as f


class LocustRunner:

    def __init__(self):
        self.unique_log_name = sup.createUnigueName("locust_logs")
        self.unique_statistics_name = sup.createUnigueName("locust_results")

    def invoker_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
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

    def cmd_run(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        try:
            sup.runCmd(str.format(const.locust_run_command, locust_file, self.unique_statistics_name, host, num_of_users,
                                  spawn_rate, run_time, stop_time, const.locust_statistics_local_run_path))
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust distributed mode locally")
    def cmd_run_distributed_mode_locally(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
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
    def env_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        env = Environment(user_classes=user_classes)
        env.create_local_runner()
        env.runner.start(num_of_users, spawn_rate=spawn_rate)
        env.host = host
        gevent.spawn_later(run_time, lambda: env.runner.quit())
        result = env.runner.greenlet.join()
        print(result)

    @allure.step("Run locust distributed mode with docker locally")
    def run_with_docker(self, locust_file_path, worker_num, host, user_num, spawn_rate, run_time):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
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
    def run_distributed_mode_on_gcp(self, host, expected_workers_num, num_of_users, spawn_rate, run_time,
                                    locust_file_to_run):
        self.unique_statistics_name = sup.createUnigueName("locust_results")
        f.replace_master_yaml_value(const.master_deployment_file_path, host)
        f.replace_worker_yaml_value(const.worker_deployment_file_path, host, expected_workers_num)
        docker_file_text = str.format(const.docker_file_text, locust_file_to_run, const.locust_templates,
                                      const.locust_files_dir, const.locust_tasks_dir, const.docker_image_dir)
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
            sup.runCmd(const.gcloud_set_project_cmd)
            sup.runCmd(const.load_test_cluster_connection_str)
            sup.runCmd(f"cd {const.locust_files_path};{const.push_image_cmd}")
            sup.runCmd(const.create_master_pod_cmd)
            sup.runCmd(const.create_worker_pod_cmd)
            pods = kub_sup.getRunningKubernetesPods(1, 180)
            for pod_name in pods:
                if "master" in pod_name:
                    master_pod = pod_name
                    break
            sup.runCmd(str.format(const.get_kubectl_logs, master_pod))
        except Exception as e:
            raise Exception(str.format("Fail to run load test on GCP cloud cause of error: {0}"), e)
        finally:
            sup.runCmd(const.delete_master_deployment_cmd)
            sup.runCmd(const.delete_worker_deployment_cmd)
            sup.runCmd(str.format(const.create_pod_cmd, const.persistence_file_path))
            kub_sup.getRunningKubernetesPods(1, 60)
            time.sleep(5)
            sup.runCmd(const.copy_locust_statistics_cmd)
            sup.runCmd(str.format(const.delete_pod_cmd, const.persistence_pod_name))
