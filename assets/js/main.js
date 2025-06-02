// 다크 모드 관리
document.addEventListener('alpine:init', () => {
    Alpine.store('darkMode', {
        dark: false,
        toggle() {
            this.dark = !this.dark;
            this.updateTheme();
        },
        updateTheme() {
            if (this.dark) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        }
    });

    // 모바일 메뉴 관리
    Alpine.data('mobileMenu', () => ({
        open: false,
        toggle() {
            this.open = !this.open;
        }
    }));
});

// 스크롤 애니메이션
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach((el) => {
        observer.observe(el);
    });
});

// 코드 하이라이팅
if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
}

// 스크롤 진행률 표시
window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.querySelector('.scroll-progress').style.width = scrolled + '%';
});

// 페이지 로드 시 시스템 다크 모드 설정 확인
window.addEventListener('DOMContentLoaded', () => {
    const darkMode = Alpine.store('darkMode');
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        darkMode.dark = true;
        darkMode.updateTheme();
    }
});

// 검색 기능
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', debounce(async (e) => {
            const query = e.target.value;
            if (query.length < 2) {
                searchResults.innerHTML = '';
                return;
            }

            try {
                // 여기에 실제 검색 로직 구현
                const results = await searchContent(query);
                displaySearchResults(results);
            } catch (error) {
                console.error('검색 중 오류 발생:', error);
            }
        }, 300));
    }
}

// 유틸리티 함수
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    initSearch();
});

// 문의 양식 처리
function handleSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        company: formData.get('company'),
        email: formData.get('email'),
        type: formData.get('type'),
        message: formData.get('message')
    };

    // 여기에 실제 이메일 전송 로직 구현
    // 예: API 엔드포인트로 데이터 전송
    console.log('문의 데이터:', data);

    // 사용자에게 성공 메시지 표시
    alert('문의가 성공적으로 전송되었습니다. 빠른 시일 내에 답변 드리겠습니다.');
    
    // 폼 초기화
    event.target.reset();
    
    return false;
} 