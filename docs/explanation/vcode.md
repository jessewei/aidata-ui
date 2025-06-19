# Explanation

## System

### Visual Code

#### Solution to Debug with Container

- Use Dev Contiaine first
  
| Feature                  | Dev Containers Extension                                      | Docker Extension                                                 |
|--------------------------|---------------------------------------------------------------|------------------------------------------------------------------|
| Purpose                  | Developing inside a containerized environment                 | Managing Docker containers and images within VS Code             |
| Environment Setup        | Define environment with Dockerfile or Docker Compose          | No specific setup for dev environments                           |
| Isolation                | Provides isolated development environments                    | Manages existing Docker environments                             |
| Remote Development       | Supports developing in a container on local or remote servers | Does not provide remote development capabilities                 |
| Configuration            | Uses .devcontainer.json for setup                             | No specific configuration file                                   |
| Container Management     | Basic container operations as part of dev environment         | Full container management (create, start, stop, remove)          |
| Image Management         | Not focused on image management                               | Pull, build, push, view, and remove Docker images                |
| Docker Compose Support   | Supports Docker Compose for defining environments             | Full Docker Compose support for multi-container applications     |
| Debugging                | Supports debugging in the defined dev container               | Supports debugging of applications running inside containers     |
| Integration with VS Code | Seamlessly integrates with VS Code for dev environment setup  | Integrates with other VS Code extensions for a seamless workflow |
| Ideal Use Cases          | Teams needing consistent development environments             | Managing Docker resources and workflows within VS Code           |

#### [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

- Architecture
  - A devcontainer.json file in your project tells VS Code how to access (or create) a development container with a well-defined tool and runtime stack.
  - Workspace files are mounted from the local file system or copied or cloned into the container.

![img](/docs/img/architecture-containers.png)

- Operating models:

  - You can use a container as your full-time development environment
  - You can attach to a running container to inspect it.
