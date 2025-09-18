#!/bin/bash
# Git Preparation Script
# Run this to clean up before Git upload

echo "🧹 Cleaning up development artifacts for Git..."

# Remove development directories (already in .gitignore)
rm -rf D:/Genome/Archive/development_archive_for_deletion 2>/dev/null || true

# Ensure key directories exist but are empty
mkdir -p D:/Genome/validation/positive_controls
mkdir -p D:/Genome/validation/negative_controls  
mkdir -p D:/Genome/validation/performance_metrics
mkdir -p D:/Genome/annotation_results/batches
mkdir -p D:/Genome/annotation_results/families

echo "✅ Cleanup complete!"
echo "📁 Ready for Git upload with clean structure"

# Show what will be committed
echo ""
echo "📋 Files ready for Git:"
find D:/Genome -type f -not -path "*/Archive/*" -not -path "*/.*" -not -name "*.vcf*" -not -name "*.log" -not -name "*.html" | head -20
echo "... and more core pipeline files"
