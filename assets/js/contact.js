document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    const messageDiv = document.getElementById('messageDiv');

    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // 버튼 비활성화 및 로딩 상태 표시
            submitButton.disabled = true;
            submitButton.innerHTML = '전송 중...';
            messageDiv.innerHTML = '';

            try {
                const formData = {
                    name: document.getElementById('name').value,
                    company: document.getElementById('company').value,
                    email: document.getElementById('email').value,
                    inquiry_type: document.getElementById('inquiryType').value,
                    message: document.getElementById('message').value
                };

                // 상대 경로로 API 호출
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok) {
                    // 성공 메시지 표시
                    messageDiv.innerHTML = `
                        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                            <span class="block sm:inline">${result.message}</span>
                        </div>
                    `;
                    contactForm.reset();
                } else {
                    throw new Error(result.detail || '문의 전송에 실패했습니다.');
                }
            } catch (error) {
                // 에러 메시지 표시
                messageDiv.innerHTML = `
                    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                        <span class="block sm:inline">${error.message}</span>
                    </div>
                `;
            } finally {
                // 버튼 상태 복구
                submitButton.disabled = false;
                submitButton.innerHTML = '전송';
            }
        });
    }
}); 