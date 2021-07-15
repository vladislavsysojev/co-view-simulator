#!/usr/bin/env python
import time

from locust_files.infra import locust_constants as const
from automation_infra.support_utils import SupportUtils as sup
from automation_infra.automation_log_config.automation_log import ILog

log = ILog("gcp support")


def wait_cluster_status(expected_status: str, wait: int, reties: int):
    retry_counter = 0
    while retry_counter < reties:
        try:
            current_status = [x.lower() for x in str.lower(sup.runCmd(const.gcp_cluster_status)).split("\n")]
            if str.lower(expected_status) not in current_status:
                retry_counter += 1
                log.info(f"Cluster status {current_status} do not equal to {expected_status}")
                time.sleep(wait)
            else:
                return
        except Exception as e:
            log.error(f"Get cluster status fail with exception {e}")
    raise Exception(str.format("Cluster not reached expected status: {}", expected_status))
