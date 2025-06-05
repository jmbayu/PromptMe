# PowerShell script to add NAT port forwarding rules for VirtualBox VM

# Define the path to VBoxManage and the VM name
$vboxManagePath = "C:\Program Files\Oracle\VirtualBox\VBoxManage"
$vmName = "owasp10llm2025"

# Loop through the port range and add NAT rules
for ($port = 5000; $port -le 5022; $port++) {
    $ruleName = "nat_rule_$port"
    & "$vboxManagePath" modifyvm $vmName --natpf1 "$ruleName,tcp,,$port,,$port"
}