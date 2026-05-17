# Insider Threat Detection Frontend

A Svelte-based frontend application for detecting and analyzing insider threats using machine learning predictions.

## Project Description

This frontend application provides an interactive interface for the Insider Threat Detection system (COS720 Project). It enables users to:

- Upload and analyze datasets related to insider threat detection
- Visualize prediction results and model outputs
- Interact with predictive models to identify potential insider threats in organizational data

The application is built with Svelte and SvelteKit, providing a modern, responsive user interface for security analysis and data visualization.

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

## Getting Started

### Installation

First, install the project dependencies:

```sh
npm install
```

### Running the Development Server

Start the development server:

```sh
npm run dev
```

This will launch the application at `http://localhost:5173`. To automatically open it in your browser:

```sh
npm run dev -- --open
```

### Building for Production

To create an optimized production build:

```sh
npm run build
```

### Preview Production Build

To test the production build locally:

```sh
npm run preview
```

## Project Structure

- `src/` - Source code directory
  - `lib/` - Reusable components and utilities
    - `models/` - Prediction model definitions
  - `routes/` - Page routes and layouts
- `static/` - Static assets

## Technology Stack

- **Framework**: Svelte / SvelteKit
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Linting**: ESLint

## Notes

For deployment, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
