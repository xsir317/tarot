import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

describe('Locale routing safety', () => {
  it('avoids unprefixed absolute links from locale pages', () => {
    const homePath = path.join(process.cwd(), 'src', 'app', '[locale]', 'page.tsx');
    const homeSource = fs.readFileSync(homePath, 'utf8');

    expect(homeSource).not.toContain('href="/question"');
    expect(homeSource).not.toContain('href="/auth/login"');
  });

  it('middleware matcher covers non-prefixed routes', () => {
    const middlewarePath = path.join(process.cwd(), 'src', 'middleware.ts');
    const middlewareSource = fs.readFileSync(middlewarePath, 'utf8');

    expect(middlewareSource).not.toContain("'/(zh|en)/:path*'");
    expect(middlewareSource).toContain('/((?!api|_next');
  });
});

