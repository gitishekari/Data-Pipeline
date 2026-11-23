# Data-Pipeline
# Cycling Tour Data Pipeline — XML & XSD Relational Modeling

An end-to-end XML Schema Definition (XSD 1.0) and XML dataset project modeling the core operational data of **Bike4You**, a cycling tour and bike rental platform (`http://bike4you.fr/cyclingtour#`).

The project demonstrates strict schema-driven data validation, custom simple/complex types, pattern-enforced data quality rules, and relational referential integrity (`xs:key` / `xs:keyref`) across nine interconnected entity collections, alongside a standalone **TourPackage** design module.

---

## Project Architecture

### 1. Integrated Cycling Tour Schema (`schemas/cyclingtour.xsd`)

The root element `<ct:cyclingtours>` enforces a deterministic structure across **9 domain databases**, populated with **52 validated sample records** in `data/cyclingtour.xml`:

| Database Element | Entity Element | Sample Records | Key Validation Constraints |
| :--- | :--- | :---: | :--- |
| `BIKES_Database` | `BIKE` | 6 | `ID_Bike` (`xs:ID`), category enum (`Mountain`, `Road`, `Gravel`, `City`, `E-bike`, `Kids`), `RoadType` (`xs:list` of surfaces), inventory counts |
| `ACTIVITIES_Database` | `ACTIVITY` | 5 | `ID_Activity` (`xs:ID`), optional `guided` attribute (`fully`, `partially`, `none`), rating regex `(10|[0-9])/10` |
| `EVENTS_Database` | `EVENT` | 4 | `ID_Event` (`xs:ID`), event categories (`Race`, `Festival`, `Workshop`, `Expo`, `Charity`, `Community Ride`), optional activity references |
| `CLIENTS_Database` | `CLIENT` | 8 | `ID_client` (`xs:ID`), regex validation for postal codes (`\d{4,10}`), phones (`\+?\d+`, 6–15 chars), emails, and `CLIENT_TYPE` enum |
| `BOOKINGS_Database` | `BOOKING` | 10 | `ID_Booking` (`xs:ID`), required `With_Guide` boolean, `xs:choice` between `ACTIVITY_REF` or `PACKAGE_REF`, status enum (`pending`, `confirmed`, `cancelled`) |
| `PATHS_Database` | `PATH` | 6 | `ID_Path` (`xs:ID`), environment enum, `RoadType` list, minimum distance (5 km) and duration (15 min) thresholds |
| `DESTINATIONS_Database` | `DESTINATION` | 5 | `ID_Destination` (`xs:ID`), country enum, `xs:choice` for departure/arrival (city, postal code, or address), repeatable crossed cities |
| `TOURPACKAGES_Database` | `TOURPACKAGE` | 4 | `ID_TourPackage` (`xs:ID`), 5-level difficulty enum, optional accommodation (0–5 rating) & meal options, `DD-HH` duration regex, group size >= 1 |
| `GUIDES_Database` | `GUIDE` | 4 | `ID_Guide` (`xs:ID`), contact details reusing shared `PhoneType` and `MailType` restrictions |

### Referential Integrity (`xs:key` & `xs:keyref`)

Declared at the `<ct:cyclingtours>` root scope to enforce foreign-key relationships across bookings:

* **`BookingClientRef`**: Every `BOOKING/CLIENT_REF` must match an existing `CLIENT/@ID_client`.
* **`BookingActivityRef`**: Every `BOOKING/ACTIVITY_REF` must match an existing `ACTIVITY/@ID_Activity`.
* **`BookingPackageRef`**: Every `BOOKING/PACKAGE_REF` must match an existing `TOURPACKAGE/@ID_TourPackage`.
* **`BookingGuideRef`**: Every optional `BOOKING/GUIDE_REF` must match an existing `GUIDE/@ID_Guide`.

---

### 2. Standalone TourPackage Module (`schemas/tourPackages.xsd`)

Designed as a modular prototype prior to integration into the unified schema, `tourPackages.xsd` (paired with `data/tourPackages.xml`) models multi-day and single-day cycling tour packages with:

* **5-Tier Difficulty Scale:**
  * `beginner`: <= 25 km/day, mostly flat bike paths
  * `easy`: 25–40 km/day, gentle hills
  * `moderate`: 40–60 km/day, mixed terrain
  * `difficult`: 60–80 km/day, sustained climbs
  * `expert`: >= 80 km/day, steep/technical mountain passes
* **Flexible Date Modeling:** Supports both single-day tours (empty or omitted `end_date` via `xs:union` of `xs:date` and an empty string) and multi-day itineraries with regex-validated `DD-HH` duration.
* **Domain Constraints:** Base package integer pricing with fixed `EUR` currency, star-rating enumerations (`*` to `*****`), meal plans (`breakfast only`, `all meal available`, `self catering`), bike rental availability, and optional `xs:IDREF` hooks (`activityRef`, `pathRef`) for external linking.

---

## Repository Structure

```text
├── schemas/
│   ├── cyclingtour.xsd      # Full integrated Bike4You schema (9 databases + identity constraints)
│   └── tourPackages.xsd     # Standalone TourPackage module schema
├── data/
│   ├── cyclingtour.xml      # Validated dataset with 52 sample entities
│   └── tourPackages.xml     # Validated sample tour packages (P001, P002)
├── scripts/
│   └── validate.py          # Automated Python XSD validator
├── requirements.txt
└── README.md
