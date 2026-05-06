$uri = "https://const-encouraged-commentary-hall.trycloudflare.com/api/v1/items"
$headers = @{
    "X-User-ID" = "00000000-0000-0000-0000-000000000000"
    "Content-Type" = "application/json"
}
$body = @{
    type = "receipt"
    extracted_text = "Test Item v129 (Script)"
    amount = 12.34
    device_id = "test-script-v129"
} | ConvertTo-Json

Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
