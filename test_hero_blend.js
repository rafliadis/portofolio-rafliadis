const fs = require('fs');
const assert = require('assert');

const html = fs.readFileSync('index.html', 'utf8');

// 1. Isolation isolate on #beranda to prevent fallback to body #0f0f0f
assert(
    html.includes('isolation: isolate;'),
    '#beranda must have isolation: isolate to bound mix-blend-mode to light backdrop'
);

// 2. No stacking context isolation (z-10, z-20, z-30) inside hero-device-card
const heroSectionMatch = html.match(/<section id="beranda"[\s\S]*?<\/section>/);
assert(heroSectionMatch, 'Hero section #beranda must exist');
const heroContent = heroSectionMatch[0];

assert(
    !heroContent.includes('z-10') && !heroContent.includes('z-20') && !heroContent.includes('z-30'),
    'Direct children inside hero-device-card must not have z-10, z-20, or z-30 which break mix-blend-mode'
);

// 3. Check giant name and blend text classes
assert(html.includes('.hero-giant-name'), '.hero-giant-name CSS class must exist');
assert(html.includes('.hero-blend-text'), '.hero-blend-text CSS class must exist');
assert(html.includes('mix-blend-mode: difference;'), 'mix-blend-mode: difference must be configured');

// 4. Ensure DOM painting order: portrait wrapper before giant name
const portraitPos = heroContent.indexOf('id="hero-portrait-wrapper"');
const namePos = heroContent.indexOf('hero-giant-name');
assert(portraitPos !== -1 && namePos !== -1, 'Both portrait and giant name must exist');
assert(portraitPos < namePos, 'Portrait must precede giant name in DOM so name blends on top of portrait');

// 5. CV Download tests
// Exactly 3 static links:
const cvMatches = html.match(/href="CV_RAFLIADIS\.pdf"\s+download="CV_RAFLIADIS\.pdf"/g) || [];
assert.strictEqual(cvMatches.length, 3, `Expected exactly 3 static CV links with download="CV_RAFLIADIS.pdf", found ${cvMatches.length}`);

// Header CV
assert(html.includes('aria-label="Unduh CV (PDF)"'), 'Header CV must have aria-label="Unduh CV (PDF)"');

// Hero buttons
assert(heroContent.includes('Unduh CV') && heroContent.includes('Lihat Proyek'), 'Hero must display Unduh CV and Lihat Proyek buttons');

// Kontak CV
assert(html.includes('Download CV (PDF)'), 'Kontak must display Download CV (PDF) button');

// Script: CV_FILE and downloadCV
assert(html.includes("const CV_FILE = 'CV_RAFLIADIS.pdf';"), 'JS must define const CV_FILE');
assert(html.includes('function downloadCV()'), 'JS must define function downloadCV()');

// Terminal: commands cv & download-cv
assert(html.includes("case 'download-cv':"), "Terminal switch must support 'download-cv'");
assert(html.includes("case 'cv':"), "Terminal switch must support 'cv'");
assert(html.includes('cv / download-cv:'), "Help list must describe cv / download-cv");

console.log('All hero mix-blend-mode and CV download checks passed successfully.');
