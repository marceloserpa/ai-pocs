# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```sh
node index.js       # Run the app
npm install         # Install dependencies
```

## Architecture

Minimal Node.js proof-of-concept. `index.js` loads `.env` via `dotenv` and prints all environment variables to stdout. No build step, no framework.
