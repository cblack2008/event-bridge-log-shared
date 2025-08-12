#!/bin/bash
set -euo pipefail

echo "🧹 Resetting repository for portfolio presentation..."

# Step 1: Delete all tags (local and remote)
echo "📋 Deleting all tags..."
if git tag -l | grep -q .; then
    echo "Found tags to delete:"
    git tag -l

    # Delete local tags
    git tag -l | xargs git tag -d

    # Delete remote tags
    echo "Deleting remote tags..."
    git tag -l | xargs -n 1 git push --delete origin 2>/dev/null || true
else
    echo "No tags found to delete."
fi

# Step 2: Create orphan branch with clean history
echo "🔄 Creating clean history..."
git checkout --orphan clean-main

# Step 3: Add all current files
echo "📁 Adding all current files..."
git add .

# Step 4: Create initial commit
echo "📝 Creating initial commit..."
git commit -m "Initial commit: Event Bridge Log Shared Package

A comprehensive shared library for Event Bridge Log Analytics Platform.

Features:
- Pydantic models for event validation
- Type-safe utilities for AWS resources
- Automated CI/CD with GitHub Actions
- PyPI publishing with trusted publisher
- Modern Python packaging (Python 3.13)"

# Step 5: Delete old main branch and rename
echo "🔀 Replacing main branch..."
git branch -D main 2>/dev/null || true
git branch -m clean-main main

# Step 6: Force push new history
echo "⬆️  Pushing clean history..."
git push -f origin main

echo "✅ Repository reset complete!"
echo ""
echo "📋 Manual steps remaining:"
echo "1. Go to GitHub Actions tab and delete workflow runs"
echo "2. Close/delete any remaining PRs"
echo "3. Update personal references in files if needed"
echo "4. Delete this script: rm reset-for-portfolio.sh"
echo ""
echo "🎯 Your portfolio repository is ready!"
