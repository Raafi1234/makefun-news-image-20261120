// SPDX-License-Identifier: MIT
// news-image-20261120 entrypoint (Node 22, standard library only).
//
// The entry image is built ahead of time by compose.py and shipped in this
// repository as entry.png. This program's only job is to place those exact
// bytes at $MAKEFUN_OUTPUT_DIR/entry.png (default /output) so the grader
// can judge them. It performs no network access and writes nothing else.
// Because the image is copied verbatim, repeated runs write identical bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(source);
writeFileSync(target, bytes);

// Confirm the copy landed whole: same byte count as the shipped image.
if (statSync(target).size !== bytes.length) {
  throw new Error(`short copy: wrote ${statSync(target).size} of ${bytes.length} bytes`);
}
