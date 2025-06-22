# GitLens Branch Comparison Guide

## Comparing GitHub Branches with GitLens

GitLens is a powerful VS Code extension that enhances Git functionality. Here are the main ways to compare branches:

### Method 1: Using the GitLens View Panel

1. **Open GitLens Panel**: Click on the GitLens icon in the Activity Bar (left sidebar)
2. **Navigate to Branches**: Expand the "Branches" section in the GitLens panel
3. **Compare Branches**: 
   - Right-click on any branch
   - Select "Compare Branch with..." or "Compare with HEAD"
   - Choose the target branch to compare against

### Method 2: Using Command Palette

1. **Open Command Palette**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. **Search for GitLens Commands**:
   - `GitLens: Compare References...` - Compare any two branches/commits
   - `GitLens: Compare Working Tree with...` - Compare current working tree with a branch
   - `GitLens: Compare HEAD with...` - Compare current branch with another

### Method 3: Using the Source Control View

1. **Open Source Control**: Click the Source Control icon in Activity Bar
2. **Branch Selection**: Click on the current branch name in the status bar
3. **Compare Options**: GitLens adds comparison options in the branch selection menu

### Method 4: Direct Branch Comparison

1. **GitLens Graph View**: 
   - Open Command Palette → `GitLens: Show Commit Graph`
   - Select two commits/branches to compare
   - Right-click and choose "Compare References"

### Key Features When Comparing

- **File Changes**: See all modified files between branches
- **Line-by-line Diff**: View detailed changes in each file
- **Commit History**: See all commits that differ between branches
- **Statistics**: View addition/deletion counts
- **Side-by-side View**: Compare files in split view

### GitHub Integration

- **Pull Request Context**: GitLens shows PR information when available
- **Remote Branches**: Compare local branches with their remote counterparts
- **GitHub Issues**: Links to related GitHub issues in commit messages

### Pro Tips

- Use `GitLens: Open Changes` to see all changes at once
- Enable "File Annotations" for inline blame information
- Use the GitLens Graph for visual branch comparison
- Configure comparison settings in GitLens extension settings

### Keyboard Shortcuts

- `Alt+G, C` - Compare branches (custom shortcut)
- `Alt+G, H` - Show commit history
- `Alt+G, G` - Show Git Graph

This guide covers the essential methods for comparing branches using GitLens in VS Code.