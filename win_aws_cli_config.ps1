# 檢查 AWS CLI 是否安裝
try {
    $awsVersion = aws --version
    Write-Host "AWS CLI 已安裝。版本: $awsVersion"
} catch {
    Write-Host "AWS CLI 未安裝。"

    # 提示用戶是否安裝 AWS CLI
    $install = Read-Host "您現在要安裝 AWS CLI 嗎？ (Y/N)"
    if ($install -eq 'Y' -or $install -eq 'y') {
        Write-Host "正在安裝 AWS CLI..."

        # 使用 PowerShell 調用安裝命令
        # 注意：這裡假設用戶使用的是 MSI 安裝程序或其他安裝方法
        # 例如，使用 MSI 安裝程序（需要提前下載）
        # Start-Process -FilePath "msiexec.exe" -ArgumentList "/i 路徑\至\awscliv2.msi /quiet" -Wait

        # 使用 Chocolatey 安裝（假設已安裝 Chocolatey）
        Start-Process -FilePath "choco" -ArgumentList "install awscli -y" -Wait

        Write-Host "AWS CLI 安裝完成。"
    } else {
        Write-Host "跳過 AWS CLI 安裝。"
        exit
    }
}

# 運行 aws configure
Write-Host "正在配置 AWS CLI..."
aws configure
