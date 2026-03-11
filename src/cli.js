import { parseArgs } from 'node:util';
import { callCommand } from './commands/call.js';
import { getCommand } from './commands/get.js';
import { setCommand } from './commands/set.js';
import { describeCommand } from './commands/describe.js';
import { scriptCommand } from './commands/script.js';
import { searchCommand } from './commands/search.js';
import { infoCommand } from './commands/info.js';
import { batchCommand } from './commands/batch.js';
import { discoverCommand } from './commands/discover.js';
import { output } from './output.js';

const VERBS = {
  call: callCommand,
  get: getCommand,
  set: setCommand,
  describe: describeCommand,
  script: scriptCommand,
  search: searchCommand,
  info: infoCommand,
  batch: batchCommand,
  discover: discoverCommand,
};

const GLOBAL_OPTIONS = {
  host: { type: 'string', default: 'http://localhost:30010' },
  'dry-run': { type: 'boolean', default: false },
  force: { type: 'boolean', default: false },
  timeout: { type: 'string', default: '5000' },
  verbose: { type: 'boolean', default: false },
  help: { type: 'boolean', short: 'h', default: false },
};

function printHelp() {
  const help = `ue-cli — Unreal Engine Remote Control API CLI

Usage: ue-cli <command> [options]

Commands:
  call      Call a function on a UE object
  get       Read a property from a UE object
  set       Write a property on a UE object
  describe  Get schema of a UE object
  script    Execute a Python template script
  search    Search for assets
  info      Show Remote Control API info
  batch     Execute multiple requests
  discover  Browse available objects and functions

Global options:
  --host <url>      UE Remote Control host (default: http://localhost:30010)
  --dry-run         Preview request without sending
  --force           Skip confirmation for write commands
  --timeout <ms>    HTTP timeout in ms (default: 5000)
  --verbose         Print request/response headers
  -h, --help        Show help`;

  console.log(help);
}

export async function run(argv) {
  const verb = argv[0];

  if (!verb || verb === '--help' || verb === '-h') {
    printHelp();
    return;
  }

  const handler = VERBS[verb];
  if (!handler) {
    output.error(verb, `Unknown command: ${verb}. Run ue-cli --help for available commands.`, 'UNKNOWN_COMMAND');
    process.exit(1);
  }

  const verbArgv = argv.slice(1);

  // Parse global options from verb argv
  const { values: globalOpts, positionals, tokens } = parseArgs({
    args: verbArgv,
    options: GLOBAL_OPTIONS,
    allowPositionals: true,
    strict: false,
  });

  const options = {
    host: globalOpts.host,
    dryRun: globalOpts['dry-run'],
    force: globalOpts.force,
    timeout: parseInt(globalOpts.timeout, 10),
    verbose: globalOpts.verbose,
  };

  if (globalOpts.help) {
    handler.help?.();
    return;
  }

  await handler.execute(positionals, verbArgv, options);
}
