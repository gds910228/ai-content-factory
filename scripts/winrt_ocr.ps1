param(
    [Parameter(Mandatory=$true)][string]$SrcDir,
    [Parameter(Mandatory=$true)][string]$OutDir
)
$ErrorActionPreference = 'Stop'

$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType=WindowsRuntime]
Add-Type -AssemblyName System.Runtime.WindowsRuntime

function Await($WinRtTask, $ResultType) {
    $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}

$langs = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages
$langTags = @($langs | ForEach-Object { $_.LanguageTag })
Write-Output ("OCR_LANGS: " + ($langTags -join ','))

$zh = $langs | Where-Object { $_.LanguageTag -like 'zh*' } | Select-Object -First 1
if (-not $zh) { Write-Output 'NO_ZH_LANG'; exit 2 }

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($zh)
if (-not $engine) { Write-Output 'ENGINE_FAIL'; exit 3 }
Write-Output ("ENGINE_OK " + $engine.RecognizerLanguage.LanguageTag)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$pngs = @(Get-ChildItem -Path $SrcDir -Filter '*.png' | Sort-Object Name)
$mapping = @()
$i = 0
foreach ($p in $pngs) {
    $i++
    try {
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($p.FullName)) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $outFile = Join-Path $OutDir ("ocr_" + $i + ".txt")
        $result.Text | Out-File -FilePath $outFile -Encoding UTF8
        $mapping += ("ocr_" + $i + ".txt = " + $p.Name + " (" + [math]::Round($result.Text.Length) + " chars)")
        $stream.Dispose()
        $bitmap.Dispose()
    } catch {
        $mapping += ("ocr_" + $i + ".txt = " + $p.Name + " FAILED: " + $_.Exception.Message)
    }
}
$mapping | Out-File -FilePath (Join-Path $OutDir 'mapping.txt') -Encoding UTF8
Write-Output 'ALL_DONE'
