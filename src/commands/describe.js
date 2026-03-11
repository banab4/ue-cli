import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateObjectPath } from '../validation.js';

export const describeCommand = {
  help() {
    console.log(`ue-cli describe — Get schema of a UE object

Usage: ue-cli describe <objectPath> [options]

Arguments:
  objectPath    Path to the UE object (e.g. /Script/Engine.EditorLevelLibrary)

Options:
  --host <url>    UE host (default: http://localhost:30010)
  --dry-run       Preview request without sending
  --verbose       Print headers`);
  },

  async execute(positionals, argv, options) {
    const objectPath = positionals[0];

    const check = validateObjectPath(objectPath);
    if (!check.valid) {
      output.error('describe', check.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/object/describe';
    const body = { objectPath };

    if (options.dryRun) {
      output.dryRun('describe', method, `${options.host}${path}`, body);
      return;
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('describe', result.error, result.code);
      process.exit(1);
    }

    output.success('describe', { method, path, body }, result.data);
  },
};
