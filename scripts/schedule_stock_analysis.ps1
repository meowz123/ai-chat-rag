# PowerShell Script: Schedule Daily Stock Analysis
# Runs at 10:00 AM GMT+7 (Vietnam time) every day
# Run this script with: powershell -ExecutionPolicy Bypass -File schedule_stock_analysis.ps1

param(
    [string]$WorkspacePath = "C:\Users\huylt\jabil_session_2",
    [string]$ScriptPath = "scripts\run_daily_analysis.bat",
    [string]$TaskName = "DailyStockAnalysis",
    [string]$Time = "10:00:00"
)

# Verify paths exist
if (-not (Test-Path $WorkspacePath)) {
    Write-Error "Workspace path not found: $WorkspacePath"
    exit 1
}

if (-not (Test-Path "$WorkspacePath\$ScriptPath")) {
    Write-Error "Script not found: $WorkspacePath\$ScriptPath"
    exit 1
}

$FullScriptPath = Join-Path $WorkspacePath $ScriptPath

# Create scheduled task action
$Action = New-ScheduledTaskAction -Execute $FullScriptPath -WorkingDirectory "$WorkspacePath\scripts"

# Create scheduled task trigger (10:00 AM daily)
# Note: System time must be set to GMT+7 or adjust trigger time accordingly
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Create task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable

# Create the scheduled task
$TaskDescription = "Daily VN stock market analysis - fetches market data at 10:00 AM GMT+7"

try {
    # Remove existing task if it exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "Removing existing task: $TaskName"
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Register new task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description $TaskDescription `
        -RunLevel Highest

    Write-Host "✅ Task scheduled successfully!"
    Write-Host "📋 Task Name: $TaskName"
    Write-Host "🕙 Time: $Time (GMT+7)"
    Write-Host "📁 Script: $FullScriptPath"
    Write-Host "📂 Working Directory: $WorkspacePath\scripts"
    Write-Host ""
    Write-Host "To view the task: tasklist /fi `"imagename eq python.exe`""
    Write-Host "To manually run: & '$FullScriptPath'"
    Write-Host "To remove task: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:\$false"

}
catch {
    Write-Error "Failed to create scheduled task: $_"
    exit 1
}
