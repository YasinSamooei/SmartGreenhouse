import json
import logging
from django.shortcuts import render
from django.views.generic import View
from embedded.models import SensorData, SystemEvent, ActuatorState
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import EventLogger
from django.utils import timezone
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

ESP_IP = getattr(settings, 'ESP_IP', '192.168.56.1')
ESP_PORT = getattr(settings, 'ESP_PORT', 8080)
ESP_API_URL = f"http://{ESP_IP}:{ESP_PORT}/"

class DisplaySensorsPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard/admin/embedded/display.html', {
            'settings': settings,
        })


class DisplaySensorsValue(View):
    def get(self, request):
        latest_sensor_data = SensorData.objects.order_by("-created").first()

        if latest_sensor_data is None:
            data = {
                "temperature": 0.0,
                "humidity": 0.0,
                "soil": 0,
                "gas": 0,
                "ldr": 0,
                "fan": False,
                "pump": False,
                "heater": False,
                "alarm": False,
                "light": False,
                "auto": True,
            }
            return JsonResponse(data)

        data = {
            "temperature": latest_sensor_data.temperature,
            "humidity": latest_sensor_data.humidity,
            "soil": latest_sensor_data.soil,
            "gas": latest_sensor_data.gas,
            "ldr": latest_sensor_data.ldr,
            "fan": latest_sensor_data.fan,
            "pump": latest_sensor_data.pump,
            "heater": latest_sensor_data.heater,
            "alarm": latest_sensor_data.alarm,
            "light": latest_sensor_data.light,
            "auto": latest_sensor_data.auto if hasattr(latest_sensor_data, 'auto') else True,
            "ip": ESP_IP,
        }
        return JsonResponse(data)


class GetSensorHistory(View):
    
    def get(self, request):
        range_hours = int(request.GET.get('range', 12))
        
        # One record every 5 seconds = 12 records per minute = 720 records per hour
        RECORDS_PER_HOUR = 720
        MAX_DISPLAY_POINTS = 1000
        
        records_needed = range_hours * RECORDS_PER_HOUR
        max_records = 10000
        if records_needed > max_records:
            records_needed = max_records
        
        sensor_data = SensorData.objects.order_by('-created')[:records_needed]
        sensor_data = list(reversed(sensor_data))
        
        if len(sensor_data) == 0:
            return JsonResponse({
                "temp": [], "hum": [], "soil": [], 
                "co2": [], "lux": [], "gas": [],
                "message": "هیچ داده‌ای در دیتابیس وجود ندارد",
                "_meta": {
                    "total": 0, 
                    "range": range_hours,
                    "records_needed": records_needed,
                    "sample_rate": "0%"
                }
            })
        
        original_count = len(sensor_data)
        step = 1
        
        if original_count > MAX_DISPLAY_POINTS:
            step = max(1, original_count // MAX_DISPLAY_POINTS)
            if original_count // step < 100:
                step = max(1, original_count // 100)
            sensor_data = sensor_data[::step]
        
        sampled_count = len(sensor_data)
        
        history = {
            "temp": [],
            "hum": [],
            "soil": [],
            "co2": [],
            "lux": [],
            "gas": []
        }
        
        for record in sensor_data:
            history["temp"].append(float(record.temperature))
            history["hum"].append(float(record.humidity))
            history["soil"].append(float(record.soil))
            history["co2"].append(float(record.gas * 4.5 + 300))
            history["lux"].append(float(record.ldr))
            history["gas"].append(float(record.gas))
        
        sample_rate = (sampled_count / records_needed * 100) if records_needed > 0 else 0
        
        history["_meta"] = {
            "range_hours": range_hours,
            "records_needed": records_needed,
            "original_count": original_count,
            "sampled_count": sampled_count,
            "sample_step": step,
            "sample_rate": f"{sample_rate:.1f}%",
            "max_display_points": MAX_DISPLAY_POINTS,
            "message": self._get_sample_message(range_hours, original_count, sampled_count)
        }
        
        return JsonResponse(history)
    
    def _get_sample_message(self, range_hours, original_count, sampled_count):
        if original_count == 0:
            return "هیچ داده‌ای موجود نیست"
        if original_count <= 500:
            return f"نمایش {original_count} نقطه داده"
        if sampled_count < original_count:
            return f"نمایش {sampled_count} نقطه از {original_count} نقطه (بهینه‌سازی شده)"
        return f"نمایش {original_count} نقطه داده"


class ToggleActuator(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            actuator = data.get('actuator')
            state = data.get('status')
            
            actuator_state = ActuatorState.get_state()
            
            if actuator == 'P':
                actuator_state.pump = state
            elif actuator == 'LI':
                actuator_state.light = state
            elif actuator == 'F':
                actuator_state.fan = state
            elif actuator == 'A':
                actuator_state.alarm = state
            elif actuator == 'HE':
                actuator_state.heater = state
            actuator_state.save()
            
            latest = SensorData.objects.order_by("-created").first()
            if latest:
                if actuator == 'P':
                    latest.pump = state
                elif actuator == 'LI':
                    latest.light = state
                elif actuator == 'F':
                    latest.fan = state
                elif actuator == 'A':
                    latest.alarm = state
                elif actuator == 'HE':
                    latest.heater = state
                latest.save()
            
            EventLogger.process_actuator_change(actuator, state)
            
            return JsonResponse({"success": True, "message": f"Actuator {actuator} updated"})
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class GetLogStats(View):
    """Get storage statistics"""
    def get(self, request):
        total_records = SensorData.objects.count()
        first_record = SensorData.objects.order_by("created").first()
        last_record = SensorData.objects.order_by("-created").first()
        
        bytes_per_record = 200
        used_bytes = total_records * bytes_per_record
        used_mb = used_bytes / (1024 * 1024)
        used_gb = used_bytes / (1024 * 1024 * 1024)
        
        total_gb = 7.4 
        used_percent = (used_gb / total_gb) * 100 if total_gb > 0 else 0
        
        data = {
            "total_records": total_records,
            "first_record": first_record.created.strftime("%Y/%m/%d %H:%M") if first_record else "--",
            "last_record": last_record.created.strftime("%Y/%m/%d %H:%M") if last_record else "--",
            "sd_usage": f"{used_gb:.3f} GB / {total_gb} GB",
            "sd_percent": min(100, used_percent),
            "used_mb": f"{used_mb:.2f} MB",
            "record_size": f"{bytes_per_record} bytes/record",
            "sample_rates": {
                "1h": f"{min(100, (SensorData.objects.count() if SensorData.objects.count() > 0 else 1) / 360 * 100):.1f}%",
                "6h": f"{min(100, SensorData.objects.count() / 2160 * 100):.1f}%",
                "24h": f"{min(100, SensorData.objects.count() / 8640 * 100):.1f}%",
            }
        }
        return JsonResponse(data)


class SendSensorsValue(APIView):
    def post(self, request):
        try:
            data = request.data if hasattr(request, "data") else json.loads(request.body.decode("utf-8"))
            
            def to_bool(value):
                if isinstance(value, bool):
                    return value
                if isinstance(value, (int, float)):
                    return bool(value)
                if isinstance(value, str):
                    return value.strip().lower() in {"1", "true", "yes", "on"}
                return False
            
            sensor_data = SensorData.objects.create(
                temperature=float(data.get("temperature", 0.0)),
                humidity=float(data.get("humidity", 0.0)),
                soil=int(data.get("soil", 0)),
                gas=int(data.get("gas", 0)),
                ldr=int(data.get("ldr", 0)),
                fan=to_bool(data.get("fan", False)),
                pump=to_bool(data.get("pump", False)),
                heater=to_bool(data.get("heater", False)),
                alarm=to_bool(data.get("alarm", False)),
                light=to_bool(data.get("light", False)),
                auto=to_bool(data.get("auto", True)),
            )
            
            events = EventLogger.process_sensor_data({
                "temperature": sensor_data.temperature,
                "humidity": sensor_data.humidity,
                "soil": sensor_data.soil,
                "gas": sensor_data.gas,
                "ldr": sensor_data.ldr,
                "pump": sensor_data.pump,
                "fan": sensor_data.fan,
                "heater": sensor_data.heater,
                "alarm": sensor_data.alarm,
                "light": sensor_data.light,
                "auto": sensor_data.auto,
            })
            
            print("========== SENSOR DATA ==========")
            for key, value in data.items():
                print(f"{key}: {value}")
            print(f"Events created: {len(events)}")
            print("=================================")
            
            return JsonResponse({
                "message": "sensor data received",
                "id": sensor_data.id,
                "events": len(events),
            })
            
        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=400)


class GetEvents(View):
    """Receive system events"""
    
    def get(self, request):
        limit = int(request.GET.get('limit', 20))
        include_seen = request.GET.get('include_seen', 'false').lower() == 'true'
        
        queryset = SystemEvent.objects.all()
        if not include_seen:
            queryset = queryset.filter(seen=False)
        
        events = queryset[:limit]
        
        data = {
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "message": event.message,
                    "level": event.level,
                    "event_type": event.event_type,
                    "created": event.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "seen": event.seen,
                    "sensor_data": event.sensor_data,
                }
                for event in events
            ],
            "unseen_count": SystemEvent.get_unseen_count(),
            "total_count": SystemEvent.objects.count(),
        }
        
        return JsonResponse(data)


class MarkEventAsSeen(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            
            if event_id:
                event = SystemEvent.objects.get(id=event_id)
                event.seen = True
                event.read_at = timezone.now()
                event.save()
                return JsonResponse({"success": True})
            else:
                count = SystemEvent.objects.filter(seen=False).update(
                    seen=True, 
                    read_at=timezone.now()
                )
                return JsonResponse({"success": True, "count": count})
                
        except SystemEvent.DoesNotExist:
            return JsonResponse({"success": False, "error": "Event not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class SendCommandToESP(View):
    """Send command to PICOW (MicroPython)"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            actuator = data.get('actuator')
            status = data.get('status')
            
            valid_actuators = ['F', 'P', 'HE', 'A', 'LI']
            if actuator not in valid_actuators:
                return JsonResponse({
                    'success': False,
                    'error': f'Actuator must be one of: {", ".join(valid_actuators)}'
                }, status=400)
            
            if status not in [0, 1]:
                return JsonResponse({
                    'success': False,
                    'error': 'Status must be 0 or 1'
                }, status=400)
            
            ESP_URL = ESP_API_URL
            
            logger.info(f"Attempting to connect to PICOW at: {ESP_URL}")
            
            try:
                response = requests.post(
                    ESP_URL,
                    json={actuator: status},
                    headers={'Content-Type': 'application/json'},
                    timeout=2
                )
                
                if response.status_code == 200:
                    try:
                        actuator_state, created = ActuatorState.objects.get_or_create(id=1)
                        if actuator == 'F':
                            actuator_state.fan = bool(status)
                        elif actuator == 'P':
                            actuator_state.pump = bool(status)
                        elif actuator == 'HE':
                            actuator_state.heater = bool(status)
                        elif actuator == 'A':
                            actuator_state.alarm = bool(status)
                        elif actuator == 'LI':
                            actuator_state.light = bool(status)
                        actuator_state.save()
                        
                        latest = SensorData.objects.order_by("-created").first()
                        if latest:
                            if actuator == 'F':
                                latest.fan = bool(status)
                            elif actuator == 'P':
                                latest.pump = bool(status)
                            elif actuator == 'HE':
                                latest.heater = bool(status)
                            elif actuator == 'A':
                                latest.alarm = bool(status)
                            elif actuator == 'LI':
                                latest.light = bool(status)
                            latest.save()
                    except Exception as db_error:
                        logger.error(f"Database error: {db_error}")
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Command sent to PICOW',
                        'actuator': actuator,
                        'status': status,
                        'esp_response': response.json() if response.text else {}
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': f'PICOW returned status {response.status_code}',
                        'response': response.text
                    }, status=500)
                    
            except requests.exceptions.ConnectionError:
                return JsonResponse({
                    'success': False,
                    'error': f'PICOW is not reachable at {ESP_URL}. Make sure PICOW is powered on and connected to WiFi.',
                    'esp_url': ESP_URL,
                    'hint': 'Check PICOW IP address and WiFi connection'
                }, status=503)
                
            except requests.exceptions.Timeout:
                return JsonResponse({
                    'success': False,
                    'error': 'PICOW connection timeout. PICOW might be busy or unreachable.',
                    'esp_url': ESP_URL
                }, status=504)
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Error connecting to PICOW: {str(e)}'
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class SendAutoMode(View):
    """Send automatic/manual mode to PICOW"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            auto_mode = data.get('auto', True)
            
            ESP_URL = ESP_API_URL
            
            try:
                response = requests.post(
                    ESP_URL,
                    json={'AUTO': 1 if auto_mode else 0},
                    headers={'Content-Type': 'application/json'},
                    timeout=2
                )
                
                if response.status_code == 200:
                    latest = SensorData.objects.order_by("-created").first()
                    if latest:
                        latest.auto = auto_mode
                        latest.save()
                    
                    SystemEvent.objects.create(
                        title=f"حالت {'اتوماتیک' if auto_mode else 'دستی'}",
                        message=f"سیستم به حالت {'اتوماتیک' if auto_mode else 'دستی'} تغییر کرد",
                        level='info',
                        event_type='mode_change',
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'message': f"Mode changed to {'AUTO' if auto_mode else 'MANUAL'}",
                        'auto': auto_mode
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': f'PICOW returned status {response.status_code}'
                    }, status=500)
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class GetActuatorStatus(View):
    """Get current status of actuators from PICOW"""
    
    def get(self, request):
        try:
            ESP_URL = ESP_API_URL
            
            response = requests.get(ESP_URL, timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                
                actuator_names = {
                    'F': 'fan',
                    'P': 'pump',
                    'HE': 'heater',
                    'A': 'alarm',
                    'LI': 'light'
                }
                
                result = {}
                for esp_key, django_key in actuator_names.items():
                    result[django_key] = bool(data.get(esp_key, 0))
                
                result['ip'] = ESP_IP
                
                return JsonResponse({
                    'success': True,
                    'actuators': result,
                    'raw': data,
                    'ip': ESP_IP
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'PICOW returned status {response.status_code}'
                }, status=500)
                
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False,
                'error': f'Cannot connect to PICOW at {ESP_API_URL}',
                'ip': ESP_IP
            }, status=503)
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'PICOW connection timeout',
                'ip': ESP_IP
            }, status=504)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
                'ip': ESP_IP
            }, status=500)