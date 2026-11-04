// Render SVGs to transparent PNGs using the pre-installed Playwright Chromium.
// Usage: node deck/make_icons.js <jobs.json> <lucide-static/icons dir>
//   Icon job (Lucide, recolored):  {"name": "pill", "color": "00D3F2", "out": "/abs/pill-00D3F2.png"}
//   Logo job (full-color SVG kept as is): {"src": "/abs/salesforce-original.svg", "out": "/abs/salesforce.png", "raw": true}
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const iconDir = process.argv[3];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1024, height: 1024 } });
  for (const job of jobs) {
    let svg;
    if (job.raw) {
      svg = fs.readFileSync(job.src, "utf8")
        .replace(/<svg([^>]*?)\swidth="[^"]*"/, "<svg$1")
        .replace(/<svg([^>]*?)\sheight="[^"]*"/, "<svg$1")
        .replace(/<svg/, '<svg style="width:512px;height:auto;display:block"');
    } else {
      svg = fs.readFileSync(path.join(iconDir, `${job.name}.svg`), "utf8")
        .replace(/stroke="currentColor"/g, `stroke="#${job.color}"`)
        .replace(/width="24"/, 'width="256"')
        .replace(/height="24"/, 'height="256"');
    }
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    const el = await page.$("svg");
    await el.screenshot({ path: job.out, omitBackground: true });
  }
  await browser.close();
  console.log(`rendered ${jobs.length} images`);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
