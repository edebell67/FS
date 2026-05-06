'use client';

import { Navbar } from '@/components/Navbar';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { useSettingsStore } from '@/store/useSettingsStore';

export default function SettingsPage() {
  const {
    network,
    displayCurrency,
    confirmLargeOrders,
    warnHighSlippage,
    slippageThreshold,
    largeOrderThreshold,
    updateSettings,
    resetSettings,
  } = useSettingsStore();

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <RiskDisclosure />
      <Navbar />

      <div className="container py-8 max-w-2xl">
        <h1 className="text-2xl font-bold mb-8">Settings</h1>

        {/* Network */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Network</CardTitle>
            <CardDescription>Choose between mainnet and testnet</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Button
                variant={network === 'mainnet' ? 'default' : 'outline'}
                onClick={() => updateSettings({ network: 'mainnet' })}
              >
                Mainnet
              </Button>
              <Button
                variant={network === 'testnet' ? 'default' : 'outline'}
                onClick={() => updateSettings({ network: 'testnet' })}
              >
                Testnet
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Display Currency */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Display Currency</CardTitle>
            <CardDescription>Currency used for displaying values</CardDescription>
          </CardHeader>
          <CardContent>
            <Select
              value={displayCurrency}
              onValueChange={(value) => updateSettings({ displayCurrency: value })}
            >
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="SETTLE">SETTLE</SelectItem>
                <SelectItem value="sNGN">sNGN</SelectItem>
                <SelectItem value="sKES">sKES</SelectItem>
                <SelectItem value="sZAR">sZAR</SelectItem>
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        {/* Confirmations */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Confirmations</CardTitle>
            <CardDescription>Trading safety settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <Label>Confirm large orders</Label>
                <p className="text-sm text-muted-foreground">
                  Show confirmation for orders above threshold
                </p>
              </div>
              <Switch
                checked={confirmLargeOrders}
                onCheckedChange={(checked) =>
                  updateSettings({ confirmLargeOrders: checked })
                }
              />
            </div>

            {confirmLargeOrders && (
              <div className="space-y-2">
                <Label>Large order threshold (SETTLE)</Label>
                <Input
                  type="number"
                  value={largeOrderThreshold}
                  onChange={(e) =>
                    updateSettings({ largeOrderThreshold: parseInt(e.target.value) || 0 })
                  }
                  className="w-48"
                />
              </div>
            )}

            <Separator />

            <div className="flex items-center justify-between">
              <div>
                <Label>Warn on high slippage</Label>
                <p className="text-sm text-muted-foreground">
                  Show warning when slippage exceeds threshold
                </p>
              </div>
              <Switch
                checked={warnHighSlippage}
                onCheckedChange={(checked) =>
                  updateSettings({ warnHighSlippage: checked })
                }
              />
            </div>

            {warnHighSlippage && (
              <div className="space-y-2">
                <Label>Slippage threshold (%)</Label>
                <Input
                  type="number"
                  step="0.1"
                  value={slippageThreshold}
                  onChange={(e) =>
                    updateSettings({ slippageThreshold: parseFloat(e.target.value) || 0 })
                  }
                  className="w-48"
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* API Endpoint */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>API Endpoint (Advanced)</CardTitle>
            <CardDescription>Custom API endpoint for development</CardDescription>
          </CardHeader>
          <CardContent>
            <Input
              value="https://api.afrix.exchange"
              disabled
              className="font-mono"
            />
            <p className="text-xs text-muted-foreground mt-2">
              Currently using mock API. Real API coming soon.
            </p>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex items-center gap-4">
          <Button onClick={() => alert('Settings saved!')}>
            Save Settings
          </Button>
          <Button variant="outline" onClick={resetSettings}>
            Reset to Defaults
          </Button>
        </div>
      </div>
    </div>
  );
}
