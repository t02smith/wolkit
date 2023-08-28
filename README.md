# Wake-on-LAN Kit

Wake-on-LAN Kit leverages (you guessed it) [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN) to trigger devices in your local network to wake up when certain conditions are met. This project can wake your device:

- at scheduled times in the day/week
- when a certain device enters your LAN
- when a bluetooth device is nearby
- when certain environmental factors occur (e.g. temperature, motion, and light)

Users interact with this application using a HTTP API, which includes complete Swagger Documentation (because I was too lazy to create a web interface for this 😝).

This was tested and ran on a 🍒 Raspberry Pi 4 (4GB RAM) and also used the [Enviro Hat](https://shop.pimoroni.com/products/enviro?variant=31155658489939) for environment sensing.

## 🛠️ Tools Used

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=for-the-badge)
![Raspberry Pi Badge](https://img.shields.io/badge/Raspberry%20Pi-A22846?logo=raspberrypi&logoColor=fff&style=for-the-badge)

## 💡 This Repository

This repo contains:

- [`/report`](/report) - The LaTeX report submitted with this project
- [`/wolkit`](/wolkit) - The source code for this project
