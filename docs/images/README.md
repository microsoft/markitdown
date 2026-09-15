# README images

## hero.gif

Animated hero at the top of the repository `README.md`.

### Source

`hero.html` in this directory is the editable source — a single self-contained HTML file (inline CSS, Google Fonts via `<link>`, inline SVG). Open in any browser to preview; Puppeteer captures a screencast that ffmpeg encodes to GIF.

### Re-rendering the GIF

Requires Node + Puppeteer and ffmpeg.

```bash
npm install puppeteer      # one-time, ~170 MB Chromium download

# 1. Capture frames
cat > /tmp/capture.js <<'EOF'
const puppeteer = require('puppeteer');
const fs = require('fs'); const path = require('path');
const DURATION = 20700, WIDTH = 1200, HEIGHT = 675;
const FRAMES = '/tmp/md-frames'; fs.mkdirSync(FRAMES, { recursive: true });
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve('docs/images/hero.html'), { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 300));
  await page.evaluate(() => window.runLoop && window.runLoop());
  const client = await page.target().createCDPSession();
  const frames = []; let i = 0;
  client.on('Page.screencastFrame', async (ev) => {
    const p = `${FRAMES}/f${String(i++).padStart(5,'0')}.png`;
    fs.writeFileSync(p, Buffer.from(ev.data, 'base64'));
    frames.push({ p, t: ev.metadata.timestamp });
    await client.send('Page.screencastFrameAck', { sessionId: ev.sessionId });
  });
  await client.send('Page.startScreencast', { format: 'png', everyNthFrame: 1 });
  await new Promise(r => setTimeout(r, DURATION + 200));
  await client.send('Page.stopScreencast');
  await browser.close();
  let txt = '';
  for (let j = 0; j < frames.length; j++) {
    const dur = (j + 1 < frames.length ? frames[j+1].t - frames[j].t : 0.04).toFixed(4);
    txt += `file '${frames[j].p}'\nduration ${dur}\n`;
  }
  txt += `file '${frames[frames.length-1].p}'\n`;
  fs.writeFileSync('/tmp/md-frames.txt', txt);
})();
EOF
node /tmp/capture.js

# 2. Encode to GIF (two-pass palette)
ffmpeg -y -f concat -safe 0 -i /tmp/md-frames.txt \
  -vf "fps=30,palettegen=stats_mode=diff:max_colors=256" /tmp/md-palette.png
ffmpeg -y -f concat -safe 0 -i /tmp/md-frames.txt -i /tmp/md-palette.png \
  -lavfi "fps=30 [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop 0 docs/images/hero.gif
```

Target size ≤ 10 MB. If over, drop `fps` to 20 or reduce `max_colors` before shortening the loop.
