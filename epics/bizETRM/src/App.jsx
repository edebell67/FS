import React, { useState } from 'react';
import { 
  FileText, 
  ShieldCheck, 
  BarChart2, 
  TrendingUp, 
  AlertTriangle,
  CreditCard,
  Settings,
  User,
  Search,
  Calendar
} from 'lucide-react';
import { STATUS, STATUS_LABELS, ROLES } from './constants/tradeStatus';
import { getAvailableActions, validateTransition } from './logic/lifecycleEngine';

const INITIAL_DEALS = [
  { id: '1001', v: 1, s: STATUS.CONFIRMED, td: '2026-03-01', cp: 'Centrica', side: 'Buy', prof: 'Peak', start: '2026-04-01', end: '2026-04-30', p: '65.20', vol: '720' },
  { id: '1002', v: 1, s: STATUS.SUBMITTED, td: '2026-03-02', cp: 'EDF Energy', side: 'Sell', prof: 'Base', start: '2026-05-01', end: '2026-05-31', p: '62.45', vol: '2232' },
  { id: '1003', v: 1, s: STATUS.DRAFT, td: '2026-03-04', cp: 'Shell Energy', side: 'Buy', prof: 'Off-Peak', start: '2026-06-01', end: '2026-06-30', p: '58.90', vol: '1440' },
];

const App = () => {
  const [role, setRole] = useState(ROLES.MO);
  const [asOfDate, setAsOfDate] = useState('2026-03-04');
  const [deals, setDeals] = useState(INITIAL_DEALS);
  const [selectedDealId, setSelectedDealId] = useState(null);
  const [activeView, setActiveView] = useState('blotter');

  const selectedDeal = deals.find(d => d.id === selectedDealId);

  const handleAction = (dealId, targetStatus) => {
    const deal = deals.find(d => d.id === dealId);
    const validation = validateTransition(deal.s, targetStatus, role);

    if (validation.allowed) {
      setDeals(prev => prev.map(d => 
        d.id === dealId ? { ...d, s: targetStatus } : d
      ));
    } else {
      alert(validation.reason);
    }
  };

  const getActionColor = (status) => {
    switch(status) {
      case STATUS.CONFIRMED: return '#27ae60';
      case STATUS.SUBMITTED: return '#3498db';
      case STATUS.REJECTED: return '#e74c3c';
      case STATUS.CANCELLED: return '#333';
      case STATUS.CANCEL_REQUESTED: return '#f39c12';
      default: return '#95a5a6';
    }
  };

  const renderView = () => {
    switch (activeView) {
      case 'blotter':
        return (
          <div className="grid-area">
            <h2 style={{ fontSize: '14px', margin: '0 0 12px 0' }}>Deal Blotter - All Trades</h2>
            <table className="etrm-grid">
              <thead>
                <tr>
                  <th style={{ width: '10px' }}></th>
                  <th>Deal ID</th>
                  <th>Ver</th>
                  <th>Status</th>
                  <th>Trade Date</th>
                  <th>Counterparty</th>
                  <th>B/S</th>
                  <th>Profile</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                  <th>Price</th>
                  <th>Volume (MWh)</th>
                </tr>
              </thead>
              <tbody>
                {deals.map(deal => (
                  <tr 
                    key={deal.id} 
                    onClick={() => setSelectedDealId(deal.id)}
                    className={selectedDealId === deal.id ? 'selected' : ''}
                  >
                    <td style={{ padding: 0 }}>
                      <div style={{ 
                        width: '4px', 
                        height: '28px', 
                        background: deal.s === STATUS.CONFIRMED ? 'var(--color-confirmed)' : (deal.s === STATUS.DRAFT ? '#888' : 'var(--color-warning)') 
                      }} />
                    </td>
                    <td>{deal.id}</td>
                    <td>{deal.v}</td>
                    <td style={{ fontWeight: '600' }}>
                      {STATUS_LABELS[deal.s]}
                    </td>
                    <td>{deal.td}</td>
                    <td>{deal.cp}</td>
                    <td>{deal.side}</td>
                    <td>{deal.prof}</td>
                    <td>{deal.start}</td>
                    <td>{deal.end}</td>
                    <td>{deal.p}</td>
                    <td>{deal.vol}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      case 'confirm':
        return (
          <div className="grid-area">
            <h2 style={{ fontSize: '14px', margin: '0 0 12px 0' }}>Confirmation Workbench</h2>
            <div style={{ padding: '20px', background: 'white', border: '1px solid #ddd' }}>
               <p>This module tracks external confirmation status for all trades.</p>
               <table className="etrm-grid">
                 <thead>
                   <tr>
                     <th>Deal ID</th>
                     <th>Counterparty</th>
                     <th>Method</th>
                     <th>Sent At</th>
                     <th>Received At</th>
                     <th>Status</th>
                   </tr>
                 </thead>
                 <tbody>
                    {deals.filter(d => d.s === STATUS.CONFIRMED).map(deal => (
                      <tr key={deal.id}>
                        <td>{deal.id}</td>
                        <td>{deal.cp}</td>
                        <td>Electronic (Internal)</td>
                        <td>{deal.td} 14:22</td>
                        <td>{deal.td} 14:22</td>
                        <td><span style={{ color: 'green', fontWeight: 'bold' }}>Matched</span></td>
                      </tr>
                    ))}
                 </tbody>
               </table>
            </div>
          </div>
        );
      case 'risk':
        return (
          <div className="grid-area">
            <h2 style={{ fontSize: '14px', margin: '0 0 12px 0' }}>Risk & Valuation (MTM)</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '16px' }}>
              <div style={{ background: 'white', padding: '12px', border: '1px solid #ddd' }}>
                <div style={{ fontSize: '10px', color: '#666' }}>Total Portfolio MTM</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#27ae60' }}>£142,520.00</div>
              </div>
              <div style={{ background: 'white', padding: '12px', border: '1px solid #ddd' }}>
                <div style={{ fontSize: '10px', color: '#666' }}>Open Positions (MWh)</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>4,392</div>
              </div>
              <div style={{ background: 'white', padding: '12px', border: '1px solid #ddd' }}>
                <div style={{ fontSize: '10px', color: '#666' }}>Active Counterparties</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{new Set(deals.map(d => d.cp)).size}</div>
              </div>
            </div>
            <table className="etrm-grid">
              <thead>
                <tr>
                  <th>Deal ID</th>
                  <th>Fixed Price</th>
                  <th>Forward Price</th>
                  <th>Volume (MWh)</th>
                  <th>MTM (£)</th>
                </tr>
              </thead>
              <tbody>
                {deals.filter(d => d.s === STATUS.CONFIRMED).map(deal => {
                  const fwd = 68.50; // Mock forward price
                  const mtm = (fwd - parseFloat(deal.p)) * parseInt(deal.vol) * (deal.side === 'Buy' ? 1 : -1);
                  return (
                    <tr key={deal.id}>
                      <td>{deal.id}</td>
                      <td>{deal.p}</td>
                      <td>{fwd.toFixed(2)}</td>
                      <td>{deal.vol}</td>
                      <td style={{ color: mtm >= 0 ? 'green' : 'red', fontWeight: 'bold' }}>
                        {mtm.toLocaleString('en-GB', { style: 'currency', currency: 'GBP' })}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        );
      default:
        return <div style={{ padding: '20px' }}>Module "{activeView}" under construction.</div>;
    }
  };

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <div className="sidebar">
        <div style={{ padding: '16px', fontWeight: 'bold', fontSize: '14px', borderBottom: '1px solid #3e4f5f' }}>
          bizETRM v1.1.8
        </div>
        <nav style={{ flex: 1, padding: '8px 0' }}>
          {[
            { id: 'blotter', icon: FileText, label: 'Deal Blotter' },
            { id: 'confirm', icon: ShieldCheck, label: 'Confirmations' },
            { id: 'risk', icon: BarChart2, label: 'Risk / MTM' },
            { id: 'limits', icon: AlertTriangle, label: 'Limits' },
            { id: 'settle', icon: CreditCard, label: 'Settlements' },
            { id: 'md', icon: TrendingUp, label: 'Market Data' },
            { id: 'admin', icon: Settings, label: 'Admin' },
          ].map(item => (
            <div 
              key={item.id} 
              onClick={() => setActiveView(item.id)}
              style={{ 
                padding: '10px 16px', 
                display: 'flex', 
                alignItems: 'center', 
                cursor: 'pointer',
                backgroundColor: activeView === item.id ? '#3e4f5f' : 'transparent'
              }}
              className="nav-item"
            >
              <item.icon size={16} style={{ marginRight: '12px', color: activeView === item.id ? '#3498db' : 'inherit' }} />
              <span>{item.label}</span>
            </div>
          ))}
        </nav>
        <div style={{ padding: '16px', fontSize: '11px', color: '#95a5a6', borderTop: '1px solid #3e4f5f' }}>
          © 2026 bizETRM Training
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <header className="top-bar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <span className="badge-training">Training Mode</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Calendar size={14} />
              <input 
                type="date" 
                value={asOfDate} 
                onChange={(e) => setAsOfDate(e.target.value)}
                style={{ border: '1px solid #ccc', fontSize: '12px', padding: '2px 4px' }}
              />
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ position: 'relative' }}>
              <Search size={14} style={{ position: 'absolute', left: '8px', top: '7px', color: '#888' }} />
              <input 
                type="text" 
                placeholder="Search Deal ID..." 
                style={{ padding: '4px 8px 4px 28px', border: '1px solid #ccc', borderRadius: '4px', fontSize: '12px' }}
              />
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', borderLeft: '1px solid #ddd', paddingLeft: '16px' }}>
              <User size={14} />
              <select 
                value={role} 
                onChange={(e) => setRole(e.target.value)}
                style={{ border: 'none', background: 'transparent', fontWeight: '600' }}
              >
                {Object.values(ROLES).map(r => <option key={r} value={r}>{r} Office</option>)}
              </select>
            </div>
          </div>
        </header>

        <div className="content-area">
          {renderView()}

          {selectedDeal && activeView === 'blotter' && (
            <div className="drawer">
              <div style={{ padding: '12px', background: '#eee', borderBottom: '1px solid #ccc', fontWeight: 'bold', display: 'flex', justifyContent: 'space-between' }}>
                Deal Details - {selectedDeal.id}
                <button onClick={() => setSelectedDealId(null)} style={{ border: 'none', background: 'transparent', cursor: 'pointer' }}>×</button>
              </div>
              <div style={{ flex: 1, overflow: 'auto', padding: '12px' }}>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', fontSize: '10px', color: '#666', marginBottom: '2px' }}>Status</label>
                  <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{STATUS_LABELS[selectedDeal.s]}</div>
                </div>
                
                <div style={{ border: '1px solid #ddd', background: '#f9f9f9', padding: '8px', marginBottom: '16px' }}>
                  <h4 style={{ margin: '0 0 8px 0', fontSize: '11px', borderBottom: '1px solid #ddd' }}>Lifecycle Audit</h4>
                  <div style={{ fontSize: '11px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span>Draft Created</span>
                      <span>{selectedDeal.td} 09:12</span>
                    </div>
                    {selectedDeal.s >= STATUS.SUBMITTED && (
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span>Submitted (FO)</span>
                        <span>{selectedDeal.td} 10:05</span>
                      </div>
                    )}
                    {selectedDeal.s === STATUS.CONFIRMED && (
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', color: 'green' }}>
                        <span>Confirmed (Auto-MO)</span>
                        <span>{selectedDeal.td} 14:22</span>
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <h4 style={{ margin: '0 0 8px 0', fontSize: '11px', borderBottom: '1px solid #ddd' }}>Lifecycle Actions</h4>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {getAvailableActions(selectedDeal.s, role).map(targetStatus => (
                      <button 
                        key={targetStatus}
                        onClick={() => handleAction(selectedDeal.id, targetStatus)}
                        style={{ 
                          padding: '6px 12px', 
                          background: getActionColor(targetStatus), 
                          color: 'white', 
                          border: 'none', 
                          cursor: 'pointer',
                          fontSize: '11px',
                          fontWeight: '600'
                        }}
                      >
                        {targetStatus === STATUS.CONFIRMED ? 'Confirm Deal' : 
                         targetStatus === STATUS.SUBMITTED ? 'Submit' : 
                         targetStatus === STATUS.REJECTED ? 'Reject' :
                         STATUS_LABELS[targetStatus]}
                      </button>
                    ))}
                    {getAvailableActions(selectedDeal.s, role).length === 0 && (
                      <div style={{ fontSize: '11px', color: '#888', fontStyle: 'italic' }}>
                        No actions available for your role.
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <footer style={{ height: '24px', background: '#333', color: '#aaa', fontSize: '10px', display: 'flex', alignItems: 'center', padding: '0 12px' }}>
          <div>Ready | Active Book: ALL | Connection: Stable</div>
          <div style={{ marginLeft: 'auto' }}>Last Refresh: {new Date().toLocaleTimeString()}</div>
        </footer>
      </div>
    </div>
  );
};

export default App;
