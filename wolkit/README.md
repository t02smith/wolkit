# Wake-on-LAN Kit

## How to run

> The environmental sensors are reliant on use of a Raspberry Pi 
> and the Enviro sensor ([buy from here](https://shop.pimoroni.com/products/enviro?variant=31155658489939))

### Docker

```bash
docker build -t wolkit-img .
docker run -d --name wolkit -p 5055:5055 wolkit-img
```