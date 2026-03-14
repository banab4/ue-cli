import { parseArgs } from 'node:util';
import { randomUUID } from 'node:crypto';
import { readFile, unlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { request } from '../http.js';
import { output } from '../output.js';
import { validateObjectPath, validateRequired, validateJSON } from '../validation.js';
import { confirmWrite } from '../safety.js';
import { fetchMergedIndex, fetchFromRegistries } from '../config.js';

async function findMatchingScript(functionName, params) {
  try {
    const index = await fetchMergedIndex();
    if (!index || !index.scripts) return null;
    const script = index.scripts.find(s => s.name === functionName);
    if (!script) return null;
    return script;
  } catch {
    return null;
  }
}

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

export const callCommand = {
  help() {
    console.log(`ue-cli call — Call a function on a UE object

Usage: ue-cli call <scriptName> [options]              (script mode)
       ue-cli call <objectPath> <functionName> [options] (API mode)

Script mode (auto-detected):
  If the first argument matches a registered script name,
  it runs as a Python script inside UE. No objectPath needed.

API mode (fallback):
  If no matching script is found, treats arguments as
  objectPath + functionName for direct Remote Control API call.

Options:
  --params <json>   Parameters as JSON
  --transaction     Generate undo transaction (API mode only)
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

    const paramsCheck = validateJSON(values.params, '--params');
    if (!paramsCheck.valid) {
      output.error('call', paramsCheck.error, 'VALIDATION_ERROR');
      process.exit(1);
    }

    // Script-first: check positionals[0] as script name
    const scriptMatch = await findMatchingScript(positionals[0], paramsCheck.parsed);
    if (scriptMatch) {
      const template = await fetchFromRegistries(`scripts/${scriptMatch.name}.py`);
      if (template) {
        const params = paramsCheck.parsed || {};
        const placeholders = extractPlaceholders(template);

        // Auto-inject output_path if template uses it
        const outputId = randomUUID();
        const outputPath = join(tmpdir(), `ue-cli-${outputId}.json`).replaceAll('\\', '/');
        const hasOutputPlaceholder = placeholders.includes('output_path');
        if (hasOutputPlaceholder) {
          params.output_path = outputPath;
        }

        const missing = placeholders.filter(p => !(p in params));
        if (missing.length > 0) {
          output.error('call', `Script "${scriptMatch.name}" requires: ${missing.join(', ')}`, 'VALIDATION_ERROR');
          process.exit(1);
        }

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

        const confirmation = await confirmWrite('call', { method, url: `${options.host}${path}`, scriptName: scriptMatch.name, params }, options);
        if (confirmation === 'dry-run') {
          output.dryRun('call', method, `${options.host}${path}`, { ...body, _scriptName: scriptMatch.name, _params: params });
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

        // Read script output from temp file if it exists
        let scriptOutput = undefined;
        if (hasOutputPlaceholder) {
          try {
            const raw = await readFile(outputPath, 'utf-8');
            scriptOutput = JSON.parse(raw);
          } catch {
            // No output file — script didn't write one
          } finally {
            try { await unlink(outputPath); } catch {}
          }
        }

        // Post-process: enrich bp_info with ParentClass via separate get call
        if (scriptMatch.name === 'bp_info' && scriptOutput && scriptOutput.found && scriptOutput.parent_class === 'Unknown' && params.blueprint_path) {
          try {
            const getResult = await request('PUT', '/remote/object/property', {
              objectPath: params.blueprint_path,
              propertyName: 'ParentClass',
              access: 'READ_ACCESS',
            }, options);
            if (getResult.ok && getResult.data && getResult.data.ParentClass) {
              const pc = getResult.data.ParentClass;
              scriptOutput.parent_class = pc.includes('.') ? pc.split('.').pop() : pc;
            }
          } catch {}
        }

        output.success('call', { method, path, scriptName: scriptMatch.name, params, via: 'script' }, { ...result.data, ...(scriptOutput !== undefined ? { scriptOutput } : {}) });
        return;
      }
    }

    // Fallback: direct Remote Control API call
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
