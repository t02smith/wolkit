class DeviceDetailsAlreadyUsed(ValueError):
    pass


class DeviceNotFoundError(ValueError):
    def __int__(self, device_id: int):
        super().__init__(f"Device with id {device_id} not found")
