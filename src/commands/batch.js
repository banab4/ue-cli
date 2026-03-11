import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateJSON } from '../validation.js';
import { confirmWrite } from '../safety.js';

export const batchCommand = {
  help() {
    console.log(`ue-cli batch — Execute multiple requests

Usage: ue-cli batch --requests '[...]' [options]

Options:
  --requests <json>   Array of request objects (required)
  --host <url>        UE host (default: http://localhost:30010)
  --dry-run           Preview request without sending
  --force             Skip confirmation
  --verbose           Print headers`);
  },

  async execute(positionals, argv, options) {
    const { values } = parseArgs({
      args: argv,
      options: {
        requests: { type: 'string' },
        host: { type: 'string' },
        'dry-run': { type: 'boolean' },
        force: { type: 'boolean' },
        timeout: { type: 'string' },
        verbose: { type: 'boolean' },
      },
      allowPositionals: true,
      strict: false,
    });

    const reqCheck = validateJSON(values.requests, '--requests');
    if (!reqCheck.valid) {
      output.error('batch', reqCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }
    if (!reqCheck.parsed || !Array.isArray(reqCheck.parsed)) {
      output.error('batch', '--requests must be a JSON array', 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/batch';
    const body = { Requests: reqCheck.parsed };

    const confirmation = await confirmWrite('batch', { method, url: `${options.host}${path}`, body }, options);
    if (confirmation === 'dry-run') {
      output.dryRun('batch', method, `${options.host}${path}`, body);
      return;
    }
    if (confirmation === 'cancelled') {
      output.error('batch', 'Cancelled by user', 'CANCELLED');
      process.exit(1);
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('batch', result.error, result.code);
      process.exit(1);
    }

    output.success('batch', { method, path, body }, result.data);
  },
};
