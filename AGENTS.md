# AGENTS.md

This file provides guidance to Codex when working with code in this repository.

## Project Overview

Flask-Vue-Nginx is a multi-tenant artist analytics platform that tracks social media metrics (Instagram, TikTok, YouTube, Bilibili) and music streaming data (Spotify, Melon) for K-pop and Asian entertainment artists. The application uses Firebase for authentication and MongoDB (via MongoEngine) for data storage.

**Key directories:**
- `backend_rebuild/` - Flask 2 backend (active codebase)
- `frontend_rebuild/` - Vue 3 + Vite frontend (active codebase)
- `nginx/` - Nginx reverse proxy configuration

**Deprecated directories (DO NOT USE):**
- `backend/` - Legacy backend code, scheduled for deletion. Never reference or modify.
- `frontend/` - Legacy frontend code, scheduled for deletion. Never reference or modify.

## Development Commands

### Backend (Flask)

```bash
cd backend_rebuild
pip install -r requirements.txt
python main.py  # Runs on port 5000 in debug mode
```

The backend connects to MongoDB on startup. Connection details are hardcoded in `app.py:create_app()` for the default environment. The `db_connect.py` file contains logic for SSH tunneling in development environments (requires `.env.development` file and PEM certificates).

### Frontend (Vue 3 + Vite)

```bash
cd frontend_rebuild
npm install
npm run dev      # Development server (default port 5173, configurable via VITE_API_PORT)
npm run build    # Production build
npm run preview  # Preview production build
```

Frontend requires a `.env` file with Firebase configuration variables:
- `VITE_API_FIREBASE_API_KEY`
- `VITE_API_FIREBASE_AUTH_DOMAIN`
- `VITE_API_FIREBASE_PROJECT_ID`
- `VITE_API_FIREBASE_STORAGEBUCKET`
- `VITE_API_FIREBASE_MESSAGINGSENDERID`
- `VITE_API_FIREBASE_APPID`
- `VITE_API_FIREBASE_MEASUREMENTID`

### Docker Compose

```bash
docker-compose up           # Start all services (nginx, frontend, backend)
docker-compose up --build   # Rebuild images and start
```

The compose file uses:
- `t024-nginx` (port 80)
- `t024-frontend` (internal port 80, exposed as 8080)
- `t024-backend` (port 5001)

Note: `docker-compose.yml` currently references `./backend` and `./frontend_rebuild` contexts.

## Architecture

### Backend Structure (Flask + MongoEngine)

**Three-layer architecture:**

1. **Routes** (`routes/*.py`) - Flask Blueprints that define API endpoints and register with URL prefixes
   - Export blueprint variables named `*_bp` (e.g., `artist_bp`, `spotify_bp`)
   - Registered in `app.py:create_app()` with prefixes like `/api/artist`, `/api/spotify`

2. **Controllers** (`controllers/*.py`) - Business logic layer with static methods
   - Named `*Controller` (e.g., `ArtistController`, `SpotifyController`)
   - Handle request parsing, validation, and orchestration
   - SNS-related controllers are in `controllers/sns/` subdirectory

3. **Models** (`models/*.py`) - MongoEngine Document definitions
   - Define MongoDB collections and schemas with relationships via `ReferenceField`
   - Named `*Model` or direct class names (e.g., `Artist`, `Tenant`)
   - SNS-related models are in `models/sns/` subdirectory
   - Use Python `Enum` classes for constrained string fields (see `Nation` enum in `artist_model.py`)

**Key models and relationships:**
- `Artist` - Central model with references to Tenant, SNS platforms, and streaming services
- `Tenant` - Multi-tenant isolation (artists belong to tenants)
- SNS models (`Instagram`, `YouTube`, `TikTok`, `Bilibili`) - Social media data
- Streaming models (`Spotify`, `Melon`) - Music platform data
- `User` - Firebase-authenticated users

**API versioning:** Routes use `/v1/` prefix (e.g., `/api/artist/v1/artist`)

### Frontend Structure (Vue 3 + Composition API)

**Directory layout:**
- `src/views/` - Page-level components organized by feature area (Auth, Dashboard, SNS, TrendingArtists, Works, Campaign)
- `src/layouts/` - Layout wrappers (SNS_Layout, Auth_Layout, Works_Layout)
- `src/components/` - Reusable Vue components
- `src/router/` - Vue Router configuration with Firebase auth guards
- `src/stores/` - Pinia state management stores
- `src/libs/` - Shared utilities and services
- `src/assets/` - Static assets and stylesheets

**Key technologies:**
- Vue 3 with Composition API (prefer `<script setup>`)
- Vuetify 3 for UI components
- Pinia for state management
- Vue Router with navigation guards
- Firebase Authentication (auth state checked via `onAuthStateChanged`)
- Axios for HTTP requests (configured in `axios.js`)
- Vue I18n for internationalization
- ApexCharts for data visualization
- Tailwind CSS for styling

**Routing & authentication:**
- All routes except `/auth/*` require authentication (`meta.requireAuth: true`)
- Router beforeEach guard redirects unauthenticated users to `/auth/login`
- Authenticated users accessing `/auth/login` are redirected to `/dashboard`
- Route structure uses nested children (see SNS and Works layouts)

**Environment variables:**
- Frontend uses Vite's `import.meta.env.VITE_*` pattern for environment variables
- Backend API URL should be configured via environment variable

### Database Connection

MongoDB connection is established in `app.py:create_app()` using MongoEngine's `connect()`. The codebase has two connection strategies:

1. **Simple connection** (in `app.py`) - Direct connection with hardcoded credentials
2. **SSH tunnel connection** (in `db_connect.py`) - Development mode uses SSH tunnel to EC2, then connects to DocumentDB with TLS

The `db_connect.py` expects:
- `.env.development` or `.env.production` file (selected by `FLASK_ENV` env var)
- PEM certificates: `docdb-connect.pem` (SSH key) and `global-bundle.pem` (TLS CA)

## API Patterns

Example artist API endpoints:
```bash
POST /api/artist/v1/artist                           # Create artist
GET  /api/artist/v1/artist/<artist_id>               # Get artist by ID
GET  /api/artist/v1/artist/tenant/<tenant_id>        # Get all artists for tenant
GET  /api/artist/v1/artist/all                       # Get all artists
```

Controllers document expected parameters and responses in docstring format at the file header.

## Deployment

Deployment workflow pushes Docker images to AWS ECR and triggers GitHub Actions to update EC2:

1. **Build and push images:** `./ready_for_deploy.sh` (or `ready_for_deploy_win.sh` on Windows)
2. **Tag release:** `git tag $version && git push --tag`
3. **GitHub Actions** automatically pulls latest code on EC2 and runs docker-compose

**AWS Infrastructure:**
- ECR repositories for backend and frontend images
- EC2 instance runs Docker containers
- MongoDB hosted separately (currently at `18.162.155.254:27017`)

**Maintenance notes:**
- EC2 IP address in `.github/workflow/aws.yml` must be updated if instance is stopped/restarted
- Old ECR images should be pruned periodically
- GitHub Actions runs `docker image prune` to clean up EC2 disk space

## Naming Conventions

**Backend:**
- Blueprints: `*_bp` suffix (e.g., `artist_bp`)
- Controllers: `*Controller` class name (e.g., `ArtistController`)
- Controller methods: static methods with snake_case names
- Models: PascalCase class names (e.g., `Artist`, `Tenant`)
- Route files: `*_route.py`

**Frontend:**
- Components: PascalCase with `.vue` extension (e.g., `DashboardView.vue`)
- Stores: camelCase file names (e.g., `counter.js`)
- Composables and utilities: camelCase
- Layouts: PascalCase with `_Layout` suffix (e.g., `SNS_Layout.vue`)
- Views: PascalCase with `View` suffix (e.g., `ArtistView.vue`)

## Code Style

**Python (PEP 8):**
- 4-space indentation
- Keep route handlers thin - delegate to controller methods
- Use docstring headers to document controller APIs (parameters, returns, errors)
- Import models at module level to avoid circular dependencies

**JavaScript/Vue:**
- ES modules with `import/export`
- Prefer Composition API with `<script setup>`
- camelCase for variables and functions
- PascalCase for component names
- Use `@` alias for `src/` directory (configured in vite.config.js)

## Configuration & Secrets

- Backend: Credentials are currently hardcoded in `app.py` and `config.py` (should be migrated to environment variables)
- Frontend: All Firebase config uses environment variables via `.env` file
- Never commit `.env` files or PEM certificates to version control
- MongoDB credentials and Firebase keys must match the target environment (staging/production)
