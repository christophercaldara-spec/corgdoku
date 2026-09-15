// ---------------------------------------------------------------------------
// Accounts, automatic backup, and packs.
//
// This file is loaded LAZILY - only when the player signs in, or on launch if
// they already have. A signed-out player never fetches it, so the app keeps
// its original promise: nothing leaves the phone and it works with no network
// at all. Signing in is opt-in, and the game never waits on it.
//
// The phone stays the source of truth. The cloud is a mirror we push to and
// merge from, never something the game reads to decide what to show. If every
// request here fails, play is unaffected.
// ---------------------------------------------------------------------------
(function(){
  "use strict";

  var SDK = 'https://www.gstatic.com/firebasejs/11.10.0/';
  var app = null, auth = null, db = null, M = null;
  var user = null;
  var ready = null;
  var listeners = [];

  // Unambiguous alphabet: no O/0, no I/1/L, so a code read aloud or copied off
  // a screen can't land on the wrong pack.
  var CODE_ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ';

  function state(){
    return {
      signedIn: !!user,
      uid: user ? user.uid : null,
      name: user ? (user.displayName || 'Corgi fan') : null
    };
  }
  function notify(){
    var s = state();
    listeners.forEach(function(fn){ try{ fn(s); }catch(e){} });
  }

  // Loads the SDK once. Everything else awaits this.
  function load(){
    if(ready) return ready;
    ready = Promise.all([
      import(SDK + 'firebase-app.js'),
      import(SDK + 'firebase-auth.js'),
      import(SDK + 'firebase-firestore.js')
    ]).then(function(mods){
      M = {a: mods[0], auth: mods[1], fs: mods[2]};
      app  = M.a.initializeApp(window.CORGDOKU_FIREBASE);
      auth = M.auth.getAuth(app);
      db   = M.fs.getFirestore(app);
      M.auth.onAuthStateChanged(auth, function(u){
        user = u || null;
        try{
          if(user) localStorage.setItem('corgdoku_signedin', '1');
          else localStorage.removeItem('corgdoku_signedin');
        }catch(e){}
        notify();
        if(user) syncNow();
      });
      // A redirect sign-in lands back here on return.
      return M.auth.getRedirectResult(auth).catch(function(){});
    });
    return ready;
  }

  function userDoc(){ return M.fs.doc(db, 'users', user.uid); }
  function packDoc(code){ return M.fs.doc(db, 'packs', code); }

  // -------------------------------------------------------------------------
  // Merge. Both sides may have moved on since they last agreed - a phone that
  // was offline for a week still holds real progress. So nothing is ever
  // overwritten wholesale: the level takes whichever is further, and each stat
  // takes its better value, which for a time means the LOWER one.
  // -------------------------------------------------------------------------
  var LOWER_IS_BETTER = {fastestWin: true};

  function mergeSnapshots(a, b){
    if(!a) return b;
    if(!b) return a;
    var out = {
      level: Math.max(a.level || 1, b.level || 1),
      stats: {},
      corgi: b.corgi || a.corgi,
      paw: b.paw || a.paw,
      name: b.name || a.name,
      pack: b.pack || a.pack || null
    };
    var keys = {};
    Object.keys(a.stats || {}).forEach(function(k){ keys[k] = 1; });
    Object.keys(b.stats || {}).forEach(function(k){ keys[k] = 1; });
    Object.keys(keys).forEach(function(k){
      var av = (a.stats || {})[k], bv = (b.stats || {})[k];
      if(typeof av !== 'number'){ out.stats[k] = bv; return; }
      if(typeof bv !== 'number'){ out.stats[k] = av; return; }
      out.stats[k] = LOWER_IS_BETTER[k] ? Math.min(av, bv) : Math.max(av, bv);
    });
    return out;
  }

  // Pull cloud, merge with local, write the result back, hand it to the game.
  function syncNow(){
    if(!user || !window.CorgdokuGame) return Promise.resolve(null);
    var local = window.CorgdokuGame.snapshot();
    return M.fs.getDoc(userDoc()).then(function(snap){
      var remote = snap.exists() ? snap.data() : null;
      var merged = mergeSnapshots(remote, local);
      merged.name = merged.name || (user.displayName || 'Corgi fan');
      window.CorgdokuGame.apply(merged);
      var write = {};
      Object.keys(merged).forEach(function(k){ write[k] = merged[k]; });
      write.updatedAt = M.fs.serverTimestamp();
      return M.fs.setDoc(userDoc(), write, {merge:true}).then(function(){
        return merged.pack ? pushToPack(merged) : null;
      }).then(function(){ return merged; });
    }).catch(function(e){
      // Offline or rules said no - the phone still has everything.
      return null;
    });
  }

  // Each pack document carries a small public summary per member, so showing
  // the whole pack costs one read instead of one per person.
  function pushToPack(snap){
    if(!user || !snap || !snap.pack) return Promise.resolve();
    var entry = {};
    entry['members.' + user.uid] = {
      name: snap.name || (user.displayName || 'Corgi fan'),
      level: snap.level || 1,
      stats: snap.stats || {},
      corgi: snap.corgi || 'classic',
      updatedAt: Date.now()
    };
    return M.fs.updateDoc(packDoc(snap.pack), entry).catch(function(){});
  }

  function randomCode(){
    var s = '';
    for(var i=0;i<6;i++) s += CODE_ALPHABET[Math.floor(Math.random()*CODE_ALPHABET.length)];
    return s;
  }

  var API = {
    // True without loading anything, so launch can decide whether to bother.
    wasSignedIn: function(){
      try{ return localStorage.getItem('corgdoku_signedin') === '1'; }catch(e){ return false; }
    },
    onState: function(fn){ listeners.push(fn); if(M) fn(state()); },
    state: state,

    start: function(){ return load().then(function(){ notify(); }); },

    signIn: function(){
      return load().then(function(){
        var provider = new M.auth.GoogleAuthProvider();
        // Popup first: it keeps the game's state alive. Some Android webviews
        // block it, and there the redirect is the only thing that works.
        return M.auth.signInWithPopup(auth, provider).catch(function(err){
          var code = err && err.code ? err.code : '';
          if(code.indexOf('popup') >= 0 || code.indexOf('operation-not-supported') >= 0){
            return M.auth.signInWithRedirect(auth, provider);
          }
          throw err;
        });
      });
    },

    signOut: function(){
      return load().then(function(){ return M.auth.signOut(auth); });
    },

    sync: syncNow,

    setName: function(name){
      if(!user) return Promise.resolve();
      return M.fs.setDoc(userDoc(), {name:name}, {merge:true}).then(function(){
        var local = window.CorgdokuGame.snapshot();
        local.name = name;
        return pushToPack(local);
      });
    },

    // Creates a pack with a code nobody else holds. Retried because two people
    // could pick the same code at the same moment; the transaction is what
    // makes "nobody else holds it" actually true rather than merely likely.
    createPack: function(packName){
      if(!user) return Promise.reject(new Error('not signed in'));
      var attempt = function(tries){
        var code = randomCode();
        return M.fs.runTransaction(db, function(tx){
          return tx.get(packDoc(code)).then(function(existing){
            if(existing.exists()) throw new Error('taken');
            var members = {};
            members[user.uid] = {
              name: user.displayName || 'Corgi fan',
              level: 1, stats: {}, corgi: 'classic', updatedAt: Date.now()
            };
            tx.set(packDoc(code), {
              name: packName || 'The Pack',
              createdBy: user.uid,
              createdAt: M.fs.serverTimestamp(),
              members: members
            });
          });
        }).then(function(){ return code; }).catch(function(e){
          if(tries > 0 && e && e.message === 'taken') return attempt(tries - 1);
          throw e;
        });
      };
      return attempt(5).then(function(code){
        return M.fs.setDoc(userDoc(), {pack:code}, {merge:true}).then(function(){
          return syncNow().then(function(){ return code; });
        });
      });
    },

    joinPack: function(code){
      if(!user) return Promise.reject(new Error('not signed in'));
      code = (code || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
      return M.fs.getDoc(packDoc(code)).then(function(snap){
        if(!snap.exists()) throw new Error('no-such-pack');
        return M.fs.setDoc(userDoc(), {pack:code}, {merge:true});
      }).then(function(){ return syncNow(); }).then(function(){ return code; });
    },

    leavePack: function(){
      if(!user) return Promise.resolve();
      return M.fs.setDoc(userDoc(), {pack:null}, {merge:true});
    },

    // Whole pack in one read. Sorted by level, the thing people came to see.
    readPack: function(code){
      if(!code) return Promise.resolve(null);
      return load().then(function(){
        return M.fs.getDoc(packDoc(code));
      }).then(function(snap){
        if(!snap.exists()) return null;
        var data = snap.data();
        var members = Object.keys(data.members || {}).map(function(uid){
          var m = data.members[uid];
          m.uid = uid;
          m.isMe = (user && uid === user.uid);
          return m;
        });
        members.sort(function(a,b){ return (b.level||0) - (a.level||0); });
        return {code:code, name:data.name || 'The Pack', members:members};
      }).catch(function(){ return null; });
    }
  };

  window.CorgdokuCloud = API;
})();
