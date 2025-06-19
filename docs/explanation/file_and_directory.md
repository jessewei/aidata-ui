# Explanation

## System

### File and directory - 1st Level

| File / Directory | Description                                                                                                                   |
|------------------|-------------------------------------------------------------------------------------------------------------------------------
| config           | Configuration files                                                                                                |
| docs             | MkDocs output directory                                                                                                       |
| fixture          | Seeded data for initial or testing                                                                                            |
| mkdocs.yml       | MkDocs project settings are configured by default using a YAML configuration file in the project directory named mkdocs.yml   |
| README.md        | Application overview                                                                                                          |
| src              | Application source root directory                                                                                             |
| script           | Scripts for Django and Airflow                                                                                                |
| test             | Unit test case                                                                                                                |
| .venv             | venv diretory                                                                                                                |
| _old             | Staging before remove files from git                                                                                         |


### /src/
- extractor: Source extraction script
- planpy: Python planner, without DI definition
- planxl: Excel planner, required DI to genereate plan
- pms: Project management logetl, eg. redmine
- dg: Data govenance, simularity compare and genealog 
- scheduler: operator, job, task helper package


