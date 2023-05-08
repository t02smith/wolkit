class ServiceNotFoundError(ValueError):
    def __init__(self, service_name: str):
        super().__init__(f"Service {service_name} not found")


class ServiceAlreadyEnabledError(ValueError):
    def __init__(self, service_name: str):
        super().__init__(f"Service {service_name} already enabled")


class ServiceAlreadyDisabledError(ValueError):
    def __init__(self, service_name: str):
        super().__init__(f"Service {service_name} already disabled")
