from django.core.management.base import BaseCommand

from directory.models import FAQ, Category, Dealer, Guide, SiteSetting, Tool

CATS = [
    ("solar", "Rooftop Solar", "Generate your own power, slash your bill.", "solar",
     "Rooftop solar is the most proven home upgrade in India today. Panels on your terrace convert sunlight into electricity, net metering lets you export what you don't use, and the central subsidy has never been better.",
     "A typical Delhi NCR home running on a Rs 2,000-4,000 monthly bill needs a 2-3 kW system. Grid-connected (on-grid) systems are the default choice - no batteries, lowest cost, and your meter runs backwards when you export. Expect 25 years of panel life with minimal cleaning and one inverter replacement around year 10-12.",
     "₹55k–70k / kW", "Up to ₹78,000 (PM Surya Ghar)", "₹1,000–3,500 / month", "3–5 years"),
    ("heater", "Solar Water Heater", "Free hot water, every morning.", "heater",
     "A solar water heater is the quiet workhorse of green tech - simple, no moving parts, and it removes your geyser (one of the biggest power-hungry appliances) from the bill.",
     "Systems are sized in LPD - litres per day. A family of four typically needs 100-150 LPD. Evacuated tube collectors (ETC) work well even in NCR winters. Once installed, running cost is essentially zero; most owners recover the cost in two to four winters.",
     "₹18k–35k (100–200 LPD)", "Varies by state", "₹400–900 / month in winter", "2–4 years"),
    ("wind", "Terrace Wind Turbine", "Small wind for windy, open sites.", "wind",
     "Small wind turbines can complement solar - but honesty first: they only make sense on genuinely windy, open sites. Urban rooftops are usually too turbulent.",
     "A turbine needs steady average wind speeds above roughly 4-5 m/s to be worthwhile. Tall unobstructed terraces near open fields or along ridge lines can qualify; a typical enclosed colony rooftop rarely does. Use our feasibility check before speaking to any dealer. Solar-wind hybrids are the usual compromise where wind is marginal.",
     "₹1–2.5 lakh / kW", "Limited", "Site-dependent", "6–12 years (good sites)"),
    ("rain", "Rainwater Harvesting", "Catch the monsoon, recharge the ground.", "rain",
     "Delhi NCR gets ~790 mm of rain a year - most of it runs off your roof into the drain. A harvesting system captures it for reuse or recharges the groundwater below you.",
     "Two approaches: storage (a tank for washing, gardening, even filtration to potable) and recharge (directing filtered roof water into a recharge pit or defunct borewell). Many municipal bodies in NCR mandate harvesting for larger plots and offer property-tax rebates. Even a modest 100 sqm roof can harvest more than 60,000 litres a year.",
     "₹25k–1.2 lakh (home systems)", "Property-tax rebates in some ULBs", "Tanker & borewell savings", "2–6 years"),
    ("ev", "EV Charging Setup", "Charge at home for a fraction of petrol.", "ev",
     "An EV is only as convenient as its charging. A dedicated home charging point - safe wiring, the right socket or AC wall box, and ideally a separate meter - makes ownership effortless.",
     "Two-wheelers charge happily from a well-wired 3-pin point; cars deserve a 3.3-7.4 kW AC wall charger on a dedicated line. Many DISCOMs offer special EV tariffs. Pair charging with rooftop solar and your running cost per km approaches zero.",
     "₹15k–75k (home AC charger)", "State EV policies vary", "₹1,500–4,000 / month vs petrol", "Immediate on running cost"),
    ("battery", "Battery & Backup", "Store power, ride through cuts.", "battery",
     "Batteries turn intermittent solar into always-on power and replace noisy diesel or inverter-battery setups with cleaner lithium storage.",
     "Modern lithium (LFP) packs last 8-12 years, charge fast, and pair with hybrid inverters for seamless backup. For most NCR homes on stable grid + net metering, batteries are optional; for areas with frequent cuts or for critical loads, they're transformative. Size the battery to your essential loads, not your whole house, to keep cost sane.",
     "₹40k–2 lakh+", "—", "Backup + solar self-use", "Use-case dependent"),
    ("biogas", "Home Biogas", "Kitchen waste in, cooking gas out.", "biogas",
     "A compact biogas digester eats your kitchen's wet waste and gives back cooking gas and liquid fertiliser - a closed loop on your own terrace or backyard.",
     "Home-scale units (1-2 cubic metre) digest 1-2 kg of food waste daily and can replace a meaningful share of LPG. They need daily feeding, a warm spot, and a little patience during the first month of culture development. Best suited to households or communities that cook fresh and generate steady wet waste.",
     "₹25k–60k (home units)", "Some state schemes", "1–2 LPG cylinders / month", "2–4 years"),
    ("compost", "Composting & Waste", "Turn waste into soil, not landfill.", "compost",
     "Composting is the cheapest green upgrade there is - and for housing societies in NCR, segregation and on-site processing of wet waste is increasingly a legal requirement, not a choice.",
     "Homes can start with a Rs 1,500 khamba or tumbler. Societies need drum composters or OWC machines sized to daily wet-waste volume. Done right, a society cuts its landfill load by more than half and produces compost its own gardens absorb.",
     "₹1.5k–15k (home) · more for societies", "ULB support for bulk generators", "Waste-collection savings for RWAs", "—"),
    ("roof", "Cool & Green Roofing", "Cut heat before it enters.", "roof",
     "The cheapest air-conditioning is the heat you never let in. High-reflectance cool-roof coatings and green (planted) roofs drop indoor temperatures noticeably in NCR summers.",
     "A white high-SRI coating on the terrace can lower the slab temperature by several degrees, easing AC load on the top floor. Green roofs go further - insulation, biodiversity, and stormwater absorption - at higher cost and structural checks. Cool coats are the easy first step for any flat roof.",
     "₹30–90 / sq ft (cool coats)", "—", "10–25% on summer cooling", "1–3 summers"),
    ("grey", "Greywater Recycling", "Reuse bath & wash water for flush and garden.", "grey",
     "Bath, basin and laundry water - greywater - is the easiest water to reclaim. Simple treatment makes it perfect for flushing and gardening, halving your freshwater demand.",
     "Systems range from simple filter-and-reuse setups for gardens to compact treatment units feeding flush lines. Best planned during construction or renovation when dual plumbing is easy; retrofits work where bathrooms cluster on one side of the house.",
     "₹35k–1.5 lakh (home systems)", "—", "Up to 30–40% of water use", "3–6 years"),
]

DEALERS = []

TOOLS = [
    ("solarcalc", "Rooftop Solar Savings Calculator", "From your monthly bill to system size, subsidy, payback and 25-year savings.", "solar"),
    ("sizer", "Roof Area to Solar Size", "How many kW fits on your terrace, and what it will generate.", "solar"),
    ("heatercalc", "Water Heater Savings", "Right LPD size for your family and the winter savings it unlocks.", "heater"),
    ("raincalc", "Rainwater Harvest Estimator", "Litres your roof can capture in a Delhi NCR monsoon.", "rain"),
    ("evcalc", "EV vs Petrol Cost", "Your monthly and yearly savings if you switch.", "ev"),
    ("windcheck", "Wind Feasibility Check", "An honest go / no-go before you spend on a turbine.", "wind"),
    ("carbon", "Home Carbon Footprint", "Your household CO2 from power, fuel and gas - in trees.", None),
]

GUIDES = [
    ("suryaghar", "Subsidy", "PM Surya Ghar: the rooftop solar subsidy, explained",
     "PM Surya Ghar: Muft Bijli Yojana is the central scheme that makes residential rooftop solar dramatically cheaper. The subsidy is paid per kilowatt of installed capacity: roughly Rs 30,000 per kW for the first 2 kW and Rs 18,000 for the third - capping out around Rs 78,000 for systems of 3 kW and above.\n\nThe flow is simpler than most people expect: register on the official pmsuryaghar.gov.in portal, choose an empanelled vendor, install, and the DISCOM inspects and commissions with net metering. The subsidy lands directly in your bank account after commissioning.\n\nTwo practical tips. First, only residential consumers qualify - and the vendor must be empanelled, so confirm before signing anything. Second, subsidy amounts and rules get revised; treat the figures here as indicative and verify on the portal before you commit."),
    ("roofready", "Checklist", "Is your roof solar-ready? A 5-minute check",
     "Shade is the killer. Stand on your terrace at 10 am, noon and 3 pm - water tanks, parapets, taller neighbours and even a single tree branch can cut a panel row's output badly. You want a patch that stays sun-lit through the middle of the day, ideally facing south.\n\nSpace: budget roughly 80-100 sq ft per kW for standard panels. A 3 kW home system wants ~250-300 sq ft of clear, strong, accessible roof. Sheet roofs and tin sheds can work with the right structure but need extra care.\n\nOwnership and wiring matter too: you'll need consent if the roof is shared, a sanctioned load that accommodates the system, and a meter location the DISCOM can reach. If all three check out, you're ready for site survey - which any good dealer does free."),
    ("netmeter", "Basics", "Net metering, in plain words",
     "Net metering is the arrangement that makes on-grid solar pay. Your meter counts in both directions: solar you consume directly reduces your draw, and surplus you export spins the count the other way as a credit.\n\nAt billing time you pay for the net - imports minus exports - plus fixed charges. Generate more than you use in a month and the credit typically rolls forward. This is why most homes skip batteries entirely: the grid is your battery.\n\nEach DISCOM has its own capacity caps and settlement rules, and they do change. Your installer files the net-metering application as part of the job - make sure that's in the quote."),
    ("gridtypes", "Basics", "On-grid, off-grid, hybrid - which solar is for you?",
     "On-grid is the default for city homes: panels + inverter tied to the grid, net metering, no batteries. Cheapest per kW, best payback - but it shuts off during a power cut (by design, for lineman safety).\n\nOff-grid means batteries carry your whole load with no grid at all. It's for farms and remote sites, and it's the most expensive way to run a house that already has a connection.\n\nHybrid sits between: grid-tied with a battery, so critical loads ride through cuts and solar self-use rises. Pick on-grid if your supply is stable, hybrid if cuts are a daily reality, and off-grid only when the grid genuinely isn't an option."),
    ("rwhbasics", "Water", "Rainwater harvesting at home: storage vs recharge",
     "Every millimetre of rain on one square metre of roof is one litre of water. Delhi NCR's ~790 mm year means a 100 sqm roof sheds nearly 79,000 litres - most of it in a few monsoon weeks.\n\nStorage systems filter roof water into a tank for gardening, washing and (with treatment) more. Recharge systems send filtered water underground through a pit or a defunct borewell, raising the water table you draw from. Recharge is cheaper and maintenance-light; storage gives you usable water on tap.\n\nMany NCR municipal bodies mandate RWH above certain plot sizes and some offer property-tax rebates for compliant systems - worth checking with your local body, and a good dealer will know the current rules."),
    ("windtruth", "Honesty", "The honest truth about rooftop wind in the city",
     "Small wind is real technology - on the right site. The physics is unforgiving: power scales with the cube of wind speed, so a site with 4 m/s average makes roughly half the energy of one at 5 m/s. Urban rooftops, surrounded by buildings, are turbulent and slow.\n\nRule of thumb: if trees around you aren't constantly swaying, a terrace turbine will disappoint. Genuinely windy open sites - farmhouses, ridge lines, coastal strips - can work, ideally after a month of actual wind logging.\n\nOur advice, and we say this running a green directory: in most NCR colonies, put the same money into more solar. Where wind is marginal, a small solar-wind hybrid at least diversifies. Use the feasibility tool before any purchase."),
]

FAQS = [
    ("solar", "How much does rooftop solar cost in Delhi NCR?",
     "A residential rooftop solar system in Delhi NCR costs roughly Rs 45,000 to Rs 65,000 per kW before subsidy. A typical 3 kW home system therefore lands around Rs 1.5-2 lakh, dropping to roughly Rs 75,000-1.2 lakh after the PM Surya Ghar subsidy. Final price depends on panel brand, inverter type, roof structure and whether you need extra mounting height."),
    ("solar", "How much solar do I need for a Rs 3,000 monthly electricity bill?",
     "A Rs 3,000 monthly bill at around Rs 8 per unit means roughly 375 units a month, which usually needs a 2.5 to 3 kW rooftop system in Delhi NCR. Our free solar calculator works this out from your exact bill and tariff in a few seconds."),
    ("solar", "How long does rooftop solar take to pay for itself?",
     "Most Delhi NCR homes recover the net cost in three to five years after subsidy. Panels are warranted for around 25 years, so the remaining two decades of generation are effectively free power. Payback is faster if your tariff is high or your usage is heavy."),
    ("solar", "Do solar panels work during Delhi's winter smog and monsoon?",
     "Yes, but output drops. Heavy smog and overcast monsoon days can cut generation significantly for short periods, which is already factored into the annual averages used in our calculator. Over a full year, Delhi NCR still gets strong solar irradiance. Regular cleaning matters more here than in cleaner-air cities."),
    ("solar", "Is rooftop solar worth it if I already have an inverter battery?",
     "Usually yes, and they solve different problems. An inverter battery gives you backup during cuts but adds nothing to your bill savings. On-grid solar cuts the bill but shuts off during a cut. Many NCR homes keep the existing inverter and add on-grid solar, or move to a hybrid inverter if cuts are frequent."),
    ("heater", "What size solar water heater does a family of four need?",
     "A family of four typically needs a 100 to 150 LPD (litres per day) solar water heater. Size up to 200 LPD if you have more bathrooms in simultaneous use or guests often. Our water heater tool sizes it from your household count and shows the winter savings."),
    ("heater", "Do solar water heaters work in Delhi winters?",
     "Yes. Evacuated tube collector (ETC) systems perform well in Delhi NCR winters, which is exactly when a geyser costs you the most. On genuinely overcast days the backup electric element covers the gap, but most owners see their winter geyser usage fall sharply."),
    ("rain", "How much rainwater can my roof collect in Delhi NCR?",
     "Every square metre of roof collects about one litre per millimetre of rain. With Delhi NCR's roughly 790 mm annual rainfall, a 100 square metre roof sheds close to 79,000 litres a year, of which around 80% is realistically capturable. Our rainwater tool calculates it from your exact roof area."),
    ("rain", "Is rainwater harvesting compulsory in Delhi NCR?",
     "For many plot sizes, yes. Several NCR municipal bodies mandate rainwater harvesting above a certain plot area, and some offer property-tax rebates for compliant systems. Rules vary by local body and do change, so confirm with your municipal corporation or ask a listed dealer who works in your area."),
    ("ev", "How much does a home EV charger cost to install in India?",
     "A home AC charging setup typically costs Rs 15,000 to Rs 75,000 installed, depending on whether you need a simple wired point for a two-wheeler or a 3.3-7.4 kW wall box on a dedicated line for a car. Cost rises if the run from your meter is long or your sanctioned load needs upgrading."),
    ("ev", "How much cheaper is an EV than petrol per kilometre?",
     "In Delhi NCR an electric two-wheeler runs at roughly 25-30 paise per km against about Rs 2 per km for petrol, and an electric car at roughly Rs 1.20 per km against about Rs 6.30. Our EV calculator gives your exact monthly saving from your daily running and local prices."),
    ("wind", "Is a rooftop wind turbine worth it in Delhi?",
     "For most Delhi NCR colony rooftops, no. Wind power scales with the cube of wind speed, and buildings make urban rooftops turbulent and slow. Genuinely open sites like farmhouses can work. Run our free wind feasibility check first, and if it comes back marginal, the same money in extra solar will almost always generate more."),
    ("battery", "Do I need a battery with rooftop solar?",
     "Usually not, if your grid supply is stable and you have net metering. Exporting surplus to the grid earns credit, so the grid effectively acts as your battery at no extra cost. Add a battery only if you face frequent cuts or need specific critical loads to ride through them."),
    ("compost", "Is composting mandatory for housing societies in NCR?",
     "Increasingly yes. Bulk waste generators, which includes many housing societies, are required to segregate and process wet waste on site under solid waste rules. Requirements and enforcement vary by local body, so check your municipal corporation's current rules."),
]


class Command(BaseCommand):
    help = "Load RenSetu starter content (categories, dealers, tools, guides)."

    def handle(self, *args, **opts):
        SiteSetting.get()

        cat_objs = {}
        for i, (slug, name, short, icon, intro, body, cost, sub, save, pay) in enumerate(CATS):
            c, _ = Category.objects.update_or_create(
                slug=slug,
                defaults=dict(name=name, short=short, icon=icon, order=i, intro=intro,
                              body=body, cost=cost, subsidy=sub, saving=save, payback=pay,
                              is_active=True),
            )
            cat_objs[slug] = c
        self.stdout.write(f"Categories: {Category.objects.count()}")

        for i, (slug, name, desc, cat) in enumerate(TOOLS):
            Tool.objects.update_or_create(
                slug=slug,
                defaults=dict(name=name, description=desc, order=i, is_active=True,
                              category=cat_objs.get(cat) if cat else None),
            )
        self.stdout.write(f"Tools: {Tool.objects.count()}")

        for i, (slug, tag, title, body) in enumerate(GUIDES):
            Guide.objects.update_or_create(
                slug=slug,
                defaults=dict(tag=tag, title=title, body=body, order=i, is_active=True),
            )
        self.stdout.write(f"Guides: {Guide.objects.count()}")

        for name, cats, city, area, phone, wa, verified, since, desc in DEALERS:
            d, _ = Dealer.objects.update_or_create(
                name=name,
                defaults=dict(city=city, area=area, phone=phone, whatsapp=wa,
                              is_verified=verified, since=since, description=desc, is_active=True),
            )
            d.categories.set([cat_objs[s] for s in cats])
        self.stdout.write(f"Dealers: {Dealer.objects.count()}")

        for i, (cat_slug, q, a) in enumerate(FAQS):
            FAQ.objects.update_or_create(
                question=q,
                defaults=dict(category=cat_objs.get(cat_slug), answer=a,
                              order=i, is_active=True),
            )
        self.stdout.write(f"FAQs: {FAQ.objects.count()}")

        self.stdout.write(self.style.SUCCESS("RenSetu content seeded."))
