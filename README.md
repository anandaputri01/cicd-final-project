# Customer Account Service

[![Build Status](https://github.com/anandaputri01/cicd-final-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/anandaputri01/cicd-final-project/actions/workflows/ci-build.yaml)

This repository contains the final project for the CI/CD Pipeline course on Coursera/Skills Network. It demonstrates an automated CI/CD pipeline using GitHub Actions, Tekton, and OpenShift.

## Project Description
A Python-based application that features a fully automated CI/CD pipeline.
- **CI**: GitHub Actions (Linting with Flake8, Testing with Nose)
- **CD**: OpenShift Pipelines (Tekton Tasks for Cleanup and Testing)

## Repository Structure
- `.github/workflows/`: GitHub Actions configuration.
- `.tekton/`: Tekton Tasks for OpenShift.
- `app/`: Source code.
- `tests/`: Unit tests.
