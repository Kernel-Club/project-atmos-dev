# ADR-002: Frontend — React + Vite

## Status

In review

## Context

Project Atmos requires a lightweight web interface that:

- allows users to enter a city;
- displays current temperature and weather description;
- displays weather history;
- communicates with the backend API;
- provides loading and error states;
- is easy to containerize and serve through Nginx.

The frontend should provide a modern and clean user experience without adding unnecessary application complexity.

## Options considered

1. **React + Vite**
   - Modern frontend stack well suited for a small single-page application.
   - Fast development and build process.
   - Simple static build that can be served by Nginx.

2. **Next.js**
   - Full-featured React framework with routing and server-side rendering.
   - Strong ecosystem and production capabilities.
   - Adds functionality that is not required for this application.

3. **Vue + Vite**
   - Lightweight and well suited for single-page applications.
   - Simple development and build workflow.
   - Introduces a different frontend ecosystem from React.

## Decision

We choose **React + Vite** for the frontend.

The application will be built as a client-side application and served as static files through **Nginx**.

## Why

- **Project fit:** React + Vite provides everything required for the Atmos UI.
- **Simplicity:** No server-side rendering or full-stack framework is required.
- **User experience:** React provides a component-based approach suitable for building a responsive and maintainable interface.
- **DevOps focus:** The frontend produces a static build that is straightforward to containerize and serve with Nginx.
- **Operational fit:** Vite produces a static build that is straightforward to package, serve, and deploy through Nginx.

## Consequences

- **Positive:** Simple frontend architecture and straightforward maintenance.
- **Positive:** Easy integration with the FastAPI backend.
- **Positive:** Static build works well with Nginx and Kubernetes.
- **Positive:** Modern UI can be developed without unnecessary framework complexity.
- **Trade-off:** React + Vite does not provide built-in server-side rendering or backend functionality like Next.js.
- **Trade-off:** Some additional frontend libraries may be needed if the UI grows beyond the current project scope.