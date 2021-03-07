import allure
import invokust
# try:
#     from gevent.monkey import patch_all
#
#     patch_all()
# except ImportError:
#     pass
from automation_infra.support_utils import SupportUtils as sup
from locust.env import Environment
import gevent
import multiprocessing


class LocustRunner:
    def __init__(self):
        self.unique_statistics_name = sup.createUnigueName("locust_results")

    def invoker_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
        settings = invokust.create_settings(
            classes=user_classes,
            host=host,
            num_users=num_of_users,
            spawn_rate=spawn_rate,
            run_time=run_time,
            loglevel="DEBUG"
        )
        load_test = invokust.LocustLoadTest(settings)
        load_test.run()
        return load_test.stats()

    def cmd_run(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        try:
            sup.runCmd(
                f"locust -f {locust_file} --csv=locust_statistic/{self.unique_statistics_name} --headless --host {host}"
                f" -u {num_of_users} -r {spawn_rate} --run-time {run_time} --stop-time {stop_time}")
        except Exception as e:
            print(e)
            pass

    @allure.step("Run locust distributed mode locally")
    def cmd_run_distributed_mode_locally(self, locust_file, host, num_of_users, spawn_rate, run_time, stop_time):
        num_of_workers = multiprocessing.cpu_count()
        cmd = f"locust -f {locust_file} --csv=locust_statistic/{self.unique_statistics_name} --master --headless " \
              f"--expect-workers={num_of_workers} --host {host} -u {num_of_users} -r {spawn_rate} --run" \
              f"-time {run_time} --stop-time {stop_time} "
        for cpu_num in range(num_of_workers):
            cmd += f";locust -f {locust_file} --worker"
        try:
            sup.runMultipleCmdsAsync(cmd)
        except Exception as e:
            print(e)
            pass

    def env_run(self, user_classes, host, num_of_users, spawn_rate, run_time):
        env = Environment(user_classes=user_classes)
        env.create_local_runner()
        env.runner.start(num_of_users, spawn_rate=spawn_rate)
        env.host = host
        # env.stop_timeout = "1m"
        gevent.spawn_later(run_time, lambda: env.runner.quit())
        result = env.runner.greenlet.join()
        print(result)
