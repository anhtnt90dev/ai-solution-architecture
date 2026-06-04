$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$siteRoot = Join-Path $root "site"
$problems = New-Object System.Collections.Generic.List[string]

$required = @(
  "site/learn/index.html",
  "site/learn/en/index.html",
  "site/learn/en/curriculum.html",
  "site/learn/en/projects.html",
  "site/learn/en/reference-atlas.html",
  "site/learn/en/glossary.html",
  "site/learn/vi/index.html",
  "site/learn/vi/curriculum.html",
  "site/learn/vi/projects.html",
  "site/learn/vi/reference-atlas.html",
  "site/learn/vi/glossary.html",
  "site/templates/index.html",
  "site/templates/architecture-decision-record.html",
  "site/templates/runtime-decision-matrix.html",
  "site/templates/rag-data-contract.html",
  "site/templates/llmops-evaluation-scorecard.html",
  "site/templates/production-readiness-checklist.html",
  "site/templates/security-governance-review.html",
  "site/capstone/index.html",
  "site/assessments/index.html",
  "site/deep-dives/index.html"
)

foreach ($relative in $required) {
  $path = Join-Path $root $relative
  if (-not (Test-Path -LiteralPath $path)) {
    $problems.Add("Missing site page: $relative")
  }
}

$landing = Join-Path $root "index.html"
$landingText = Get-Content -LiteralPath $landing -Raw
if ($landingText -match "github\.com/anhtnt90dev/ai-solution-architecture/(blob|tree)/main") {
  $problems.Add("Landing page still links to GitHub source file/tree views.")
}

if ($landingText -notmatch "site/learn/en/" -or $landingText -notmatch "site/templates/" -or $landingText -notmatch "site/deep-dives/") {
  $problems.Add("Landing page does not link to generated site pages.")
}

$htmlFiles = Get-ChildItem -LiteralPath $siteRoot -Recurse -Filter "*.html"
foreach ($file in $htmlFiles) {
  $content = Get-Content -LiteralPath $file.FullName -Raw
  $localMarkdownLinks = [regex]::Matches($content, 'href="(?!https?://|mailto:|tel:|#)[^"]+\.md(?:#[^"]*)?"')
  if ($localMarkdownLinks.Count -gt 0) {
    $problems.Add("Generated page contains local Markdown links: $($file.FullName)")
  }

  $hrefs = [regex]::Matches($content, 'href="([^"]+)"')
  foreach ($hrefMatch in $hrefs) {
    $href = [System.Net.WebUtility]::HtmlDecode($hrefMatch.Groups[1].Value)
    if ($href -match "^(https?://|mailto:|tel:|#)") {
      continue
    }
    $targetPart = ($href -split "#", 2)[0]
    $targetPart = ($targetPart -split "\?", 2)[0]
    if ([string]::IsNullOrWhiteSpace($targetPart)) {
      continue
    }
    $baseDir = Split-Path -Parent $file.FullName
    $resolved = [System.IO.Path]::GetFullPath((Join-Path $baseDir $targetPart))
    if ($href.EndsWith("/")) {
      $resolved = Join-Path $resolved "index.html"
    }
    if (-not (Test-Path -LiteralPath $resolved)) {
      $relativeFile = [System.IO.Path]::GetRelativePath($root, $file.FullName)
      $problems.Add("Broken local link in ${relativeFile}: $href")
    }
  }
}

if ($problems.Count -gt 0) {
  Write-Output "Problems:"
  foreach ($problem in $problems) {
    Write-Output " - $problem"
  }
  exit 1
}

Write-Output "Validation passed: generated site pages exist, landing links are internal, and local HTML links resolve."
