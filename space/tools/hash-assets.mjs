#!/usr/bin/env node
/**
 * 资源 hash 同步工具
 *
 * 作用：space/index.html 引用的是内容 hash 文件名（app.<hash>.js / app.<hash>.css）。
 * 你手动改过 assets/ 下的文件后，文件名不会自动变，浏览器和 CDN 会继续用旧文件。
 * 这个脚本会：
 *   1) 按当前文件内容重算 hash
 *   2) 文件名不一致时改名（删除旧的同名系列文件）
 *   3) 同步更新 index.html 里的引用
 *
 * 用法：
 *   node space/tools/hash-assets.mjs          # 同步
 *   node space/tools/hash-assets.mjs --check  # 只检查，不改动（退出码 1 表示需要同步）
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SPACE = path.resolve(__dirname, "..");
const ASSETS = path.join(SPACE, "assets");
const INDEX = path.join(SPACE, "index.html");
const CHECK_ONLY = process.argv.includes("--check");

const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex").slice(0, 8);

if (!fs.existsSync(INDEX)) {
  console.error("找不到 index.html:", INDEX);
  process.exit(2);
}

let html = fs.readFileSync(INDEX, "utf8");
const changes = [];
const problems = [];

// 解析 index.html 中当前引用的 assets 文件
const refs = [...html.matchAll(/\.\/assets\/([A-Za-z0-9._-]+?)\.([0-9a-f]{8})\.(js|css)/g)].map((m) => ({
  full: m[0],
  stem: m[1],
  hash: m[2],
  ext: m[3],
  file: `${m[1]}.${m[2]}.${m[3]}`,
}));

if (!refs.length) {
  console.log("index.html 未引用带 hash 的 assets（可能还没拆分），无需处理。");
  process.exit(0);
}

for (const ref of refs) {
  const abs = path.join(ASSETS, ref.file);
  if (!fs.existsSync(abs)) {
    problems.push(`引用存在但文件缺失: assets/${ref.file}`);
    continue;
  }
  const want = sha(fs.readFileSync(abs));
  if (want === ref.hash) continue;

  const newFile = `${ref.stem}.${want}.${ref.ext}`;
  changes.push({ from: ref.file, to: newFile, oldRef: ref.full, newRef: `./assets/${newFile}` });
}

if (problems.length) {
  console.error("发现问题：");
  problems.forEach((p) => console.error("  - " + p));
  process.exit(2);
}

if (!changes.length) {
  console.log("✅ 所有资源 hash 已是最新，无需改动。");
  process.exit(0);
}

console.log(CHECK_ONLY ? "需要同步：" : "正在同步：");
for (const c of changes) {
  console.log(`  ${c.from}  ->  ${c.to}`);
  if (CHECK_ONLY) continue;
  fs.renameSync(path.join(ASSETS, c.from), path.join(ASSETS, c.to));
  html = html.split(c.oldRef).join(c.newRef);
}

if (CHECK_ONLY) {
  console.log("\n（--check 模式，未做改动）");
  process.exit(1);
}

fs.writeFileSync(INDEX, html, "utf8");
console.log(`\n✅ 完成，已更新 ${changes.length} 处引用。`);
console.log("   记得同步更新 space/index.html 里的 <link>/<script> 顺序不受影响。");