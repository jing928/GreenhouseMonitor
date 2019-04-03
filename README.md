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



