// Run: node tools/request-alerts.test.js tools/request-alerts.gs  (Node only; mocks Google's services)
// Mock Google services and exercise request-alerts.gs end to end.
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const src = fs.readFileSync(process.argv[2], 'utf8');

function world() {
  const W = { clock: 1000, folders: {}, props: {}, mail: [], triggers: [] };
  const mkFile = (name, text, created, doc = true, trashed = false) => ({
    getName: () => name, getId: () => 'id-' + name, getUrl: () => 'https://docs/' + name,
    getDateCreated: () => new Date(created), isTrashed: () => trashed,
    getMimeType: () => doc ? 'application/vnd.google-apps.document' : 'text/plain',
    getBlob: () => ({ getDataAsString: () => text }), _text: text });
  const iter = a => { let i = 0; return { hasNext: () => i < a.length, next: () => a[i++] }; };
  W.add = (folderId, name, text, opts = {}) => {
    W.folders[folderId] = W.folders[folderId] || { requests: [] };
    W.folders[folderId].requests.push(mkFile(name, text, opts.created ?? W.clock, opts.doc ?? true, opts.trashed));
  };
  const allFiles = () => Object.values(W.folders).flatMap(f => f.requests || []);
  const ctx = {
    console,
    Date: class extends Date { constructor(...a) { a.length ? super(...a) : super(W.clock); } },
    MimeType: { GOOGLE_DOCS: 'application/vnd.google-apps.document' },
    DriveApp: { getFolderById: id => {
      const f = W.folders[id]; if (!f) throw new Error('no access');
      return { getFoldersByName: () => iter(f.requests ? [{ getFiles: () => iter(f.requests) }] : []) }; } },
    DocumentApp: { openById: id => ({ getBody: () => ({ getText: () => allFiles().find(f => f.getId() === id)._text }) }) },
    PropertiesService: { getScriptProperties: () => ({
      getProperty: k => (k in W.props ? W.props[k] : null), setProperty: (k, v) => { W.props[k] = v; },
      deleteProperty: k => { delete W.props[k]; } }) },
    MailApp: { sendEmail: (to, s, b) => W.mail.push({ to, s, b }) },
    Session: { getEffectiveUser: () => ({ getEmail: () => 'ross@example.com' }) },
    ScriptApp: {
      WeekDay: { MONDAY: 'MON' },
      getProjectTriggers: () => W.triggers.slice(),
      deleteTrigger: t => { W.triggers = W.triggers.filter(x => x !== t); },
      newTrigger: fn => { const t = { fn, getHandlerFunction: () => fn }; const b = {
        timeBased: () => b, atHour: h => { t.hour = h; return b; }, everyDays: () => b,
        onWeekDay: d => { t.day = d; return b; }, create: () => { W.triggers.push(t); return t; } }; return b; } },
  };
  return { W, ctx };
}
function load(clients) {
  const { W, ctx } = world();
  vm.createContext(ctx);
  vm.runInContext(src.replace(/const CLIENTS = \{[\s\S]*?\};/, 'const CLIENTS = ' + JSON.stringify(clients) + ';')
    + '\nthis.API={setup,checkRequests,weeklyCheckIn,stopAlerts};', ctx);
  return { W, api: ctx.API };
}
let n = 0; const ok = (name, f) => { f(); n++; console.log('PASS', name); };

ok('setup: 8 checks + 1 weekly, one "on" email, no flood of old files', () => {
  const { W, api } = load({ Kyle: 'K' });
  W.add('K', 'old.md', 'kind: request\n## Kyle asked for\nold', { created: 500 });
  api.setup();
  assert.equal(W.triggers.filter(t => t.fn === 'checkRequests').length, 8);
  assert.deepEqual(W.triggers.filter(t => t.fn === 'checkRequests').map(t => t.hour), [0,3,6,9,12,15,18,21]);
  assert.equal(W.triggers.filter(t => t.fn === 'weeklyCheckIn').length, 1);
  assert.equal(W.mail.length, 1); assert.match(W.mail[0].s, /alerts are on/); assert.match(W.mail[0].b, /✓ Kyle — 1 file/);
});
ok('setup twice: triggers replaced, not doubled', () => {
  const { W, api } = load({ Kyle: 'K' }); W.add('K', 'a.md', 'x', { created: 1 });
  api.setup(); api.setup(); assert.equal(W.triggers.length, 9);
});
ok('new request → one email with text and link; next check silent', () => {
  const { W, api } = load({ Kyle: 'K' }); W.add('K', 'old.md', 'x', { created: 1 });
  api.setup(); W.mail = [];
  W.clock = 5000; W.add('K', '2026-10-22-gate.md', '---\nkind: request\n---\n## Kyle asked for\nGroup lessons', { created: 4000 });
  api.checkRequests();
  assert.equal(W.mail.length, 1); assert.equal(W.mail[0].s, '1 new from Kyle');
  assert.match(W.mail[0].b, /Request · Kyle · 2026-10-22-gate\.md/); assert.match(W.mail[0].b, /Group lessons/);
  assert.match(W.mail[0].b, /https:\/\/docs\//);
  W.clock = 9000; api.checkRequests(); assert.equal(W.mail.length, 1);
});
ok('note is labelled Note; plain file read too; trashed file ignored', () => {
  const { W, api } = load({ Kyle: 'K' }); W.add('K', 'o.md', 'x', { created: 1 });
  api.setup(); W.mail = []; W.clock = 5000;
  W.add('K', 'n.md', '---\nkind: note\n---\n## Note\nGate code changed', { created: 4000, doc: false });
  W.add('K', 'bin.md', 'kind: request', { created: 4000, trashed: true });
  api.checkRequests();
  assert.equal(W.mail.length, 1); assert.match(W.mail[0].b, /Note · Kyle · n\.md/); assert.match(W.mail[0].b, /Gate code/);
  assert.doesNotMatch(W.mail[0].b, /bin\.md/);
});
ok('many clients → still one email per check, subject counts each', () => {
  const { W, api } = load({ Kyle: 'K', 'Car wash': 'C' });
  W.add('K', 'o.md', 'x', { created: 1 }); W.add('C', 'o2.md', 'x', { created: 1 });
  api.setup(); W.mail = []; W.clock = 5000;
  W.add('K', 'a.md', 'kind: request', { created: 4000 }); W.add('K', 'b.md', 'kind: note', { created: 4000 });
  W.add('C', 'c.md', 'kind: request', { created: 4000 });
  api.checkRequests();
  assert.equal(W.mail.length, 1); assert.equal(W.mail[0].s, '3 new from Kyle (2), Car wash (1)');
});
ok('lost access: emailed once, not every check; recovers quietly', () => {
  const { W, api } = load({ Kyle: 'K' }); W.add('K', 'o.md', 'x', { created: 1 });
  api.setup(); W.mail = []; const saved = W.folders.K; delete W.folders.K;
  api.checkRequests(); api.checkRequests();
  assert.equal(W.mail.length, 1); assert.match(W.mail[0].b, /can't open the folder/);
  W.folders.K = saved; api.checkRequests(); assert.equal(W.mail.length, 1);
  assert.equal(W.props['problem:K'], undefined);
});
ok('unfilled folder ID: setup says so once, checks stay silent', () => {
  const { W, api } = load({ Kyle: 'PASTE_FOLDER_ID_HERE' });
  api.setup(); assert.equal(W.mail.length, 1); assert.match(W.mail[0].b, /✗ Kyle — no folder ID yet/);
  api.checkRequests(); assert.equal(W.mail.length, 1);
});
ok('client added later: no flood of their old files', () => {
  const r1 = load({ Kyle: 'K', New: 'N' }); const { W, api } = r1;
  W.add('K', 'o.md', 'x', { created: 1 }); api.setup(); W.mail = [];
  W.add('N', 'old1.md', 'x', { created: 2 });   // folder appears later, with old files
  W.clock = 6000; api.checkRequests();
  assert.ok(W.mail.every(m => !/old1/.test(m.b)));
});
ok('weekly check-in lists every client', () => {
  const { W, api } = load({ Kyle: 'K', Other: 'O' }); W.add('K', 'o.md', 'x', { created: 1 });
  api.weeklyCheckIn(); assert.match(W.mail[0].b, /✓ Kyle — 1 file/); assert.match(W.mail[0].b, /✗ Other — can't open/);
});
ok('stopAlerts removes only this script\'s triggers', () => {
  const { W, api } = load({ Kyle: 'K' }); W.add('K', 'o.md', 'x', { created: 1 });
  W.triggers.push({ fn: 'somethingElse', getHandlerFunction: () => 'somethingElse' });
  api.setup(); api.stopAlerts(); assert.deepEqual(W.triggers.map(t => t.fn), ['somethingElse']);
});
console.log(`\n${n}/10 passed`);
