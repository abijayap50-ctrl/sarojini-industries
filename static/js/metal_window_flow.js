/**
 * Sarojini Steel - Realistic Flowing Metal Window with Blended Background
 * 
 * Features:
 * - Real photorealistic architectural steel window & security grill (No box container, 100% blended)
 * - 3D GPU-accelerated Perspective Floating & Flowing Physics
 * - Full 3D tilt tracking mouse pointer & mobile touch
 * - Dynamic metallic specular glint reflection following cursor
 * - Realistic arc-welding spark particle burst on click / tap / touch
 */

(function () {
    class RealisticMetalWindowHero {
        constructor() {
            this.container = document.getElementById('flowingWindowStage');
            this.heroSection = document.getElementById('heroSection');
            this.glintEl = document.getElementById('flowingWindowGlint');
            this.sparkCanvas = document.getElementById('sparkOverlayCanvas');

            if (!this.container || !this.sparkCanvas) return;

            this.ctx = this.sparkCanvas.getContext('2d');
            this.dpr = window.devicePixelRatio || 1;

            // 3D Tilt angles (in degrees)
            this.rotX = -2;
            this.rotY = 8;
            this.rotZ = 0;
            this.targetRotX = -2;
            this.targetRotY = 8;
            this.scale = 1.0;
            this.targetScale = 1.0;

            // Flowing wave offsets
            this.time = 0;
            this.floatX = 0;
            this.floatY = 0;
            this.floatRotZ = 0;

            // Mouse / Touch tracking
            this.isPointerActive = false;
            this.pointerX = 0;
            this.pointerY = 0;

            // Welding spark particle system
            this.sparks = [];

            this.init();
        }

        init() {
            this.resizeCanvas();
            window.addEventListener('resize', () => this.resizeCanvas());

            // Pointer Tracking across the entire Hero Section
            window.addEventListener('mousemove', (e) => this.onMouseMove(e));

            if (this.heroSection) {
                this.heroSection.addEventListener('mouseleave', () => this.onPointerLeave());
            }

            // Direct Interaction on the Metal Window
            this.container.addEventListener('mouseenter', () => {
                this.targetScale = 1.05;
                if (this.glintEl) this.glintEl.style.opacity = '1';
            });

            this.container.addEventListener('mouseleave', () => {
                this.targetScale = 1.0;
                if (this.glintEl) this.glintEl.style.opacity = '0';
            });

            this.container.addEventListener('click', (e) => {
                const rect = this.container.getBoundingClientRect();
                const sparkX = e.clientX - rect.left;
                const sparkY = e.clientY - rect.top;
                this.spawnSparks(sparkX, sparkY, 35);
            });

            // Mobile Touch Events
            this.container.addEventListener('touchstart', (e) => {
                if (e.touches.length > 0) {
                    const rect = this.container.getBoundingClientRect();
                    const touch = e.touches[0];
                    const relX = touch.clientX - rect.left;
                    const relY = touch.clientY - rect.top;
                    this.updateTiltFromPos(touch.clientX, touch.clientY);
                    this.spawnSparks(relX, relY, 28);
                }
            }, { passive: true });

            this.container.addEventListener('touchmove', (e) => {
                if (e.touches.length > 0) {
                    const touch = e.touches[0];
                    this.updateTiltFromPos(touch.clientX, touch.clientY);
                }
            }, { passive: true });

            this.container.addEventListener('touchend', () => {
                this.onPointerLeave();
            });

            // Expose globally for any UI trigger
            window.triggerWeldingSparks = (clientX, clientY) => {
                const rect = this.container.getBoundingClientRect();
                const x = clientX ? clientX - rect.left : rect.width / 2;
                const y = clientY ? clientY - rect.top : rect.height / 2;
                this.spawnSparks(x, y, 40);
            };

            // Start Animation Loop
            requestAnimationFrame((ts) => this.animate(ts));
        }

        resizeCanvas() {
            if (!this.sparkCanvas || !this.container) return;
            const rect = this.container.getBoundingClientRect();
            this.sparkCanvas.width = Math.floor(rect.width * this.dpr);
            this.sparkCanvas.height = Math.floor(rect.height * this.dpr);
            this.sparkCanvas.style.width = `${rect.width}px`;
            this.sparkCanvas.style.height = `${rect.height}px`;
        }

        onMouseMove(e) {
            const rect = this.container.getBoundingClientRect();
            // Check if hero is in viewport
            if (rect.bottom < 0 || rect.top > window.innerHeight) return;

            const cX = rect.left + rect.width / 2;
            const cY = rect.top + rect.height / 2;
            const dist = Math.hypot(e.clientX - cX, e.clientY - cY);

            // Responsive range: up to 1000px from window
            if (dist < 1000) {
                this.updateTiltFromPos(e.clientX, e.clientY);
            } else if (this.isPointerActive) {
                this.onPointerLeave();
            }
        }

        updateTiltFromPos(clientX, clientY) {
            const rect = this.container.getBoundingClientRect();
            const cX = rect.left + rect.width / 2;
            const cY = rect.top + rect.height / 2;

            // Normalized distance [-1, 1]
            const normX = Math.max(-1.4, Math.min(1.4, (clientX - cX) / (window.innerWidth * 0.4)));
            const normY = Math.max(-1.4, Math.min(1.4, (clientY - cY) / (window.innerHeight * 0.4)));

            // 3D Tilt angles (facing the pointer)
            this.targetRotY = normX * 18;
            this.targetRotX = -normY * 14;
            this.targetScale = 1.03;
            this.isPointerActive = true;

            // Move Specular Glint Reflection across the realistic glass & metal
            if (this.glintEl) {
                const relX = clientX - rect.left;
                const relY = clientY - rect.top;
                this.glintEl.style.opacity = '1';
                this.glintEl.style.background = `radial-gradient(circle 220px at ${relX}px ${relY}px, rgba(255, 255, 255, 0.42), rgba(245, 158, 11, 0.22) 40%, transparent 75%)`;
            }
        }

        onPointerLeave() {
            this.isPointerActive = false;
            // Return to graceful default resting angle
            this.targetRotY = 6;
            this.targetRotX = -2;
            this.targetScale = 1.0;
            if (this.glintEl) {
                this.glintEl.style.opacity = '0';
            }
        }

        spawnSparks(x, y, count) {
            const colors = ['#F59E0B', '#FBBF24', '#FCD34D', '#FFFFFF', '#EA580C', '#38BDF8'];

            for (let i = 0; i < count; i++) {
                const angle = Math.random() * Math.PI * 2;
                const speed = 3.0 + Math.random() * 8.0;
                this.sparks.push({
                    x: x,
                    y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed - 2.5,
                    size: 1.5 + Math.random() * 2.8,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    life: 1.0,
                    decay: 0.015 + Math.random() * 0.025,
                    gravity: 0.2
                });
            }
        }

        animate(timestamp) {
            this.time = timestamp;

            // Smooth spring damping interpolation
            this.rotX += (this.targetRotX - this.rotX) * 0.07;
            this.rotY += (this.targetRotY - this.rotY) * 0.07;
            this.scale += (this.targetScale - this.scale) * 0.07;

            // Continuous "flowing" wave oscillation
            const t = this.time * 0.0016;
            this.floatY = Math.sin(t) * 15;
            this.floatX = Math.cos(t * 0.75) * 8;
            this.floatRotZ = Math.sin(t * 0.5) * 1.6;

            // Apply 3D GPU Transform
            if (this.container) {
                this.container.style.transform = `perspective(1200px) translate3d(${this.floatX}px, ${this.floatY}px, 0) rotateX(${this.rotX}deg) rotateY(${this.rotY}deg) rotateZ(${this.floatRotZ}deg) scale3d(${this.scale}, ${this.scale}, ${this.scale})`;
            }

            // Draw Welding Sparks Overlay
            this.renderSparks();

            requestAnimationFrame((ts) => this.animate(ts));
        }

        renderSparks() {
            if (!this.ctx) return;
            const w = this.sparkCanvas.width / this.dpr;
            const h = this.sparkCanvas.height / this.dpr;

            this.ctx.save();
            this.ctx.scale(this.dpr, this.dpr);
            this.ctx.clearRect(0, 0, w, h);

            for (let i = this.sparks.length - 1; i >= 0; i--) {
                const s = this.sparks[i];
                s.x += s.vx;
                s.y += s.vy;
                s.vy += s.gravity;
                s.vx *= 0.96;
                s.vy *= 0.96;
                s.life -= s.decay;

                if (s.life <= 0) {
                    this.sparks.splice(i, 1);
                    continue;
                }

                this.ctx.save();
                this.ctx.globalAlpha = Math.max(0, s.life);
                this.ctx.fillStyle = s.color;
                this.ctx.shadowColor = '#F59E0B';
                this.ctx.shadowBlur = 10;

                this.ctx.beginPath();
                this.ctx.arc(s.x, s.y, s.size * s.life, 0, Math.PI * 2);
                this.ctx.fill();

                // Spark streak / tail
                this.ctx.strokeStyle = s.color;
                this.ctx.lineWidth = s.size * 0.7;
                this.ctx.beginPath();
                this.ctx.moveTo(s.x, s.y);
                this.ctx.lineTo(s.x - s.vx * 2.2, s.y - s.vy * 2.2);
                this.ctx.stroke();

                this.ctx.restore();
            }

            this.ctx.restore();
        }
    }

    // Auto-init on page load
    window.addEventListener('DOMContentLoaded', () => {
        new RealisticMetalWindowHero();
    });

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        new RealisticMetalWindowHero();
    }
})();
