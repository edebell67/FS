// Deliberately its own file with zero other imports. middleware.ts (Edge
// runtime) needs this constant but must NOT pull in session.ts's `db`
// import — Edge can't bundle `pg`/`node:crypto`. Keeping this isolated is
// what makes that possible.
export const SESSION_COOKIE_NAME = "ep047_admin_session";
