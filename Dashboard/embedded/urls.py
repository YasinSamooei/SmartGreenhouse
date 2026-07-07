from django.urls import path
from embedded.views import (GetLogStats, GetSensorHistory, SendSensorsValue,
DisplaySensorsValue, DisplaySensorsPage, ToggleActuator, GetEvents, MarkEventAsSeen,
SendCommandToESP, GetActuatorStatus, SendAutoMode )

app_name = "embedded"

urlpatterns = [
    # Display page
    path("display/sensors/page", DisplaySensorsPage.as_view(), name="display-sensors-page"),

    # Display information inside the panel
    path("get/sensor/data", DisplaySensorsValue.as_view(), name="get_sensor_data"),
    path('get/sensor/history/', GetSensorHistory.as_view(), name='get_sensor_history'),
    path('get/log/stats/', GetLogStats.as_view(), name='get_log_stats'),
    path('get/events/', GetEvents.as_view(), name='get_events'),
    path('api/events/mark-seen/', MarkEventAsSeen.as_view(), name='mark_event_seen'),
    path('toggle-actuator/', ToggleActuator.as_view(), name='toggle_actuator'),

    # Communication with Micro
    path("send/sensor/value", SendSensorsValue.as_view(), name="send_sensors_value"),
    path('api/send-command/', SendCommandToESP.as_view(), name='send_command'),
    path('api/get-actuator-status/', GetActuatorStatus.as_view(), name='get_actuator_status'),
    path('api/send-auto-mode/', SendAutoMode.as_view(), name='send_auto_mode'),
]
