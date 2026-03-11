import { parseArgs } from 'node:util';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateRequired, validateJSON } from '../validation.js';
import { confirmWrite } from '../safety.js';

const REPO_BASE = 'https://raw.githubusercontent.com/banab4/ue-cli/master/skills/ue-cli/scripts';
const GITHUB_API = 'https://api.github.com/repos/banab4/ue-cli/contents/skills/ue-cli/scripts';

function extractPlaceholders(templateContent) {
  const placeholders = new Set();
  const lines = templateContent.split('\n');
  for (const line of lines) {
    const matches = line.match(/"\{(\w+)\}"/g) || line.match(/\{(\w+)\}/g) || [];
    for (const match of matches) {
      const name = match.replace(/["{}\s]/g, '');
      if (name) placeholders.add(name);
    }
  }
  return [...placeholders];
}

async function fetchTemplate(scriptName) {
  const url = `${REPO_BASE}/${scriptName}.py`;
  const res = await fetch(url);
  if (!res.ok) return null;
  return await res.text();
}

async function listTemplates() {
  try {
    const res = await fetch(GITHUB_API, {
      headers: { 'Accept': 'application/vnd.github.v3+json' },
    });
    if (!res.ok) return [];

    const files = await res.json();
    const pyFiles = files.filter(f => f.name.endsWith('.py'));

    const templates = [];
    for (const file of pyFiles) {
      const content = await fetchTemplate(file.name.replace('.py', ''));
      if (content) {
        templates.push({
          name: file.name.replace('.py', ''),
          params: extractPlaceholders(content),
        });
      }
    }
    return templates;
  } catch {
    return [];
  }
}

export const scriptCommand = {
  help() {
    console.log(`ue-cli script — Execute a Python template script

Usage: ue-cli script <scriptName> --params '{}' [options]
       ue-cli script --list

Arguments:
  scriptName      Name of the template (without .py)

Options:
  --params <json>   Template parameters as JSON
  --list            List available templates (fetched from GitHub)
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
        list: { type: 'boolean', default: false },
        host: { type: 'string' },
        'dry-run': { type: 'boolean' },
        force: { type: 'boolean' },
        timeout: { type: 'string' },
        verbose: { type: 'boolean' },
      },
      allowPositionals: true,
      strict: false,
    });

    if (values.list) {
      const templates = await listTemplates();
      console.log(JSON.stringify({ ok: true, verb: 'script', templates }, null, 2));
      return;
    }

    const scriptName = positionals[0];
    const nameCheck = validateRequired(scriptName, 'scriptName');
    if (!nameCheck.valid) {
      output.error('script', nameCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    // Fetch template from GitHub
    const template = await fetchTemplate(scriptName);
    if (!template) {
      output.error('script', `Template not found: ${scriptName}`, 'TEMPLATE_NOT_FOUND');
      process.exit(1);
    }

    // Parse and validate params
    const paramsCheck = validateJSON(values.params, '--params');
    if (!paramsCheck.valid) {
      output.error('script', paramsCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    const params = paramsCheck.parsed || {};
    const placeholders = extractPlaceholders(template);

    // Check all placeholders have values
    const missing = placeholders.filter(p => !(p in params));
    if (missing.length > 0) {
      output.error('script', `Missing parameters: ${missing.join(', ')}. Required: ${placeholders.join(', ')}`, 'VALIDATION_ERROR');
      process.exit(1);
    }

    // Substitute placeholders
    let script = template;
    for (const [key, value] of Object.entries(params)) {
      script = script.replaceAll(`{${key}}`, String(value));
    }

    const method = 'PUT';
    const path = '/remote/object/call';
    const body = {
      objectPath: '/Script/PythonScriptPlugin.Default__PythonScriptLibrary',
      functionName: 'ExecutePythonScript',
      parameters: { PythonScript: script },
    };

    const confirmation = await confirmWrite('script', { method, url: `${options.host}${path}`, scriptName, params }, options);
    if (confirmation === 'dry-run') {
      output.dryRun('script', method, `${options.host}${path}`, { ...body, _scriptName: scriptName, _params: params });
      return;
    }
    if (confirmation === 'cancelled') {
      output.error('script', 'Cancelled by user', 'CANCELLED');
      process.exit(1);
    }

    const result = await request(method, path, body, options);
    if (!result.ok) {
      output.error('script', result.error, result.code);
      process.exit(1);
    }

    output.success('script', { method, path, scriptName, params }, result.data);
  },
};
