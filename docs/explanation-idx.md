# Explanation

This part of the project documentation focuses on an
**understanding-oriented** approach. You'll get a
chance to read about the background of the project,
as well as reasoning about how it was implemented.

> **Note:** Expand this section by considering the
> following points:

- Give context and background on this applicaiton
- Explain why
- Provide multiple examples and approaches of how
    to work with it
- Help the reader make connections
- Avoid writing instructions or technical descriptions
    here

## System

### Application structure

#### [File and Directory](explanation/file_and_directory.md)

- Application source code file and directory explanation

#### Application Architecture

- Layer Archtiecture

- Sequence diagram

### Develop tools

#### [Visual Code](explanation/vcode.md)

- Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS and Linux.

- Workbench

#### Data Inventory/SQLG

- Data zone view

- Program Map

### Application deployment architecture

#### Architecture

### Components

- This section explain feature and architecture for each components

### Configuration

#### Configuration by phase

#### Configuration file relationship

- TBD

#### Service-Side Rendering

- (Django+HTMX, iommi, dash)
- (Django+Vue.js+Components)

| Aspect| ServerSideRender| FrontEnd/BackEnd| Role Changes in DevOps                                                                                                                                       |
|----------------------|-------------------------------------------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Frontend Development | Minimal JavaScript, more HTML and server-side logic   | Heavy JavaScript, client-side rendering         | Frontend developers may focus more on HTML and less on complex JavaScript in SSR. In Vue.js, frontend developers handle most of the UI logic.                |
| Backend Development  | Increased responsibility for  Domain Models and Logic | Backend serves APIs, minimal direct UI updates  | Backend developers need to ensure server responses include appropriate HTML for SSR. In Vue.js, they provide JSON data.                                      |
| State Management     | Managed primarily server-side                         | Managed primarily client-side with Vuex         | Backend developers in SSR handle more state logic, while in Vue.js, frontend developers manage state with tools like Vuex.                                   |
| Build Process        | Simpler build process, less dependency management     | Complex build process with Webpack, Babel       | DevOps may simplify CI/CD pipelines for SSR due to fewer dependencies, whereas Vue.js requires handling complex build tools.                                 |
| Testing              | Backend endpoints and Domain Models                   | Frontend components and backend APIs            | DevOps needs to focus more on backend tests and integration tests for SSR. For Vue.js, there is a heavier emphasis on frontend unit and integration testing. |
| CI/CD Pipelines      | Unified pipeline focusing on backend deployments      | Separate pipelines for frontend and backend     | DevOps integrates more backend-oriented CI/CD processes for SSR, while in Vue.js, they maintain separate pipelines for both.                                 |

<!-- 
## Business

### Process

### Organization

 -->
