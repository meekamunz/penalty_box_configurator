# Penalty Box Configurator Docker Setup

This project provides a Dockerized version of the Penalty Box Configurator tool, served by a Python FastAPI backend that acts as a bridge to Git repositories and an Alarm API.

## Prerequisites

- Docker installed on your system.
- An SSH key pair for accessing the Git repository.

## Running with Docker Compose

This project includes a `docker-compose.yml` file to simplify building and running the application.

### 1. Configure Environment

The `docker-compose.yml` is pre-configured with defaults:
-   Mounts `~/.ssh` to `/root/.ssh` (read-only) for Git authentication.
-   Sets `ALARM_API_URL` to `http://host.docker.internal:8080` to access services on the host machine.
-   Persists cloned repositories in a local `./repos` directory.

If you need to change these (e.g., your SSH keys are in a different location), edit `docker-compose.yml`.

### 2. Start the Application

Run the following command in the root of the project:

```bash
docker-compose up -d --build
```

This will build the image and start the container in the background.

### 3. Stop the Application

To stop the container:

```bash
docker-compose down
```

**Note on SSH Keys:**
The container runs as root. Mounting `~/.ssh` to `/root/.ssh` allows the container to use your host's SSH keys. Ensure your `known_hosts` file is also populated or mount it, otherwise you might get host verification errors.

**Note on Networking:**
The configuration uses `host.docker.internal` to allow the container to access services running on your host machine (like the Alarm API). If your Alarm API is running in another Docker container, you should put them in the same Docker network and use the container name as the hostname.

## Usage

Open your browser and navigate to `http://localhost:8000`.
The tool should load.

### Git Operations
The tool uses the `/repos` endpoint to list repositories.
To clone a repository, you can send a POST request to `/repos/clone` (or implement a UI button for it).
The backend expects SSH access to the Git server.

### Alarm API
The tool proxies requests to the Alarm API via `/alarm-proxy`. Ensure `ALARM_API_URL` is set correctly.
