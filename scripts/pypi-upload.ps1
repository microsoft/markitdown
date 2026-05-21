# 上传 markitdown-glmocr 和 markitdown-paddleocr 到 PyPI
# 用法: .\scripts\pypi-upload.ps1 [-Version "0.2.0"]
#   -Version: 可选，指定版本号，默认上传 dist 目录下所有文件

param(
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== PyPI Upload Script ===" -ForegroundColor Green
Write-Host ""

# 从用户环境变量读取 PYPI_API_TOKEN
$PypiToken = [System.Environment]::GetEnvironmentVariable('PYPI_API_TOKEN', 'User')

if ([string]::IsNullOrEmpty($PypiToken)) {
    Write-Host "错误: 未找到 PYPI_API_TOKEN 环境变量" -ForegroundColor Red
    Write-Host "请在 Windows 用户环境变量中配置 PYPI_API_TOKEN"
    exit 1
}

Write-Host "✓ PyPI API Token 已加载" -ForegroundColor Green
Write-Host ""

# 设置 UTF-8 编码
$env:PYTHONUTF8 = "1"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

$Packages = @("markitdown-glmocr", "markitdown-paddleocr")

foreach ($Pkg in $Packages) {
    $PkgDir = Join-Path $ProjectRoot "packages\$Pkg"
    $DistDir = Join-Path $PkgDir "dist"
    
    if (-not (Test-Path $DistDir)) {
        Write-Host "跳过 $Pkg : dist 目录不存在" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "--- 上传 $Pkg ---" -ForegroundColor Green
    
    # 获取包名格式 (markitdown-glmocr -> markitdown_glmocr)
    $PkgName = $Pkg -replace '-', '_'
    
    # 确定要上传的文件
    if ($Version) {
        $Pattern = "$PkgName-$Version*"
    } else {
        $Pattern = "$PkgName*"
    }
    
    $UploadFiles = Get-ChildItem -Path $DistDir -Filter $Pattern -ErrorAction SilentlyContinue
    
    if ($UploadFiles) {
        Write-Host "文件:"
        $UploadFiles | ForEach-Object { Write-Host "  $($_.Name)" }
        Write-Host ""
        
        $FilesArg = $UploadFiles | ForEach-Object { $_.FullName }
        & twine upload --username __token__ --password $PypiToken --disable-progress-bar @FilesArg
        
        # 提取版本号
        $LatestVersion = ($UploadFiles[0].Name | Select-String -Pattern '\d+\.\d+\.\d+').Matches.Value
        Write-Host "✓ $Pkg 上传成功!" -ForegroundColor Green
        Write-Host "  https://pypi.org/project/$Pkg/$LatestVersion/" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "跳过 $Pkg : 未找到版本 $Version 的构建文件" -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host "=== 上传完成 ===" -ForegroundColor Green
