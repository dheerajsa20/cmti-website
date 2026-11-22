/**
 * CMTI website enquiries -> Google Sheet.
 *
 * Paste this whole file into the Google Sheet's Apps Script editor
 * (Extensions > Apps Script), run setup once, then deploy as a web app.
 * Step-by-step instructions: tools/ENQUIRY-SHEET-SETUP.txt
 *
 * Each enquiry from the website form becomes one row, with the date and
 * time it was sent (India time). Download the sheet as Excel any time with
 * File > Download > Microsoft Excel (.xlsx).
 */

// Optional: email address that gets a short alert for every new enquiry.
// Leave as '' for no emails. Separate several addresses with commas.
const NOTIFY_EMAIL = '';

const SHEET_NAME = 'Enquiries';
const TIME_ZONE = 'Asia/Kolkata';
const HEADERS = ['Date', 'Time', 'Name', 'Email', 'Phone', 'Organisation',
  'Programme', 'Preferred format', 'Training requirements'];
// Form field name and the longest value kept, in column order after Date and Time.
const FIELDS = [['name', 100], ['email', 150], ['phone', 35], ['organisation', 120],
  ['programme', 120], ['format', 20], ['message', 1000]];

/** Run once from the editor: creates the Enquiries tab and its header row. */
function setup() {
  const book = SpreadsheetApp.getActiveSpreadsheet();
  book.setSpreadsheetTimeZone(TIME_ZONE);
  const sheet = book.getSheetByName(SHEET_NAME) || book.insertSheet(SHEET_NAME, 0);
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.getRange('A2:A').setNumberFormat('dd-mm-yyyy');
  sheet.getRange('B2:B').setNumberFormat('hh:mm am/pm');
  sheet.setColumnWidth(9, 400);
}

/** The website sends each enquiry here. */
function doPost(e) {
  const p = (e && e.parameter) || {};
  // "website" is a hidden field people never see; only spam bots fill it in.
  if (p.website) return reply('ok');
  if (!p.name || !p.phone || !p.programme) return reply('missing fields');

  // Phone is always stored as text so a leading 0 or +91 is kept as typed.
  const values = FIELDS.map(([key, max]) => clean(p[key], max, key === 'phone'));
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) throw new Error('Run setup() first.');
    const now = new Date();
    sheet.appendRow([now, now, ...values]);
  } finally {
    lock.releaseLock();
  }

  if (NOTIFY_EMAIL) {
    const lines = HEADERS.slice(2).map((h, i) => h + ': ' + (values[i].replace(/^'/, '') || '-'));
    MailApp.sendEmail(NOTIFY_EMAIL, 'New CMTI enquiry: ' + values[4], lines.join('\n'),
      { replyTo: values[1] || undefined });
  }
  return reply('ok');
}

/** Opening the web-app link in a browser shows this, so you can check it is live. */
function doGet() {
  return reply('CMTI enquiry sheet is connected.');
}

function clean(value, max, asText) {
  const text = String(value || '').trim().slice(0, max);
  // A leading ' keeps the value as plain text (hidden in the sheet). It also
  // stops typed text being treated as a formula in Sheets or Excel.
  return text && (asText || /^[=+\-@]/.test(text)) ? "'" + text : text;
}

function reply(text) {
  return ContentService.createTextOutput(text);
}
