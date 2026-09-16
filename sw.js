// Bump this on every deploy - old caches are dropped on activate, and it's
// what forces a stale service worker to notice there's an update at all.
var CACHE_NAME = 'corgdoku-v31';
var CORGI_IDS = [
  'classic','happy','wink','sleepy','blep','cream','fox','sable','tri','patch','shades','party',
  'crowned','batter','bookworm','gentleman','darling','frosty','lucky','smitten','dino','bandit',
  'beats','jolly','officer','topgun','blossom','astro','sheriff','buccaneer','retro','rudolph',
  'monocle','merlin','serene','puddle','maverick','unicorn','rex','nerdy','boater','pirate',
  'shark','royal','crush','chill','ranger','sherlock','dj','cadet','blitzen','captain',
  'aviator','shady','witchy','clover','sweetheart','snowflake','rookie','angel','toughpup','cozy'
];
var PAW_IDS = ['chunky','slim','heart','tilted','walking','scratched','dainty','singlepad','outline','trail'];
var DANCE_IDS = ['dance-1-stand','dance-2-pawsup','dance-3-hop','dance-4-sidelean','dance-5-spin','dance-6-backtostand'];
var ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './privacy.html',
  './terms.html',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './art/mad-scientist-corgi.png',
  './vendor/fonts.css',
  './vendor/fonts/nunito.woff2',
  './vendor/fonts/quicksand.woff2',
  './vendor/confetti.browser.min.js'
]
  .concat(CORGI_IDS.map(function(id){ return './art/corgis/' + id + '.png'; }))
  .concat(PAW_IDS.map(function(id){ return './art/paws/' + id + '.png'; }))
  .concat(DANCE_IDS.map(function(id){ return './art/dance/' + id + '.png'; }));

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
//
// The catch that took a while to spot: a plain fetch() still consults the
// HTTP cache, and GitHub Pages serves index.html with max-age=600. So this
// was really "up to ten minutes stale first, network second", and a fresh
// deploy genuinely would not appear on reopening until that expired.
// Documents now bypass the HTTP cache outright. Everything else keeps using
// it on purpose - re-downloading the corgi art on every single launch would
// be a far worse trade than a slightly stale image that never changes anyway.
self.addEventListener('fetch', function(event){
  if(event.request.method !== 'GET') return;
  var isDoc = event.request.mode === 'navigate';
  // A navigate-mode Request can't be passed to the Request constructor, so
  // the bypass is expressed as a fresh fetch of the same URL.
  var fromNetwork = isDoc
    ? fetch(event.request.url, {cache:'reload', credentials:'same-origin'})
    : fetch(event.request);
  event.respondWith(
    fromNetwork.then(function(response){
      if(response && response.status === 200 && response.type === 'basic'){
        var copy = response.clone();
        var key = isDoc ? event.request.url : event.request;
        caches.open(CACHE_NAME).then(function(cache){ cache.put(key, copy); });
      }
      return response;
    }).catch(function(){
      return caches.match(event.request);
    })
  );
});
