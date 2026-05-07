const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const db = require('./config/db');
const path = require('path');
require('dotenv').config();

const app = express();
const mvpQuarterlyMode = process.env.MVP_QUARTERLY_EXPORT_MODE !== 'false';

// Routes
const authRoutes = require('./routes/authRoutes');
const voiceRoutes = require('./routes/voiceRoutes');
const itemRoutes = require('./routes/itemRoutes');
const actionRoutes = require('./routes/actionRoutes');
const searchRoutes = require('./routes/searchRoutes');
const upcomingRoutes = require('./routes/upcomingRoutes');
const statsRoutes = require('./routes/statsRoutes');
const vatRoutes = require('./routes/vatRoutes');
const insightRoutes = require('./routes/insightRoutes');
const syncRoutes = require('./routes/syncRoutes');
const notificationRoutes = require('./routes/notificationRoutes');
const exportRoutes = require('./routes/exportRoutes');
const clientRoutes = require('./routes/clientRoutes');
const jobRoutes = require('./routes/jobRoutes');
const revenueRoutes = require('./routes/revenueRoutes');
const calendarRoutes = require('./routes/calendarRoutes');
const diaryRoutes = require('./routes/diaryRoutes');
const teamRoutes = require('./routes/teamRoutes');
const inboxRoutes = require('./routes/inboxRoutes');
const evidenceRoutes = require('./routes/evidenceRoutes');
const businessEventRoutes = require('./routes/businessEventRoutes');
const {
  isAllowedOrigin,
  isRequestSecure,
  parseAllowedOrigins,
  sanitizeRequestPath,
} = require('./services/authSessionService');

// Middleware
const userMiddleware = require('./middleware/userMiddleware');

// Custom Network Logger
const allowedOrigins = parseAllowedOrigins();

app.set('trust proxy', 1);

app.use((req, res, next) => {
  console.log(`[NETWORK] ${new Date().toISOString()} | ${req.method} ${sanitizeRequestPath(req.originalUrl)} | From: ${req.ip}`);
  next();
});

app.use((req, res, next) => {
  if (process.env.NODE_ENV === 'production' && process.env.ENFORCE_HTTPS !== 'false' && !isRequestSecure(req)) {
    return res.status(426).json({ error: 'HTTPS is required' });
  }
  return next();
});

app.use(helmet({
  crossOriginResourcePolicy: false,
  contentSecurityPolicy: false,
}));
app.use(cors({
  origin(origin, callback) {
    if (isAllowedOrigin(origin, allowedOrigins)) {
      return callback(null, true);
    }
    return callback(new Error('CORS origin rejected'));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-User-ID', 'bypass-tunnel-reminder']
}));
app.use(morgan('dev'));
app.use(express.json({ limit: '1mb' }));
app.use(userMiddleware);
app.use('/uploads', express.static('uploads'));

// Serve static frontend from build folder
app.use(express.static(path.join(__dirname, '../../frontend/build')));

const disabledInMvp = new Set(['/api/v1/tax', '/api/v1/revenue']);
app.use((req, res, next) => {
  if (!mvpQuarterlyMode) return next();
  for (const prefix of disabledInMvp) {
    if (req.path === prefix || req.path.startsWith(`${prefix}/`)) {
      return res.status(403).json({
        error: 'Disabled in MVP quarterly export mode',
        mode: 'MVP_QUARTERLY_EXPORT_MODE',
        path: req.path
      });
    }
  }
  return next();
});

// Bind API Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/voice', voiceRoutes);
app.use('/api/v1/items', itemRoutes);
app.use('/api/v1/action', actionRoutes);
app.use('/api/v1/search', searchRoutes);
app.use('/api/v1/upcoming', upcomingRoutes);
app.use('/api/v1/stats', statsRoutes);
app.use('/api/v1/tax', vatRoutes);
app.use('/api/v1/insights', insightRoutes);
app.use('/api/v1/sync', syncRoutes);
app.use('/api/v1/notifications', notificationRoutes);
app.use('/api/v1/export', exportRoutes);
app.use('/api/v1/clients', clientRoutes);
app.use('/api/v1/jobs', jobRoutes);
app.use('/api/v1/revenue', revenueRoutes);
app.use('/api/v1/calendar', calendarRoutes);
app.use('/api/v1/diary', diaryRoutes);
app.use('/api/v1/teams', teamRoutes);
app.use('/api/v1/inbox', inboxRoutes);
app.use('/api/v1/evidence', evidenceRoutes);
app.use('/api/v1/business-events', businessEventRoutes);

// Health Check
app.get('/api/health', (req, res) => {
  const supabase = require('./config/supabase');
  res.status(200).json({
    status: 'UP',
    version: '1.3.9',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV,
    cloud_storage: supabase ? 'connected' : 'disconnected',
    mvp_quarterly_export_mode: mvpQuarterlyMode,
    disclaimer: 'No HMRC submission. Not tax advice. You remain responsible for filings.',
    transport_security: process.env.NODE_ENV === 'production' && process.env.ENFORCE_HTTPS !== 'false' ? 'https_enforced' : 'local_dev_mode',
    auth_storage: 'http_only_cookie'
  });
});

// Wildcard Handler for Frontend (SPA) - Should be LAST
app.use((req, res, next) => {
  // If request is for an API or upload that reached here, it's a 404
  if (req.url.startsWith('/api/') || req.url.startsWith('/uploads/')) {
    console.log(`[404] API route not found: ${req.method} ${req.url}`);
    return res.status(404).json({ error: 'Not Found', path: req.url });
  }
  // Otherwise, serve index.html for React SPA
  res.sendFile(path.join(__dirname, '../../frontend/build/index.html'));
});

// Background Maintenance
setInterval(async () => {
  try {
    await db.query('SELECT update_overdue_statuses()');
    await db.query('SELECT check_and_trigger_overdue_notifications()');
    if (!mvpQuarterlyMode) {
      await db.query("SELECT check_revenue_milestones('00000000-0000-0000-0000-000000000000')");
    }
    console.log('[Maintenance] Lifecycle checks completed.');
  } catch (err) {
    console.error('[Maintenance] Error during background checks:', err);
  }
}, 3600000);

// Error Handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

const PORT = process.env.PORT || 5056;

if (require.main === module) {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`[Server] bizPA Backend running on port ${PORT} (Listening on 0.0.0.0)`);
  });
}

module.exports = app;
