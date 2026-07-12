/*
 * ============================================================================
 *  GARAGE CONFIGURATION — SINGLE SOURCE OF TRUTH
 * ============================================================================
 *  Everything visible on this site is populated from the objects below.
 *  To personalise this template for a real garage, replace the sample values
 *  in this file only — no other file should need editing for basic rebrand.
 *
 *  See ../../README.md for the full personalisation checklist.
 *
 *  All data here is SAMPLE / PLACEHOLDER content for demonstration purposes.
 * ============================================================================
 */

const garageConfig = {
  // ---- Demo mode --------------------------------------------------------
  // When true: forms show a demo confirmation instead of sending real data,
  // payment buttons open a "demonstration only" modal, and a small demo
  // notice is shown in the footer. Set to false once wired to a live backend.
  demoMode: true,

  // ---- Identity -----------------------------------------------------------
  businessName: "A C Automotive Engineering",
  shortName: "A C Automotive",
  tagline: "American car specialist preview for Goldhawk Road drivers who need sales, service, parts, diagnostics and repair enquiries handled quickly.",
  emblemInitials: "ACA",
  logo: null, // e.g. "assets/img/logo.svg" — leave null to use the generated text emblem
  heroKicker: "American car specialists · Goldhawk Road preview",

  // ---- Contact --------------------------------------------------------
  phone: "+44 20 8741 9993",
  phoneDisplay: "020 8741 9993",
  whatsapp: "442087419993",
  email: "",
  address: "247-251 Goldhawk Road, London",
  postcode: "",
  fullAddress: "247-251 Goldhawk Road, London",
  mapEmbedUrl: "https://www.openstreetmap.org/export/embed.html?bbox=-0.2424097%2C51.4955377%2C-0.2344097%2C51.5035377&layer=mapnik&marker=51.4995377%2C-0.2384097",
  directionsUrl: "https://www.openstreetmap.org/?mlat=51.4995377&mlon=-0.2384097#map=17/51.4995377/-0.2384097",

  // ---- Opening hours ------------------------------------------------------
  openingHours: [
    { day: "Monday", hours: "08:00 – 18:00" },
    { day: "Tuesday", hours: "08:00 – 18:00" },
    { day: "Wednesday", hours: "08:00 – 18:00" },
    { day: "Thursday", hours: "08:00 – 18:00" },
    { day: "Friday", hours: "08:00 – 18:00" },
    { day: "Saturday", hours: "08:30 – 13:00" },
    { day: "Sunday", hours: "Closed" }
  ],

  // ---- Brand colours (also mirrored as CSS variables in styles.css) -------
  primaryColour: "#101317",   // charcoal
  secondaryColour: "#8EA0AD", // steel
  accentColour: "#E11D48",    // racing red
  accentColourAlt: "#0891B2", // petrol blue

  // ---- Stats (placeholders — replace with verified figures before launch) -
  stats: [
    { value: 1, suffix: "", label: "Private preview", placeholder: true },
    { value: 247, suffix: "-251", label: "Goldhawk Road", placeholder: true },
    { value: 0, suffix: "", label: "Reviews to add", placeholder: true },
    { value: 1, suffix: "", label: "Owner to verify", placeholder: true }
  ],

  // ---- About ---------------------------------------------------------------
  about: {
    established: "sample",
    founder: "Owner details to confirm",
    technicians: "sample",
    experience: "to confirm",
    areaServed: "Goldhawk Road, West London",
    bodyCopy:
      "This private preview is built around the public business identity and visible frontage for A C Automotive Engineering on Goldhawk Road: American car specialists offering sales, service and parts. It demonstrates how a mobile-first page could make the garage instantly recognisable and easier to contact.",
    values: [
      "Clear estimates before any work begins",
      "No unnecessary work recommended",
      "Experienced technicians, not guesswork",
      "Modern fault-finding equipment"
    ]
  },

  // ---- Trust strip ----------------------------------------------------------
  trustIndicators: [
    { icon: "wrench", label: "Qualified Technicians" },
    { icon: "scan", label: "Modern Diagnostics" },
    { icon: "tag", label: "Transparent Pricing" },
    { icon: "map-pin", label: "Local Garage" },
    { icon: "shield", label: "Warranty Available" },
    { icon: "car", label: "American Car Specialists" }
  ],

  // ---- Why choose us ----------------------------------------------------
  whyChooseUs: [
    "Honest, understandable advice — no jargon",
    "No unnecessary work without your approval",
    "Sales, service and parts enquiry paths",
    "Experienced, time-served technicians",
    "Modern diagnostic equipment on site",
    "Convenient appointment scheduling",
    "Local, accountable, and easy to reach",
    "Digital inspection reports on request",
    "Vehicle collection and delivery available"
  ],

  // ---- Vehicle specialisms (typographic badges — no brand logos used) -----
  vehicleSpecialisms: [
    "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Ford", "Vauxhall",
    "Toyota", "Land Rover", "Peugeot", "Renault", "Nissan",
    "American Cars", "Classic Imports", "Sales", "Service", "Parts", "Diagnostics"
  ],

  // ---- Social ---------------------------------------------------------------
  socialLinks: {
    facebook: "#",
    instagram: "#",
    google: "#",
    tiktok: "#"
  },

  // ---- Links (demo placeholders — wire up before launch) -------------------
  bookingUrl: "#book",
  paymentUrl: "#pay",
  motBookingUrl: "#book",
  tyreQuoteUrl: "#quote",

  // ---- SEO ---------------------------------------------------------------
  seo: {
    title: "A C Automotive Engineering — Private Garage Website Preview",
    description:
      "Private website preview for A C Automotive Engineering on Goldhawk Road, showing a mobile-first garage page with booking, quote and diagnostic enquiry tools.",
    serviceArea: "Goldhawk Road, West London",
    canonicalUrl: ""
  }
};

// ============================================================================
//  SERVICES
// ============================================================================
const servicesData = [
  {
    id: "mot-testing",
    title: "MOT Testing",
    icon: "clipboard-check",
    short: "Government-standard MOT testing with clear, same-day results.",
    description:
      "Full MOT testing carried out to DVSA standards. If a fault is found, we'll explain it plainly and quote before any repair work begins.",
    price: "From £45"
  },
  {
    id: "interim-servicing",
    title: "Interim Servicing",
    icon: "settings",
    short: "A mid-term check to keep your vehicle running safely between full services.",
    description:
      "Covers essential safety and wear items — oil, filters, fluid levels, brakes and tyres — ideal for higher-mileage drivers.",
    price: "From £89"
  },
  {
    id: "full-servicing",
    title: "Full Servicing",
    icon: "cog",
    short: "Comprehensive annual service following manufacturer schedules.",
    description:
      "A complete check covering the engine, transmission, steering, suspension, brakes and electrics, plus all fluids and filters.",
    price: "From £169"
  },
  {
    id: "engine-diagnostics",
    title: "Engine Diagnostics",
    icon: "scan",
    short: "Modern diagnostic equipment to identify warning lights and faults.",
    description:
      "We connect to your vehicle's on-board systems to read fault codes accurately, then talk you through what they mean before recommending work.",
    price: "From £39"
  },
  {
    id: "brake-repairs",
    title: "Brake Repairs",
    icon: "disc",
    short: "Pads, discs and full brake system inspection and repair.",
    description: "Braking is safety-critical — we inspect the full system, not just the visible wear items.",
    price: "From £79"
  },
  {
    id: "clutch-repairs",
    title: "Clutch Repairs",
    icon: "circle-dot",
    short: "Diagnosis and replacement for slipping or worn clutches.",
    description: "From a soft pedal to full failure, we'll assess the clutch and gearbox together to avoid repeat callouts.",
    price: "Quote on inspection"
  },
  {
    id: "exhaust-repairs",
    title: "Exhaust Repairs",
    icon: "wind",
    short: "Repairs and replacement for exhausts and emissions faults.",
    description: "Noise, emissions failures, or visible corrosion — we'll inspect the full system and quote before work starts.",
    price: "Quote on inspection"
  },
  {
    id: "suspension",
    title: "Suspension",
    icon: "waves",
    short: "Shock absorbers, springs and steering component repairs.",
    description: "Worn suspension affects both comfort and safety — we check for uneven wear and steering play.",
    price: "Quote on inspection"
  },
  {
    id: "air-conditioning",
    title: "Air Conditioning",
    icon: "snowflake",
    short: "Re-gas, fault-finding and air-con system servicing.",
    description: "A losing-charge or warm-air system usually needs more than a re-gas — we check for leaks first.",
    price: "From £69"
  },
  {
    id: "tyres",
    title: "Tyres",
    icon: "circle",
    short: "Supply and fitting for a wide range of tyre brands and budgets.",
    description: "Tell us your registration and we'll confirm the correct size and a choice of budget, mid-range and premium tyres.",
    price: "From £59 per tyre"
  },
  {
    id: "wheel-alignment",
    title: "Wheel Alignment",
    icon: "move",
    short: "Laser alignment to reduce uneven tyre wear and improve handling.",
    description: "Uneven wear or a car pulling to one side is often a simple alignment fix.",
    price: "From £49"
  },
  {
    id: "battery-replacement",
    title: "Battery Replacement",
    icon: "battery-charging",
    short: "Testing and replacement for cars, hybrids and EVs.",
    description: "Free battery health check with any service — replacement fitted while you wait where stock allows.",
    price: "From £89"
  },
  {
    id: "electrical-fault-finding",
    title: "Electrical Fault Finding",
    icon: "zap",
    short: "Tracing intermittent faults, warning lights and wiring issues.",
    description: "Modern vehicles are heavily electronic — our diagnostic tools trace faults systematically rather than guessing.",
    price: "From £45"
  },
  {
    id: "timing-belts-chains",
    title: "Timing Belts & Chains",
    icon: "link",
    short: "Scheduled replacement to prevent serious engine damage.",
    description: "We follow manufacturer intervals — a timely belt change is far cheaper than the engine damage a snapped one can cause.",
    price: "Quote on inspection"
  },
  {
    id: "oil-filter-changes",
    title: "Oil & Filter Changes",
    icon: "droplet",
    short: "Quick-turnaround oil and filter service.",
    description: "Using the correct grade oil for your engine, with a full fluid and visual safety check included.",
    price: "From £59"
  },
  {
    id: "breakdown-repairs",
    title: "Breakdown Repairs",
    icon: "alert-triangle",
    short: "Fault-finding and repair for vehicles that won't start or run.",
    description: "Bring it in or ask about local collection — we prioritise get-you-going diagnosis where we can.",
    price: "Quote on inspection"
  },
  {
    id: "fleet-maintenance",
    title: "Fleet Maintenance",
    icon: "truck",
    short: "Scheduled maintenance plans for small and medium fleets.",
    description: "Flexible servicing schedules and account invoicing to keep fleet vehicles on the road.",
    price: "Contact for a fleet rate"
  },
  {
    id: "hybrid-servicing",
    title: "Hybrid Vehicle Servicing",
    icon: "leaf",
    short: "Servicing and diagnostics for hybrid drivetrains.",
    description: "Technicians trained on high-voltage hybrid systems, from routine servicing to fault diagnosis.",
    price: "Quote on inspection"
  },
  {
    id: "vehicle-health-check",
    title: "Vehicle Health Check",
    icon: "heart-pulse",
    short: "A no-obligation multi-point check of your vehicle's condition.",
    description: "A useful option before a long trip, a change of season, or before buying a used car.",
    price: "From £25"
  }
];

// ============================================================================
//  REVIEWS — sample / placeholder data. Replace with genuine reviews before launch.
// ============================================================================
const reviewsData = [
  {
    name: "Sarah M.",
    rating: 5,
    text: "Explained exactly what needed doing and why, no pressure to add extra work. Car's been running perfectly since.",
    service: "Full Service",
    source: "Google",
    date: "2026-05",
    placeholder: true
  },
  {
    name: "David R.",
    rating: 5,
    text: "I needed an American car specialist and the preview made the sales, service and parts route clear straight away.",
    service: "MOT Testing",
    source: "Google",
    date: "2026-04",
    placeholder: true
  },
  {
    name: "Priya K.",
    rating: 4,
    text: "Good honest garage. Booking was easy and they text you updates while the car's in.",
    service: "Brake Repair",
    source: "Facebook",
    date: "2026-03",
    placeholder: true
  },
  {
    name: "James T.",
    rating: 5,
    text: "Diagnosed an intermittent electrical fault two other garages couldn't find. Worth the drive.",
    service: "Electrical Fault Finding",
    source: "Trustpilot",
    date: "2026-02",
    placeholder: true
  },
  {
    name: "Emma L.",
    rating: 5,
    text: "Fair pricing on tyres and they were fitted within the hour while I waited.",
    service: "Tyres",
    source: "Google",
    date: "2026-01",
    placeholder: true
  }
];

// ============================================================================
//  GALLERY — placeholder categories/captions; swap real photography before launch.
// ============================================================================
const galleryData = [
  { category: "Workshop", caption: "Main workshop bay" },
  { category: "Workshop", caption: "Ramp and lifting equipment" },
  { category: "Diagnostics", caption: "Diagnostic equipment station" },
  { category: "Repairs", caption: "Brake component replacement" },
  { category: "Vehicles", caption: "Customer vehicle ready for collection" },
  { category: "Team", caption: "Technician at work" },
  { category: "Before and After", caption: "Bodywork before repair" },
  { category: "Before and After", caption: "Bodywork after repair" },
  { category: "Workshop", caption: "MOT testing bay" },
  { category: "Vehicles", caption: "Tyre fitting equipment" },
  { category: "Team", caption: "Reception and customer waiting area" },
  { category: "Diagnostics", caption: "Reading live fault codes" }
];


// ============================================================================
//  BLOG / GUIDES — sample educational articles for the preview site.
//  Replace with real owner-approved posts before launch.
// ============================================================================
const blogData = [
  {
    category: "American Cars",
    title: "What to ask before booking an American car specialist",
    excerpt: "A short guide for drivers with imported or specialist US vehicles: parts availability, diagnostic access, service history and what to mention when requesting a quote.",
    readTime: "4 min read",
    date: "Sample post",
    placeholder: true
  },
  {
    category: "Servicing",
    title: "Sales, service and parts: why one enquiry form should route correctly",
    excerpt: "This preview shows how A C Automotive could separate sales, service and parts enquiries before the customer even picks up the phone.",
    readTime: "3 min read",
    date: "Sample post",
    placeholder: true
  },
  {
    category: "Diagnostics",
    title: "Warning lights on an imported vehicle: details to send first",
    excerpt: "Registration, make/model, warning-light photo, recent work and symptoms help a specialist garage respond faster and avoid guesswork.",
    readTime: "5 min read",
    date: "Sample post",
    placeholder: true
  }
];

// ============================================================================
//  OFFERS — enable/disable and edit freely. Prices are placeholders.
// ============================================================================
const offersData = [
  {
    id: "mot-service-bundle",
    title: "MOT & Service Package",
    description: "Book your MOT and interim service together and save.",
    price: "From £119",
    expiry: "2026-08-31",
    terms: "Subject to vehicle inspection. Cannot be combined with other offers.",
    enabled: true
  },
  {
    id: "seasonal-check",
    title: "Free Seasonal Vehicle Check",
    description: "A complimentary check of tyres, lights, fluids and battery.",
    price: "Free",
    expiry: "2026-09-30",
    terms: "One per customer. No purchase necessary.",
    enabled: true
  },
  {
    id: "aircon-recharge",
    title: "Air-Conditioning Recharge Offer",
    description: "Full re-gas with leak check included.",
    price: "From £59",
    expiry: "2026-08-31",
    terms: "Price applies to standard R134a/1234yf systems.",
    enabled: true
  },
  {
    id: "new-customer",
    title: "New Customer Offer",
    description: "10% off your first service when you book online.",
    price: "10% off",
    expiry: "2026-12-31",
    terms: "New customers only. Cannot be combined with other offers.",
    enabled: true
  }
];

// ============================================================================
//  DIAGNOSTIC SELECTOR — symptom picker responses
// ============================================================================
const diagnosticSymptoms = [
  { id: "warning-light", label: "Warning light displayed", icon: "alert-circle" },
  { id: "wont-start", label: "Vehicle will not start", icon: "power" },
  { id: "engine-noise", label: "Unusual engine noise", icon: "activity" },
  { id: "brake-noise", label: "Brakes making noise", icon: "disc" },
  { id: "steering-vibration", label: "Steering vibration", icon: "move" },
  { id: "loss-of-power", label: "Loss of power", icon: "trending-down" },
  { id: "exhaust-smoke", label: "Smoke from exhaust", icon: "wind" },
  { id: "overheating", label: "Vehicle overheating", icon: "thermometer" },
  { id: "battery-warning", label: "Battery warning", icon: "battery-warning" },
  { id: "aircon-not-cold", label: "Air conditioning not cold", icon: "snowflake" },
  { id: "clutch-slipping", label: "Clutch slipping", icon: "circle-dot" },
  { id: "tyre-pressure", label: "Tyre pressure problem", icon: "circle" },
  { id: "fluid-leak", label: "Fluid leaking", icon: "droplet" },
  { id: "mot-failure", label: "MOT failure", icon: "clipboard-x" },
  { id: "unsure", label: "Unsure / something else", icon: "help-circle" }
];

// ============================================================================
//  PRODUCTS — payment demonstration only
// ============================================================================
const paymentProducts = [
  { name: "Vehicle Diagnostic Assessment", price: "From £39" },
  { name: "MOT Booking Deposit", price: "£20" },
  { name: "Interim Service Package", price: "From £89" },
  { name: "Air-Conditioning Recharge", price: "From £59" },
  { name: "Winter Vehicle Health Check", price: "£25" }
];
