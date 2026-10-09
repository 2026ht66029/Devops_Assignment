# Introduction to DevOps Assignment 1

## ACEest Fitness and Gym Rocky Linux Execution Guide

This guide explains the assignment in simple words and gives the exact order for completing it on the provided **Rocky Linux 9.5 (Blue Onyx)** cloud server. Follow the steps from top to bottom. Whenever the guide says **TAKE SCREENSHOT NOW**, capture the evidence before continuing.

## 1. What the assignment is asking you to build

The assignment asks you to take a fitness and gym application through a complete DevOps lifecycle.

You must provide:

1. A working Flask web application.
2. A Git repository with meaningful branches and commit messages.
3. Pytest unit tests that verify the application.
4. A Docker image that packages the application.
5. A GitHub Actions workflow that runs for every push and pull request.
6. A Jenkins BUILD job that pulls the GitHub repository and performs validation.
7. A professional README with setup, testing, Docker, GitHub Actions, and Jenkins explanations.
8. A publicly accessible GitHub repository link for submission.

The supplied code ZIP contains ten Tkinter desktop versions. Those files are useful references for the ACEest fitness domain, but they are not Flask web applications. This solution therefore preserves the gym theme while implementing the required web, test, container, and pipeline structure.

## 2. What the completed solution contains

```text
ACEest_DevOps_CICD_Assignment/
|-- .github/workflows/main.yml
|-- aceest/
|   |-- __init__.py
|   |-- fitness.py
|   `-- templates/index.html
|-- tests/test_app.py
|-- app.py
|-- Dockerfile
|-- Jenkinsfile
|-- compose.yaml
|-- pyproject.toml
|-- requirements.txt
|-- requirements-dev.txt
|-- README.md
`-- ACEest_DevOps_Assignment_Guide.md
```

The application provides a dashboard, health endpoint, training programs, BMI calculation, membership checking, and weekly classes. The tests cover both valid and invalid requests. The Dockerfile uses separate test and runtime stages, and the runtime container uses a non-root user.

## 3. Simple DevOps flow

```text
Cloud server code
      |
      v
Git commits and branches
      |
      v
Public GitHub repository
      |
      +--> GitHub Actions checks every push and pull request
      |
      +--> Jenkins pulls the repository and runs the BUILD pipeline
      |
      v
Tested Docker image
```

## 4. Before starting on the cloud server

This guide is written for the supplied Rocky Linux 9.5 server. Use a normal user with `sudo` access. Do not upgrade the operating-system release unless the course administrator explicitly permits it.

Connect from your computer:

```bash
ssh YOUR_CLOUD_USER@YOUR_SERVER_IP
```

Replace the two placeholders with the real username and IP address.

Customize the cloud terminal prompt so screenshots show your exact BITS ID:

```bash
export PS1='YOUR_REAL_BITS_ID> '
```

Do not submit screenshots containing the placeholder.

Check the server:

```bash
cat /etc/os-release
python3 --version
python3 -m pip --version
git --version
docker --version
java -version
sudo systemctl is-active docker
sudo systemctl is-active jenkins
```

**TAKE SCREENSHOT NOW - SCREENSHOT 1: CLOUD SERVER PREFLIGHT**

Show the BITS ID prompt and the installed versions. If Docker or Java is missing, install them in the next section before taking the screenshot.

## 5. Install required tools on the cloud server

### Basic Python and Git tools for Rocky Linux

```bash
sudo dnf makecache
sudo dnf install -y git python3 python3-pip curl wget ca-certificates unzip dnf-plugins-core

python3 --version
python3 -m pip --version
git --version
```

Rocky Linux 9 normally provides Python 3.9 through its standard repositories. The ACEest host-side code and pinned development tools support Python 3.9. The Docker image and GitHub Actions workflow still use Python 3.12, so their results remain isolated and reproducible.

### Docker Engine

Use Docker's official RHEL repository, which is the appropriate RPM repository for Rocky Linux 9:

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Log out of SSH and reconnect once so the Docker group is applied. Then verify:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

### Jenkins

Install Java first:

```bash
sudo dnf install -y fontconfig java-21-openjdk
java -version
```

Add the Jenkins LTS RPM repository and its current signing key:

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/rpm-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/rpm-stable/jenkins.io-2026.key
```

```bash
sudo dnf install -y jenkins
sudo systemctl daemon-reload
sudo systemctl enable --now jenkins
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

Check the service:

```bash
sudo systemctl status docker --no-pager
sudo systemctl status jenkins --no-pager
```

Jenkins uses port 8080. The safest way to reach it is an SSH tunnel, which requires no public Jenkins firewall rule. Run this on your own computer in a separate terminal:

```bash
ssh -L 8080:127.0.0.1:8080 YOUR_CLOUD_USER@YOUR_SERVER_IP
```

Then open `http://127.0.0.1:8080` on your own computer. If your course environment requires direct access instead, restrict both the cloud-provider security rule and Rocky `firewalld` to your own public IP. Replace the placeholder before running:

```bash
sudo firewall-cmd --permanent --zone=public \
  --add-rich-rule='rule family="ipv4" source address="YOUR_PUBLIC_IP/32" port port="8080" protocol="tcp" accept'
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-rich-rules
```

Never expose Jenkins port 8080 to `0.0.0.0/0`.

## 6. Copy and open the assignment package

Copy the final ZIP from your computer to the cloud server:

```bash
scp ACEest_DevOps_Assignment_Package.zip \
  YOUR_CLOUD_USER@YOUR_SERVER_IP:~/
```

On the cloud server:

```bash
cd ~
unzip ACEest_DevOps_Assignment_Package.zip
cd ACEest_DevOps_CICD_Assignment
ls -la
```

The listing should show `app.py`, `Dockerfile`, `Jenkinsfile`, `README.md`, the `aceest` folder, the `tests` folder, and `.github`.

## 7. Create meaningful Git history

The assignment evaluates Git maturity. Do not place every file into one unexplained commit.

Initialize the repository:

```bash
git init
git branch -M main
git config user.name "YOUR_NAME"
git config user.email "YOUR_EMAIL"
```

### Commit the Flask application

```bash
git add app.py aceest requirements.txt .gitignore
git commit -m "feat: add ACEest Flask API and dashboard"
```

### Add the tests on a separate branch

```bash
git switch -c test/pytest-suite
git add tests requirements-dev.txt pyproject.toml
git commit -m "test: add API and fitness domain coverage"
git switch main
git merge --no-ff test/pytest-suite -m "merge: add automated test suite"
```

### Add Docker and pipelines on another branch

```bash
git switch -c ci/docker-pipelines
git add Dockerfile .dockerignore compose.yaml Jenkinsfile .github
git commit -m "ci: add Docker GitHub Actions and Jenkins pipelines"
git switch main
git merge --no-ff ci/docker-pipelines -m "merge: add CI CD automation"
```

### Add documentation

```bash
git add README.md ACEest_DevOps_Assignment_Guide.md
git commit -m "docs: add cloud execution and pipeline guide"
```

Display the history:

```bash
git log --oneline --graph --decorate --all
git branch
git status
```

**TAKE SCREENSHOT NOW - SCREENSHOT 2: GIT HISTORY**

Show the BITS ID prompt, branch names, meaningful commits, and clean status.

## 8. Run the Python tests on the cloud server

Create the cloud-server virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the build, lint, and tests:

```bash
python -m compileall -q app.py aceest tests
ruff check .
pytest
```

Expected result:

```text
13 passed
Required test coverage of 90% reached
```

**TAKE SCREENSHOT NOW - SCREENSHOT 3: PYTEST AND COVERAGE**

Show the BITS ID prompt, the `pytest` command, passing tests, and coverage at or above 90 percent.

## 9. Run the Flask application

Start the development server:

```bash
python app.py
```

Keep this terminal open. In a second SSH terminal, run:

```bash
curl http://127.0.0.1:5000/health
```

Expected JSON:

```json
{"service":"aceest-fitness-api","status":"healthy","version":"1.0.0"}
```

Test the BMI endpoint:

```bash
curl -X POST http://127.0.0.1:5000/api/bmi \
  -H 'Content-Type: application/json' \
  -d '{"height_cm":180,"weight_kg":75}'
```

Stop the development server with `Control+C` after testing.

**TAKE SCREENSHOT NOW - SCREENSHOT 4: FLASK APPLICATION**

Show the server running and the successful `/health` response. A browser screenshot of the ACEest dashboard can be included as an additional figure.

## 10. Test and run the Docker image

Build the test stage:

```bash
docker build --target test -t aceest:test .
```

Run Pytest inside the container:

```bash
docker run --rm aceest:test
```

**TAKE SCREENSHOT NOW - SCREENSHOT 5: TESTS INSIDE DOCKER**

Show the Docker command and passing tests.

Build the smaller runtime image:

```bash
docker build --target runtime -t aceest:1.0.0 .
docker image ls aceest
```

Run the production container:

```bash
docker run -d --name aceest-app -p 8000:8000 aceest:1.0.0
curl http://127.0.0.1:8000/health
docker ps --filter name=aceest-app
```

**TAKE SCREENSHOT NOW - SCREENSHOT 6: RUNNING DOCKER CONTAINER**

Show the image, running container, and healthy JSON response.

When finished:

```bash
docker stop aceest-app
docker rm aceest-app
```

## 11. Publish the repository to GitHub

In GitHub, create an empty public repository. Do not add a README, license, or `.gitignore` in the GitHub form because those files already exist locally.

On the cloud server, connect and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
git push -u origin test/pytest-suite
git push -u origin ci/docker-pipelines
```

Replace both placeholders. Use a GitHub personal access token or SSH key when prompted. Never place the token inside a command, screenshot, source file, or README.

Open the GitHub repository and confirm that the files are visible.

**TAKE SCREENSHOT NOW - SCREENSHOT 7: PUBLIC GITHUB REPOSITORY**

Show the repository name, public visibility, files, and recent commits. Crop or hide any token, session value, unrelated tab, or private browser information.

## 12. Verify GitHub Actions

The workflow at `.github/workflows/main.yml` automatically runs after a push or pull request. It performs syntax checking, linting, host tests, tests inside Docker, a runtime image build, and a health smoke test.

On GitHub:

1. Open the repository.
2. Select the Actions tab.
3. Open the newest `ACEest CI` run.
4. Wait until every stage is green.
5. Open the job to show the completed steps.

**TAKE SCREENSHOT NOW - SCREENSHOT 8: GITHUB ACTIONS**

Show the repository name, green workflow result, and completed build and test steps.

## 13. Configure the Jenkins BUILD pipeline

If you created the SSH tunnel in Section 5, open Jenkins on your own computer at:

```text
http://127.0.0.1:8080
```

Use `http://YOUR_SERVER_IP:8080` only when direct access has been explicitly allowed and restricted to your own public IP.

Get the initial password on the cloud server:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Do not include that password in a screenshot.

Complete the setup wizard, install suggested plugins, and create the administrator account. Then:

1. Select **New Item**.
2. Enter `ACEest-BUILD`.
3. Select **Pipeline** and choose **OK**.
4. Under Pipeline, choose **Pipeline script from SCM**.
5. Select **Git**.
6. Enter the public GitHub repository URL.
7. Set the branch to `*/main`.
8. Set Script Path to `Jenkinsfile`.
9. Save and select **Build Now**.

The expected stages are Checkout, Build and Lint, Unit Tests, Docker Test Image, and Docker Runtime Image.

If Jenkins reports Docker permission denied, run:

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

**TAKE SCREENSHOT NOW - SCREENSHOT 9: JENKINS BUILD**

Show the `ACEest-BUILD` job, green success status, build number, and completed pipeline stages. Do not show passwords, credentials, or tokens.

## 14. Final screenshot checklist

```text
01-cloud-server-preflight.png
02-git-history.png
03-pytest-coverage.png
04-flask-application.png
05-docker-tests.png
06-docker-runtime.png
07-public-github-repository.png
08-github-actions.png
09-jenkins-build.png
```

Every terminal screenshot should show the exact BITS ID prompt.

## 15. Order for the final assignment document

1. Title page with student name, BITS ID, course, and date.
2. Assignment objective in simple words.
3. Architecture and repository structure.
4. Flask application explanation.
5. Git strategy and Screenshot 2.
6. Pytest strategy and Screenshot 3.
7. Flask execution and Screenshot 4.
8. Docker design and Screenshots 5 and 6.
9. Public GitHub repository and Screenshot 7.
10. GitHub Actions explanation and Screenshot 8.
11. Jenkins BUILD explanation and Screenshot 9.
12. Conclusion and public repository link.

Place a one-sentence caption under every screenshot. Example:

```text
Figure 5: The Docker test image executed the Pytest suite inside the container and passed the required coverage gate.
```

## 16. Final safety and submission checks

- The GitHub repository is public and opens without signing in.
- The repository contains `app.py`, tests, Dockerfile, workflow YAML, Jenkinsfile, and README.
- Git commits are meaningful and branch merges are visible.
- Pytest passes with at least 90 percent coverage.
- Docker tests run inside the test image.
- The runtime container returns a healthy response.
- GitHub Actions is green for the latest `main` commit.
- Jenkins BUILD is green for the same repository.
- The README explains cloud setup, testing, Docker, GitHub Actions, and Jenkins.
- Every screenshot shows the required proof clearly.
- No password, token, SSH key, session token, or unrelated private information is visible.

## 17. Official installation references

- Docker Engine on RHEL: `https://docs.docker.com/engine/install/rhel/`
- Jenkins on Linux: `https://www.jenkins.io/doc/book/installing/linux/`
- Rocky Linux firewalld: `https://docs.rockylinux.org/guides/security/firewalld-beginners/`
- GitHub Actions documentation: `https://docs.github.com/actions`

## 18. Quick troubleshooting

- **`python3: command not found`:** run `sudo dnf install -y python3 python3-pip`, then repeat Section 8.
- **`No module named venv`:** confirm `python3` is installed from the Rocky repositories, then run `sudo dnf reinstall -y python3` and retry `python3 -m venv .venv`.
- **`dnf config-manager: command not found`:** run `sudo dnf install -y dnf-plugins-core`.
- **`permission denied` while using Docker:** reconnect after adding your cloud user to the `docker` group. For Jenkins, add the `jenkins` user to that group and restart Jenkins.
- **Docker commands fail on Rocky Linux:** verify both services and group membership with `sudo systemctl status docker --no-pager` and `id`.
- **Port 5000 or 8000 is already in use:** stop the older Flask process or Docker container before starting another one.
- **GitHub Actions is not visible:** confirm the workflow exists at `.github/workflows/main.yml` on the pushed branch.
- **Jenkins cannot find the repository:** confirm that the repository is public, the URL ends in `.git`, the branch is `*/main`, and the Script Path is exactly `Jenkinsfile`.
- **A test fails:** read the first failure message, fix the code, rerun `pytest`, commit the fix with a meaningful message, and push again so both pipelines validate the same revision.

The safest rule is simple: continue to the next screenshot only after the current command shows the expected successful result.
