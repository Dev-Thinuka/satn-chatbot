// build.js
import tailwindcss from 'tailwindcss';
import postcss from 'postcss';
import fs from 'fs';

const css = `
@tailwind base;
@tailwind components;
@tailwind utilities;
`;

postcss([tailwindcss])
  .process(css, { from: undefined })
  .then(result => fs.writeFileSync('src/styles.css', result.css));
