$ErrorActionPreference = "Stop"

$expected = @(
  @{ Group = "01-ai-app-agent-architecture"; Repos = @("openai-agents-python", "langchain", "autogen", "llama_index") },
  @{ Group = "02-model-serving-inference"; Repos = @("vllm", "llama.cpp", "transformers") },
  @{ Group = "03-fine-tuning-training"; Repos = @("peft", "DeepSpeed") },
  @{ Group = "04-rag-vector-database"; Repos = @("qdrant", "chroma") },
  @{ Group = "05-observability-evaluation-llmops"; Repos = @("langfuse", "phoenix", "mlflow", "trulens") },
  @{ Group = "06-tooling-mcp-ai-platform"; Repos = @("servers", "open-webui") }
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$problems = New-Object System.Collections.Generic.List[string]
$docs = New-Object System.Collections.Generic.List[object]
$minimumMermaidDiagrams = 6
$minimumTokensByLang = @{
  en = 2500
  vi = 3000
}

foreach ($group in $expected) {
  foreach ($repo in $group.Repos) {
    foreach ($lang in @("en", "vi")) {
      $path = Join-Path $root (Join-Path $group.Group (Join-Path $repo "README.$lang.md"))
      if (-not (Test-Path -LiteralPath $path)) {
        $problems.Add("Missing: $path")
        continue
      }

      $content = Get-Content -LiteralPath $path -Raw
      $mermaidCount = ([regex]::Matches($content, "```mermaid")).Count
      $wordishCount = ([regex]::Matches($content, "\b[\p{L}\p{N}][\p{L}\p{N}\-_/\.]*\b")).Count
      $placeholderCount = ([regex]::Matches($content, "\b(TBD|TODO|FIXME|PLACEHOLDER|Lorem ipsum)\b", "IgnoreCase")).Count

      if ($mermaidCount -lt $minimumMermaidDiagrams) {
        $problems.Add("Too few Mermaid diagrams ($mermaidCount, expected >= $minimumMermaidDiagrams): $path")
      }
      if ($wordishCount -lt $minimumTokensByLang[$lang]) {
        $problems.Add("Likely too shallow ($wordishCount tokens, expected >= $($minimumTokensByLang[$lang])): $path")
      }
      if ($placeholderCount -gt 0) {
        $problems.Add("Placeholder text found ($placeholderCount): $path")
      }

      $docs.Add([pscustomobject]@{
        Group = $group.Group
        Repo = $repo
        Lang = $lang
        Mermaid = $mermaidCount
        Tokens = $wordishCount
        Path = $path
      })
    }
  }
}

$docs | Sort-Object Group, Repo, Lang | Format-Table Group, Repo, Lang, Mermaid, Tokens -AutoSize

if ($problems.Count -gt 0) {
  Write-Output ""
  Write-Output "Problems:"
  foreach ($problem in $problems) {
    Write-Output " - $problem"
  }
  exit 1
}

Write-Output ""
Write-Output "Validation passed: all expected bilingual docs exist, contain >= $minimumMermaidDiagrams Mermaid diagrams, and pass the depth/placeholder sanity checks."
