# Environment file
$environment = "Mogadpally_Brothers_API.postman_environment.json"

# Get all JSON request files except the environment file
$files = Get-ChildItem -Recurse -Filter *.json |
    Where-Object { $_.Name -ne $environment } |
    Sort-Object FullName

$total = $files.Count
$current = 1

foreach ($file in $files) {

    Write-Host ""
    Write-Host "================================================="
    Write-Host "[$current/$total] Running $($file.FullName)"
    Write-Host "================================================="

    postman collection run `
        $file.FullName `
        -e $environment

    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $($file.Name)" -ForegroundColor Red
    }
    else {
        Write-Host "PASSED: $($file.Name)" -ForegroundColor Green
    }

    $current++
}

Write-Host ""
Write-Host "All requests completed."