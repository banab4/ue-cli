import { request } from '../http.js';
import { output } from '../output.js';
import { validateObjectPath, validateRequired } from '../validation.js';

export const getCommand = {
  help() {
    console.log(`ue-cli get — Read a property from a UE object

Usage: ue-cli get <objectPath> <propertyName> [options]

Arguments:
  objectPath      Path to the UE object
  propertyName    Name of the property to read

Options:
  --host <url>    UE host (default: http://localhost:30010)
  --dry-run       Preview request without sending
  --verbose       Print headers`);
  },

  async execute(positionals, argv, options) {
    const objectPath = positionals[0];
    const propertyName = positionals[1];

    const pathCheck = validateObjectPath(objectPath);
    if (!pathCheck.valid) {
      output.error('get', pathCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const propCheck = validateRequired(propertyName, 'propertyName');
    if (!propCheck.valid) {
      output.error('get', propCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const method = 'PUT';
    const path = '/remote/object/property';
    const body = {
      objectPath,
      propertyName,
      access: 'READ_ACCESS',
    };

    if (options.dryRun) {
      output.dryRun('get', method, `${options.host}${path}`, body);
      return;
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('get', result.error, result.code);
      process.exit(1);
    }

    output.success('get', { method, path, body }, result.data);
  },
};
