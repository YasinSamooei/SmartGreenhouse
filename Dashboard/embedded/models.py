from django.db import models


class SensorData(models.Model):
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    soil = models.IntegerField(default=0)
    gas = models.IntegerField(default=0)
    ldr = models.IntegerField(default=0)
    fan = models.BooleanField(default=False)
    pump = models.BooleanField(default=False)
    heater = models.BooleanField(default=False)
    alarm = models.BooleanField(default=False)
    light = models.BooleanField(default=False)
    auto = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} - T:{self.temperature} H:{self.humidity}%"



class SystemEvent(models.Model):
    LEVEL_CHOICES = [
        ("info", "اطلاعات"),
        ("warning", "هشدار"),
        ("critical", "خطرناک"),
        ("success", "موفقیت"),
    ]
    
    EVENT_TYPES = [
        ("temp_high", "دمای بالا"),
        ("temp_low", "دمای پایین"),
        ("temp_normal", "دمای نرمال"),
        ("hum_high", "رطوبت بالا"),
        ("hum_low", "رطوبت پایین"),
        ("hum_normal", "رطوبت نرمال"),
        ("soil_dry", "خاک خشک"),
        ("soil_wet", "خاک مرطوب"),
        ("gas_danger", "گاز خطرناک"),
        ("gas_normal", "گاز نرمال"),
        ("light_low", "نور ناکافی"),
        ("light_normal", "نور نرمال"),
        ("pump_on", "پمپ روشن شد"),
        ("pump_off", "پمپ خاموش شد"),
        ("fan_on", "فن روشن شد"),
        ("fan_off", "فن خاموش شد"),
        ("light_on", "نور مصنوعی روشن شد"),
        ("light_off", "نور مصنوعی خاموش شد"),
        ("heater_on", "گرمایش روشن شد"),
        ("heater_off", "گرمایش خاموش شد"),
        ("alarm_on", "آلارم فعال شد"),
        ("alarm_off", "آلارم غیرفعال شد"),
        ("device_online", "دستگاه آنلاین شد"),
        ("device_offline", "دستگاه آفلاین شد"),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="info")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)
    
    sensor_data = models.JSONField(default=dict, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    seen = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["created", "seen"]),
        ]
    
    def __str__(self):
        return f"[{self.get_level_display()}] {self.title} - {self.created.strftime('%H:%M')}"
    
    @classmethod
    def get_unseen_count(cls):
        return cls.objects.filter(seen=False).count()
    

# embedded/models.py
class ActuatorState(models.Model):
    pump = models.BooleanField(default=False)
    light = models.BooleanField(default=False)
    fan = models.BooleanField(default=False)
    alarm = models.BooleanField(default=False)
    heater = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_state(cls):
        state, created = cls.objects.get_or_create(id=1)
        return state
    
    def to_dict(self):
        return {
            "pump": self.pump,
            "light": self.light,
            "fan": self.fan,
            "alarm": self.alarm,
            "heater": self.heater,
        }