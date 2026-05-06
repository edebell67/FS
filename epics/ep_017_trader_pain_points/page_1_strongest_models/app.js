document.addEventListener('DOMContentLoaded', () => {
    const leadForm = document.getElementById('lead-form');
    const toast = document.getElementById('toast');

    const showToast = (message, isError = false) => {
        toast.textContent = message;
        toast.style.background = isError ? '#ef4444' : '#16a34a';
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    };

    leadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const pageId = 'strongest_models';
        const painPointKey = 'finding_right_models';

        const submitBtn = leadForm.querySelector('button');
        const originalText = submitBtn.querySelector('span').textContent;
        submitBtn.querySelector('span').textContent = 'Processing...';
        submitBtn.disabled = true;

        // JSON Backend URL (Points to local Flask or deployed Serverless function)
        const BACKEND_URL = 'https://ep-017.onrender.com/api/capture_lead';

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, page_id: pageId, pain_point_key: painPointKey }),
            });

            if (response.ok) {
                showToast('Success! Your trial is being activated.');
                leadForm.reset();
            } else {
                throw new Error('Capture failed');
            }
        } catch (error) {
            console.error('Capture error:', error);
            showToast('Something went wrong. Please try again.', true);
        } finally {
            submitBtn.querySelector('span').textContent = originalText;
            submitBtn.disabled = false;
        }
    });

    const performanceItems = document.querySelectorAll('.performance-item');
    performanceItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        item.style.transition = `all 0.6s cubic-bezier(0.16, 1, 0.3, 1) ${0.5 + index * 0.1}s`;
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 100);
    });
});
