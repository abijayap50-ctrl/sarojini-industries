/**
 * SAROJINI STEEL WORKS • MOBILE PHOTO UPLOAD & INSTANT PREVIEW HELPER
 * Enhances mobile file inputs with instant camera previews and touch-friendly controls.
 */

document.addEventListener('DOMContentLoaded', function () {
    initMobilePhotoUploaders();

    // Re-run if inline forms are dynamically added (e.g. Django's "Add another" button)
    const observer = new MutationObserver(function (mutations) {
        initMobilePhotoUploaders();
    });
    const inlineGroups = document.querySelectorAll('.inline-group');
    inlineGroups.forEach(group => {
        observer.observe(group, { childList: true, subtree: true });
    });
});

function initMobilePhotoUploaders() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(input => {
        // Prevent duplicate initializations
        if (input.dataset.previewInitialized === "true") return;
        input.dataset.previewInitialized = "true";

        const container = input.closest('.form-row') || input.parentElement;
        if (!container) return;

        // Create touch-friendly trigger button
        const uploadBtn = document.createElement('label');
        uploadBtn.className = 'custom-file-upload-btn';
        uploadBtn.innerHTML = `
            <span class="icon">📷</span>
            <span>Take Photo with Camera or Choose from Gallery</span>
        `;
        uploadBtn.setAttribute('for', input.id || (input.id = 'file_' + Math.random().toString(36).substr(2, 9)));

        // Create container for live preview
        let previewBox = container.querySelector('.admin-live-preview-box');
        if (!previewBox) {
            previewBox = document.createElement('div');
            previewBox.className = 'admin-live-preview-box';
            previewBox.style.display = 'none';
            previewBox.innerHTML = `
                <div class="admin-preview-badge">✨ Selected Photo Preview</div>
                <img src="" alt="Selected Photo" />
                <div style="padding: 8px 12px; font-size: 12px; color: #94a3b8; display: flex; justify-content: space-between; align-items: center;">
                    <span class="file-name" style="font-weight: 600; color: #f1f5f9;"></span>
                    <span class="file-size" style="color: #f59e0b;"></span>
                </div>
            `;
            // Insert preview box after input
            input.parentElement.appendChild(previewBox);
        }

        // Insert touch button right above input
        input.parentElement.insertBefore(uploadBtn, input);

        // Hide default ugly file input slightly but keep accessible
        input.style.display = 'none';

        // Check if there is already an existing image link (Django's "Currently: ...")
        const currentLink = container.querySelector('a[href*="/media/"], a[href*="cloudinary"], a[href*="http"]');
        if (currentLink && !previewBox.querySelector('img').src) {
            const currentImgUrl = currentLink.getAttribute('href');
            if (currentImgUrl && (currentImgUrl.match(/\.(jpeg|jpg|gif|png|webp)/i) || currentImgUrl.includes('cloudinary'))) {
                previewBox.style.display = 'block';
                previewBox.querySelector('.admin-preview-badge').textContent = '📸 Current Saved Photo';
                previewBox.querySelector('img').src = currentImgUrl;
                previewBox.querySelector('.file-name').textContent = 'Active on Website';
            }
        }

        // Handle file change event
        input.addEventListener('change', function (e) {
            const file = e.target.files && e.target.files[0];
            if (!file) return;

            // Update button label
            uploadBtn.innerHTML = `
                <span class="icon">🔄</span>
                <span>Change Photo (${file.name.substring(0, 18)}...)</span>
            `;

            // Validate if it is an image
            if (!file.type.startsWith('image/')) {
                previewBox.style.display = 'none';
                return;
            }

            const reader = new FileReader();
            reader.onload = function (event) {
                previewBox.style.display = 'block';
                previewBox.querySelector('.admin-preview-badge').textContent = '✨ New Photo Selected (Tap Save Below)';
                previewBox.querySelector('img').src = event.target.result;
                previewBox.querySelector('.file-name').textContent = file.name;
                previewBox.querySelector('.file-size').textContent = (file.size / 1024 > 1024) 
                    ? (file.size / (1024 * 1024)).toFixed(1) + ' MB' 
                    : (file.size / 1024).toFixed(0) + ' KB';
            };
            reader.readAsDataURL(file);
        });
    });
}
