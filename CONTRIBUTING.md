# Contributing to ABIDES Configuration Generator

Thank you for your interest in contributing to the ABIDES Configuration Generator! This document provides guidelines for contributing to the project.

## 🚀 Quick Start for Contributors

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Basic understanding of ABIDES framework (helpful but not required)

### Development Setup
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/abides-jpmc-public.git
   cd abides-jpmc-public/ABIDES-Configuration-Generator
   ```
3. Verify the application works:
   ```bash
   python configgen.py --version
   python configgen.py --list-templates
   ```

## 📝 How to Contribute

### 1. Research Templates
Add new academic or industry-standard templates:
- Add template definition to `ResearchTemplates` class in `configgen.py`
- Implement corresponding `build_[template]_config()` method
- Update CLI help text and documentation
- Add usage examples

### 2. Agent Types  
Extend the agent ecosystem:
- Add agent definition to `AgentDefinitions` class
- Update scaling logic and validation
- Add CLI argument for the new agent type
- Document agent behavior and use cases

### 3. Features and Enhancements
- ABIDES-Gym integration improvements
- CLI usability enhancements  
- Performance optimizations
- Additional output formats
- Enhanced validation

### 4. Documentation
- Usage examples and tutorials
- Best practices guides
- Research application documentation
- API documentation improvements

### 5. Testing
- Unit tests for new functionality
- Integration tests for templates
- Performance benchmarks
- Cross-platform compatibility

## 🔧 Development Workflow

### Code Changes
1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes to `configgen.py`
3. Test your changes thoroughly:
   ```bash
   python comprehensive_test_v1.py
   make test
   ```
4. Update documentation as needed
5. Commit with descriptive messages:
   ```bash
   git commit -m "Add momentum-based market maker agent type"
   ```

### Testing Requirements
Before submitting a pull request:
- [ ] All existing tests pass
- [ ] New functionality includes tests
- [ ] Syntax validation passes (`python -m py_compile configgen.py`)
- [ ] Documentation updated for new features
- [ ] Examples provided for new templates/agents

### Pull Request Process
1. Push your branch to your fork
2. Create a pull request with:
   - Clear description of changes
   - Motivation and use case
   - Testing performed
   - Documentation updates
3. Address review feedback promptly
4. Ensure CI/CD checks pass

## 📋 Contribution Guidelines

### Code Style
- Follow existing code patterns in `configgen.py`
- Use descriptive variable and function names
- Add docstrings for new functions and classes
- Maintain the single-file architecture
- Keep zero external dependencies

### Template Guidelines
New research templates should:
- Be based on published research or industry standards
- Include comprehensive documentation
- Provide realistic agent compositions
- Follow existing template patterns
- Include validation and error handling

### Agent Type Guidelines
New agent types should:
- Serve distinct research or simulation purposes
- Include configurable parameters
- Follow ABIDES agent architecture patterns
- Be well-documented with use cases
- Include scaling and validation logic

### Documentation Standards
- Update README.md for major features
- Add examples to `docs/examples.md`
- Include CLI help text updates
- Provide usage examples
- Document research applications

## 🐛 Bug Reports

### Before Reporting
1. Search existing issues for duplicates
2. Test with the latest version
3. Verify the bug with minimal reproduction steps

### Bug Report Template
```
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Command or action taken
2. Expected behavior
3. Actual behavior

## Environment
- Python version: 
- Operating system:
- Configuration generator version: 

## Additional Context
Any additional information, logs, or screenshots
```

## 💡 Feature Requests

### Feature Request Template
```
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Implementation
High-level approach (if you have ideas)

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any additional information or research
```

## 🎯 Research Applications

We especially welcome contributions that:
- Add support for new financial research methodologies
- Extend ABIDES-Gym integration for ML/RL applications
- Improve market microstructure simulation capabilities
- Add behavioral finance modeling features
- Enhance high-frequency trading simulation
- Support new academic research standards

## 📚 Resources

### ABIDES Framework
- [ABIDES Core Documentation](https://github.com/jpmorganchase/abides-jpmc-public)
- [ABIDES-Gym Documentation](https://github.com/jpmorganchase/abides-jpmc-public/tree/main/abides-gym)
- [ABIDES-Markets Documentation](https://github.com/jpmorganchase/abides-jpmc-public/tree/main/abides-markets)

### Research Papers
- RMSC03/04: Reference implementations in the codebase
- Market microstructure literature for agent modeling
- Behavioral finance research for psychological agent types

### Development Tools
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## 🤝 Community

### Communication
- Use GitHub Issues for bugs and feature requests
- GitHub Discussions for questions and general discussion
- Tag maintainers for urgent issues

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Follow open source best practices

### Recognition
Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes for major features

## 📄 License

By contributing to the ABIDES Configuration Generator, you agree that your contributions will be licensed under the Apache 2.0 License.

---

Thank you for contributing to the ABIDES Configuration Generator! Your contributions help advance financial research and market simulation capabilities for the entire community.