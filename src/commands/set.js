import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateObjectPath, validateRequired, validateJSON } from '../validation.js';
import { confirmWrite } from '../safety.js';

export const setCommand = {
  help() {
    console.log(`ue-cli set — Write a property on a UE object

Usage: ue-cli set <objectPath> <propertyName> --value '{}' [options]

Arguments:
  objectPath      Path to the UE object
  propertyName    Name of the property to write

Options:
  --value <json>    Property value as JSON (required)
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
        value: { type: 'string' },
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
    const propertyName = positionals[1];

    const pathCheck = validateObjectPath(objectPath);
    if (!pathCheck.valid) {
      output.error('set', pathCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const propCheck = validateRequired(propertyName, 'propertyName');
    if (!propCheck.valid) {
      output.error('set', propCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const valueCheck = validateJSON(values.value, '--value');
    if (!valueCheck.valid) {
      output.error('set', valueCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }
    if (!valueCheck.parsed) {
      output.error('set', '--value is required', 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/object/property';
    const body = {
      objectPath,
      propertyName,
      propertyValue: valueCheck.parsed,
      access: 'WRITE_ACCESS',
    };

    if (values.transaction) {
      body.generateTransaction = true;
    }

    const confirmation = await confirmWrite('set', { method, url: `${options.host}${path}`, body }, options);
    if (confirmation === 'dry-run') {
      output.dryRun('set', method, `${options.host}${path}`, body);
      return;
    }
    if (confirmation === 'cancelled') {
      output.error('set', 'Cancelled by user', 'CANCELLED');
      process.exit(1);
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('set', result.error, result.code);
      process.exit(1);
    }

    output.success('set', { method, path, body }, result.data);
  },
};
