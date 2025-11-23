# Nastavení časového pásma v Odoo

## Problém
Timestamp je posunutý o hodinu, protože:
- Data se ukládají v UTC čase (správně)
- Odoo automaticky převádí UTC na časové pásmo uživatele při zobrazení
- Uživatel musí mít správně nastavené časové pásmo

## Řešení

### 1. Nastavení časového pásma pro uživatele

1. Přihlaste se do Odoo jako administrátor
2. Klikněte na **Settings** (Nastavení) v hlavním menu
3. Vyberte **Users & Companies** → **Users** (Uživatelé)
4. Najděte a otevřete uživatele, kterému chcete nastavit časové pásmo
5. V záložce **Preferences** (Předvolby) nastavte:
   - **Timezone** (Časové pásmo): `Europe/Prague`
6. Klikněte na **Save** (Uložit)
7. **Odhlaste se a znovu se přihlaste** - důležité pro aplikování změn!

### 2. Výchozí časové pásmo pro nové uživatele

1. V **Settings** → **General Settings**
2. Najděte sekci **Companies**
3. Otevřete vaši společnost
4. Nastavte **Timezone**: `Europe/Prague`
5. Uložte změny

### 3. Ověření

Po nastavení:
- Časy v databázi jsou v UTC (správně)
- Zobrazené časy v UI jsou v českém čase (UTC+1 v zimě, UTC+2 v létě)
- Název záznamu obsahuje český čas (např. "BPS 2025-11-23 15:30:45")

## Jak to funguje

```
Příchod dat:
1. Data přijdou z externího systému
2. Uloží se jako UTC čas do databáze
3. Název záznamu se vytvoří s českým časem pro čitelnost

Zobrazení v Odoo:
1. Odoo načte UTC čas z databáze
2. Automaticky převede na časové pásmo uživatele (Europe/Prague)
3. Uživatel vidí správný lokální čas
```

## Technické detaily

- **REST API**: Ukládá `datetime.utcnow()` - čistý UTC čas bez timezone info
- **Název záznamu**: Používá český čas pro lidskou čitelnost
- **Database field**: `fields.Datetime` automaticky pracuje s UTC
- **View**: Standardní `<field name="timestamp"/>` automaticky převádí na user timezone

## Testování

Pro ověření správného nastavení:

1. Odešlete testovací data:
```bash
curl -X POST http://localhost:8069/api/power_plant_data2 \
  -H "Content-Type: application/json" \
  -d '{"1": 100, "2": 150}'
```

2. Zkontrolujte v Odoo UI:
   - Název záznamu by měl obsahovat aktuální český čas
   - Timestamp sloupec by měl také zobrazovat český čas
   - Oba časy by měly být stejné (nebo velmi blízké)

## Poznámky

- Odoo VŽDY ukládá časy v UTC do databáze
- Konverze na lokální čas se děje pouze při zobrazení
- Toto je best practice pro multi-timezone aplikace
- Letní/zimní čas se řeší automaticky díky `pytz` knihovně
