// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://forrestswan3.github.io',
  trailingSlash: 'ignore',
  build: { format: 'directory', inlineStylesheets: 'always' },
  compressHTML: true,
});
