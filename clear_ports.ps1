# Function to kill processes blocking ports 5001 to 5010
function Kill-BlockingPorts {
    for ($port = 5001; $port -le 5010; $port++) {
        $conns = netstat -ano | Select-String ":$port"
        foreach ($conn in $conns) {
            if ($conn -match "\s+(\d+)$") {
                $pid = $matches[1]
                if ($pid -ne "0") {
                    try {
                        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                        Write-Host "Killed process $pid on port $port"
                    } catch {}
                }
            }
        }
    }
}

Kill-BlockingPorts

