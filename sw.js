// Bump this on every deploy - old caches are dropped on activate, and it's
// what forces a stale service worker to notice there's an update at all.
var CACHE_NAME = 'corgdoku-v7';
var ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

self.addEventListener('install', function(event){
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache){ return cache.addAll(ASSETS); })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(event){
  event.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.filter(function(k){ return k !== CACHE_NAME; }).map(function(k){ return caches.delete(k); }));
    })
  );
  self.clients.claim();
});

// Network-first: always prefer a fresh copy when online (so a new deploy
// shows up the moment the app is reopened), only falling back to the cache
// when there's no network at all. A cache-first strategy was tried initially
// for offline support, but it meant every reopen showed last version's
// content while quietly fetching this version for "next time" - so updates
// never visibly landed. Freshness matters more than offline support here.
self.addEventListener('fetch', function(event){
  if(event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).then(function(response){
      if(response && response.status === 200 && response.type === 'basic'){
        var copy = response.clone();
        caches.open(CACHE_NAME).then(function(cache){ cache.put(event.request, copy); });
      }
      return response;
    }).catch(function(){
      return caches.match(event.request);
    })
  );
});
