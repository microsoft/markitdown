# Contributing to MarkItDown

Welcome! We're pleased that you're considering contributing to this project. Whether you're fixing a typo, reporting a bug, suggesting a feature, or writing code, your contributions are highly valued and appreciated.

## Steps to Contribute

Follow these steps to get started:

1. **Fork the Repository**
   Create a copy of the repository by forking it on GitHub.

2. **Create a Branch**
   Make a branch for your feature or bug fix. Use a meaningful name like `feature/add-login` or `fix/typo-readme`.

3. **Write Your Code**
   Add your changes, write tests if necessary, and ensure your code is clean and well-documented.

4. **Run Tests and Pre-Commit Checks**
   Before submitting, please make sure your code passes all tests and follows the code formatting guidelines (see the [Running Tests and Checks](#running-tests-and-checks) section).

5. **Submit a Pull Request (PR)**
   Open a pull request to share your changes with us. Reviewers will help you improve it.

## Contributor License Agreement (CLA)
Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

- When you submit a pull request, a CLA bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., status check, comment).
- Follow the instructions provided by the bot.
- You will only need to do this once across all repos using our CLA.

## Code of Conduct

We have adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). By participating in this project, you agree to uphold these standards.

- **For FAQs or more information:** Visit the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq).
- **For questions or concerns:** Contact [opencode@microsoft.com](mailto:opencode@microsoft.com).

## Getting Started

Ready to contribute? Start here:

### Issues and PRs
You can help by looking at issues or helping review PRs. Any issue or PR is welcome, but we have also marked some as 'open for contribution' and 'open for reviewing' to help facilitate community contributions. These are of course just suggestions and you are welcome to contribute in any way you like.

<div align="center">

|                       | All                                      | Especially Needs Help from Community                                                                 |
|-----------------------|------------------------------------------|------------------------------------------------------------------------------------------|
| **Issues**            | [All Issues](https://github.com/microsoft/markitdown/issues) | [Issues open for contribution](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs**               | [All PRs](https://github.com/microsoft/markitdown/pulls)     | [PRs open for reviewing](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)               |

</div>

## Running Tests and Checks

- Install `hatch` in your environment and run tests:
    ```sh
    pip install hatch  # Other ways of installing hatch: https://hatch.pypa.io/dev/install/
    hatch shell
    hatch test
    ```

  (Alternative) Use the Devcontainer which has all the dependencies installed:
    ```sh
    # Reopen the project in Devcontainer and run:
    hatch test
    ```

- Run pre-commit checks before submitting a PR: `pre-commit run --all-files`

##### Pre-Commit Checks

Before submitting your pull request, run these checks to ensure code quality:
```sh
pre-commit run --all-files
```

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

Thank you for helping make this project better!
