import { loginAction } from "./actions";

export const dynamic = "force-dynamic";

interface PageProps {
  searchParams: Promise<{ error?: string; next?: string }>;
}

export default async function AdminLoginPage({ searchParams }: PageProps) {
  const params = await searchParams;

  return (
    <main className="mx-auto flex min-h-[70vh] max-w-sm flex-col justify-center px-6 py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">
        Admin — Sign in
      </p>
      <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
        The Directory admin
      </h1>

      {params.error === "rate_limited" && (
        <p className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
          Too many failed attempts for this email. Try again in a few minutes.
        </p>
      )}
      {params.error && params.error !== "rate_limited" && (
        <p className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
          Invalid email or password.
        </p>
      )}

      <form action={loginAction} className="mt-6 space-y-4">
        {params.next && <input type="hidden" name="next" value={params.next} />}
        <div>
          <label htmlFor="email" className="mb-1 block text-sm font-medium text-slate-700">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            autoComplete="username"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          />
        </div>
        <div>
          <label htmlFor="password" className="mb-1 block text-sm font-medium text-slate-700">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            required
            autoComplete="current-password"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          />
        </div>
        <button
          type="submit"
          className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
        >
          Sign in
        </button>
      </form>
    </main>
  );
}
