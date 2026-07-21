from django.core.management.base import BaseCommand

from directory.models import Category, Dealer, Guide, SiteSetting, Tool

CATS = [
    ("solar", "Rooftop Solar", "Generate your own power, slash your bill.", "solar",
     "Rooftop solar is the most proven home upgrade in India today. Panels on your terrace convert sunlight into electricity, net metering lets you export what you don't use, and the central subsidy has never been better.",
     "A typical Delhi NCR home running on a Rs 2,000-4,000 monthly bill needs a 2-3 kW system. Grid-connected (on-grid) systems are the default choice - no batteries, lowest cost, and your meter runs backwards when you export. Expect 25 years of panel life with minimal cleaning and one inverter replacement around year 10-12.",
     "₹45k–65k / kW", "Up to ₹78,000 (PM Surya Ghar)", "₹1,000–3,500 / month", "3–5 years"),
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

DEALERS = [
    ("SuryaTech Solar Solutions", ["solar", "battery"], "Faridabad", "Sector 16, Faridabad", "+91 90000 00001", "919000000001", True, "2018", "Residential rooftop specialists. On-grid & hybrid systems, net-metering paperwork handled end to end."),
    ("GreenVolt Energy", ["solar", "ev"], "Delhi", "Lajpat Nagar, Delhi", "+91 90000 00002", "919000000002", True, "2016", "MNRE-empanelled installer. Rooftop solar for homes & societies, plus home EV charger installation."),
    ("AquaSanchay Systems", ["rain", "grey"], "Gurugram", "Sector 45, Gurugram", "+91 90000 00003", "919000000003", True, "2019", "Rainwater harvesting pits, recharge borewells and greywater reuse for villas and RWAs."),
    ("Hawa Urja Renewables", ["wind", "solar"], "Ghaziabad", "Raj Nagar, Ghaziabad", "+91 90000 00004", "919000000004", False, "2021", "Solar-wind hybrid systems for farmhouses and open sites. Free wind-feasibility survey."),
    ("EverSun Water Heaters", ["heater"], "Faridabad", "NIT, Faridabad", "+91 90000 00005", "919000000005", True, "2014", "ETC solar water heaters 100-500 LPD. Installation, AMC and winter servicing."),
    ("ChargeGhar EV", ["ev", "battery"], "Noida", "Sector 62, Noida", "+91 90000 00006", "919000000006", True, "2020", "Home & society EV charging points, dedicated wiring, DISCOM EV-tariff assistance."),
    ("BhoomiCycle Compost Co.", ["compost", "biogas"], "Delhi", "Dwarka, Delhi", "+91 90000 00007", "919000000007", False, "2019", "Society-scale OWC composters, home khambas, and compact biogas units with training."),
    ("ThandaChhat Cool Roofs", ["roof"], "Gurugram", "Udyog Vihar, Gurugram", "+91 90000 00008", "919000000008", False, "2022", "High-SRI cool roof coatings and terrace gardens. Free thermal assessment."),
    ("Nirmal Jal Biogas", ["biogas"], "Faridabad", "Ballabgarh, Faridabad", "+91 90000 00009", "919000000009", True, "2017", "Home and community biogas digesters, installation with first-month culture support."),
    ("UrjaStore Lithium", ["battery", "solar"], "Delhi", "Okhla, Delhi", "+91 90000 00010", "919000000010", True, "2020", "LFP battery backup, hybrid inverters, and solar retrofits for existing systems."),
    ("VarshaJal Harvesters", ["rain"], "Noida", "Sector 137, Noida", "+91 90000 00011", "919000000011", True, "2015", "Recharge pits, rooftop RWH for towers & villas, annual pre-monsoon maintenance."),
    ("SolarSaathi NCR", ["solar", "heater"], "Ghaziabad", "Indirapuram, Ghaziabad", "+91 90000 00012", "919000000012", False, "2021", "Budget-friendly rooftop solar and water heaters with EMI options."),
    ("GreyWise Water Tech", ["grey"], "Gurugram", "Sohna Road, Gurugram", "+91 90000 00013", "919000000013", False, "2022", "Compact greywater treatment for villas; flush & garden reuse plumbing."),
    ("PavanShakti Windworks", ["wind"], "Delhi", "Najafgarh, Delhi", "+91 90000 00014", "919000000014", False, "2023", "1-5 kW small wind turbines for open plots and farmhouses. Site wind-logging service."),
]

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


class Command(BaseCommand):
    help = "Load HARIT starter content (categories, dealers, tools, guides)."

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

        self.stdout.write(self.style.SUCCESS("HARIT content seeded."))
