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
        const pageId = 'early_momentum';
        const painPointKey = 'early_momentum_detection';

        const submitBtn = leadForm.querySelector('button');
        const originalText = submitBtn.querySelector('span').textContent;
        submitBtn.querySelector('span').textContent = 'Syncing...';
        submitBtn.disabled = true;

        const BACKEND_URL = 'https://ep-017.onrender.com/api/capture_lead';

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, page_id: pageId, pain_point_key: painPointKey }),
            });

            if (response.ok) {
                showToast('Success! Your edge is being prepared.');
                leadForm.reset();
            } else {
                throw new Error('Capture failed');
            }
        } catch (error) {
            console.error('Lead capture error:', error);
            showToast('Something went wrong. Please try again.', true);
        } finally {
            submitBtn.querySelector('span').textContent = originalText;
            submitBtn.disabled = false;
        }
    });

    const momentumItems = document.querySelectorAll('.momentum-item');
    momentumItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        item.style.transition = `all 0.6s var(--ease-out-expo) ${0.5 + index * 0.1}s`;
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 100);
    });
});
