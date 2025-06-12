const CACHE_NAME = 'educonnect-cache-v2'; // تغيير الإصدار لتحديث الكاش
const urlsToCache = [
  '/',
  '/index.html',
  '/aboutUS.html',
  '/messenger.html',
  '/post.html',
  '/posts.html',
  '/profile.html',
  '/login.html',
  '/register.html',
  '/styles.css',
  '/css/aboutUS.css',
  '/css/index.css',
  '/css/messenger.css',
  '/css/post.css',
  '/css/posts.css',
  '/css/login.css',
  '/css/profile.css',
  '/css/register.css',
  '/js/auth.js',
  '/js/api.js',
  '/images/MainImage.jpg',
  '/images/hero-bg.jpg',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/manifest.json',
  '/vendor/idb/index.js',
  '/offline.html'
];

// Install Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Caching resources');
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Activate Service Worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Handle Fetch Requests
self.addEventListener('fetch', event => {
  const requestUrl = new URL(event.request.url);

  // Bypass cache for API requests
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(
          JSON.stringify({ ok: false, error: 'No internet connection' }),
          {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'application/json' }
          }
        );
      })
    );
    return;
  }

  // Cache-first strategy for other requests
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then(networkResponse => {
        if (!networkResponse || networkResponse.status !== 200 || event.request.method !== 'GET') {
          return networkResponse;
        }
        return caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      }).catch(() => {
        // Return offline page for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/offline.html');
        }
        return new Response('', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      });
    })
  );
});

// Handle Push Notifications (Optional)
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : { title: 'EduConnect', body: 'New update available!' };
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-192x192.png'
    })
  );
});

// Handle Notification Click
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/index.html')
  );
});