# Tildeling af organisationer for vikarkorpset i Nexus

Robotten sikrer, at vikarer i vikarkorpset har de rette organisationer tildelt i Nexus baseret på aktive og kommende vagter hentet fra Temponizer, og registrerer hvilke organisationer der skal fjernes igen efterfølgende.

## Hvad gør robotten?

1. Henter igangværende og kommende vagter for dags dato fra Temponizer
2. Filtrerer vagter, så kun vagter tilhørende vikarkorpset beholdes
3. Henter stamoplysninger (herunder uddannelse) for den relevante vikar fra Temponizer
4. Tildeler de nødvendige organisationer i Nexus til vikarer med aktive vagter
5. Registrerer hvilke organisationer der er tildelt, så en efterfølgende proces kan fjerne dem igen

> **Bemærk:** Processen er delvist under udvikling — logikken til at fylde og behandle arbejdskøen indeholder endnu placeholder-implementeringer. En tidsbegrænsning på 2 timer for vagter er kommenteret ud og kan aktiveres på et senere tidspunkt.

## Forudsætninger

- Python ≥ 3.13
- [`uv`](https://docs.astral.sh/uv/) til pakkehåndtering
- Adgang til **Automation Server** (arbejdskø og credentials)
- Adgang til **Temponizer** (vagtplaner og medarbejderoplysninger)
- Adgang til **Nexus** (organisationstildeling)
- Adgang til **Odense SQL Server**

## Installation

```sh
uv sync
```

## Konfiguration

Credentials registreres i Automation Server:
- `Odense SQL Server`
- `Temponizer - Roboa`

| Miljøvariabel | Beskrivelse |
|---|---|
| `ATS_URL` | URL til Automation Server API |
| `ATS_TOKEN` | Adgangstoken til Automation Server |
| `ATS_WORKQUEUE_OVERRIDE` | Overstyrer workqueue-ID (valgfrit) |

## Kørsel

```sh
uv run python main.py --queue   # Fyld arbejdskøen
uv run python main.py           # Behandl arbejdskøen
```

## Afhængigheder

| Pakke | Formål |
|---|---|
| `automation-server-client` | Kommunikation med Automation Server, herunder arbejdskø og credentials |
| `temponizer-client` | Hentning af vagtplaner og medarbejderoplysninger fra Temponizer |
| `odk-tools` | Sporing og logging via Tracker |

## GDPR og sikkerhed

Processen behandler personoplysninger om vikarer i vikarkorpset, herunder navn, vikar-ID og uddannelse samt oplysninger om, hvilke kunder/organisationer de er tilknyttet i forbindelse med deres vagter. Oplysningerne hentes fra Temponizer og anvendes udelukkende til at styre adgange i Nexus. Der lagres ikke personoplysninger ud over hvad der er nødvendigt i arbejdskøen i Automation Server.
