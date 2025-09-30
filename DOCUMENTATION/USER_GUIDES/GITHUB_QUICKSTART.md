# GitHub Quick Start Checklist

**🚀 Get your pipeline on GitHub in 5 minutes**

---

## ✅ Pre-Flight Check

Run these commands to verify everything is safe:

```bash
cd /mnt/d/Genome

# 1. Verify .gitignore exists
ls -la .gitignore && echo "✅ .gitignore exists" || echo "❌ Missing!"

# 2. Check that databases are excluded
git check-ignore databases/ && echo "✅ Databases excluded" || echo "❌ WARNING: Databases NOT excluded!"

# 3. Check that VCF files are excluded  
git check-ignore DATA/INPUTS/raw_vcfs/*.vcf.gz && echo "✅ VCFs excluded" || echo "✅ No VCFs found (or excluded)"

# 4. Check email credentials
git check-ignore UTILITIES/email_notifications/email_config.json && echo "✅ Credentials excluded" || echo "⚠️ Check manually"
```

**If all checks pass, proceed! If not, fix issues first.**

---

## 🎯 5-Minute Setup

### Step 1: Initialize Git (30 seconds)

```bash
cd /mnt/d/Genome

# Initialize repository if not already done
git init

# Verify
git status
```

### Step 2: Stage Files (1 minute)

```bash
# Option A: Use automated script (recommended)
bash stage_for_github.sh

# Option B: Manual staging
git add .gitignore MAIN_README.md environment.yml requirements.txt
git add COMPONENTS/**/*.py PIPELINES/**/*.py UTILITIES/**/*.py
git add COMPONENTS/**/*.sh PIPELINES/**/*.sh UTILITIES/**/*.sh
git add DOCUMENTATION/**/*.md
git add PIPELINES/**/*.json PIPELINES/**/*.yaml
git add DATA/**/.gitkeep DATA/**/README.md
```

### Step 3: Review What's Staged (30 seconds)

```bash
# Quick check
git status

# Count files
git diff --cached --name-only | wc -l

# Should be ~100-200 files, ~50-150MB total
# If you see 1000+ files or >500MB, STOP and investigate!
```

### Step 4: Commit (30 seconds)

```bash
git commit -m "Initial commit: Clinical Genomics Pipeline v4.1

- Complete 3-stage pipeline (DRAGEN → VEP → Analysis)
- 22 medical specialties, 626 genes
- Comprehensive documentation
- Tested on whole genome scale

Excludes: ~1.1TB databases and patient data"
```

### Step 5: Push to GitHub (2 minutes)

#### Option A: GitHub CLI (fastest)
```bash
# Install if needed: winget install GitHub.cli
gh auth login
gh repo create clinical-genomics-pipeline --private --source=. --remote=origin --push
```

#### Option B: Manual
1. Create repo at https://github.com/new
   - Name: `clinical-genomics-pipeline`
   - Private repository
   - Do NOT initialize with README
2. Connect and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/clinical-genomics-pipeline.git
git branch -M main
git push -u origin main
```

---

## ⚠️ CRITICAL: Verify Upload

```bash
# 1. Check repository size (should be <200MB)
gh repo view --json diskUsage

# 2. Verify no sensitive files
# Go to GitHub.com and manually check:
# - No *.vcf.gz files
# - No *.bam files  
# - No email_config.json (only email_config_template.json)
# - No large database files

# 3. Check file count
# Should see ~100-200 files total on GitHub
```

---

## 🎉 Success Criteria

Your GitHub repository should have:

- ✅ **~100-200 files** (code + documentation)
- ✅ **~50-150MB** total size
- ✅ **No patient data** (no .vcf.gz, .bam files)
- ✅ **No credentials** (no email_config.json)
- ✅ **No databases** (no databases/ content)
- ✅ **Complete structure** (all directories present)
- ✅ **All documentation** (all .md files)
- ✅ **All code** (all .py and .sh files)

---

## 🆘 Quick Troubleshooting

### "Too many files being added"
```bash
# Check what's being tracked
git ls-files | wc -l

# Should be ~100-200 files
# If >500 files, something is wrong with .gitignore
```

### "Repository too large"  
```bash
# Find large files
git ls-files | xargs ls -lh | awk '{if ($5+0 > 10) print $9, $5}'

# Should see no files >10MB
# If you do, they shouldn't be committed!
```

### "Can't find .git directory"
```bash
# Check if Git is initialized
ls -la .git

# If missing, run: git init
```

### "VCF files are being added"
```bash
# STOP IMMEDIATELY!
# Fix .gitignore first
# Remove from staging: git reset HEAD *.vcf.gz
```

---

## 📚 Full Documentation

For detailed information, see:
- `GITHUB_PREPARATION.md` - Complete preparation guide
- `DOCUMENTATION/USER_GUIDES/INSTALLATION_GUIDE.md` - Setup instructions
- `DOCUMENTATION/TECHNICAL_DOCS/TROUBLESHOOTING.md` - Common issues

---

## 🔄 Daily Workflow

After initial setup, use this simple workflow:

```bash
# 1. Make changes to your code
# 2. Stage changes
git add <modified_files>

# 3. Commit
git commit -m "Description of changes"

# 4. Push
git push origin main
```

---

**Last Updated:** September 2025  
**Pipeline Version:** 4.1.0  
**Estimated Time:** 5-10 minutes
