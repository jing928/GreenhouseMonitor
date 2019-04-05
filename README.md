# Greenhouse Monitor
RMIT Programming Internet of Things Assignment 1

by _Jing Li_ and _Cheng Qian_

## Introduction

The project once installed and configured, allows the Raspberry Pi with Sense Hat to automatically monitor ambient temperature and humidity, and compares them with preset __range__ data and send __out-of-range reading notification__ to user's __Pushbullet__ device(s). Besides, it will also have the Raspberry Pi run bluetooth scanner and send out temperature/humidity readings to user's device(s), once it finds a paired device nearby.

This project also allows user to generate sensor data report to see if there is any out-of-range reading for each day. Last but not the least, user can also use this project to generate two pre-defined data visualization _png_ files to learn more about the collected data.

## Installation

1. Flash the Raspbian image provided by RMIT School of Science to the Raspberry Pi with Sense Hat.
2. SSH into the Raspbian and run `mkdir Workspaces`
3. Run `cd Workspaces` and then `git clone` this repository.

### Dependencies

Run the following to install all required dependencies:

1. `sudo apt-get install bluez bluez-firmware bluez-tools blueman`
2. `sudo apt-get install libatlas-base-dev`
3. `sudo apt-get install sqlite3`
4. `pip3 install pybluez`
5. `pip3 install requests`
6. `pip3 install matplotlib`
7. `pip3 install seaborn`
8. `pip3 install pandas`

## Configuration

### Pushbullet API

1. Go to [https://www.pushbullet.com/](<https://www.pushbullet.com/>) and create an account. Then go to __My Account__ -> __Settings__ and __Create Access Token__ under __Access Tokens__.

2. Copy the newly created token from above step.

3. SSH into Raspbian and `cd Workspaces/GreenhouseMonitor`

4. Run `vi token.json` and add the following to the file and make sure to replace `[COPIED ACCESS TOKEN]` with your access token, and then save and quit with `:wq`:

   ```json
   {
     "pushbullet": "[COPIED ACCESS TOKEN]"
   }
   ```

5. Download Pushbullet App and/or web browser extensions and log in with the same account.

### Create SQLite Database

1. SSH into Raspbian and `cd Workspaces/GreenhouseMonitor`
2. Run `sqlite3 greenhouse_monitor.db`
3. Type `.databases` to verify and `.exit` to quit SQLite CLI.

### Cron Job

1. SSH into Raspbian and `cd ~`
2. Run `mkdir CronJobs`

#### Greenhouse Monitor

1. `vi CronJobs/RunGreenhouseMonitor.sh` and add the following to the file and save:

   ```bash
   #!/bin/sh
   cd /home/pi/Workspaces/GreenhouseMonitor; python3 monitor_and_notify.py
   ```

2. Run `chmod +x /home/pi/CronJobs/RunGreenhouseMonitor.sh`

3. `sudo vi /etc/cron.d/GreenhouseMonitorJob` and add the following to the file and save:

   `* * * * * pi /home/pi/CronJobs/RunGreenhouseMonitor.sh`

#### Greenhouse Bluetooth

1. `vi CronJobs/RunGreenhouseBluetooth.sh` and add the following to the file and save:

   ```bash
   #!/bin/sh
   cd /home/pi/Workspaces/GreenhouseMonitor; python3 greenhouse_bluetooth.py
   ```

2. Run `chmod +x /home/pi/CronJobs/RunGreenhouseBluetooth.sh`

3. `sudo vi /etc/cron.d/GreenhouseMonitorJob` and add the following to the file and save:

   ```
   * * * * * pi /home/pi/CronJobs/RunGreenhouseBluetooth.sh
   * * * * * pi sleep 30; /home/pi/CronJobs/RunGreenhouseBluetooth.sh
   ```

   The script itself takes about 15 seconds to run, and the two cron jobs above run the script every 30 seconds and therefore create a 15-second interval between two runs.

Finally, run `sudo reboot` to restart Raspbian for the changes to take effect.

## Usage

### Greenhouse Monitor

Once configured, the script should automatically run every minute and it will collect the sensor data (temperature and humidity) and save them to the local database. For every reading, it will also compare with the `config.json` file and notify user if the reading is out of range. The notification is sent maximum once each day, local time.

To manually run the script, run:

 `cd /home/pi/Workspaces/GreenhouseMonitor; python3 monitor_and_notify.py`

### Greenhouse Bluetooth

Once configured, the script should automatically run every 30 seconds and it will look for paired devices. If a paired device is nearby, it will collect the sensor data and send notification with the data to the user. The notification is sent maximum once every minute.

To manually run the script, run:

`cd /home/pi/Workspaces/GreenhouseMonitor; python3 greenhouse_bluetooth.py`

### Report Generation

To see if readings are out-of-range for each day, user can manually run:
`cd /home/pi/Workspaces/GreenhouseMonitor; python3 create_report.py`

User can also modify the range in `config.json` before creating the report.

### Data Visualization

User can manually run:

`cd /home/pi/Workspaces/GreenhouseMonitor; python3 analytics.py`

to generate two predefined graphs — `line_chart.png` and `joint_plot.png`.

The former shows the trends of temperature and humid, and the latter depicts the relationship between temperature and humidity along with their distributions.

