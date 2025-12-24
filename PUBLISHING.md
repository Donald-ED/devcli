# 📦 Publishing DevCLI to PyPI

Make installation dead simple: `pip install devcli`

---

## 🎯 Goal

**Before:**
```bash
git clone https://github.com/user/devcli.git
cd devcli
pip install -e .
```

**After:**
```bash
pip install devcli
```

---

## ✅ Prerequisites

### 1. Create PyPI Account
- Go to https://pypi.org/account/register/
- Verify email
- Enable 2FA (required for publishing)

### 2. Create API Token
- Go to https://pypi.org/manage/account/
- Scroll to "API tokens"
- Click "Add API token"
- Name: "DevCLI Publishing"
- Scope: "Entire account" (or specific to devcli later)
- **Copy the token** (starts with `pypi-`)
- **Save it securely** - you can't see it again!

### 3. Install Publishing Tools
```bash
pip install build twine
```

---

## 📝 Pre-Publishing Checklist

Before publishing, make sure:

- [ ] Version updated in `pyproject.toml` (currently `0.3.1`)
- [ ] `CHANGELOG.md` updated with release notes
- [ ] `README.md` is accurate and helpful
- [ ] All tests pass (if you have any)
- [ ] GitHub username updated in `pyproject.toml` URLs
- [ ] Email updated in `pyproject.toml` authors

**Update these files:**
```bash
# In pyproject.toml, replace:
YOUR_GITHUB_USERNAME → your-actual-username
your-email@example.com → your-actual-email
```

---

## 🚀 Publishing Steps

### Step 1: Clean Previous Builds
```bash
cd /path/to/devcli
rm -rf dist/ build/ *.egg-info
```

### Step 2: Build the Package
```bash
python -m build
```

This creates:
- `dist/devcli-0.3.1-py3-none-any.whl` (wheel)
- `dist/devcli-0.3.1.tar.gz` (source)

### Step 3: Check the Build
```bash
twine check dist/*
```

Should output: `Checking dist/devcli-0.3.1*: PASSED`

### Step 4: Test Upload (TestPyPI)

**First time? Upload to TestPyPI to make sure it works:**

```bash
twine upload --repository testpypi dist/*
```

Enter:
- Username: `__token__`
- Password: `pypi-...` (your API token)

Then test install:
```bash
pip install --index-url https://test.pypi.org/simple/ devcli
```

### Step 5: Upload to Real PyPI
```bash
twine upload dist/*
```

Enter:
- Username: `__token__`
- Password: `pypi-...` (your API token)

**Done!** 🎉

---

## ✅ Verify It Worked

### Check PyPI Page
Visit: https://pypi.org/project/devcli/

Should show:
- Version 0.3.1
- Description
- README
- Links

### Test Installation
```bash
# In a fresh terminal/virtualenv
pip install devcli

# Test it works
devcli --version
devcli hello
```

---

## 📋 Post-Publishing

### 1. Update README
Change installation instructions from:
```markdown
# Install from source
git clone https://github.com/user/devcli.git
cd devcli
pip install -e .
```

To:
```markdown
# Install from PyPI
pip install devcli

# Or install from source for development
git clone https://github.com/user/devcli.git
cd devcli
pip install -e .
```

### 2. Update Website
Change `docs/index.html` installation to:
```html
<code>pip install devcli</code>
```

### 3. Announce It!
- Tweet: "DevCLI is now on PyPI! pip install devcli 🚀"
- Reddit post update
- GitHub release

### 4. Create GitHub Release
- Go to GitHub → Releases → "Create a new release"
- Tag: `v0.3.1`
- Title: "v0.3.1 - Simple AI Coding Assistant"
- Copy changelog notes
- Publish!

---

## 🔄 Future Updates

When you release v0.3.2, v0.4.0, etc:

### 1. Update Version
```bash
# In pyproject.toml
version = "0.3.2"
```

### 2. Update Changelog
```markdown
## [0.3.2] - 2024-12-XX
### Added
- New feature
### Fixed
- Bug fix
```

### 3. Build & Upload
```bash
rm -rf dist/
python -m build
twine check dist/*
twine upload dist/*
```

### 4. Tag Release on GitHub
```bash
git tag v0.3.2
git push origin v0.3.2
```

---

## 💡 Pro Tips

### Save API Token Locally
```bash
# Create ~/.pypirc
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
EOF

chmod 600 ~/.pypirc
```

Now you don't need to enter token each time!

### Automate with GitHub Actions
Later, you can automate publishing with GitHub Actions:
- Push a tag → Automatically builds and publishes to PyPI
- Example: https://github.com/actions/starter-workflows/blob/main/ci/python-publish.yml

### Version Bumping
Use `bump2version` to automate version updates:
```bash
pip install bump2version
bump2version patch  # 0.3.1 → 0.3.2
bump2version minor  # 0.3.1 → 0.4.0
bump2version major  # 0.3.1 → 1.0.0
```

---

## ⚠️ Common Issues

### Issue: "File already exists"
**Solution:** You can't re-upload the same version. Bump version number.

### Issue: "Invalid distribution"
**Solution:** Run `twine check dist/*` to see what's wrong.

### Issue: "Invalid credentials"
**Solution:** 
- Make sure username is `__token__` (with underscores)
- Check your API token is correct
- Try generating a new token

### Issue: Package name taken
**Solution:** 
- Check https://pypi.org/project/devcli/
- If taken, choose different name in `pyproject.toml`
- Common pattern: `devcli-ai`, `cli-dev`, etc.

---

## 📊 After Publishing

### Your package will be:
- ✅ Installable via `pip install devcli`
- ✅ Listed on https://pypi.org/project/devcli/
- ✅ Searchable on PyPI
- ✅ Available in all Python environments
- ✅ Version tracked

### People can now:
```bash
# Install globally
pip install devcli

# Install in virtualenv
python -m venv venv
source venv/bin/activate
pip install devcli

# Use immediately
devcli --version
devcli init
devcli
```

**No more git clone! Just pip install!** 🎉

---

## 🎊 Success!

Once published, users can install with one command:

```bash
pip install devcli
```

**That's it!** No git, no cloning, no confusion. Just works. ✨

---

## 📈 Growth Strategy

1. **v0.3.1:** Initial PyPI release
2. **v0.4.0:** Add features, get feedback
3. **v0.5.0:** Polish based on user requests
4. **v1.0.0:** Stable, production-ready

Each release = more users = more feedback = better product!

---

**Ready to publish?** Follow the steps above and you'll be on PyPI in 10 minutes! 🚀
