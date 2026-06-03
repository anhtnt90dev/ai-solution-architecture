$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent $root

$requiredFiles = @(
  "README.md",
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

  if ($relative -eq "README.md" -and $tokens -lt 1200) {
    $problems.Add("Root README is likely too shallow ($tokens tokens): $relative")
  }

  if ($relative -ne "README.md" -and $tokens -lt 450) {
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
