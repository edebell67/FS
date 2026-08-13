"use client";

import { useMemo, useState } from "react";

type Story = {
  id: string;
  slug: string;
  headline: string;
  town: string;
  postcode: string | null;
  source_name: string;
  source_url: string;
  verified_update: string;
  local_reading: string;
  business_voices: string | null;
  published_at: string | null;
  topic: string | null;
};

type Sort = "newest" | "place";

function formatDate(value: string | null, short = false) {
  if (!value) return "Date pending";
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: short ? "short" : "long",
    year: "numeric",
  }).format(new Date(value));
}

export function PublicNewsReader({ stories }: { stories: Story[] }) {
  const [search, setSearch] = useState("");
  const [place, setPlace] = useState("");
  const [date, setDate] = useState("");
  const [sort, setSort] = useState<Sort>("newest");
  const [selectedId, setSelectedId] = useState<string | null>(stories[0]?.id ?? null);

  const places = useMemo(() => [...new Set(stories.map((story) => story.town).filter(Boolean))].sort(), [stories]);
  const dates = useMemo(() => [...new Set(stories.map((story) => story.published_at?.slice(0, 10)).filter((value): value is string => Boolean(value)))].sort().reverse(), [stories]);
  const filteredStories = useMemo(() => {
    const query = search.trim().toLowerCase();
    return stories.filter((story) => {
      const searchable = [story.headline, story.town, story.postcode, story.topic, story.verified_update, story.source_name].filter(Boolean).join(" ").toLowerCase();
      return (!query || searchable.includes(query)) && (!place || story.town === place) && (!date || story.published_at?.slice(0, 10) === date);
    }).sort((a, b) => sort === "place"
      ? a.town.localeCompare(b.town) || b.published_at?.localeCompare(a.published_at ?? "") || 0
      : b.published_at?.localeCompare(a.published_at ?? "") || 0);
  }, [date, place, search, sort, stories]);
  const selectedStory = filteredStories.find((story) => story.id === selectedId) ?? filteredStories[0] ?? null;

  function clearFilters() {
    setSearch("");
    setPlace("");
    setDate("");
    setSort("newest");
  }

  return <>
    <section className="border-b border-[#d6d2c9] bg-[#152022] text-white" aria-label="Scrolling local headlines">
      <div className="mx-auto flex h-12 max-w-7xl items-center gap-3 overflow-hidden px-4 sm:px-6 lg:px-8">
        <span className="shrink-0 bg-[#d85f35] px-2.5 py-1 font-mono text-[11px] font-medium uppercase tracking-[0.1em]">By place</span>
        <div className="flex min-w-max gap-8 overflow-x-auto py-1 text-sm [scrollbar-width:none]">
          {stories.map((story) => <button key={story.id} type="button" onClick={() => setSelectedId(story.id)} className="min-h-11 whitespace-nowrap text-left text-white hover:text-[#8fe1d5] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#f5c451]">
            <strong className="mr-2 font-mono text-[11px] uppercase tracking-[0.08em] text-[#8fe1d5]">{story.town}</strong>{story.headline}
          </button>)}
        </div>
      </div>
    </section>
    <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-10 lg:px-8">
      <section className="grid grid-cols-1 gap-3 border-b border-[#d6d2c9] pb-5 md:grid-cols-[minmax(240px,1.5fr)_repeat(3,minmax(130px,.65fr))]" aria-label="Find local news">
        <label className="sr-only" htmlFor="news-search">Search news</label>
        <input id="news-search" type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search headlines, places or topics…" className="min-h-11 w-full rounded-sm border border-[#b9b6ad] bg-[#fffdf8] px-3 text-sm text-[#152022]" />
        <label className="sr-only" htmlFor="news-place">View by town, city or postcode</label>
        <select id="news-place" aria-label="View by town, city or postcode" value={place} onChange={(event) => setPlace(event.target.value)} className="min-h-11 w-full rounded-sm border border-[#b9b6ad] bg-[#fffdf8] px-3 text-sm text-[#152022]">
          <option value="">All towns, cities & postcodes</option>{places.map((value) => <option key={value} value={value}>{value}</option>)}
        </select>
        <label className="sr-only" htmlFor="news-date">View by date</label>
        <select id="news-date" aria-label="View by date" value={date} onChange={(event) => setDate(event.target.value)} className="min-h-11 w-full rounded-sm border border-[#b9b6ad] bg-[#fffdf8] px-3 text-sm text-[#152022]">
          <option value="">All dates</option>{dates.map((value) => <option key={value} value={value}>{formatDate(value)}</option>)}
        </select>
        <label className="sr-only" htmlFor="news-sort">Sort results</label>
        <select id="news-sort" aria-label="Sort results" value={sort} onChange={(event) => setSort(event.target.value as Sort)} className="min-h-11 w-full rounded-sm border border-[#b9b6ad] bg-[#fffdf8] px-3 text-sm text-[#152022]">
          <option value="newest">Newest first</option><option value="place">Town / city</option>
        </select>
      </section>
      <div className="flex min-h-12 flex-wrap items-center justify-between gap-3 border-b border-[#d6d2c9] py-3 text-sm text-[#667174]">
        <p aria-live="polite">{filteredStories.length} {filteredStories.length === 1 ? "story" : "stories"} in this edition</p>
        <button type="button" onClick={clearFilters} className="min-h-11 px-1 font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-brand-700 underline underline-offset-4 hover:text-brand-600">Clear filters</button>
      </div>
      <section className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,.95fr)]" aria-label="News stories">
        <div className="space-y-3" aria-live="polite">
          {filteredStories.length ? filteredStories.map((story) => <article key={story.id} className={`border bg-[#fffdf8] ${selectedStory?.id === story.id ? "border-[#152022] shadow-[0_9px_25px_rgba(31,39,37,.08)]" : "border-[#d6d2c9]"}`}>
            <button type="button" aria-pressed={selectedStory?.id === story.id} onClick={() => setSelectedId(story.id)} className="min-h-11 w-full p-4 text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-[-3px] focus-visible:outline-[#0d746a] sm:p-5">
              <p className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">{story.town}{story.postcode ? ` · ${story.postcode}` : ""} · {formatDate(story.published_at, true)}</p>
              <h2 className="mt-2 font-display text-2xl font-semibold tracking-[-0.025em] text-[#152022]">{story.headline}</h2>
              <p className="mt-3 text-sm leading-6 text-[#4c5657]">{story.verified_update}</p>
              <span className="mt-4 inline-block font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-brand-700">Read article →</span>
            </button>
          </article>) : <div className="border border-[#d6d2c9] bg-[#fffdf8] p-6 text-[#667174]">No stories match those filters. Try clearing the search or place/date choices.</div>}
        </div>
        <aside className="h-fit border border-[#d6d2c9] bg-[#fffdf8] p-5 sm:p-6 lg:sticky lg:top-6" aria-label="Selected article">
          {selectedStory ? <article>
            <p className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">{selectedStory.town}{selectedStory.postcode ? ` · ${selectedStory.postcode}` : ""} · {formatDate(selectedStory.published_at)}</p>
            <h2 className="mt-2 font-display text-3xl font-semibold tracking-[-0.035em] text-[#152022]">{selectedStory.headline}</h2>
            <section className="mt-6 border-t border-[#d6d2c9] pt-5"><h3 className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">Verified update</h3><p className="mt-2 text-sm leading-6 text-[#4c5657]">{selectedStory.verified_update}</p></section>
            <section className="mt-5 border-l-2 border-brand-600 pl-4"><h3 className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">Local reading</h3><p className="mt-2 text-sm leading-6 text-[#667174]">{selectedStory.local_reading}</p></section>
            {selectedStory.business_voices ? <section className="mt-5"><h3 className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">Business voices</h3><p className="mt-2 text-sm leading-6 text-[#667174]">{selectedStory.business_voices}</p></section> : null}
            {selectedStory.source_url ? <a href={selectedStory.source_url} target="_blank" rel="noreferrer" className="mt-6 inline-flex min-h-11 items-center text-sm font-semibold text-brand-700 underline underline-offset-4 hover:text-brand-600">Source: {selectedStory.source_name || "Read update"} ↗</a> : null}
          </article> : <div><p className="font-mono text-[11px] font-medium uppercase tracking-[0.1em] text-brand-700">Article reader</p><h2 className="mt-2 font-display text-3xl font-semibold text-[#152022]">Choose a local headline.</h2><p className="mt-3 text-sm leading-6 text-[#667174]">Selected stories stay highlighted in the list. Use the search and filters to narrow this edition.</p></div>}
        </aside>
      </section>
    </main>
  </>;
}
