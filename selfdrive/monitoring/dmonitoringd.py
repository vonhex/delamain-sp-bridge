#!/usr/bin/env python3
# [Delamain] Stub: publishes permanently non-distracted driverMonitoringState
# at 20 Hz. dmonitoringmodeld (camera model) is not started. No alerts fire.
import time
import cereal.messaging as messaging
from openpilot.common.realtime import config_realtime_process

def main():
  config_realtime_process([0, 1, 2, 3], 5)
  pm = messaging.PubMaster(['driverMonitoringState'])
  interval = 1.0 / 20
  while True:
    dat = messaging.new_message('driverMonitoringState', valid=True)
    dat.driverMonitoringState.isRHD = False
    pm.send('driverMonitoringState', dat)
    time.sleep(interval)

if __name__ == '__main__':
  main()
