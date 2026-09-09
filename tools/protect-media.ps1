[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [SecureString]$Passphrase
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$mediaDirectory = Join-Path $root 'fotos'
$archivePath = Join-Path $root 'fotos.tar.gz'
$encryptedPath = Join-Path $root 'fotos.enc'
$plaintextPassphrase = [System.Net.NetworkCredential]::new('', $Passphrase).Password
$openSslCommand = (Get-Command openssl -ErrorAction SilentlyContinue).Source

if (-not $openSslCommand) {
    $gitOpenSsl = 'C:\Program Files\Git\mingw64\bin\openssl.exe'
    if (Test-Path -LiteralPath $gitOpenSsl) {
        $openSslCommand = $gitOpenSsl
    }
}

try {
    if (-not $openSslCommand) {
        throw 'OpenSSL is required. Install it or Git for Windows, then run this script again.'
    }

    $files = Get-ChildItem -LiteralPath $mediaDirectory -File |
        Where-Object { $_.Name -ne '.mantener-esta-carpeta' }
    if (-not $files) {
        throw 'No media files were found in fotos/.'
    }

    Remove-Item -LiteralPath $archivePath, $encryptedPath -Force -ErrorAction SilentlyContinue
    & tar -czf $archivePath -C $root fotos
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not create the media archive.'
    }

    & $openSslCommand enc -aes-256-cbc -md sha256 -pbkdf2 -iter 600000 -salt `
        -in $archivePath -out $encryptedPath -pass "pass:$plaintextPassphrase"
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not encrypt the media archive.'
    }

    Remove-Item -LiteralPath $archivePath -Force
    Write-Host 'Created fotos.enc. Add MEDIA_PASSPHRASE as a GitHub Actions secret before deploying.'
}
finally {
    $plaintextPassphrase = $null
}