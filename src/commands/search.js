import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateJSON } from '../validation.js';

export const searchCommand = {
  help() {
    console.log(`ue-cli search — Search for assets

Usage: ue-cli search --query '{}' [options]

Options:
  --query <json>  Search query as JSON
  --host <url>    UE host (default: http://localhost:30010)
  --dry-run       Preview request without sending
  --verbose       Print headers`);
  },

  async execute(positionals, argv, options) {
    const { values } = parseArgs({
      args: argv,
      options: {
        query: { type: 'string' },
        host: { type: 'string' },
        'dry-run': { type: 'boolean' },
        force: { type: 'boolean' },
        timeout: { type: 'string' },
        verbose: { type: 'boolean' },
      },
      allowPositionals: true,
      strict: false,
    });

    const queryStr = values.query;
    const queryCheck = validateJSON(queryStr, '--query');
    if (!queryCheck.valid) {
      output.error('search', queryCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/search/assets';
    const body = queryCheck.parsed || {};

    if (options.dryRun) {
      output.dryRun('search', method, `${options.host}${path}`, body);
      return;
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('search', result.error, result.code);
      process.exit(1);
    }

    output.success('search', { method, path, body }, result.data);
  },
};
