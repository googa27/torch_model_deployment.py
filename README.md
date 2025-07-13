# Overview

This project demonstrates deploying a machine learning model using modern DevOps practices, including containerization, unit testing, CI/CD, Infrastructure as Code (IaC), and comprehensive docstrings.

## Objectives

- **Containerization:** Package the model and its dependencies using Docker.
- **Unit Tests:** Ensure code reliability with automated tests.
- **CI/CD:** Automate build, test, and deployment pipelines.
- **IaC:** Provision infrastructure using tools like Terraform or Ansible.
- **Docstrings:** Maintain clear and informative code documentation.

## Project Structure

```
.
├── src/                # Source code and model
├── tests/              # Unit tests
├── Dockerfile          # Containerization setup
├── .github/workflows/  # CI/CD pipelines
├── infra/              # IaC scripts
└── README.md           # Project documentation
```

## Getting Started

1. **Clone the repository**
2. **Build the Docker image**
    ```bash
    docker build -t tenpo-model .
    ```
3. **Run unit tests**
    ```bash
    pytest tests/
    ```
4. **Deploy infrastructure**
    ```bash
    cd infra/
    terraform apply
    ```

## Contributing

- Write clear docstrings for all functions and classes.
- Ensure all tests pass before submitting changes.
- Follow the established CI/CD workflow.

## License

MIT License.
