from django.urls import path
from detect_plant.views import (DetectNumber, live_detection_page, PlantCountView
                                , video_feed, get_camera_status, get_frame_api,
                                save_detection,get_frame_batch)

app_name = "plant"

urlpatterns = [
    path("detect/plants", DetectNumber.as_view(), name="plant-detect"),
    path('plant-count/', PlantCountView.as_view(), name='plant-count'),

    path('video-stream/', live_detection_page, name='video_stream'),
    path('video-feed/', video_feed, name='video_feed'),
    
    path('api/get-frame/', get_frame_api, name='get_frame_api'),
    path('api/camera-status/', get_camera_status, name='camera_status'),
    path('api/save-detection/', save_detection, name='save_detection'),
    path('api/get-frame-batch/', get_frame_batch, name='get_frame_batch'),
]

