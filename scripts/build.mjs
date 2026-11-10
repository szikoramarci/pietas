// Egyszerű, függőség nélküli statikus oldalgenerátor.
// Futtatás: node scripts/build.mjs  →  kimenet: dist/
//
// Minden src/pages/*.html fájl elején egy HTML-kommentben lévő JSON írja le
// az oldalt (cím, leírás, útvonal). A közös fejléc/lábléc a src/layout.html-ben van.

import { readFile, writeFile, mkdir, readdir, cp, rm } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "src");
const out = join(root, "dist");
const SITE_URL = (process.env.SITE_URL || "https://pietas-temetkezes.hu").replace(/\/$/, "");

// Főmenü – sorrend és feliratok itt módosíthatók.
const NAV = [
  { href: "/teendok/", label: "Mi a teendő?" },
  { href: "/temetes-modjai/", label: "Temetési módok" },
  { href: "/szolgaltatasok/", label: "Szolgáltatások" },
  { href: "/cegunkrol/", label: "Rólunk" },
  { href: "/kapcsolat/", label: "Kapcsolat" },
];

const escapeAttr = (s) => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

function parsePage(raw, file) {
  const m = raw.match(/^\s*<!--\s*(\{[\s\S]*?\})\s*-->\s*/);
  if (!m) throw new Error(`Hiányzó meta-komment: ${file}`);
  const meta = JSON.parse(m[1]);
  return { meta, body: raw.slice(m[0].length) };
}

function navHtml(path) {
  return NAV.map(({ href, label }) => {
    const current = path === href ? ' aria-current="page"' : "";
    return `<li><a href="${href}"${current}>${label}</a></li>`;
  }).join("\n          ");
}

async function build() {
  await rm(out, { recursive: true, force: true });
  await mkdir(out, { recursive: true });
  await cp(join(src, "static"), out, { recursive: true });

  const layout = await readFile(join(src, "layout.html"), "utf8");
  const files = (await readdir(join(src, "pages"))).filter((f) => f.endsWith(".html"));
  const sitemap = [];

  for (const file of files) {
    const raw = await readFile(join(src, "pages", file), "utf8");
    const parsed = parsePage(raw, file);
    const meta = parsed.meta;
    // <!-- include:nev --> → src/partials/nev.html
    let body = parsed.body;
    for (const [, name] of body.matchAll(/<!--\s*include:([\w-]+)\s*-->/g)) {
      const part = await readFile(join(src, "partials", `${name}.html`), "utf8");
      body = body.replace(new RegExp(`<!--\\s*include:${name}\\s*-->`), part);
    }
    const path = meta.path;
    const fullTitle = path === "/" ? meta.title : `${meta.title} | Pietas Temetkezés, Miskolc`;
    const html = layout
      .replaceAll("{{title}}", escapeAttr(fullTitle))
      .replaceAll("{{description}}", escapeAttr(meta.description || ""))
      .replaceAll("{{canonical}}", `${SITE_URL}${path === "404" ? "/" : path}`)
      .replaceAll("{{robots}}", meta.noindex ? "noindex" : "index, follow")
      .replaceAll("{{bodyClass}}", meta.bodyClass || "page")
      .replaceAll("{{nav}}", navHtml(path))
      .replaceAll("{{year}}", String(new Date().getFullYear()))
      .replace("{{content}}", body);

    const target = path === "404" ? join(out, "404.html") : join(out, path, "index.html");
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, html);
    if (!meta.noindex && path !== "404") sitemap.push(path);
    console.log(`  ${file}  →  ${target.replace(root + "/", "")}`);
  }

  const today = new Date().toISOString().slice(0, 10);
  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    sitemap
      .sort()
      .map((p) => `  <url><loc>${SITE_URL}${p}</loc><lastmod>${today}</lastmod></url>`)
      .join("\n") +
    `\n</urlset>\n`;
  await writeFile(join(out, "sitemap.xml"), xml);
  await writeFile(join(out, "robots.txt"), `User-agent: *\nAllow: /\n\nSitemap: ${SITE_URL}/sitemap.xml\n`);
  console.log(`Kész: ${files.length} oldal, sitemap.xml, robots.txt`);
}

build().catch((err) => {
  console.error(err);
  process.exit(1);
});
