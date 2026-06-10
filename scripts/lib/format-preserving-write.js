// Byte-format-preserving reader/writer for docs/data/churches.json.
//
// The canonical file is ASCII-escaped (\uXXXX for every non-ASCII char) with NO
// trailing newline. Node's default JSON.stringify writes literal Unicode, so a
// naive writer re-encodes every em-dash in the file and a 2-line edit explodes
// into a ~50k-line cosmetic diff (this has burned us twice). This helper detects
// the file's exact byte format on read and returns a writer that reproduces it;
// if the round-trip doesn't reproduce the file byte-for-byte it throws rather
// than guess (same contract as the prune-churches skill's serializer).
//
// Usage:
//   const { makeWriter } = require('./lib/format-preserving-write.js');
//   const { data, write } = makeWriter(CHURCHES_PATH);
//   ...mutate data...
//   write(data);
const fs = require('fs');

function makeWriter(filePath) {
  const origBuf = fs.readFileSync(filePath);
  const data = JSON.parse(origBuf);
  const esc = s => s.replace(/[^\x00-\x7F]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
  const body = JSON.stringify(data, null, 2);
  for (const useEsc of [false, true]) {
    for (const nl of ['\n', '']) {
      if (origBuf.equals(Buffer.from((useEsc ? esc(body) : body) + nl))) {
        const write = obj => fs.writeFileSync(
          filePath,
          (useEsc ? esc(JSON.stringify(obj, null, 2)) : JSON.stringify(obj, null, 2)) + nl
        );
        return { data, write };
      }
    }
  }
  throw new Error(filePath + ': serialization does not round-trip byte-for-byte — refusing to write. ' +
    'Canon is ASCII-escaped + no trailing newline; inspect what changed before forcing.');
}

module.exports = { makeWriter };
