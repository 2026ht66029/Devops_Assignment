# ACEest Fitness and Gym DevOps Assignment

ACEest is a small Flask web application packaged as a complete CI/CD demonstration. The repository includes unit tests, lint and coverage rules, a multi-stage Docker build, a GitHub Actions workflow, and a Jenkins pipeline.

## Features

- Responsive fitness-program dashboard
- Health endpoint for container and pipeline checks
- Program recommendations by goal
- BMI calculation with validation
- Membership-expiry checking
- Weekly class schedule
- Pytest suite with a 90 percent coverage gate

## Repository structure

```text
.
├── .github/workflows/main.yml
├── aceest/
│   ├── __init__.py
│   ├── fitness.py
│   └── templates/index.html
├── tests/test_app.py
├── app.py
├── Dockerfile
├── Jenkinsfile
├── compose.yaml
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Rocky Linux 9.5 cloud server setup

Run these commands only after copying or cloning this repository to the Rocky Linux 9.5 cloud server. Its standard Python 3.9 installation is supported for host-side testing. The Docker image and GitHub Actions workflow intentionally use Python 3.12.

Install the basic host tools:

```bash
sudo dnf makecache
sudo dnf install -y git python3 python3-pip curl unzip
```

Create the project environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python app.py
```

From the cloud server, check `http://127.0.0.1:5000`. If browser access is required, use an SSH tunnel or allow the application port only from your own IP address. Do not expose development ports globally.

Health check:

```bash
curl http://127.0.0.1:5000/health
```

BMI example:

```bash
curl -X POST http://127.0.0.1:5000/api/bmi \
  -H 'Content-Type: application/json' \
  -d '{"height_cm":180,"weight_kg":75}'
```

## Manual validation

```bash
python -m compileall -q app.py aceest tests
ruff check .
pytest
```

The configured test command enforces at least 90 percent coverage.

## Docker

Install Docker Engine from Docker's official RHEL repository:

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Disconnect and reconnect once before running Docker without `sudo`.

Run tests inside the test image:

```bash
docker build --target test -t aceest:test .
docker run --rm aceest:test
```

Build and run the smaller production image:

```bash
docker build --target runtime -t aceest:1.0.0 .
docker run --rm -p 8000:8000 aceest:1.0.0
```

Open `http://127.0.0.1:8000` or check `http://127.0.0.1:8000/health`.

Docker Compose alternative:

```bash
docker compose up --build
```

## GitHub Actions pipeline

`.github/workflows/main.yml` runs for every push and pull request. It:

1. installs the Python dependencies;
2. compiles the application and tests;
3. runs Ruff linting;
4. runs Pytest with coverage on the runner;
5. builds a Docker test image and runs Pytest inside it;
6. builds the runtime image; and
7. starts the runtime container and checks `/health`.

## Jenkins pipeline

The `Jenkinsfile` defines the Jenkins BUILD and quality gate. The Jenkins agent requires Python 3, the `venv` module, Docker, and permission to run Docker commands. Configure a Pipeline job from SCM, point it at this repository, and use `Jenkinsfile` as the script path.

For Rocky Linux, install Java 21 and Jenkins from the official RPM repository:

```bash
sudo dnf install -y fontconfig java-21-openjdk wget
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/rpm-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/rpm-stable/jenkins.io-2026.key
sudo dnf install -y jenkins
sudo systemctl daemon-reload
sudo systemctl enable --now jenkins
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

The Jenkins stages are Checkout, Build and Lint, Unit Tests, Docker Test Image, and Docker Runtime Image. A failed command stops the pipeline. Pytest results are published and archived.

## Suggested Git history

Use separate branches and meaningful commits, for example:

```text
main
├── feature/flask-api
├── test/pytest-suite
└── ci/docker-pipelines
```

Suggested commits:

```text
feat: add ACEest Flask API and dashboard
test: add API and fitness-domain coverage
build: add secure multi-stage Docker image
ci: add GitHub Actions and Jenkins pipelines
docs: add setup and CI CD documentation
```

## Publishing from the cloud server to GitHub

Create an empty public GitHub repository, then run:

```bash
git init
git branch -M main
git add .
git commit -m "feat: add ACEest Flask application"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the placeholders with the real GitHub username and repository name. Never commit passwords, access tokens, `.venv`, or local cache files.
