
## What is WoL-Kit

**WoL-kit** is a device manager that allows you to wake you device according to various events. This includes:

- Manually waking your device,
- Scheduling your device to wake at recurring periods every week,
- Waking devices when another device joins the local network,
- Waking devices when a nearby Bluetooth device is detected,
- and more...

This project was made for the Advanced Networking module at the University of Southampton. 

## Default user

The default user will have the following information:

```bash
username = "admin"
password = "admin"
```

It is **highly recommended** that you change this password immediately. This can be done using the `PUT /api/v1/auth` endpoint.

## Where to Start

Make sure your device support wake-on-LAN. You will need to enable it in the following locations:

- your OS will have an option for it under your network card's settings, and
- your BIOS may have an option to enable it.

If you're stuck, I recommend [**this article**](https://www.intel.co.uk/content/www/uk/en/support/articles/000006559/server-products.html).

Now you can add your device to the application using the `POST /api/v1/devices` endpoint by submitting 
its **MAC address**, **static IP address**, and an **alias**. Then test that your device can be turned on from 
this application using the `POST /api/v1/devices/{device_id}/wake` endpoint.

From here, feel free to play around with the other sections.