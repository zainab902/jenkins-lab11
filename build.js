const fs = require('fs');

fs.mkdirSync('dist', { recursive: true });

const now = new Date().toISOString();
const html = fs.readFileSync('src/index.html', 'utf8').replace('__BUILD_TIME__', now);

fs.writeFileSync('dist/index.html', html);
fs.writeFileSync('dist/build-info.txt', 'Built with Node ' + process.version + ' at ' + now + '\n');

console.log('Build finished. Node version: ' + process.version);
