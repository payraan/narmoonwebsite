// Service Worker برای PWA نارموون
const CACHE_NAME = 'narmoon-v2.0.0';
const urlsToCache = [
  '/',
  '/static/css/style.min.css',        // ✅ minified
  '/static/js/main.min.js',           // ✅ minified  
  '/static/images/logo.png',
  '/static/images/logo-white.png',
  '/static/images/hero-dashboard.webp', // ✅ WebP
  '/static/images/favicon.ico',
  '/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap'
];

// نصب Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('✅ Cache باز شد');
        return cache.addAll(urlsToCache);
      })
  );
});

// فعال کردن Service Worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Cache قدیمی حذف شد:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// دریافت درخواست‌ها
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // اگر در cache بود، برگردان
        if (response) {
          return response;
        }
        
        // در غیر این صورت از شبکه دریافت کن
        return fetch(event.request).then(function(response) {
          // بررسی validity پاسخ
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // کپی پاسخ برای cache
          var responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then(function(cache) {
              cache.put(event.request, responseToCache);
            });

          return response;
        }).catch(function() {
          // اگر آفلاین بود و صفحه HTML بود
          if (event.request.destination === 'document') {
            return caches.match('/');
          }
        });
      })
  );
});

// Push Notification (آماده برای آینده)
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'پیام جدید از نارموون',
    icon: '/static/images/logo-192.png',
    badge: '/static/images/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'مشاهده',
        icon: '/static/images/favicon.ico'
      },
      {
        action: 'close', 
        title: 'بستن'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('نارموون', options)
  );
});
