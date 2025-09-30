# GitHub Preparation Guide

**Clinical Genomics Pipeline v4.1 - Production System**

This guide will help you prepare your clinical genomics pipeline for GitHub while excluding large data files and maintaining PHI/PII security.

---

## 📋 Pre-Flight Checklist

### ✅ What WILL Be Committed (~100MB total)
- ✅ All Python scripts (`.py` files) - **Core pipeline code**
- ✅ All Bash scripts (`.sh` files) - **Pipeline orchestration**
- ✅ All documentation (`.md` files) - **Comprehensive guides**
- ✅ Configuration templates (`.json`, `.yaml`, `.yml`) - **Setup examples**
- ✅ Requirements files (`requirements.txt`, `environment.yml`) - **Dependencies**
- ✅ Directory structure (`.gitkeep` files) - **Preserves empty folders**
- ✅ Example data (small test files in `examples/`) - **Usage demonstrations**

### ❌ What WON'T Be Committed (~1.1TB+ excluded)
- ❌ Genomic databases (~436GB) - **Too large, publicly available**
- ❌ Patient VCF files (5-50GB each) - **PHI/PII protected**
- ❌ BAM/CRAM files (10-100GB each) - **PHI/PII protected**
- ❌ Processing results (VCFs, large CSVs) - **Generated outputs**
- ❌ Runtime logs (`.log` files) - **Temporary operational data**
- ❌ HTML reports with patient data - **PHI/PII protected**
- ❌ Email credentials (`email_config.json`) - **Sensitive authentication**

---

## 🚀 Step-by-Step GitHub Preparation

### Step 1: Initialize Git Repository (if not already done)

```bash
cd /mnt/d/Genome

# Check if Git is initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Verify .gitignore is in place
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore file exists"
else
    echo "❌ ERROR: .gitignore missing! This is critical for data security."
    exit 1
fi
```

### Step 2: Verify Database Exclusion

**CRITICAL SECURITY CHECK:**

```bash
# Verify databases are excluded
git check-ignore databases/
git check-ignore DATA/INPUTS/raw_vcfs/*.vcf.gz
git check-ignore DATA/RESULTS/**/*.vcf.gz

# Should return file paths (meaning they're ignored)
# If empty, STOP and fix .gitignore immediately!
```

### Step 3: Stage Files for Commit

```bash
# Add all Python pipeline code
git add COMPONENTS/**/*.py
git add PIPELINES/**/*.py
git add UTILITIES/**/*.py

# Add all shell scripts
git add PIPELINES/**/*.sh
git add UTILITIES/**/*.sh
git add COMPONENTS/**/*.sh

# Add all documentation
git add DOCUMENTATION/**/*.md
git add **/*.md
git add README.md

# Add configuration files
git add environment.yml
git add requirements.txt
git add PIPELINES/**/*.yaml
git add PIPELINES/**/*.json
git add UTILITIES/**/email_config_template.json  # Template only, not actual config!

# Add directory structure markers
git add **/.gitkeep

# Add .gitignore itself
git add .gitignore
```

### Step 4: Review What Will Be Committed

```bash
# See what files are staged
git status

# Review file sizes (ensure no large files)
git ls-files | xargs ls -lh | awk '{if ($5 ~ /M$/) print $9, $5}'

# If you see files >10MB, they probably shouldn't be committed!
```

### Step 5: Create Initial Commit

```bash
# First commit with descriptive message
git commit -m "Initial commit: Clinical Genomics Pipeline v4.1 - Production System

- Complete 3-stage pipeline: DRAGEN preprocessing → VEP v114.2 → Multi-specialty analysis
- 22 medical specialties covering 626 genes
- Research-grade clinical guidance system
- Comprehensive documentation and installation guides
- Tested on whole genome scale (4.7M variants)

Note: Excludes large databases (~1.1TB) and patient data (PHI/PII protected)"
```

### Step 6: Create GitHub Repository

#### Option A: Using GitHub CLI (Recommended)
```bash
# Install GitHub CLI if needed
# Windows: winget install GitHub.cli
# Linux: sudo apt install gh

# Authenticate
gh auth login

# Create repository
gh repo create clinical-genomics-pipeline \
    --private \
    --description "Production Clinical Genomics Pipeline v4.1 - Research-grade variant interpretation system for 22 medical specialties" \
    --source=. \
    --remote=origin \
    --push
```

#### Option B: Using GitHub Web Interface
1. Go to https://github.com/new
2. Repository name: `clinical-genomics-pipeline`
3. Description: "Production Clinical Genomics Pipeline v4.1 - Research-grade variant interpretation"
4. **Select: Private** (recommended for clinical tools)
5. **Do NOT initialize with README** (we already have one)
6. Click "Create repository"

Then connect your local repo:
```bash
git remote add origin https://github.com/YOUR_USERNAME/clinical-genomics-pipeline.git
git branch -M main
git push -u origin main
```

### Step 7: Verify Upload

```bash
# Check remote connection
git remote -v

# Verify pushed commits
git log --oneline

# Check GitHub repository size
gh repo view --json diskUsage
# Should be ~100MB or less
```

---

## 🔍 What Should Appear on GitHub

### Expected Repository Structure
```
clinical-genomics-pipeline/
├── .gitignore                          ✅ Data protection rules
├── README.md                           ✅ Main documentation  
├── MAIN_README.md                      ✅ Detailed overview
├── environment.yml                     ✅ Conda environment
├── requirements.txt                    ✅ Python dependencies
├── EMAIL_NOTIFICATIONS_README.md       ✅ Notification setup
│
├── COMPONENTS/                         ✅ Pipeline components
│   ├── ANNOTATION/                     ✅ VEP configuration
│   ├── BAM_ADVANCED/                   ✅ BAM processing (7 modules)
│   ├── CLASSIFICATION/                 ✅ ACMG classification
│   ├── REPORTING/                      ✅ Report generation
│   └── VCF_PROCESSING/                 ✅ VCF preprocessing
│
├── PIPELINES/                          ✅ Pipeline orchestration
│   ├── BAM_PIPELINE/                   ✅ BAM analysis pipeline
│   └── VCF_PIPELINE/                   ✅ VCF analysis pipeline
│
├── UTILITIES/                          ✅ Helper tools
│   ├── email_notifications/            ✅ Email system (template only)
│   ├── ssh_remote_access/              ✅ Remote access setup
│   └── vcf_downloader/                 ✅ VCF download utility
│
├── DOCUMENTATION/                      ✅ Complete documentation
│   ├── USER_GUIDES/                    ✅ Installation & usage
│   ├── TECHNICAL_DOCS/                 ✅ Architecture & specs
│   └── COMPONENT_DOCS/                 ✅ Component details
│
├── DATA/                               ⚠️ Structure only (data excluded)
│   ├── INPUTS/
│   │   ├── raw_vcfs/                   ❌ Patient VCFs (excluded)
│   │   │   └── README.md               ✅ Usage instructions
│   │   └── bam_files/                  ❌ BAM files (excluded)
│   │       └── README.md               ✅ Usage instructions
│   ├── PROCESSED/                      ❌ Processed data (excluded)
│   ├── LOGS/                           ❌ Runtime logs (excluded)
│   └── RESULTS/                        ❌ Analysis results (excluded)
│
└── databases/                          ❌ 1.1TB databases (excluded)
    └── README.md                       ✅ Download instructions
```

### Key Points
- **~100MB** total repository size (mostly code + documentation)
- **~1.1TB+** excluded (databases + patient data)
- All patient data protected
- Complete setup and usage documentation
- Reproducible installation process

---

## ⚠️ Critical Security Checks

### Before Every Push

```bash
# 1. Verify .gitignore is working
git status --ignored

# 2. Check for large files
git ls-files | xargs ls -lh | awk '{if ($5+0 > 10) print $9, $5}'

# 3. Search for potential PHI/PII
git grep -l "Patient\|MRN\|DOB\|SSN" 2>/dev/null || echo "✅ No obvious PHI found"

# 4. Check email credentials aren't included
git ls-files | grep "email_config.json" && echo "❌ DANGER: email_config.json found!" || echo "✅ Safe"

# 5. Verify VCF files excluded  
git ls-files | grep ".vcf.gz" && echo "❌ DANGER: VCF files found!" || echo "✅ Safe"
```

### If You Find Problems

```bash
# Remove file from staging
git reset HEAD <file>

# Remove file from all history (if accidentally committed)
git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch <file>" \
    --prune-empty --tag-name-filter cat -- --all

# Force push to update remote
git push origin --force --all
```

---

## 📝 Recommended Repository Settings

### On GitHub.com

#### 1. Repository Settings → General
- ✅ **Visibility: Private** (or Public if appropriate)
- ✅ **Default branch: main**
- ✅ **Disable: Wikis** (use DOCUMENTATION/ instead)
- ✅ **Disable: Projects** (unless needed)

#### 2. Repository Settings → Branches
- ✅ **Branch protection for main:**
  - Require pull request before merging
  - Require status checks to pass
  - Require conversation resolution before merging

#### 3. Repository Settings → Collaborators
- Add team members with appropriate permissions
- Use **Read** access for users who should view only
- Use **Write** access for developers
- Use **Admin** access sparingly

#### 4. Repository Settings → Security
- ✅ **Enable: Dependabot alerts**
- ✅ **Enable: Code scanning** (if available)
- ✅ **Enable: Secret scanning**

---

## 🎯 Post-Upload Checklist

### Immediate Actions

```bash
# 1. Add comprehensive README badges
# Add to README.md:
# - License badge
# - Python version badge
# - VEP version badge
# - Last commit badge

# 2. Create releases/tags
git tag -a v4.1.0 -m "Production release v4.1.0 - Tested on whole genome"
git push origin v4.1.0

# 3. Set up branch protection
gh repo edit --enable-branch-protection=main

# 4. Enable GitHub Actions (optional)
# Create .github/workflows/ for automated testing
```

### Documentation Review

- [ ] README.md is comprehensive and welcoming
- [ ] Installation guide is clear and tested
- [ ] Usage examples are provided
- [ ] Troubleshooting guide is detailed
- [ ] License file is included
- [ ] Contributing guidelines (if open source)
- [ ] Citation information (if research tool)

### Community Engagement (if public)

- [ ] Add topics/tags for discoverability
- [ ] Create GitHub Discussions for Q&A
- [ ] Set up issue templates
- [ ] Add code of conduct
- [ ] Create pull request template

---

## 🔄 Ongoing Maintenance

### Regular Updates

```bash
# Update local repository
git pull origin main

# Add changes
git add <modified_files>
git commit -m "Descriptive commit message"
git push origin main
```

### Monthly Database Updates

**Important:** Database updates happen locally only, never push to GitHub!

```bash
# Update ClinVar (monthly)
cd /mnt/d/Genome/databases/clinvar
bash ../../UTILITIES/update_clinvar.sh

# Commit database update documentation
cd /mnt/d/Genome
git add DOCUMENTATION/DATABASE_UPDATES.md
git commit -m "docs: Updated ClinVar to $(date +%Y-%m)"
git push
```

---

## 🆘 Troubleshooting

### "Repository size too large"
```bash
# Find large files
git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    sed -n 's/^blob //p' | \
    sort --numeric-sort --key=2 --reverse | \
    head -20
```

### "Sensitive data detected"
```bash
# Use BFG Repo-Cleaner
brew install bfg  # or download from https://rtyley.github.io/bfg-repo-cleaner/

# Remove large files
bfg --delete-files '*.vcf.gz'
bfg --delete-files '*.bam'

# Clean Git history
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### "Can't push - remote ahead of local"
```bash
# Pull changes first
git pull --rebase origin main

# Resolve conflicts if any
git add <resolved_files>
git rebase --continue

# Push
git push origin main
```

---

## 📚 Additional Resources

### Git Best Practices
- https://git-scm.com/book/en/v2
- https://github.com/github/gitignore
- https://chris.beams.io/posts/git-commit/

### GitHub Documentation
- https://docs.github.com/
- https://docs.github.com/en/get-started/quickstart

### Security
- https://docs.github.com/en/code-security
- https://github.com/awslabs/git-secrets

---

## 📧 Support

For issues with GitHub setup:
1. Check GitHub's status: https://www.githubstatus.com/
2. GitHub documentation: https://docs.github.com/
3. GitHub Community: https://github.community/

For pipeline issues:
- See `DOCUMENTATION/TECHNICAL_DOCS/TROUBLESHOOTING.md`

---

**Last Updated:** September 2025  
**Pipeline Version:** 4.1.0  
**Repository:** Private (recommended for clinical tools)
