
class ScheduleNotFoundError(ValueError):
    def __init__(self, device_id: int, schedule_id: int):
        super().__init__(f"Schedule {schedule_id} for device {device_id} not found")


class ScheduleAlreadyEnabledError(ValueError):
    def __init__(self, device_id: int, schedule_id: int):
        super().__init__(f"Schedule {schedule_id} for device {device_id} already enabled")


class ScheduleAlreadyDisabledError(ValueError):
    def __init__(self, device_id: int, schedule_id: int):
        super().__init__(f"Schedule {schedule_id} for device {device_id} already disabled")
