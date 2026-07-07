// ========================================
// LIVE DETECTION - FETCH API METHOD
// ========================================

class LiveDetectionManager {
    constructor(options = {}) {
        this.options = {
            frameInterval: 150,  // ms between frames (~7 FPS)
            maxRetries: 3,
            retryDelay: 2000,
            autoStart: true,
            ...options
        };
        
        this.isRunning = false;
        this.intervalId = null;
        this.frameCount = 0;
        this.fps = 0;
        this.lastFpsUpdate = Date.now();
        this.retryCount = 0;
        this.detectionHistory = [];
        this.maxHistory = 10;
        
        // DOM Elements
        this.canvas = document.getElementById('videoCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Status elements
        this.statusEl = document.getElementById('streamStatus');
        this.fpsEl = document.getElementById('fpsDisplay');
        this.plantNameEl = document.getElementById('plantName');
        this.plantProblemEl = document.getElementById('plantProblem');
        this.plantAccuracyEl = document.getElementById('plantAccuracy');
        this.detectionTimeEl = document.getElementById('detectionTime');
        
        // Stats elements
        this.statsEl = document.getElementById('detectionStats');
        
        // Bind methods
        this.fetchFrame = this.fetchFrame.bind(this);
        this.start = this.start.bind(this);
        this.stop = this.stop.bind(this);
        this.takeScreenshot = this.takeScreenshot.bind(this);
        
        // Event listeners
        this.setupEventListeners();
        
        // Auto start if enabled
        if (this.options.autoStart) {
            this.start();
        }
    }
    
    setupEventListeners() {
        // Start button
        const startBtn = document.getElementById('startStreamBtn');
        if (startBtn) {
            startBtn.addEventListener('click', this.start);
        }
        
        // Stop button
        const stopBtn = document.getElementById('stopStreamBtn');
        if (stopBtn) {
            stopBtn.addEventListener('click', this.stop);
        }
        
        // Screenshot button
        const screenshotBtn = document.getElementById('screenshotBtn');
        if (screenshotBtn) {
            screenshotBtn.addEventListener('click', this.takeScreenshot);
        }
        
        // Fullscreen button
        const fullscreenBtn = document.getElementById('fullscreenBtn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                const container = document.querySelector('.stream-container');
                if (!document.fullscreenElement) {
                    container?.requestFullscreen().catch(() => {});
                } else {
                    document.exitFullscreen();
                }
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            switch(e.key.toLowerCase()) {
                case ' ':
                    e.preventDefault();
                    this.isRunning ? this.stop() : this.start();
                    break;
                case 's':
                    if (!e.ctrlKey) this.takeScreenshot();
                    break;
                case 'f':
                    if (!e.ctrlKey) {
                        const container = document.querySelector('.stream-container');
                        if (!document.fullscreenElement) {
                            container?.requestFullscreen().catch(() => {});
                        } else {
                            document.exitFullscreen();
                        }
                    }
                    break;
            }
        });
        
        // Handle visibility change (pause when tab hidden)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.isRunning) {
                this.pause();
            } else if (!document.hidden && this.isRunning) {
                this.resume();
            }
        });
    }
    
    async fetchFrame() {
        if (!this.isRunning) return;
        
        try {
            const response = await fetch('/api/get-frame/', {
                headers: {
                    'Accept': 'application/json',
                },
                cache: 'no-cache'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Unknown error');
            }
            
            // Reset retry count on success
            this.retryCount = 0;
            
            // Display frame
            this.displayFrame(data);
            
            // Update detection info
            this.updateDetectionInfo(data.detection, data.timestamp);
            
            // Update status
            this.updateStatus('🟢 آنلاین', 'online');
            
            // Update stats
            this.updateStats();
            
        } catch (error) {
            console.error('Error fetching frame:', error);
            this.retryCount++;
            
            if (this.retryCount >= this.options.maxRetries) {
                this.updateStatus('⚠️ خطا در ارتباط', 'error');
                this.stop();
                setTimeout(() => {
                    if (!this.isRunning) {
                        this.start();
                    }
                }, this.options.retryDelay);
            } else {
                this.updateStatus(`🔄 تلاش مجدد (${this.retryCount}/${this.options.maxRetries})`, 'warning');
            }
        }
    }
    
    displayFrame(data) {
        if (!data.image || !this.canvas) return;
        
        const image = new Image();
        image.onload = () => {
            // Set canvas size if needed
            if (this.canvas.width !== image.width || this.canvas.height !== image.height) {
                this.canvas.width = image.width;
                this.canvas.height = image.height;
                this.canvas.style.width = '100%';
                this.canvas.style.height = 'auto';
            }
            
            // Draw image
            this.ctx.drawImage(image, 0, 0);
            
            // Update FPS
            this.frameCount++;
            const now = Date.now();
            if (now - this.lastFpsUpdate > 1000) {
                this.fps = this.frameCount;
                this.frameCount = 0;
                this.lastFpsUpdate = now;
                if (this.fpsEl) {
                    this.fpsEl.textContent = `${this.fps} FPS`;
                }
            }
        };
        image.onerror = () => {
            console.error('Failed to load image');
        };
        image.src = 'data:image/jpeg;base64,' + data.image;
    }
    
    updateDetectionInfo(detection, timestamp) {
        if (!detection) return;
        
        // Update plant name
        if (this.plantNameEl) {
            this.plantNameEl.textContent = detection.name || '--';
            this.plantNameEl.className = 'value success';
        }
        
        // Update problem
        if (this.plantProblemEl) {
            const problem = detection.problem || 'No problem';
            this.plantProblemEl.textContent = problem;
            this.plantProblemEl.className = 'value ' + 
                (problem.toLowerCase().includes('no problem') ? 'success' : 'danger');
        }
        
        // Update accuracy
        if (this.plantAccuracyEl) {
            const accuracy = detection.accuracy || 0;
            this.plantAccuracyEl.textContent = accuracy > 0 ? `${accuracy}%` : '--';
            this.plantAccuracyEl.className = 'value ' + 
                (accuracy > 80 ? 'success' : accuracy > 50 ? 'warning' : 'danger');
        }
        
        // Update time
        if (this.detectionTimeEl && timestamp) {
            const date = new Date(timestamp);
            this.detectionTimeEl.textContent = date.toLocaleTimeString('fa-IR');
        }
        
        // Add to history
        this.detectionHistory.push({
            ...detection,
            timestamp: timestamp
        });
        if (this.detectionHistory.length > this.maxHistory) {
            this.detectionHistory.shift();
        }
        
        // Update stats
        this.updateDetectionStats();
    }
    
    updateDetectionStats() {
        if (!this.statsEl || this.detectionHistory.length === 0) return;
        
        // Calculate statistics from history
        const uniquePlants = new Set(this.detectionHistory.map(d => d.name));
        const avgAccuracy = this.detectionHistory.reduce((sum, d) => sum + (d.accuracy || 0), 0) / 
                           this.detectionHistory.length;
        const problems = this.detectionHistory.filter(d => 
            d.problem && !d.problem.toLowerCase().includes('no problem')
        ).length;
        
        this.statsEl.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">تشخیص‌ها</span>
                <span class="stat-value">${this.detectionHistory.length}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">گونه‌ها</span>
                <span class="stat-value">${uniquePlants.size}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">میانگین دقت</span>
                <span class="stat-value">${avgAccuracy.toFixed(1)}%</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">مشکلات</span>
                <span class="stat-value ${problems > 0 ? 'danger' : 'success'}">${problems}</span>
            </div>
        `;
    }
    
    updateStatus(text, status) {
        if (this.statusEl) {
            this.statusEl.textContent = text;
            this.statusEl.className = `stream-status ${status}`;
        }
    }
    
    updateStats() {
        // Additional stats update if needed
    }
    
    start() {
        if (this.isRunning) {
            console.warn('Stream is already running');
            return;
        }
        
        this.isRunning = true;
        this.retryCount = 0;
        this.updateStatus('🟢 در حال اتصال...', 'online');
        
        // Clear canvas
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
        
        // Start fetching
        this.intervalId = setInterval(this.fetchFrame, this.options.frameInterval);
        
        // Fetch first frame immediately
        setTimeout(this.fetchFrame, 100);
        
        console.log('✅ Live detection started');
        this.showToast('استریم شروع شد', 'success');
    }
    
    stop() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        this.updateStatus('⏹️ متوقف شده', 'offline');
        console.log('⏹️ Live detection stopped');
        this.showToast('استریم متوقف شد', 'info');
    }
    
    pause() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
            console.log('⏸️ Stream paused (tab hidden)');
        }
    }
    
    resume() {
        if (this.isRunning && !this.intervalId) {
            this.intervalId = setInterval(this.fetchFrame, this.options.frameInterval);
            this.fetchFrame();
            console.log('▶️ Stream resumed');
        }
    }
    
    takeScreenshot() {
        if (!this.canvas) return;
        
        const link = document.createElement('a');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        link.download = `plant_detection_${timestamp}.png`;
        link.href = this.canvas.toDataURL('image/png');
        link.click();
        
        this.showToast('📸 عکس ذخیره شد', 'success');
    }
    
    showToast(message, type = 'info') {
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`[${type}] ${message}`);
        }
    }
}

// ========================================
// INITIALIZE ON PAGE LOAD
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the stream manager with custom options
    const streamManager = new LiveDetectionManager({
        frameInterval: 150,  // ~7 FPS (good balance)
        maxRetries: 3,
        retryDelay: 2000,
        autoStart: true
    });
    
    // Expose to window for debugging
    window.streamManager = streamManager;
    
    console.log('✅ Live Detection Manager initialized');
    console.log('📸 Press SPACE to start/stop, S for screenshot, F for fullscreen');
});

// ========================================
// WEB VITALITY CHECK (keep-alive)
// ========================================

// Check if camera is still available
setInterval(async function() {
    try {
        const response = await fetch('/api/camera-status/');
        const data = await response.json();
        
        if (data.status === 'offline' && window.streamManager?.isRunning) {
            console.warn('Camera went offline, reconnecting...');
            window.streamManager.stop();
            setTimeout(() => {
                window.streamManager.start();
            }, 2000);
        }
    } catch (error) {
        // Silent fail
    }
}, 30000);  // Check every 30 seconds