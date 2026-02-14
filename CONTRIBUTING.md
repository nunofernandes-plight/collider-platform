# Contributing to Collider Platform

Thank you for your interest in contributing to the Collider Platform! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- **Report Bugs**: Submit detailed bug reports with reproduction steps
- **Suggest Features**: Propose new features or improvements
- **Write Documentation**: Improve docs, tutorials, or examples
- **Submit Code**: Fix bugs or implement new features
- **Review Pull Requests**: Help review and test PRs

## 🚀 Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/collider-platform.git
cd collider-platform
```

### 2. Set Up Development Environment

```bash
# Start all services
./start.sh

# Or manually
docker-compose up -d
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Code Style

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Maximum line length: 100 characters

```python
def calculate_invariant_mass(px: np.ndarray, py: np.ndarray, 
                            pz: np.ndarray, energy: np.ndarray) -> float:
    """
    Calculate invariant mass from 4-vectors.
    
    Args:
        px: x-component of momentum
        py: y-component of momentum
        pz: z-component of momentum
        energy: Energy
        
    Returns:
        Invariant mass in GeV
    """
    # Implementation
```

### JavaScript/Vue

- Use ES6+ syntax
- Follow Vue.js style guide
- Use meaningful variable names
- Add JSDoc comments for complex functions

```javascript
/**
 * Render particle tracks in Three.js scene
 * @param {Array} particles - Array of particle data
 * @param {THREE.Scene} scene - Three.js scene object
 */
function renderParticleTracks(particles, scene) {
  // Implementation
}
```

## 🧪 Testing

### Backend Tests

```bash
# Run Python tests
cd collision_service
pytest

cd ../analysis_service
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test:unit
```

## 📦 Pull Request Process

1. **Update Documentation**: If you change functionality, update README.md
2. **Add Tests**: Include tests for new features
3. **Update Changelog**: Add entry to CHANGELOG.md
4. **Check Style**: Ensure code follows style guidelines
5. **Test Locally**: Verify everything works with `docker-compose up`

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally with Docker Compose
- [ ] Added unit tests
- [ ] Updated documentation

## Screenshots (if applicable)
Add screenshots for UI changes
```

## 🐛 Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Docker version, etc.)
- Relevant logs

## 💡 Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Implementation complexity estimate

## 📋 Development Guidelines

### Adding a New Service

1. Create service directory
2. Add Dockerfile
3. Add requirements.txt or package.json
4. Update docker-compose.yml
5. Document in README.md

### Database Changes

1. Update init_db.sql
2. Add migration script if needed
3. Test with clean database
4. Document schema changes

### API Changes

1. Update schemas.py
2. Update OpenAPI docs
3. Test endpoints
4. Document in README.md

## 🤝 Code Review

We review PRs for:
- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

- Open a discussion on GitHub
- Tag maintainers in your PR
- Check existing issues and documentation

Thank you for contributing! 🚀⚛️
