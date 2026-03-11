#!/usr/bin/env node

import { run } from '../src/cli.js';

try {
  await run(process.argv.slice(2));
} catch (err) {
  console.error(JSON.stringify({ ok: false, error: err.message, code: 'UNEXPECTED_ERROR' }));
  process.exit(1);
}
