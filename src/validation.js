export function validateRequired(value, name) {
  if (!value || (typeof value === 'string' && value.trim() === '')) {
    return { valid: false, error: `${name} is required` };
  }
  return { valid: true };
}

export function validateObjectPath(path) {
  const req = validateRequired(path, 'objectPath');
  if (!req.valid) return req;

  if (!path.startsWith('/')) {
    return { valid: false, error: `objectPath must start with /: got "${path}"` };
  }
  return { valid: true };
}

export function validateJSON(str, name) {
  if (!str) return { valid: true, parsed: undefined };

  try {
    const parsed = JSON.parse(str);
    return { valid: true, parsed };
  } catch (err) {
    return { valid: false, error: `${name} must be valid JSON: ${err.message}` };
  }
}
