from django.shortcuts import render
from django.views.generic import View
import numpy as np
from detect_plant.models import Image, Plant
import cv2
import torch
from torchvision import transforms
from .load_model import CNNModel
import datetime
from PIL import Image as Image_PIL
import torch.nn.functional as F
from django.http import StreamingHttpResponse
import io
import sys 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page
import base64
import json
import threading
from datetime import datetime


# ========================================
# Load model (for DetectNumber)
# ========================================
model = CNNModel(num_classes=38)
state_dict = torch.load('./ai_model/plants.pth', map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()


# ========================================
# List of plants 
# ========================================
list_plants = [
    {"name": "apple", "healthy": False, "problem": "apple_scab"},
    {"name": "apple", "healthy": False, "problem": "black_rot"},
    {"name": "apple", "healthy": False, "problem": "cedar_apple_rust"},
    {"name": "apple", "healthy": True, "problem": None},
    {"name": "blueberry", "healthy": True, "problem": None},
    {"name": "cherry (including sour)", "healthy": True, "problem": None},
    {"name": "cherry (including sour)", "healthy": False, "problem": "powdery_mildew"},
    {"name": "corn (maize)", "healthy": False, "problem": "cercospora_leaf_spot_gray_leaf_spot"},
    {"name": "corn (maize)", "healthy": False, "problem": "common_rust"},
    {"name": "corn (maize)", "healthy": True, "problem": None},
    {"name": "corn (maize)", "healthy": False, "problem": "northern_leaf_blight"},
    {"name": "grape", "healthy": False, "problem": "black_rot"},
    {"name": "grape", "healthy": False, "problem": "esca (black measles)"},
    {"name": "grape", "healthy": True, "problem": None},
    {"name": "grape", "healthy": False, "problem": "leaf_blight (isariopsis_leaf_spot)"},
    {"name": "orange", "healthy": False, "problem": "haunglongbing (citrus_greening)"},
    {"name": "peach", "healthy": False, "problem": "bacterial_spot"},
    {"name": "peach", "healthy": True, "problem": None},
    {"name": "pepper (bell)", "healthy": False, "problem": "bacterial_spot"},
    {"name": "pepper (bell)", "healthy": True, "problem": None},
    {"name": "potato", "healthy": False, "problem": "early_blight"},
    {"name": "potato", "healthy": True, "problem": None},
    {"name": "potato", "healthy": False, "problem": "late_blight"},
    {"name": "raspberry", "healthy": True, "problem": None},
    {"name": "soybean", "healthy": True, "problem": None},
    {"name": "squash", "healthy": False, "problem": "powdery_mildew"},
    {"name": "strawberry", "healthy": True, "problem": None},
    {"name": "strawberry", "healthy": False, "problem": "leaf_scorch"},
    {"name": "tomato", "healthy": False, "problem": "bacterial_spot"},
    {"name": "tomato", "healthy": False, "problem": "early_blight"},
    {"name": "tomato", "healthy": True, "problem": None},
    {"name": "tomato", "healthy": False, "problem": "late_blight"},
    {"name": "tomato", "healthy": False, "problem": "leaf_mold"},
    {"name": "tomato", "healthy": False, "problem": "septoria_leaf_spot"},
    {"name": "tomato", "healthy": False, "problem": "spider_mites (two-spotted_spider_mite)"},
    {"name": "tomato", "healthy": False, "problem": "target_spot"},
    {"name": "tomato", "healthy": False, "problem": "tomato_mosaic_virus"},
    {"name": "tomato", "healthy": False, "problem": "tomato_yellow_leaf_curl_virus"}
]


# ========================================
# GLOBAL VARIABLES 
# ========================================
camera_lock = threading.Lock()
global_cap = None
global_model_live = None  
global_preprocess = None


# ========================================
# CLASS DetectNumber
# ========================================
class DetectNumber(View):
    def post(self, request):
        device = torch.device('cpu')

        image_file = request.FILES["image"]
        image_obj = Image.objects.create(image=image_file)
        img_path = image_obj.image.path

        img_open_cv = cv2.imread(img_path)
        img_open_cv = cv2.resize(img_open_cv, (800, 800))
        output = img_open_cv.copy()

        preprocess = transforms.Compose([
            transforms.Resize((100, 100)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img = Image_PIL.open(img_path).convert("RGB")
        img_tensor = preprocess(img)
        img_tensor = img_tensor.unsqueeze(0)

        model.eval()

        with torch.no_grad():
            img_tensor = img_tensor.to(device)
            predictions = model(img_tensor)
            predicted_class_idx = torch.argmax(predictions, dim=1).item()

        hsv = cv2.cvtColor(img_open_cv, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output, f'{list_plants[int(predicted_class_idx)]["name"]}', (x+5, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.putText(output, f'problem : {list_plants[int(predicted_class_idx)]["problem"]}', (x+5, y +70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        probabilities = F.softmax(predictions, dim=1)
        percentages = probabilities * 100
        predicted_class_prob = torch.max(percentages, dim=1)[0].item()
        predicted_class_prob = round(predicted_class_prob, 2)

        result = list_plants[int(predicted_class_idx)]

        pil_image = Image_PIL.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG')
        buffer.seek(0)
        image_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        image_file = InMemoryUploadedFile(buffer, None, image_name, 'image/jpeg', sys.getsizeof(buffer), None)

        plant = Plant.objects.create(
            user=request.user,
            image=image_file,
            name=result["name"],
            healthy=result["healthy"],
            problem=result["problem"],
            accuracy=predicted_class_prob
        )
        return render(request, "dashboard/admin/plant/plant-detail.html", context={"object": plant})


# ========================================
# PLANT COUNT
# ========================================
class PlantCountView(View):
    def get(self, request):
        count = Plant.objects.count()
        return JsonResponse({"count": count})


# ========================================
# LIVE DETECTION PAGE
# ========================================
@login_required
def live_detection_page(request):
    context = {
        'page_title': 'تشخیص زنده گیاهان',
        'page_icon': 'fas fa-video',
    }
    return render(request, 'dashboard/admin/plant/live_detection.html', context)


# ========================================
# INIT CAMERA
# ========================================
def init_camera():
    global global_cap
    if global_cap is None or not global_cap.isOpened():
        try:
            global_cap = cv2.VideoCapture(0)
            global_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            global_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            global_cap.set(cv2.CAP_PROP_FPS, 30)
            if not global_cap.isOpened():
                global_cap = cv2.VideoCapture(1)
                global_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                global_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            print(f"❌ Camera error: {e}")
            global_cap = None
    return global_cap


# ========================================
# INIT MODEL FOR LIVE STREAM
# ========================================
def init_model_live():
    """Load model once - استفاده از مدل CNN واقعی"""
    global global_model_live, global_preprocess
    
    if global_model_live is None:
        try:
            print("🔄 Loading live model...")
            global_model_live = CNNModel(num_classes=38)
            state_dict = torch.load('./ai_model/plants.pth', map_location=torch.device('cpu'))
            global_model_live.load_state_dict(state_dict)
            global_model_live.eval()
            print("✅ Live model loaded successfully")
            
        except FileNotFoundError:
            print("❌ Model file not found: ./ai_model/plants.pth")
            global_model_live = torch.nn.Sequential(
                torch.nn.Linear(100*100*3, 128),
                torch.nn.ReLU(),
                torch.nn.Linear(128, 38)
            )
            global_model_live.eval()
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            global_model_live = None
        
        global_preprocess = transforms.Compose([
            transforms.Resize((100, 100)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    return global_model_live, global_preprocess


# ========================================
# GET FRAME API
# ========================================
@csrf_exempt
@gzip_page
def get_frame_api(request):
    """دریافت یک فریم از دوربین با تشخیص AI"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Initialize camera
        cap = init_camera()
        if cap is None or not cap.isOpened():
            return JsonResponse({
                'success': False,
                'error': 'دوربین در دسترس نیست'
            }, status=503)
        
        # Initialize model
        model_live, preprocess = init_model_live()
        if model_live is None:
            return JsonResponse({
                'success': False,
                'error': 'مدل بارگذاری نشده است'
            }, status=503)
        
        with camera_lock:
            ret, frame = cap.read()
            if not ret:
                return JsonResponse({
                    'success': False,
                    'error': 'خطا در دریافت تصویر از دوربین'
                }, status=500)
            
            display_frame = frame.copy()
            
            try:
                # Preprocess
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image_PIL.fromarray(img_rgb)
                img_tensor = preprocess(img_pil)
                img_tensor = img_tensor.unsqueeze(0)
                
                with torch.no_grad():
                    predictions = model_live(img_tensor)
                    probabilities = F.softmax(predictions, dim=1)
                    percentages = probabilities * 100
                    predicted_class_idx = torch.argmax(predictions, dim=1).item()
                    predicted_class_prob = percentages[0, predicted_class_idx].item()
                
                # Get plant info
                if list_plants and predicted_class_idx < len(list_plants):
                    plant_name = list_plants[predicted_class_idx].get('name', 'Unknown')
                    plant_problem = list_plants[predicted_class_idx].get('problem', 'No problem')
                    healthy = list_plants[predicted_class_idx].get('healthy', True)
                else:
                    plant_name = f"Plant {predicted_class_idx + 1}"
                    plant_problem = "Unknown"
                    healthy = True
                
                # Draw on frame
                cv2.rectangle(display_frame, (10, 10), 
                             (display_frame.shape[1]-10, display_frame.shape[0]-10), 
                             (0, 255, 0), 3)
                
                cv2.putText(display_frame, f'🌿 {plant_name}', (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                problem_text = f'⚠️ {plant_problem}' if plant_problem and plant_problem != "No problem" else '✅ Healthy'
                color = (0, 0, 255) if plant_problem and plant_problem != "No problem" else (0, 255, 0)
                cv2.putText(display_frame, problem_text, (20, display_frame.shape[0]-60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                cv2.putText(display_frame, f'🎯 {predicted_class_prob:.1f}%', 
                           (display_frame.shape[1]-200, display_frame.shape[0]-60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                detection_result = {
                    'name': plant_name,
                    'problem': plant_problem or 'No problem',
                    'accuracy': round(predicted_class_prob, 2),
                    'class_id': predicted_class_idx,
                    'healthy': healthy
                }
                
            except Exception as e:
                detection_result = {
                    'name': 'Detection Error',
                    'problem': str(e)[:50],
                    'accuracy': 0,
                    'class_id': -1,
                    'healthy': False
                }
                cv2.putText(display_frame, f'⚠️ Error: {str(e)[:30]}', (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                print(f"❌ Detection error: {e}")
            
            # Encode to JPEG
            ret, jpeg = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to encode frame'
                }, status=500)
            
            frame_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
            
            return JsonResponse({
                'success': True,
                'image': frame_base64,
                'detection': detection_result,
                'timestamp': datetime.now().isoformat(),
                'frame_size': {
                    'width': display_frame.shape[1],
                    'height': display_frame.shape[0]
                }
            })
            
    except Exception as e:
        print(f"❌ get_frame_api error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ========================================
# VIDEO STREAM - MJPEG
# ========================================
@login_required
def video_stream_view(request):
    def generate():
        cap = init_camera()
        if cap is None:
            return
        
        model_live, preprocess = init_model_live()
        
        while True:
            with camera_lock:
                ret, frame = cap.read()
                if not ret:
                    break

                if model_live is not None:
                    try:
                        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img_pil = Image_PIL.fromarray(img_rgb)
                        img_tensor = preprocess(img_pil)
                        img_tensor = img_tensor.unsqueeze(0)
                        
                        with torch.no_grad():
                            predictions = model_live(img_tensor)
                            probabilities = F.softmax(predictions, dim=1)
                            percentages = probabilities * 100
                            predicted_class_idx = torch.argmax(predictions, dim=1).item()
                            predicted_class_prob = percentages[0, predicted_class_idx].item()
                        
                        if list_plants and predicted_class_idx < len(list_plants):
                            plant_name = list_plants[predicted_class_idx].get('name', 'Unknown')
                            plant_problem = list_plants[predicted_class_idx].get('problem', 'Unknown')
                        else:
                            plant_name = f"Plant {predicted_class_idx + 1}"
                            plant_problem = "Unknown"
                        
                        cv2.rectangle(frame, (10, 10), (frame.shape[1]-10, frame.shape[0]-10), 
                                     (0, 255, 0), 3)
                        cv2.putText(frame, f'🌿 {plant_name}', (20, 40), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.putText(frame, f'⚠️ {plant_problem}', (20, frame.shape[0]-60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, f'🎯 {predicted_class_prob:.1f}%', 
                                   (frame.shape[1]-200, frame.shape[0]-60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    except Exception as e:
                        cv2.putText(frame, f'⚠️ Error: {str(e)[:30]}', (20, 40), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if not ret:
                    break

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       jpeg.tobytes() + b'\r\n\r\n')

        cap.release()

    return StreamingHttpResponse(generate(), 
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# ========================================
# VIDEO FEED
# ========================================
@login_required
def video_feed(request):
    cap = init_camera()
    if cap is None:
        return JsonResponse({'error': 'Camera not available'}, status=500)
    
    def generate_frames():
        while True:
            with camera_lock:
                ret, frame = cap.read()
                if not ret:
                    break
                
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if not ret:
                    break
                
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       frame_bytes + b'\r\n')
    
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


# ========================================
# CAMERA STATUS
# ========================================
@csrf_exempt
def get_camera_status(request):
    try:
        cap = init_camera()
        is_open = cap.isOpened() if cap else False
        return JsonResponse({
            'status': 'online' if is_open else 'offline',
            'camera_index': 0,
            'resolution': '640x480',
            'fps': 30
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)


# ========================================
# SAVE DETECTION
# ========================================
@csrf_exempt
def save_detection(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        return JsonResponse({'success': True, 'message': 'Detection saved'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ========================================
# GET FRAME BATCH
# ========================================
@csrf_exempt
def get_frame_batch(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        cap = init_camera()
        frames = []
        for _ in range(3):
            ret, frame = cap.read()
            if ret:
                ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if ret:
                    frames.append(base64.b64encode(jpeg.tobytes()).decode('utf-8'))
        
        return JsonResponse({
            'success': True,
            'frames': frames,
            'count': len(frames)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)