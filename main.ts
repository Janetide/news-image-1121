// news-image-20261121 entry: ships the drawn front page (entry.png) to the
// grader's output directory. Node 22, standard library only, no network.
//
// The output directory itself is never removed: only the files inside it are
// cleared (each child is made writable first, then removed), so a pre-created
// /output keeps existing. The copy is verified byte for byte with sha256 and
// left world-readable (0644) so the grader can collect it as another user.

import { createHash } from 'node:crypto';
import { chmodSync, copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

function sha256(path: string): string {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

function makeWritable(path: string): void {
  const st = statSync(path);
  chmodSync(path, st.isDirectory() ? 0o755 : 0o644);
  if (st.isDirectory()) {
    for (const child of readdirSync(path)) makeWritable(join(path, child));
  }
}

function clearContents(dir: string): void {
  for (const child of readdirSync(dir)) {
    const p = join(dir, child);
    makeWritable(p);
    rmSync(p, { recursive: true, force: true });
  }
}

const here = fileURLToPath(new URL('.', import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
if (existsSync(outDir)) clearContents(outDir);
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);
chmodSync(dest, 0o644);
const srcHash = sha256(source);
if (sha256(dest) !== srcHash) {
  throw new Error('entry.png copy failed verification');
}
console.log(`wrote ${dest} (${statSync(dest).size} bytes, sha256 ${srcHash})`);
