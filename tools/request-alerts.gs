/**
 * Request alerts — emails Ross when a new file lands in a client's `_requests/` folder.
 *
 * Runs in Ross's own Google account at script.google.com. Ross only: it is not part
 * of any client's workspace and no client's Claude ever sees it.
 * Setup, click by click: setup/onboarding.md § Request alerts.
 *
 * - Checks every 3 hours. One email per check at most, however many clients;
 *   no email when nothing is new.
 * - A problem (a folder it can't open) is emailed once, not every check.
 * - Monday morning: one short "still working" email.
 * - Free. Uses Google's Apps Script allowance, never Claude usage.
 */

// ── Edit these ──────────────────────────────────────────────────────────────
// One line per client: a name you'll recognise → the ID of their data folder
// (in the folder's web address, the part after /folders/).
const CLIENTS = {
  'Kyle': 'PASTE_FOLDER_ID_HERE',
};
const CHECK_HOURS = [0, 3, 6, 9, 12, 15, 18, 21];   // every 3 hours
const WEEKLY_DAY = 'MONDAY';                         // "still working" email
const WEEKLY_HOUR = 8;
// ────────────────────────────────────────────────────────────────────────────

const MAX_CHARS = 3000;   // longest request text copied into an email

/** Run this once after pasting, and again after editing CLIENTS. */
function setup() {
  stopAlerts();
  CHECK_HOURS.forEach(function (h) {
    ScriptApp.newTrigger('checkRequests').timeBased().atHour(h).everyDays(1).create();
  });
  ScriptApp.newTrigger('weeklyCheckIn').timeBased()
    .onWeekDay(ScriptApp.WeekDay[WEEKLY_DAY]).atHour(WEEKLY_HOUR).create();

  const props = PropertiesService.getScriptProperties();
  const lines = [];
  Object.keys(CLIENTS).forEach(function (name) {
    const state = openRequests_(CLIENTS[name]);
    if (state.problem) props.setProperty('problem:' + CLIENTS[name], state.problem);   // reported here, not again
    lines.push(state.problem
      ? '✗ ' + name + ' — ' + state.problem
      : '✓ ' + name + ' — ' + state.files.length + ' file(s) already in _requests');
  });
  checkRequests();   // starts the clock for any client seen for the first time
  send_('Request alerts are on — watching ' + Object.keys(CLIENTS).length + ' client(s)',
    'Checks every 3 hours. You get one email when something new arrives.\n\n' +
    lines.join('\n'));
}

/** Runs every 3 hours. Also safe to run by hand from the editor. */
function checkRequests() {
  const props = PropertiesService.getScriptProperties();
  const now = new Date();
  const found = [];      // {client, kind, title, url, text}
  const problems = [];   // new problems only

  Object.keys(CLIENTS).forEach(function (name) {
    const id = CLIENTS[name];
    const state = openRequests_(id);
    const problemKey = 'problem:' + id;
    if (state.problem) {
      if (props.getProperty(problemKey) !== state.problem) {
        problems.push(name + ' — ' + state.problem);
        props.setProperty(problemKey, state.problem);
      }
      return;
    }
    props.deleteProperty(problemKey);

    const sinceKey = 'since:' + id;
    const since = props.getProperty(sinceKey);
    props.setProperty(sinceKey, String(now.getTime()));
    if (!since) return;   // first time this client is seen: nothing is "new" yet

    state.files.forEach(function (f) {
      if (f.getDateCreated().getTime() < Number(since)) return;
      const text = readText_(f);
      found.push({
        client: name,
        kind: /^kind:\s*note\b/m.test(text) ? 'Note' : 'Request',
        title: f.getName(),
        url: f.getUrl(),
        text: text.length > MAX_CHARS ? text.slice(0, MAX_CHARS) + '\n…(cut — open the file)' : text,
      });
    });
  });

  if (!found.length && !problems.length) return;
  send_(subject_(found, problems), body_(found, problems));
}

/** Monday morning: proves the alerts are still running. */
function weeklyCheckIn() {
  const lines = Object.keys(CLIENTS).map(function (name) {
    const state = openRequests_(CLIENTS[name]);
    return state.problem
      ? '✗ ' + name + ' — ' + state.problem
      : '✓ ' + name + ' — ' + state.files.length + ' file(s) in _requests';
  });
  send_('Request alerts: still working', lines.join('\n'));
}

/** Turns the alerts off. Run setup() to turn them back on. */
function stopAlerts() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    const fn = t.getHandlerFunction();
    if (fn === 'checkRequests' || fn === 'weeklyCheckIn') ScriptApp.deleteTrigger(t);
  });
}

// ── helpers ─────────────────────────────────────────────────────────────────

function openRequests_(folderId) {
  if (!folderId || folderId.indexOf('PASTE') === 0) {
    return { problem: 'no folder ID yet — paste it into CLIENTS', files: [] };
  }
  let root;
  try {
    root = DriveApp.getFolderById(folderId);
  } catch (e) {
    return { problem: "can't open the folder — check the ID and that it's still shared with you", files: [] };
  }
  const subs = root.getFoldersByName('_requests');
  if (!subs.hasNext()) {
    return { problem: 'no _requests folder yet (the workspace may not be set up)', files: [] };
  }
  const files = [];
  const it = subs.next().getFiles();
  while (it.hasNext()) {
    const f = it.next();
    if (!f.isTrashed()) files.push(f);
  }
  return { problem: null, files: files };
}

function readText_(file) {
  try {
    if (file.getMimeType() === MimeType.GOOGLE_DOCS) {
      return DocumentApp.openById(file.getId()).getBody().getText();
    }
    return file.getBlob().getDataAsString();
  } catch (e) {
    return '(couldn\'t read it — open the file)';
  }
}

function subject_(found, problems) {
  if (!found.length) return 'Request alerts: a folder needs a look';
  const per = {};
  found.forEach(function (x) { per[x.client] = (per[x.client] || 0) + 1; });
  const names = Object.keys(per);
  const who = names.length === 1
    ? names[0]
    : names.map(function (n) { return n + ' (' + per[n] + ')'; }).join(', ');
  return found.length + ' new from ' + who;
}

function body_(found, problems) {
  const parts = found.map(function (x) {
    return '── ' + x.kind + ' · ' + x.client + ' · ' + x.title + '\n' + x.url + '\n\n' + x.text.trim();
  });
  if (problems.length) {
    parts.push('── Needs a look\n' + problems.join('\n'));
  }
  return parts.join('\n\n');
}

function send_(subject, body) {
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(), subject, body);
}
