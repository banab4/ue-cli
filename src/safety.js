import { createInterface } from 'node:readline';
import { output } from './output.js';

const WRITE_VERBS = new Set(['call', 'set', 'script', 'batch']);

export function isWriteVerb(verb) {
  return WRITE_VERBS.has(verb);
}

export async function confirmWrite(verb, requestPreview, options) {
  if (options.dryRun) return 'dry-run';
  if (options.force) return 'forced';

  if (!process.stdin.isTTY) {
    output.error(verb, 'Write command requires --force in non-interactive mode', 'CONFIRMATION_REQUIRED');
    return 'cancelled';
  }

  console.error(JSON.stringify(requestPreview, null, 2));
  console.error(`\nThis is a write command (${verb}). Proceed? [y/N]`);

  const answer = await new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin, output: process.stderr });
    rl.question('', (ans) => {
      rl.close();
      resolve(ans);
    });
  });

  return answer.toLowerCase() === 'y' ? 'confirmed' : 'cancelled';
}
