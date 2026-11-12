// Run with Node.js and Sharp available (or set NODE_PATH to its package directory).
// PNGs are inspection previews; the notes embed the vector SVGs.
const path = require('node:path');
const sharp = require('sharp');

(async () => {
  for (const name of ['roc-operating-point', 'two-error-areas']) {
    await sharp(path.join(__dirname, name + '.svg'), { density: 120 })
      .flatten({ background: '#ffffff' })
      .png()
      .toFile(path.join(__dirname, name + '.png'));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
