import { request } from '../http.js';
import { output } from '../output.js';

export const infoCommand = {
  help() {
    console.log(`ue-cli info — Show Remote Control API info

Usage: ue-cli info [options]

Options:
  --host <url>    UE host (default: http://localhost:30010)
  --dry-run       Preview request without sending
  --verbose       Print headers`);
  },

  async execute(positionals, argv, options) {
    const method = 'GET';
    const path = '/remote/info';

    if (options.dryRun) {
      output.dryRun('info', method, `${options.host}${path}`, null);
      return;
    }

    const result = await request(method, path, null, options);
    if (!result.ok) {
      output.error('info', result.error, result.code);
      process.exit(1);
    }

    output.success('info', { method, path }, result.data);
  },
};
