# embedded/services.py
from django.utils import timezone
from .models import SystemEvent, SensorData
import logging

logger = logging.getLogger(__name__)

class EventLogger:
    """Smart event logging management with repetition prevention"""
    
    # Alert thresholds
    THRESHOLDS = {
        "temp_high": 30,
        "temp_low": 18,
        "hum_high": 80,
        "hum_low": 55,
        "soil_dry": 40,
        "gas_danger": 61,
        "co2_high": 1000,
    }
    
    _states = {
        "temp_status": "normal",
        "hum_status": "normal",
        "soil_status": "normal",
        "gas_status": "normal",
        "pump_status": False,
        "fan_status": False,
        "heater_status": False,
        "alarm_status": False,
        "device_status": "online",
    }
    
    @classmethod
    def process_sensor_data(cls, data):
        events = []
        
        co2_value = data.get("gas", 0) * 4.5 + 300
        
        #1. Check the temperature
        temp = data.get("temperature", 0)
        if temp > cls.THRESHOLDS["temp_high"] and cls._states["temp_status"] != "high":
            cls._states["temp_status"] = "high"
            events.append(cls._create_event(
                "temp_high",
                "🔥 دمای گلخانه بالا رفت",
                f"دمای فعلی: {temp:.1f}°C (حد مجاز: {cls.THRESHOLDS['temp_high']}°C)",
                "critical",
                data
            ))
        elif temp < cls.THRESHOLDS["temp_low"] and cls._states["temp_status"] != "low":
            cls._states["temp_status"] = "low"
            events.append(cls._create_event(
                "temp_low",
                "❄️ دمای گلخانه پایین آمد",
                f"دمای فعلی: {temp:.1f}°C (حد مجاز: {cls.THRESHOLDS['temp_low']}°C)",
                "warning",
                data
            ))
        elif cls._states["temp_status"] in ["high", "low"] and cls.THRESHOLDS["temp_low"] <= temp <= cls.THRESHOLDS["temp_high"]:
            cls._states["temp_status"] = "normal"
            events.append(cls._create_event(
                "temp_normal",
                "✅ دمای گلخانه به حالت نرمال برگشت",
                f"دمای فعلی: {temp:.1f}°C",
                "success",
                data
            ))
        
        #2. Check the humidity
        hum = data.get("humidity", 0)
        if hum > cls.THRESHOLDS["hum_high"] and cls._states["hum_status"] != "high":
            cls._states["hum_status"] = "high"
            events.append(cls._create_event(
                "hum_high",
                "💧 رطوبت هوا زیاد شد",
                f"رطوبت فعلی: {hum:.1f}% (حد مجاز: {cls.THRESHOLDS['hum_high']}%)",
                "warning",
                data
            ))
        elif hum < cls.THRESHOLDS["hum_low"] and cls._states["hum_status"] != "low":
            cls._states["hum_status"] = "low"
            events.append(cls._create_event(
                "hum_low",
                "🌵 رطوبت هوا کم شد",
                f"رطوبت فعلی: {hum:.1f}% (حد مجاز: {cls.THRESHOLDS['hum_low']}%)",
                "warning",
                data
            ))
        elif cls._states["hum_status"] in ["high", "low"] and cls.THRESHOLDS["hum_low"] <= hum <= cls.THRESHOLDS["hum_high"]:
            cls._states["hum_status"] = "normal"
            events.append(cls._create_event(
                "hum_normal",
                "✅ رطوبت هوا به حالت نرمال برگشت",
                f"رطوبت فعلی: {hum:.1f}%",
                "success",
                data
            ))
        
        #3. Check soil moisture
        soil = data.get("soil", 0)
        if soil < cls.THRESHOLDS["soil_dry"] and cls._states["soil_status"] != "dry":
            cls._states["soil_status"] = "dry"
            events.append(cls._create_event(
                "soil_dry",
                "🌱 رطوبت خاک کم شد!",
                f"رطوبت فعلی خاک: {soil}% (حداقل مجاز: {cls.THRESHOLDS['soil_dry']}%)",
                "critical",
                data
            ))
        elif cls._states["soil_status"] == "dry" and soil >= cls.THRESHOLDS["soil_dry"] + 10:
            cls._states["soil_status"] = "normal"
            events.append(cls._create_event(
                "soil_wet",
                "✅ رطوبت خاک به حد مطلوب رسید",
                f"رطوبت فعلی خاک: {soil}%",
                "success",
                data
            ))
        
        #4. Gas check
        gas = data.get("gas", 0)
        if gas >= cls.THRESHOLDS["gas_danger"] and cls._states["gas_status"] != "danger":
            cls._states["gas_status"] = "danger"
            events.append(cls._create_event(
                "gas_danger",
                "⚠️ نشت گاز تشخیص داده شد!",
                f"سطح گاز: {gas} ppm (حد مجاز: {cls.THRESHOLDS['gas_danger']} ppm)",
                "critical",
                data
            ))
        elif cls._states["gas_status"] == "danger" and gas < cls.THRESHOLDS["gas_danger"] - 10:
            cls._states["gas_status"] = "normal"
            events.append(cls._create_event(
                "gas_normal",
                "✅ سطح گاز به حالت عادی برگشت",
                f"سطح گاز فعلی: {gas} ppm",
                "success",
                data
            ))
        
        # 5. Checking operator changes
        pump = data.get("pump", False)
        if pump != cls._states["pump_status"]:
            cls._states["pump_status"] = pump
            events.append(cls._create_event(
                "pump_on" if pump else "pump_off",
                "🚿 پمپ آبیاری " + ("روشن شد" if pump else "خاموش شد"),
                f"وضعیت پمپ: {'فعال' if pump else 'غیرفعال'}",
                "info" if not pump else "success",
                data
            ))
        
        fan = data.get("fan", False)
        if fan != cls._states["fan_status"]:
            cls._states["fan_status"] = fan
            events.append(cls._create_event(
                "fan_on" if fan else "fan_off",
                "🌀 فن تهویه " + ("روشن شد" if fan else "خاموش شد"),
                f"وضعیت فن: {'فعال' if fan else 'غیرفعال'}",
                "info",
                data
            ))
        
        created_events = []
        for event_data in events:
            try:
                event = SystemEvent.objects.create(**event_data)
                created_events.append(event)
            except Exception as e:
                logger.error(f"Error creating event: {e}")
        
        return created_events
    
    @classmethod
    def _create_event(cls, event_type, title, message, level, data):
        return {
            "title": title,
            "message": message,
            "level": level,
            "event_type": event_type,
            "sensor_data": {
                "temperature": data.get("temperature"),
                "humidity": data.get("humidity"),
                "soil": data.get("soil"),
                "gas": data.get("gas"),
                "ldr": data.get("ldr"),
            }
        }
    
    @classmethod
    def check_device_status(cls, is_online):
        """بررسی وضعیت اتصال دستگاه"""
        if is_online and cls._states["device_status"] != "online":
            cls._states["device_status"] = "online"
            return cls._create_event(
                "device_online",
                "🟢 دستگاه آنلاین شد",
                "ارتباط با دستگاه برقرار شد",
                "success",
                {}
            )
        elif not is_online and cls._states["device_status"] != "offline":
            cls._states["device_status"] = "offline"
            return cls._create_event(
                "device_offline",
                "🔴 دستگاه آفلاین شد!",
                "ارتباط با دستگاه قطع شده است",
                "critical",
                {}
            )
        return None