# Penalty Box Configurator Docker Setup

This project provides a Dockerized version of the Penalty Box Configurator tool, served by a Python FastAPI backend that acts as a bridge to Git repositories and an Alarm API.

## Prerequisites

- Docker installed on your system.
- An SSH key pair for accessing the Git repository.

## Building the Docker Image

Run the following command in the root of the project:

```bash
docker build -t penalty-box-configurator .
```

## Running the Container

To run the container, you need to:
1.  Mount your SSH keys so the container can authenticate with the Git server.
2.  (Optional) Set the `ALARM_API_URL` environment variable if the Alarm API is not at `http://localhost:8080`.
3.  Ensure the container can reach the Git server and Alarm API (e.g., using `--network host` or a shared bridge network).

### Example Command (Linux/Mac)

```bash
docker run -d \
  -p 8000:8000 \
  -v ~/.ssh:/root/.ssh:ro \
  -e ALARM_API_URL="http://localhost:8080" \
  --name penalty-box-app \
  penalty-box-configurator
```

### Example Command (Windows PowerShell)

```powershell
docker run -d `
  -p 8000:8000 `
  -v $HOME/.ssh:/root/.ssh:ro `
  -e ALARM_API_URL="http://localhost:8080" `
  --name penalty-box-app `
  penalty-box-configurator
```

**Note on SSH Keys:**
The container runs as root by default (or the user configured in the base image, but we haven't created a specific user, so it's root). Mounting `~/.ssh` to `/root/.ssh` allows the container to use your host's SSH keys. Ensure your `known_hosts` file is also populated or mount it, otherwise you might get host verification errors.

**Note on Networking:**
If the Git server and Alarm API are running in other Docker containers on the same machine, you should put them all in the same Docker network.
```bash
docker network create my-network
docker network connect my-network penalty-box-app
# Connect other containers to my-network as well
```
Then you can refer to them by container name (e.g., `http://alarm-api:8080`).

## Usage

Open your browser and navigate to `http://localhost:8000`.
The tool should load.

### Git Operations
The tool uses the `/repos` endpoint to list repositories.
To clone a repository, you can send a POST request to `/repos/clone` (or implement a UI button for it).
The backend expects SSH access to the Git server.

### Alarm API
The tool proxies requests to the Alarm API via `/alarm-proxy`. Ensure `ALARM_API_URL` is set correctly.
