$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent $root

$requiredFiles = @(
  "README.md",
  "../README.md",
  "docs/en/README.md",
  "docs/en/curriculum.md",
  "docs/en/projects.md",
  "docs/en/reference-atlas.md",
  "docs/en/glossary.md",
  "docs/vi/README.md",
  "docs/vi/curriculum.md",
  "docs/vi/projects.md",
  "docs/vi/reference-atlas.md",
  "docs/vi/glossary.md"
  "../templates/README.md",
  "../templates/architecture-decision-record.md",
  "../templates/runtime-decision-matrix.md",
  "../templates/rag-data-contract.md",
  "../templates/llmops-evaluation-scorecard.md",
  "../templates/production-readiness-checklist.md",
  "../templates/security-governance-review.md",
  "../capstone/README.md",
  "../assessments/README.md",
  "../assessments/en/architecture-review-exam.md",
  "../assessments/en/answer-key.md",
  "../assessments/vi/bai-kiem-tra-kien-truc.md",
  "../assessments/vi/dap-an.md",
  "../CONTRIBUTING.md",
  "../CODE_OF_CONDUCT.md",
  "../SECURITY.md",
  "../ROADMAP.md",
  "../CHANGELOG.md",
  "../LICENSE",
  "../assets/social-preview.svg"
)

$requiredAssets = @(
  "../assets/social-preview.png"
)

$problems = New-Object System.Collections.Generic.List[string]
$summary = New-Object System.Collections.Generic.List[object]

foreach ($relative in $requiredFiles) {
  $path = Join-Path $root $relative
  if (-not (Test-Path -LiteralPath $path)) {
    $problems.Add("Missing required file: $relative")
    continue
  }

  $content = Get-Content -LiteralPath $path -Raw
  $tokens = ([regex]::Matches($content, "\b[\p{L}\p{N}][\p{L}\p{N}\-_/\.]*\b")).Count
  $mermaid = ([regex]::Matches($content, "```mermaid")).Count
  $placeholders = ([regex]::Matches($content, "\b(TBD|TODO|FIXME|PLACEHOLDER|Lorem ipsum)\b", "IgnoreCase")).Count

  $isMarkdown = [System.IO.Path]::GetExtension($relative) -eq ".md"

  if ($relative -eq "README.md" -and $tokens -lt 1200) {
    $problems.Add("Root README is likely too shallow ($tokens tokens): $relative")
  }

  if ($isMarkdown -and $relative -ne "README.md" -and $tokens -lt 250) {
    $problems.Add("Knowledge page is likely too shallow ($tokens tokens): $relative")
  }

  if ($relative -like "docs/*/README.md" -and $mermaid -lt 1) {
    $problems.Add("Language homepage needs at least one Mermaid diagram: $relative")
  }

  if ($relative -like "docs/*/curriculum.md" -and $mermaid -lt 3) {
    $problems.Add("Curriculum should contain at least three Mermaid diagrams: $relative")
  }

  if ($relative -like "docs/*/projects.md" -and $mermaid -lt 2) {
    $problems.Add("Projects page should contain at least two Mermaid diagrams: $relative")
  }

  if ($placeholders -gt 0) {
    $problems.Add("Placeholder text found ($placeholders): $relative")
  }

  $summary.Add([pscustomobject]@{
    File = $relative
    Mermaid = $mermaid
    Tokens = $tokens
  })
}

foreach ($relative in $requiredAssets) {
  $path = Join-Path $root $relative
  if (-not (Test-Path -LiteralPath $path)) {
    $problems.Add("Missing required asset: $relative")
    continue
  }
  $asset = Get-Item -LiteralPath $path
  if ($asset.Length -lt 1000) {
    $problems.Add("Required asset looks too small ($($asset.Length) bytes): $relative")
  }
  $summary.Add([pscustomobject]@{
    File = $relative
    Mermaid = 0
    Tokens = "asset:$($asset.Length)"
  })
}

$linkedTargets = @(
  "repo-architecture-docs/README.md",
  "repo-architecture-docs/01-ai-app-agent-architecture",
  "repo-architecture-docs/02-model-serving-inference",
  "repo-architecture-docs/03-fine-tuning-training",
  "repo-architecture-docs/04-rag-vector-database",
  "repo-architecture-docs/05-observability-evaluation-llmops",
  "repo-architecture-docs/06-tooling-mcp-ai-platform"
)

foreach ($relative in $linkedTargets) {
  $target = Join-Path $workspaceRoot $relative
  if (-not (Test-Path -LiteralPath $target)) {
    $problems.Add("Expected source documentation target is missing: $relative")
  }
}

$summary | Sort-Object File | Format-Table File, Mermaid, Tokens -AutoSize

if ($problems.Count -gt 0) {
  Write-Output ""
  Write-Output "Problems:"
  foreach ($problem in $problems) {
    Write-Output " - $problem"
  }
  exit 1
}

Write-Output ""
Write-Output "Validation passed: bilingual knowledge system files exist, are substantive, include diagrams, and link to the source architecture docs."
