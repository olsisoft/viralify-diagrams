# Push Instructions for viralify-diagrams

## Option 1: Using GitHub Web Interface (Easiest)

1. Go to https://github.com/new
2. Create repository:
   - Owner: olsisoft
   - Name: viralify-diagrams
   - Description: Professional diagram generation for video content with theme customization and animation support
   - Visibility: Public
   - Do NOT initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"
4. Run these commands in terminal:

```bash
cd "C:\Users\njomi\OneDrive\Documents\projects\viralify-diagrams"
git remote add origin git@github.com:olsisoft/viralify-diagrams.git
git push -u origin master
```

## Option 2: Using HTTPS with Personal Access Token

If SSH doesn't work, use HTTPS with a PAT:

1. Create PAT at: https://github.com/settings/tokens/new
   - Note: "viralify-diagrams push"
   - Select scopes: repo (full control)
   - Generate token and copy it

2. Run these commands:

```bash
cd "C:\Users\njomi\OneDrive\Documents\projects\viralify-diagrams"
git remote add origin https://github.com/olsisoft/viralify-diagrams.git
git push -u origin master
```

When prompted:
- Username: your-github-username
- Password: paste your PAT (not your GitHub password)

## Option 3: Using GitHub CLI

Install GitHub CLI first, then:

```bash
gh auth login
cd "C:\Users\njomi\OneDrive\Documents\projects\viralify-diagrams"
gh repo create olsisoft/viralify-diagrams --public --source=. --remote=origin --push
```

## After Push

Delete this file:
```bash
rm PUSH_TO_GITHUB.md
```

The library will be available at: https://github.com/olsisoft/viralify-diagrams
