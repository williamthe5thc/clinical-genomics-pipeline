#!/bin/bash
# =============================================================================
# Git Staging Script for Clinical Genomics Pipeline
# =============================================================================
# This script stages all appropriate files for GitHub commit while excluding
# large databases and patient data
#
# Usage: bash stage_for_github.sh
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Clinical Genomics Pipeline${NC}"
echo -e "${BLUE}GitHub Staging Script${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "MAIN_README.md" ]; then
    echo -e "${RED}❌ ERROR: Not in Genome directory!${NC}"
    echo "Please run this script from /mnt/d/Genome"
    exit 1
fi

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git repository not initialized${NC}"
    read -p "Initialize Git repository? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        echo -e "${GREEN}✅ Git repository initialized${NC}"
    else
        echo -e "${RED}Exiting...${NC}"
        exit 1
    fi
fi

# Verify .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo -e "${RED}❌ CRITICAL: .gitignore missing!${NC}"
    echo "This is a security risk. Please create .gitignore before proceeding."
    exit 1
fi
echo -e "${GREEN}✅ .gitignore found${NC}"

# Security check: Verify databases are excluded
echo -e "\n${BLUE}Running security checks...${NC}"

# Check if any large files would be added
LARGE_FILES=$(git ls-files --others --exclude-standard | xargs -I {} sh -c 'stat -f%z "{}" 2>/dev/null || stat -c%s "{}" 2>/dev/null' | awk '$1 > 104857600 {count++} END {print count+0}')

if [ "$LARGE_FILES" -gt 0 ]; then
    echo -e "${RED}❌ WARNING: Found $LARGE_FILES files > 100MB${NC}"
    echo "These files should be in .gitignore. Please review before proceeding."
    git ls-files --others --exclude-standard | while read file; do
        SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$SIZE" -gt 104857600 ]; then
            echo "  - $file ($(numfmt --to=iec $SIZE))"
        fi
    done
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Exiting...${NC}"
        exit 1
    fi
fi

# Check for VCF files (patient data)
VCF_COUNT=$(find . -name "*.vcf.gz" -not -path "./.git/*" -not -path "./examples/*" 2>/dev/null | wc -l)
if [ "$VCF_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $VCF_COUNT VCF files (should be excluded)${NC}"
    git check-ignore **/*.vcf.gz >/dev/null 2>&1 && echo -e "${GREEN}✅ VCF files are properly excluded${NC}" || echo -e "${RED}❌ WARNING: VCF files may not be excluded!${NC}"
fi

# Check for email credentials
if [ -f "UTILITIES/email_notifications/email_config.json" ]; then
    if git check-ignore UTILITIES/email_notifications/email_config.json >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Email credentials are excluded${NC}"
    else
        echo -e "${RED}❌ WARNING: email_config.json is NOT excluded!${NC}"
        echo "This file may contain passwords. Please add to .gitignore."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Security checks passed${NC}\n"

# Stage files by category
echo -e "${BLUE}Staging files for commit...${NC}\n"

# 1. Core pipeline files
echo -e "${YELLOW}📦 Staging core pipeline files...${NC}"
git add .gitignore 2>/dev/null || true
git add MAIN_README.md README.md 2>/dev/null || true
git add EMAIL_NOTIFICATIONS_README.md 2>/dev/null || true
git add environment.yml requirements.txt 2>/dev/null || true
git add GITHUB_PREPARATION.md 2>/dev/null || true
echo -e "${GREEN}✅ Core files staged${NC}"

# 2. Python modules
echo -e "\n${YELLOW}🐍 Staging Python modules...${NC}"
git add COMPONENTS/**/*.py 2>/dev/null || true
git add PIPELINES/**/*.py 2>/dev/null || true
git add UTILITIES/**/*.py 2>/dev/null || true
echo -e "${GREEN}✅ Python files staged${NC}"

# 3. Shell scripts
echo -e "\n${YELLOW}📜 Staging shell scripts...${NC}"
git add COMPONENTS/**/*.sh 2>/dev/null || true
git add PIPELINES/**/*.sh 2>/dev/null || true
git add UTILITIES/**/*.sh 2>/dev/null || true
git add **/*.sh 2>/dev/null || true
echo -e "${GREEN}✅ Shell scripts staged${NC}"

# 4. Configuration files
echo -e "\n${YELLOW}⚙️  Staging configuration files...${NC}"
git add PIPELINES/**/*.json 2>/dev/null || true
git add PIPELINES/**/*.yaml 2>/dev/null || true
git add COMPONENTS/**/*.json 2>/dev/null || true
# Add template only, not actual email_config.json
git add UTILITIES/email_notifications/email_config_template.json 2>/dev/null || true
git add COMPONENTS/ANNOTATION/*.txt 2>/dev/null || true
git add COMPONENTS/ANNOTATION/*.pm 2>/dev/null || true
echo -e "${GREEN}✅ Configuration files staged${NC}"

# 5. Documentation
echo -e "\n${YELLOW}📚 Staging documentation...${NC}"
git add DOCUMENTATION/**/*.md 2>/dev/null || true
git add UTILITIES/**/*.md 2>/dev/null || true
git add **/*.md 2>/dev/null || true
echo -e "${GREEN}✅ Documentation staged${NC}"

# 6. Data directory structure (without actual data)
echo -e "\n${YELLOW}📁 Staging directory structure...${NC}"
git add DATA/**/.gitkeep 2>/dev/null || true
git add DATA/**/README.md 2>/dev/null || true
git add databases/README.md 2>/dev/null || true
echo -e "${GREEN}✅ Directory structure staged${NC}"

# Show status
echo -e "\n${BLUE}======================================${NC}"
echo -e "${BLUE}Git Status Summary${NC}"
echo -e "${BLUE}======================================${NC}\n"

# Count staged files
STAGED_COUNT=$(git diff --cached --name-only | wc -l)
echo -e "${GREEN}✅ Total files staged: $STAGED_COUNT${NC}\n"

# Show file breakdown
echo -e "${YELLOW}Staged files by type:${NC}"
echo -e "  Python (.py):      $(git diff --cached --name-only | grep '\.py$' | wc -l)"
echo -e "  Shell (.sh):       $(git diff --cached --name-only | grep '\.sh$' | wc -l)"
echo -e "  Markdown (.md):    $(git diff --cached --name-only | grep '\.md$' | wc -l)"
echo -e "  Config (.json/.yaml): $(git diff --cached --name-only | grep -E '\.(json|yaml)$' | wc -l)"
echo -e "  Other:             $(git diff --cached --name-only | grep -v -E '\.(py|sh|md|json|yaml)$' | wc -l)"

# Estimate repository size
echo -e "\n${YELLOW}Estimated commit size:${NC}"
git diff --cached --name-only | xargs -I {} sh -c 'stat -f%z "{}" 2>/dev/null || stat -c%s "{}" 2>/dev/null || echo 0' | awk '{s+=$1} END {
    if (s < 1024) printf "  %.0f bytes\n", s
    else if (s < 1048576) printf "  %.2f KB\n", s/1024
    else printf "  %.2f MB\n", s/1048576
}'

# Show what's staged
echo -e "\n${BLUE}Preview of staged files (first 20):${NC}"
git diff --cached --name-only | head -20

TOTAL=$(git diff --cached --name-only | wc -l)
if [ "$TOTAL" -gt 20 ]; then
    echo "  ... and $(($TOTAL - 20)) more files"
fi

# Final instructions
echo -e "\n${BLUE}======================================${NC}"
echo -e "${BLUE}Next Steps${NC}"
echo -e "${BLUE}======================================${NC}\n"

echo -e "${YELLOW}Review staged files:${NC}"
echo -e "  git status\n"

echo -e "${YELLOW}Review changes in detail:${NC}"
echo -e "  git diff --cached\n"

echo -e "${YELLOW}Unstage specific file if needed:${NC}"
echo -e "  git reset HEAD <file>\n"

echo -e "${YELLOW}Commit the changes:${NC}"
echo -e "  git commit -m \"Initial commit: Clinical Genomics Pipeline v4.1\"\n"

echo -e "${YELLOW}Create GitHub repository and push:${NC}"
echo -e "  See GITHUB_PREPARATION.md for detailed instructions\n"

echo -e "${GREEN}✅ Staging complete!${NC}"
echo -e "${GREEN}Files are ready for commit.${NC}\n"
