$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
try {
    $pythonCandidate = $null
    $pythonPrefix = @()
    $checkCode = 'import sys,struct; sys.exit(0 if (3,10)<=sys.version_info[:2]<=(3,13) and struct.calcsize(chr(80))==8 else 1)'
    if (Get-Command py -ErrorAction SilentlyContinue) {
        foreach ($version in @('-3.12','-3.13','-3.11','-3.10')) {
            try {
                & py $version -c $checkCode 2>$null
                if ($LASTEXITCODE -eq 0) { $pythonCandidate='py'; $pythonPrefix=@($version); break }
            } catch { }
        }
    }
    if (-not $pythonCandidate) {
        $candidates = @('python', (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'))
        foreach ($candidate in $candidates) {
            if (Get-Command $candidate -ErrorAction SilentlyContinue) {
                try {
                    & $candidate -c $checkCode 2>$null
                    if ($LASTEXITCODE -eq 0) { $pythonCandidate=$candidate; break }
                } catch { }
            }
        }
    }
    if (-not $pythonCandidate) { throw 'Instale Python 3.12 x64 (python.org), incluindo o launcher py, e execute novamente.' }
    if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
        & $pythonCandidate @pythonPrefix -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar o ambiente virtual.' }
    }
    & .\.venv\Scripts\python.exe -c $checkCode
    if ($LASTEXITCODE -ne 0) { throw 'O ambiente .venv existente nao usa Python 3.10-3.13 x64 compativel.' }
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias. Confira a conexao e a mensagem do pip.' }
    Write-Host 'Ambiente preparado. Abra INICIAR.bat.' -ForegroundColor Green
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
