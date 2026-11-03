/* Pikafish UCI worker for the XS space-station chess game.
 * Engine: Pikafish (GPL-3.0) official web build dev-20240226, mirrored at
 * https://github.com/ningh-o/engine-builds (release pikafish-20240226).
 */
var ENGINE_BASE = '';
self.importScripts('pikafish-single.js');

var modReady = false;
var waiters = [];

var Module = {
  locateFile: function (f) { return ENGINE_BASE + f; },
  print: function () {},
  printErr: function () {},
  read_stdout: function (line) { onLine(line); }
};

function onLine(line) {
  line = String(line || '').trim();
  if (!line) return;
  if (line === 'uciok') { self.postMessage({ type: 'uciok' }); return; }
  if (line.indexOf('bestmove') === 0) {
    var mv = line.split(/\s+/)[1] || '';
    var cb = waiters.shift();
    if (cb) cb(mv);
    return;
  }
  if (line.indexOf('info') === 0) { self.postMessage({ type: 'info', text: line }); }
}

Pikafish(Module).then(function () {
  var t = setInterval(function () {
    if (Module.engine_ready) {
      clearInterval(t);
      Module.send_command('uci');
      Module.send_command('setoption name Threads value 1');
      modReady = true;
      self.postMessage({ type: 'ready' });
    }
  }, 50);
}).catch(function (e) {
  self.postMessage({ type: 'error', message: String(e && e.message || e) });
});

self.onmessage = function (e) {
  var d = e.data || {};
  if (d.type === 'init') { if (d.base) ENGINE_BASE = d.base; return; }
  if (d.type === 'go') {
    if (!modReady) { var cb = waiters.shift(); if (cb) cb(''); return; }
    waiters.push(function (mv) { self.postMessage({ type: 'bestmove', id: d.id, move: mv }); });
    try {
      Module.send_command('position fen ' + d.fen);
      Module.send_command('go ' + (d.limit || 'movetime 1000'));
    } catch (err) {
      var cb2 = waiters.pop(); if (cb2) cb2('');
    }
  }
};
