import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateObjectPath, validateRequired, validateJSON } from '../validation.js';
import { confirmWrite } from '../safety.js';

export const callCommand = {
  help() {
    console.log(`ue-cli call — Call a function on a UE object

Usage: ue-cli call <objectPath> <functionName> [options]

Arguments:
  objectPath      Path to the UE object
  functionName    Name of the function to call

Options:
  --params <json>   Function parameters as JSON
  --transaction     Generate undo transaction
  --host <url>      UE host (default: http://localhost:30010)
  --dry-run         Preview request without sending
  --force           Skip confirmation
  --verbose         Print headers`);
  },

  async execute(positionals, argv, options) {
    const { values } = parseArgs({
      args: argv,
      options: {
        params: { type: 'string' },
        transaction: { type: 'boolean', default: false },
        host: { type: 'string' },
        'dry-run': { type: 'boolean' },
        force: { type: 'boolean' },
        timeout: { type: 'string' },
        verbose: { type: 'boolean' },
      },
      allowPositionals: true,
      strict: false,
    });

    const objectPath = positionals[0];
    const functionName = positionals[1];

    const pathCheck = validateObjectPath(objectPath);
    if (!pathCheck.valid) {
      output.error('call', pathCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const funcCheck = validateRequired(functionName, 'functionName');
    if (!funcCheck.valid) {
      output.error('call', funcCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const paramsCheck = validateJSON(values.params, '--params');
    if (!paramsCheck.valid) {
      output.error('call', paramsCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/object/call';
    const body = { objectPath, functionName };

    if (paramsCheck.parsed) {
      body.parameters = paramsCheck.parsed;
    }
    if (values.transaction) {
      body.generateTransaction = true;
    }

    const confirmation = await confirmWrite('call', { method, url: `${options.host}${path}`, body }, options);
    if (confirmation === 'dry-run') {
      output.dryRun('call', method, `${options.host}${path}`, body);
      return;
    }
    if (confirmation === 'cancelled') {
      output.error('call', 'Cancelled by user', 'CANCELLED');
      process.exit(1);
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('call', result.error, result.code);
      process.exit(1);
    }

    output.success('call', { method, path, body }, result.data);
  },
};
