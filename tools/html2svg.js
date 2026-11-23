// Render each page with Playwright and convert the laid-out DOM to an SVG
// that Figma imports as editable layers (groups, rects, text, vector icons).
// Usage: node html2svg.js <pagesDir> <outDir> [file ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const pagesDir = process.argv[2], outDir = process.argv[3];
const only = process.argv.slice(4);
fs.mkdirSync(outDir, { recursive: true });

function walker() {
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const parseColor = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); const a = p.length > 3 ? p[3] : 1; if (a === 0) return null; return { hex: '#' + p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join(''), a }; };
  const fillAttr = (c, name = 'fill') => `${name}="${c.hex}"${c.a < 1 ? ` ${name}-opacity="${+c.a.toFixed(3)}"` : ''}`;
  const used = new Map();
  const uid = base => { base = (base || 'layer').replace(/[^A-Za-z0-9_\-]/g, '_').slice(0, 60) || 'layer'; const n = (used.get(base) || 0) + 1; used.set(base, n); return n === 1 ? base : `${base}_${n}`; };
  const nameOf = el => { const c = (el.getAttribute('class') || '').trim().split(/\s+/)[0]; return c || el.tagName.toLowerCase(); };
  const filters = []; let fid = 0;
  const shadowFilter = (sh) => { // first non-inset shadow only
    const parts = sh.split(/,(?![^(]*\))/).map(s => s.trim()).filter(s => !s.includes('inset'));
    if (!parts.length) return '';
    const p = parts[parts.length > 1 ? 0 : 0];
    const col = parseColor((p.match(/rgba?\([^)]+\)/) || [])[0]); const nums = p.replace(/rgba?\([^)]+\)/, '').trim().split(/\s+/).map(parseFloat);
    if (!col || nums.length < 3) return '';
    const [dx, dy, blur, spread = 0] = nums; if (blur < 6 && spread <= 0) return ''; // skip hairline xs shadows
    const id = 'sh' + (++fid);
    filters.push(`<filter id="${id}" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="${dx}" dy="${dy}" stdDeviation="${blur / 2}" flood-color="${col.hex}" flood-opacity="${col.a}"/></filter>`);
    return ` filter="url(#${id})"`;
  };
  const out = [];
  const visible = (el, cs) => cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0;

  function textLines(node, cs) {
    const raw = node.textContent; if (!raw.trim()) return [];
    const r = document.createRange(); const lines = []; let cur = null;
    const re = /\S+/g; let m;
    while ((m = re.exec(raw))) {
      r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length);
      const rects = [...r.getClientRects()].filter(b => b.width > 0);
      if (!rects.length) continue; const b = rects[0];
      if (cur && Math.abs(b.top - cur.top) < 2) { cur.text += ' ' + m[0]; cur.right = b.right; }
      else { cur = { text: m[0], left: b.left, top: b.top, h: b.height, right: b.right }; lines.push(cur); }
    }
    return lines;
  }

  function emitText(node, el) {
    const cs = getComputedStyle(el); if (!visible(el, cs)) return;
    const col = parseColor(cs.color); if (!col) return;
    const fs = parseFloat(cs.fontSize), fw = cs.fontWeight;
    const ls = cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing);
    const tt = cs.textTransform;
    for (const l of textLines(node, cs)) {
      let t = l.text; if (tt === 'uppercase') t = t.toUpperCase(); else if (tt === 'capitalize') t = t.replace(/\b\w/g, c => c.toUpperCase());
      const y = l.top + (l.h - fs * 1.21) / 2 + fs * 0.969;
      out.push(`<text id="${uid("w" + fw + "__" + t.slice(0, 40))}" x="${l.left.toFixed(1)}" y="${y.toFixed(1)}" font-family="Inter" font-size="${fs}" font-weight="${fw}"${ls ? ` letter-spacing="${ls}"` : ''} ${fillAttr(col)}${cs.fontStyle === 'italic' ? ' font-style="italic"' : ''}>${esc(t)}</text>`);
    }
  }

  function walk(el, depth) {
    const cs = getComputedStyle(el);
    if (!visible(el, cs)) return;
    if (el.tagName === 'INPUT' && el.type === 'checkbox' && el.className.includes('toggle')) return;
    const b = el.getBoundingClientRect();
    const op = parseFloat(cs.opacity);
    const tag = el.tagName.toLowerCase();
    if (tag === 'svg') {
      if (b.width === 0) return;
      const clone = el.cloneNode(true); const color = parseColor(cs.color);
      clone.setAttribute('x', b.left); clone.setAttribute('y', b.top); clone.setAttribute('width', b.width); clone.setAttribute('height', b.height);
      clone.removeAttribute('class'); clone.removeAttribute('aria-hidden'); clone.removeAttribute('style');
      let s = new XMLSerializer().serializeToString(clone).replace(/currentColor/g, color ? color.hex : '#000');
      out.push(`<g id="${uid('icon')}">${s}</g>`); return;
    }
    if (tag === 'img') { const src = el.getAttribute('src') || ''; out.push(`<image id="${uid(path_base(src))}" x="${b.left}" y="${b.top}" width="${b.width}" height="${b.height}" href="IMG:${src}"/>`); return; }
    const open = out.length; out.push(null);
    // box
    if (b.width > 0 && b.height > 0) {
      const bg = parseColor(cs.backgroundColor);
      const bw = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseFloat(cs['border' + s + 'Width']) || 0);
      const bc = ['Top', 'Right', 'Bottom', 'Left'].map(s => parseColor(cs['border' + s + 'Color']));
      const bs = ['Top', 'Right', 'Bottom', 'Left'].map(s => cs['border' + s + 'Style']);
      const rx = Math.min(parseFloat(cs.borderTopLeftRadius) || 0, b.width / 2, b.height / 2);
      const uniform = bw.every(w => w === bw[0]) && bw[0] > 0 && bc[0] && bc.every(c => c && c.hex === bc[0].hex) && bs[0] !== 'none';
      const sh = cs.boxShadow !== 'none' ? shadowFilter(cs.boxShadow) : '';
      if (bg || uniform) {
        const w = uniform ? bw[0] : 0;
        const dash = uniform && bs[0] === 'dashed' ? ` stroke-dasharray="${w * 3} ${w * 2}"` : uniform && bs[0] === 'dotted' ? ` stroke-dasharray="${w} ${w * 2}"` : '';
        out.push(`<rect id="${uid(nameOf(el) + '_bg')}" x="${(b.left + w / 2).toFixed(1)}" y="${(b.top + w / 2).toFixed(1)}" width="${(b.width - w).toFixed(1)}" height="${(b.height - w).toFixed(1)}"${rx ? ` rx="${Math.max(0, rx - w / 2)}"` : ''} ${bg ? fillAttr(bg) : 'fill="none"'}${uniform ? ` ${fillAttr(bc[0], 'stroke')} stroke-width="${w}"${dash}` : ''}${sh}/>`);
      }
      if (!uniform) { // individual sides
        const L = b.left, T = b.top, R = b.right, B = b.bottom;
        const seg = [[L, T + bw[0] / 2, R, T + bw[0] / 2], [R - bw[1] / 2, T, R - bw[1] / 2, B], [L, B - bw[2] / 2, R, B - bw[2] / 2], [L + bw[3] / 2, T, L + bw[3] / 2, B]];
        seg.forEach((s, i) => { if (bw[i] > 0 && bc[i] && bs[i] !== 'none') out.push(`<line id="${uid(nameOf(el) + '_border')}" x1="${s[0]}" y1="${s[1]}" x2="${s[2]}" y2="${s[3]}" ${fillAttr(bc[i], 'stroke')} stroke-width="${bw[i]}"/>`); });
      }
    }
    for (const n of el.childNodes) {
      if (n.nodeType === 3) emitText(n, el);
      else if (n.nodeType === 1) walk(n, depth + 1);
    }
    if (out.length === open + 1) { out.length = open; return; } // empty element
    out[open] = `<g id="${uid(nameOf(el))}"${op < 1 ? ` opacity="${op}"` : ''}>`;
    out.push('</g>');
  }
  function path_base(s) { return s.split('/').pop().replace(/\.\w+$/, ''); }
  const W = document.documentElement.scrollWidth, H = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
  const bodyBg = parseColor(getComputedStyle(document.body).backgroundColor) || { hex: '#ffffff', a: 1 };
  walk(document.body, 0);
  return { W, H, svg: `<rect id="page_bg" x="0" y="0" width="${W}" height="${H}" ${fillAttr(bodyBg)}/>` + out.join('\n'), defs: filters.join('') };
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const files = only.length ? only : fs.readdirSync(pagesDir).filter(f => f.endsWith('.html')).sort();
  for (const f of files) {
    await page.goto('file://' + path.resolve(pagesDir, f));
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(`(${walker.toString()})()`);
    let svg = r.svg.replace(/href="IMG:([^"]+)"/g, (_, src) => {
      const p = path.resolve(pagesDir, src); const b64 = fs.readFileSync(p).toString('base64');
      return `href="data:image/png;base64,${b64}"`;
    });
    const name = f.replace(/\.html$/, '');
    const doc = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${r.W}" height="${r.H}" viewBox="0 0 ${r.W} ${r.H}"><defs>${r.defs}</defs>${svg}</svg>`;
    fs.writeFileSync(path.join(outDir, name + '.svg'), doc);
    console.log(name, r.W + 'x' + r.H, Math.round(doc.length / 1024) + 'KB');
  }
  await browser.close();
})();
