#!/usr/bin/env node

import { readFile, mkdir, stat } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";
import sharp from "sharp";

const siteRoot = path.resolve(process.argv[2] || "_site");
const catalog = JSON.parse(await readFile(path.join(siteRoot, "catalog.json"), "utf8"));
const prototypes = catalog.items.filter((item) => item.kind === "prototype");
const previewsRoot = path.join(siteRoot, "previews");
await mkdir(previewsRoot, { recursive: true });

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});
let cursor = 0;
const failures = [];

async function captureNext() {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  while (cursor < prototypes.length) {
    const item = prototypes[cursor++];
    const sourceUrl = new URL(item.url, pathToFileURL(`${siteRoot}${path.sep}`).href);
    const outputPath = path.join(siteRoot, item.preview);
    try {
      await page.goto(sourceUrl.href, { waitUntil: "domcontentloaded", timeout: 30_000 });
      await page.waitForTimeout(800);
      const screenshot = await page.screenshot({ type: "jpeg", quality: 86 });
      await sharp(screenshot).webp({ quality: 82 }).toFile(outputPath);
      const details = await stat(outputPath);
      if (details.size < 100) throw new Error("generated preview is empty");
      process.stdout.write(`✓ ${item.title}\n`);
    } catch (error) {
      failures.push(`${item.url}: ${error.message}`);
    }
  }
  await page.close();
}

await Promise.all(Array.from({ length: Math.min(4, prototypes.length) }, captureNext));
await browser.close();

if (failures.length) {
  process.stderr.write(`${failures.join("\n")}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`Captured ${prototypes.length} previews.\n`);
}
