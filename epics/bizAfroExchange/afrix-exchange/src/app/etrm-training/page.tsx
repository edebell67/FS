'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

type Role = 'FO' | 'MO' | 'BO' | 'MD' | 'Admin';
type ScreenId =
  | 'deal-blotter'
  | 'deal-entry'
  | 'confirmations'
  | 'positions'
  | 'valuation'
  | 'limits'
  | 'settlement-run'
  | 'invoice-workbench'
  | 'gl-export'
  | 'curves'
  | 'admin';

type NavItem = { id: ScreenId; label: string; module: string; roles?: Role[] };

const NAV_ITEMS: NavItem[] = [
  { id: 'deal-blotter', label: 'Deal Blotter', module: 'Trading' },
  { id: 'deal-entry', label: 'Deal Entry', module: 'Trading' },
  { id: 'confirmations', label: 'Confirmations', module: 'Trading' },
  { id: 'positions', label: 'Positions (Daily)', module: 'Risk & Valuation' },
  { id: 'valuation', label: 'Valuation (MTM)', module: 'Risk & Valuation' },
  { id: 'limits', label: 'Limits', module: 'Risk & Valuation' },
  { id: 'settlement-run', label: 'Settlement Run', module: 'Settlements' },
  { id: 'invoice-workbench', label: 'Invoice Workbench', module: 'Settlements' },
  { id: 'gl-export', label: 'GL Export', module: 'Settlements' },
  { id: 'curves', label: 'Curves', module: 'Market Data', roles: ['MD', 'Admin'] },
  { id: 'admin', label: 'Parties/Books/Users', module: 'Admin', roles: ['Admin'] },
];

const DEAL_BLOTTER_ROWS = [
  ['D-1001', 'v3', 'Validated', 'NorthBase', 'E.Bell', 'Octopus', 'Buy', 'Base', '2026-03-01', '2026-03-31', '120', 'Fixed', '81.20', 'GB_BASE', '2026-03-05 09:54'],
  ['D-1002', 'v1', 'Submitted', 'Peaking', 'M.Khan', 'EDF', 'Sell', 'Peak', '2026-03-01', '2026-03-31', '75', 'Index', 'UKP_BASE_FWD + 1.2', 'GB_BASE', '2026-03-05 09:50'],
  ['D-1003', 'v2', 'Confirmed', 'RetailHedge', 'A.Jones', 'Centrica', 'Buy', 'Off-peak', '2026-04-01', '2026-04-30', '90', 'Fixed', '72.10', 'GB_BASE', '2026-03-05 09:42'],
];

const confirmRows = [
  ['D-1001', 'Octopus', 'Email', '2026-03-05 09:30', '-', 'Sent', 'MO Desk'],
  ['D-0998', 'EDF', 'EDI', '2026-03-04 15:10', '2026-03-04 16:00', 'Received', 'MO Desk'],
  ['D-0997', 'Centrica', 'Email', '2026-03-04 13:11', '-', 'Disputed', 'MO Desk'],
];

function DataTable({ headers, rows }: { headers: string[]; rows: string[][] }) {
  return (
    <div className="overflow-auto rounded border border-zinc-700 bg-zinc-950">
      <table className="w-full min-w-[980px] text-xs">
        <thead className="bg-zinc-900">
          <tr>
            {headers.map((header) => (
              <th key={header} className="whitespace-nowrap border-b border-zinc-700 px-2 py-2 text-left font-medium text-zinc-300">
                {header}
              </th>
            ))}
            <th className="border-b border-zinc-700 px-2 py-2 text-left font-medium text-zinc-300">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row[0]}-${index}`} className="border-b border-zinc-800 hover:bg-zinc-900/60">
              {row.map((value, cellIndex) => (
                <td key={`${row[0]}-${cellIndex}`} className="whitespace-nowrap px-2 py-2 text-zinc-200">
                  {value}
                </td>
              ))}
              <td className="px-2 py-2">
                <Button size="sm" variant="outline" className="h-7 text-[11px]">
                  Open Details
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ActionBar({ screen, role }: { screen: ScreenId; role: Role }) {
  if (screen === 'deal-blotter') {
    return (
      <div className="flex flex-wrap gap-2">
        <Button size="sm">New Deal</Button>
        <Button size="sm" variant="outline">Copy Deal</Button>
        <Button size="sm" variant="outline">Amend</Button>
        <Button size="sm" variant="outline">Request Cancel</Button>
        <Button size="sm" variant="outline">Submit</Button>
        {role === 'MO' || role === 'Admin' ? <Button size="sm" variant="secondary">Validate / Confirm / Run MTM</Button> : null}
      </div>
    );
  }
  if (screen === 'limits') {
    return (
      <div className="flex flex-wrap gap-2">
        <Button size="sm" variant="outline" disabled={role !== 'MO' && role !== 'Admin'}>Acknowledge</Button>
        <Button size="sm" variant="outline" disabled={role !== 'MO' && role !== 'Admin'}>Resolve</Button>
        <Button size="sm" variant="outline" disabled={role !== 'MO' && role !== 'Admin'}>Add Comment</Button>
      </div>
    );
  }
  if (screen === 'settlement-run') {
    return <Button size="sm" disabled={role !== 'BO' && role !== 'Admin'}>Generate Settlement</Button>;
  }
  if (screen === 'invoice-workbench') {
    return (
      <div className="flex flex-wrap gap-2">
        <Button size="sm" variant="outline">Preview</Button>
        <Button size="sm" disabled={role !== 'BO' && role !== 'Admin'}>Issue Invoice</Button>
        <Button size="sm" variant="outline">Generate Credit Note</Button>
      </div>
    );
  }
  if (screen === 'gl-export') {
    return <Button size="sm">Mark Sent</Button>;
  }
  if (screen === 'curves') {
    return <Button size="sm">Publish Version (Locks)</Button>;
  }
  return null;
}

export default function EtrmTrainingPage() {
  const [role, setRole] = useState<Role>('MO');
  const [screen, setScreen] = useState<ScreenId>('deal-blotter');

  const visibleNav = useMemo(() => NAV_ITEMS.filter((item) => !item.roles || item.roles.includes(role)), [role]);

  const screenTitle = visibleNav.find((item) => item.id === screen)?.label ?? 'Deal Blotter';

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="sticky top-0 z-20 border-b border-zinc-800 bg-zinc-900/95">
        <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3">
          <div className="flex items-center gap-3">
            <Badge className="bg-amber-500 text-zinc-900 hover:bg-amber-500">TRAINING</Badge>
            <span className="text-sm font-semibold">UK Power ETRM</span>
            <span className="text-xs text-zinc-400">v2026.03.05-blotter</span>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Input className="h-8 w-36 bg-zinc-950" defaultValue="2026-03-05" aria-label="As-of date" />
            <Select defaultValue="all_books">
              <SelectTrigger className="h-8 w-36 bg-zinc-950"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all_books">All Books</SelectItem>
                <SelectItem value="northbase">NorthBase</SelectItem>
                <SelectItem value="peaking">Peaking</SelectItem>
              </SelectContent>
            </Select>
            <Select value={role} onValueChange={(value) => { setRole(value as Role); if (!visibleNav.some((item) => item.id === screen && (!item.roles || item.roles.includes(value as Role)))) setScreen('deal-blotter'); }}>
              <SelectTrigger className="h-8 w-28 bg-zinc-950"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="FO">FO</SelectItem>
                <SelectItem value="MO">MO</SelectItem>
                <SelectItem value="BO">BO</SelectItem>
                <SelectItem value="MD">MD</SelectItem>
                <SelectItem value="Admin">Admin</SelectItem>
              </SelectContent>
            </Select>
            <Link href="/">
              <Button size="sm" variant="outline">Back</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex min-h-[calc(100vh-61px)]">
        <aside className="w-60 border-r border-zinc-800 bg-zinc-900/60 p-3">
          {['Trading', 'Risk & Valuation', 'Settlements', 'Market Data', 'Admin'].map((moduleName) => (
            <div key={moduleName} className="mb-5">
              <p className="mb-2 text-[11px] uppercase tracking-widest text-zinc-500">{moduleName}</p>
              <div className="space-y-1">
                {visibleNav.filter((item) => item.module === moduleName).map((item) => (
                  <button
                    key={item.id}
                    className={`w-full rounded px-2 py-1.5 text-left text-sm ${screen === item.id ? 'bg-zinc-700 text-zinc-100' : 'text-zinc-300 hover:bg-zinc-800'}`}
                    onClick={() => setScreen(item.id)}
                    type="button"
                  >
                    {item.label}
                  </button>
                ))}
                {visibleNav.filter((item) => item.module === moduleName).length === 0 ? <p className="text-xs text-zinc-600">Not available for role</p> : null}
              </div>
            </div>
          ))}
        </aside>

        <section className="flex-1 p-4">
          <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
            <h1 className="text-lg font-semibold">{screenTitle}</h1>
            <div className="flex items-center gap-2">
              <Select defaultValue="my_book_open_trades">
                <SelectTrigger className="h-8 w-48 bg-zinc-900"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="my_book_open_trades">Saved View: My Book - Open Trades</SelectItem>
                  <SelectItem value="pending_confirms">Saved View: Pending Confirmations</SelectItem>
                </SelectContent>
              </Select>
              <Button size="sm" variant="outline">Column Chooser</Button>
              <Button size="sm" variant="outline">Export CSV</Button>
            </div>
          </div>

          <Card className="border-zinc-800 bg-zinc-900/70">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">Filters</CardTitle>
              <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
                <Input className="h-8 bg-zinc-950" placeholder="Date Range / Month" />
                <Input className="h-8 bg-zinc-950" placeholder="Status" />
                <Input className="h-8 bg-zinc-950" placeholder="Book" />
                <Input className="h-8 bg-zinc-950" placeholder="Counterparty" />
                <Input className="h-8 bg-zinc-950" placeholder="Profile / Curve / Location" />
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <ActionBar screen={screen} role={role} />

              {screen === 'deal-blotter' && (
                <DataTable
                  headers={['Deal ID', 'Ver', 'Status', 'Trade Date', 'Book', 'Trader', 'Counterparty', 'B/S', 'Profile', 'Start', 'End', 'Qty (MWh/h)', 'Price Type', 'Price/Spread', 'Location', 'Last Changed']}
                  rows={DEAL_BLOTTER_ROWS}
                />
              )}
              {screen === 'deal-entry' && (
                <div className="grid gap-3 lg:grid-cols-2">
                  {['Deal Type', 'Buy/Sell', 'Counterparty', 'Book', 'Trader', 'Start Date', 'End Date', 'Profile', 'Qty MWh/h', 'Location', 'Curve', 'Spread', 'Payment Terms', 'Notes', 'Contract Ref'].map((field) => (
                    <div key={field} className="space-y-1">
                      <p className="text-xs text-zinc-400">{field}</p>
                      <Input className="h-8 bg-zinc-950" placeholder={field} />
                    </div>
                  ))}
                  <div className="col-span-full flex gap-2">
                    <Button size="sm">Save Draft</Button>
                    <Button size="sm" variant="outline">Submit for Validation</Button>
                    <Button size="sm" variant="outline">Create Amendment</Button>
                  </div>
                </div>
              )}
              {screen === 'confirmations' && (
                <DataTable
                  headers={['Deal ID', 'Counterparty', 'Method', 'Sent At', 'Received At', 'Status', 'Owner']}
                  rows={confirmRows}
                />
              )}
              {screen === 'positions' && (
                <DataTable
                  headers={['Delivery Date', 'Book', 'Location', 'Profile', 'Buy MWh', 'Sell MWh', 'Net MWh', '#Deals']}
                  rows={[
                    ['2026-03-10', 'NorthBase', 'GB_BASE', 'Base', '2400', '1800', '+600', '12'],
                    ['2026-03-10', 'Peaking', 'GB_BASE', 'Peak', '900', '1100', '-200', '5'],
                  ]}
                />
              )}
              {screen === 'valuation' && (
                <>
                  <div className="grid gap-2 sm:grid-cols-3">
                    <Card className="border-zinc-700 bg-zinc-950"><CardContent className="p-3 text-xs">Total MTM: GBP 1,248,500</CardContent></Card>
                    <Card className="border-zinc-700 bg-zinc-950"><CardContent className="p-3 text-xs">MTM by Book: NorthBase GBP 980k</CardContent></Card>
                    <Card className="border-zinc-700 bg-zinc-950"><CardContent className="p-3 text-xs">MTM by Profile: Base GBP 760k</CardContent></Card>
                  </div>
                  <DataTable
                    headers={['Deal ID', 'Book', 'Profile', 'Volume (MWh)', 'Fixed/Index', 'Curve', 'Forward Price', 'Fixed Price', 'Spread', 'MTM (GBP)', 'Last Run']}
                    rows={[
                      ['D-1001', 'NorthBase', 'Base', '3720', 'Fixed', 'UKP_BASE_FWD', '79.8', '81.2', '-', '145200', '2026-03-05 09:22'],
                      ['D-1002', 'Peaking', 'Peak', '1550', 'Index', 'UKP_PEAK_FWD', '91.4', '-', '1.2', '-22800', '2026-03-05 09:22'],
                    ]}
                  />
                </>
              )}
              {screen === 'limits' && (
                <div className="space-y-3">
                  <DataTable
                    headers={['Limit Type', 'Threshold', 'Period', 'Book']}
                    rows={[
                      ['Volume', '5000 MWh/day', 'Daily', 'NorthBase'],
                      ['MTM', 'GBP 2,000,000', 'Monthly', 'All'],
                    ]}
                  />
                  <DataTable
                    headers={['Breach ID', 'Limit', 'Book', 'As-of', 'Actual', 'Threshold', 'Status', 'Owner']}
                    rows={[
                      ['BR-18', 'Volume', 'NorthBase', '2026-03-05', '5210', '5000', 'Open', 'MO Desk'],
                    ]}
                  />
                </div>
              )}
              {screen === 'settlement-run' && (
                <DataTable
                  headers={['Deal ID', 'Counterparty', 'Profile', 'Period', 'Est Volume', 'Pricing', 'Eligible Y/N']}
                  rows={[
                    ['D-0988', 'EDF', 'Base', 'Mar-2026', '3010', 'Fixed 77.2', 'Y'],
                    ['D-0994', 'Octopus', 'Peak', 'Mar-2026', '1775', 'Curve+Spread', 'Y'],
                  ]}
                />
              )}
              {screen === 'invoice-workbench' && (
                <DataTable
                  headers={['Invoice ID', 'Counterparty', 'Period', 'Amount', 'Status', 'Issued At']}
                  rows={[
                    ['INV-1008', 'EDF', 'Mar-2026', 'GBP 343,200', 'Draft', '-'],
                    ['INV-1007', 'Octopus', 'Feb-2026', 'GBP 298,100', 'Issued', '2026-03-01 12:10'],
                  ]}
                />
              )}
              {screen === 'gl-export' && (
                <DataTable
                  headers={['Export ID', 'Invoice ID', 'Period', 'Amount', 'Status']}
                  rows={[
                    ['GL-302', 'INV-1007', 'Feb-2026', 'GBP 298,100', 'Ready'],
                    ['GL-301', 'INV-1006', 'Feb-2026', 'GBP 254,880', 'Sent'],
                  ]}
                />
              )}
              {screen === 'curves' && (
                <div className="space-y-3">
                  <DataTable
                    headers={['Curve', 'Version', 'Status', 'As-of', 'Created by', 'Created at']}
                    rows={[
                      ['UKP_BASE_FWD', 'v84', 'Published', '2026-03-05', 'md.admin', '2026-03-05 08:00'],
                      ['UKP_PEAK_FWD', 'v62', 'Draft', '2026-03-05', 'md.admin', '2026-03-05 08:20'],
                    ]}
                  />
                  <DataTable
                    headers={['Delivery Month', 'Price']}
                    rows={[
                      ['2026-04', '84.20'],
                      ['2026-05', '82.10'],
                    ]}
                  />
                </div>
              )}
              {screen === 'admin' && (
                <div className="grid gap-3 sm:grid-cols-2">
                  {['Parties', 'Books', 'Users/Roles', 'Locations', 'Calendar', 'Maker/Checker Toggles'].map((item) => (
                    <Card key={item} className="border-zinc-700 bg-zinc-950">
                      <CardHeader className="pb-2"><CardTitle className="text-sm">{item}</CardTitle></CardHeader>
                      <CardContent><Button size="sm" variant="outline">Manage</Button></CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </section>

        <aside className="w-80 border-l border-zinc-800 bg-zinc-900/60 p-4">
          <p className="mb-2 text-xs uppercase tracking-widest text-zinc-500">Details Drawer</p>
          <div className="mb-3 flex gap-1">
            {['Summary', 'Lifecycle', 'Versions', 'Positions Impact', 'Valuation', 'Settlement'].map((tab) => (
              <Button key={tab} size="sm" variant="outline" className="h-7 px-2 text-[10px]">{tab}</Button>
            ))}
          </div>
          <Card className="border-zinc-700 bg-zinc-950">
            <CardContent className="space-y-2 p-3 text-xs text-zinc-300">
              <p>Deal summary and timeline render here on row click.</p>
              <p>Confirmation drawer includes send method + timestamps.</p>
              <p>Valuation driver panel shows simplified calculation components.</p>
              <p>GL Export drawer shows JSON payload preview.</p>
            </CardContent>
          </Card>
        </aside>
      </main>

      <footer className="border-t border-zinc-800 bg-zinc-900 px-4 py-2 text-xs text-zinc-400">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>Rows: 3</span>
          <span>Last refresh: 2026-03-05 10:18:00</span>
          <span>Saved views and column chooser hooks enabled</span>
        </div>
      </footer>
    </div>
  );
}
