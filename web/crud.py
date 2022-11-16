import models

def get_sensor_value(sensor_name: str):
    return models.Sensor.filter(models.Sensor.name == sensor_name).first()

def get_all_sensors():
    return list(models.Sensor.select())

def get_config_value(config_name: str):
    return models.Configs.filter(models.Configs.name == config_name).first()

def get_all_configs():
    return list(models.Configs.select())